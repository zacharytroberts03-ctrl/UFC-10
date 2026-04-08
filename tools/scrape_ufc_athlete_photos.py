"""
Tool: scrape_ufc_athlete_photos.py
Purpose: Scrape https://www.ufc.com/athletes/all (paginated) and save one JPG per
         athlete to UFC 10/fighter_photos/, named Firstname_Lastname.jpg.
         Athletes with no real photo get a 400x400 black placeholder JPG.

Usage:
  python tools/scrape_ufc_athlete_photos.py            # full run
  python tools/scrape_ufc_athlete_photos.py --limit 20 # dry-run on first N athletes
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from firecrawl import Firecrawl
from PIL import Image

if sys.stdout.encoding != "utf-8":
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

load_dotenv()

LIST_URL = "https://www.ufc.com/athletes/all?gender=All&page={page}"
OUT_DIR = Path(__file__).resolve().parent.parent / "fighter_photos"
DELAY = 2
MAX_EMPTY_PAGES = 2


# ── Firecrawl client ─────────────────────────────────────────────────────────

def _get_firecrawl():
    key = os.getenv("FIRECRAWL_API_KEY")
    if not key:
        raise EnvironmentError("FIRECRAWL_API_KEY not set in .env")
    return Firecrawl(api_key=key)


def firecrawl_html(url: str) -> str:
    client = _get_firecrawl()
    try:
        result = client.scrape(url, formats=["html"])
        return result.html or ""
    except Exception as e:
        err = str(e)
        if "429" in err or "rate" in err.lower():
            print("  Rate limited. Waiting 10s then retrying...")
            time.sleep(10)
            result = client.scrape(url, formats=["html"])
            return result.html or ""
        raise


# ── Listing parser ───────────────────────────────────────────────────────────

def parse_athlete_cards(html: str) -> list[dict]:
    """Extract {name, image_url} from one ufc.com athlete listing page."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.c-listing-athlete-flipcard")
    out = []
    for card in cards:
        name_el = card.select_one(".c-listing-athlete__name")
        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            continue

        img_url = None
        thumb = card.select_one(".c-listing-athlete__thumbnail img")
        if thumb:
            for attr in ("src", "data-src"):
                val = thumb.get(attr)
                if val:
                    img_url = val.strip()
                    break

        if img_url and ("no-profile-image" in img_url.lower() or "silhouette" in img_url.lower()):
            img_url = None

        out.append({"name": name, "image_url": img_url})
    return out


def paginate_all(limit: int | None = None) -> list[dict]:
    athletes: list[dict] = []
    seen: set[tuple] = set()
    empty_streak = 0
    page = 0
    while True:
        url = LIST_URL.format(page=page)
        print(f"Fetching page {page}: {url}")
        try:
            html = firecrawl_html(url)
        except Exception as e:
            print(f"  ERROR fetching page {page}: {e}")
            empty_streak += 1
            if empty_streak >= MAX_EMPTY_PAGES:
                break
            page += 1
            time.sleep(DELAY)
            continue

        cards = parse_athlete_cards(html)
        new_count = 0
        for c in cards:
            key = (c["name"].lower(), c.get("image_url"))
            if key in seen:
                continue
            seen.add(key)
            athletes.append(c)
            new_count += 1

        print(f"  page {page}: parsed {len(cards)} cards, {new_count} new (total {len(athletes)})")

        if new_count == 0:
            empty_streak += 1
        else:
            empty_streak = 0

        if empty_streak >= MAX_EMPTY_PAGES:
            print(f"  Stopping: {empty_streak} consecutive empty pages")
            break
        if limit and len(athletes) >= limit:
            print(f"  Reached --limit {limit}")
            break

        page += 1
        time.sleep(DELAY)

    return athletes[:limit] if limit else athletes


# ── Filename + image helpers ─────────────────────────────────────────────────

def safe_filename(name: str) -> str:
    norm = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    norm = re.sub(r"[^A-Za-z0-9\s\-]", "", norm)
    norm = re.sub(r"\s+", " ", norm).strip()
    return norm.replace(" ", "_")


def make_black_placeholder(dest: Path) -> None:
    Image.new("RGB", (400, 400), (0, 0, 0)).save(dest, "JPEG", quality=85)


def download_image(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        img.save(dest, "JPEG", quality=90)
        return True
    except Exception as e:
        print(f"    download failed for {url}: {e}")
        return False


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="Cap athletes (for dry runs)")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output dir: {OUT_DIR}")

    athletes = paginate_all(limit=args.limit)
    print(f"\nTotal athletes collected: {len(athletes)}\n")

    if not athletes:
        print("ERROR: zero athletes parsed. CSS selector may be wrong — inspect listing HTML.")
        sys.exit(1)

    name_counts: Counter = Counter()
    downloaded = placeholders = skipped = 0

    for a in athletes:
        base = safe_filename(a["name"])
        if not base:
            continue
        name_counts[base] += 1
        suffix = "" if name_counts[base] == 1 else f"_{name_counts[base]}"
        filename = f"{base}{suffix}.jpg"
        dest = OUT_DIR / filename

        if dest.exists():
            skipped += 1
            continue

        if a.get("image_url"):
            if download_image(a["image_url"], dest):
                downloaded += 1
                time.sleep(0.1)
                continue

        make_black_placeholder(dest)
        placeholders += 1
        print(f"    placeholder: {filename}")

    print(f"\nSummary: {len(athletes)} athletes | {downloaded} downloaded | "
          f"{placeholders} placeholders | {skipped} skipped (already existed)")


if __name__ == "__main__":
    main()
