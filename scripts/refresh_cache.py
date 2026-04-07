"""Daily cron: pre-generate analyses for the current UFC card.

Usage:
    python scripts/refresh_cache.py           # only run for fights not yet cached
    python scripts/refresh_cache.py --force   # re-run for every fight on the card
"""

import os
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "tools"))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except ImportError:
    pass

from scrape_ufc_card import scrape_upcoming_card
from analysis_runner import run_analysis
from cache import load_cache, save_cache, fight_key


def event_key(card: dict) -> str:
    name = card.get("event_name", "unknown").lower().replace(" ", "-")
    date = card.get("date", "")
    return f"{name}__{date}"


def main() -> int:
    force = "--force" in sys.argv

    for var in ("ANTHROPIC_API_KEY", "FIRECRAWL_API_KEY"):
        if not os.environ.get(var):
            print(f"ERROR: {var} not set", file=sys.stderr)
            return 2

    print("Scraping current UFC card...")
    card = scrape_upcoming_card()
    fights = card.get("fights", [])
    print(f"Found {len(fights)} fights for: {card.get('event_name')}")

    cache = load_cache()
    new_event = event_key(card)
    if cache.get("event_key") != new_event:
        print(f"New event detected ({new_event}); resetting cache.")
        cache = {"event_key": new_event, "generated_at": None, "fights": {}}

    failures = []
    for i, f in enumerate(fights, 1):
        f1 = f["fighter1"]
        f2 = f["fighter2"]
        key = fight_key(f1, f2)

        if not force and key in cache["fights"]:
            print(f"  [{i}/{len(fights)}] cached, skipping: {f1} vs {f2}")
            continue

        print(f"  [{i}/{len(fights)}] running: {f1} vs {f2}")
        try:
            result = run_analysis(f1, f2)
            cache["fights"][key] = result
            cache["generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            save_cache(cache)
        except Exception as e:
            print(f"      FAILED: {e}", file=sys.stderr)
            failures.append((f1, f2, str(e)))

    save_cache(cache)
    print(f"\nDone. {len(cache['fights'])} fights cached, {len(failures)} failures.")

    if failures:
        for f1, f2, err in failures:
            print(f"  - {f1} vs {f2}: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
