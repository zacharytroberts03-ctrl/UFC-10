"""Headless analysis pipeline — no Streamlit imports.

Used by both app.py (live, cache hit) and scripts/refresh_cache.py (cron).
"""

import os
import re
import sys
import datetime

BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, "tools"))
sys.path.insert(0, os.path.join(BASE_DIR, "Analysis", "tools"))

from scrape_ufc_fighter import scrape_fighter
from scrape_debut_fighter import scrape_debut_fighter
from scrape_odds import find_fight_odds
from hedge_calculator import summarize_hedge
import anthropic


_RULES_PATH = os.path.join(BASE_DIR, "Analysis", "rules", "BETTING_AI_RULES.md")
with open(_RULES_PATH, "r", encoding="utf-8") as f:
    BETTING_AI_RULES = f.read()


SYSTEM_PROMPT = f"""You are an expert UFC analyst and sports betting strategist with deep knowledge of mixed martial arts, fighter styles, matchup dynamics, and line value identification.

{BETTING_AI_RULES}

When analyzing a matchup:
1. Follow all rules in the FIGHT ANALYSIS RULES section above
2. Use the exact output format defined in OUTPUT FORMAT RULES
3. Always include the BETTING section as defined in BETTING RECOMMENDATION RULES
4. Be specific -- cite statistics, not adjectives
5. If stats show N/A (UFC debut), acknowledge the gap and analyze from available data only
"""


def format_fighter_block(f: dict) -> str:
    r = f["record"]
    s = f["striking"]
    g = f["grappling"]
    wm = f["win_methods"]
    wm_note = wm.get("note", "")
    is_debut = f.get("ufc_debut", False)
    debut_source = f.get("debut_source", "Tapology")

    history_lines = []
    for fight in f["fight_history"]:
        line = f"  {fight['result']} vs {fight['opponent']} -- {fight['method']}"
        if fight.get("promotion"):
            line += f" [{fight['promotion']}]"
        if fight.get("round") and fight["round"] != "N/A":
            line += f", R{fight['round']}"
        if fight.get("time") and fight["time"] != "N/A":
            line += f" ({fight['time']})"
        history_lines.append(line)

    history_text = "\n".join(history_lines) if history_lines else "  (No fight history parsed)"

    debut_header = ""
    stats_note = ""
    if is_debut:
        debut_header = f"  *** UFC DEBUT -- stats sourced from {debut_source} (pre-UFC career) ***\n"
        stats_note = (
            "\nNOTE: UFC per-minute striking/grappling averages are not available for this fighter "
            "as they have no UFC fights. Analyze their style based on fight history and win methods only."
        )

    return f"""=== {f['name'].upper()} ===
{debut_header}Record: {r['wins']}-{r['losses']}-{r['draws']}
Height: {f['height']} | Weight: {f['weight']} | Reach: {f['reach']} | Stance: {f['stance']}

Striking (career averages -- UFC only):
  {s['slpm']} sig. strikes landed/min | {s['sapm']} absorbed/min
  {s['str_acc']} striking accuracy | {s['str_def']} strike defense

Grappling (career averages -- UFC only):
  {g['td_avg']} takedowns/15min | {g['td_acc']} TD accuracy | {g['td_def']} TD defense
  {g['sub_avg']} submission attempts/15min

Win methods {wm_note}: {wm['ko']} KO/TKO | {wm['sub']} Submissions | {wm['dec']} Decisions

Recent fight history (most recent first):
{history_text}{stats_note}"""


def build_prompt(f1: dict, f2: dict) -> str:
    return f"""{format_fighter_block(f1)}

{format_fighter_block(f2)}

---

Produce the following analysis in this EXACT format, including the HTML comment markers exactly as shown:

<!--F1_PROFILE-->
## {f1['name']} -- Style & Profile
[Write 4-6 concise bullet points. Each bullet = one key insight: fighting style, best weapon, stat-backed tendency, behavior under pressure, or notable pattern from fight history. Be specific, cite numbers. No filler.]
<!--END-->

<!--F2_PROFILE-->
## {f2['name']} -- Style & Profile
[Same structure as above -- 4-6 concise bullet points.]
<!--END-->

<!--HEAD2HEAD-->
## Head-to-Head: Strengths & Weaknesses
[2-3 paragraphs analyzing how these styles interact. Where does each fighter have the edge? What are the critical exchanges that will decide this fight? Be specific about which stats matter most in this matchup.]
<!--END-->

<!--ENDINGS-->
## 3-5 Most Likely Fight Endings (Ranked by Probability)

Generate between 3 and 5 outcomes. Use 3 when the matchup has a clear stylistic favorite and limited realistic scenarios. Use 4 or 5 when there are multiple genuinely plausible paths to victory for either fighter.

**#1 -- [Specific description, e.g., "Jon Jones wins by TKO, Round 3"]**
Probability: [X]%
Why: [2-3 sentences of specific reasoning]

**#2 -- [Specific description]**
Probability: [X]%
Why: [2-3 sentences of specific reasoning]

**#3 -- [Specific description]**
Probability: [X]%
Why: [2-3 sentences of specific reasoning]

[Add #4 and #5 only if the matchup genuinely warrants additional scenarios]
<!--END-->

<!--BETTING-->
Include the full betting recommendation as defined in the BETTING RECOMMENDATION RULES in the system prompt. Use the exact structure specified there.
<!--END-->"""


def parse_analysis_sections(text: str) -> dict:
    sections = {}
    pattern = r"<!--(\w+)-->(.*?)<!--END-->"
    for match in re.finditer(pattern, text, re.DOTALL):
        key = match.group(1).lower()
        sections[key] = match.group(2).strip()
    return sections


def get_analysis(f1: dict, f2: dict) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
    prompt = build_prompt(f1, f2)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _scrape_one(name: str) -> dict:
    try:
        return scrape_fighter(name)
    except (ValueError, SystemExit):
        return scrape_debut_fighter(name)


def run_analysis(f1_name: str, f2_name: str, total_stake: float = 100.0) -> dict:
    """Run the full pipeline headlessly. Returns a JSON-serializable dict."""
    f1_data = _scrape_one(f1_name)
    f2_data = _scrape_one(f2_name)

    odds_data = None
    hedge_summary = None
    try:
        odds_data = find_fight_odds(f1_data["name"], f2_data["name"])
        if odds_data:
            hedge_summary = summarize_hedge(
                f1_data["name"], f2_data["name"], odds_data, total_stake
            )
    except Exception:
        pass

    raw_analysis = get_analysis(f1_data, f2_data)
    analysis_sections = parse_analysis_sections(raw_analysis)

    return {
        "f1_name": f1_data["name"],
        "f2_name": f2_data["name"],
        "f1_data": f1_data,
        "f2_data": f2_data,
        "odds_data": odds_data,
        "hedge_summary": hedge_summary,
        "analysis_sections": analysis_sections,
        "raw_analysis": raw_analysis,
        "total_stake": total_stake,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
