"""UFC 8 Design System — Cream + UFC Red Theme.

Call get_css() once at app start and inject via:
    st.markdown(get_css(), unsafe_allow_html=True)
"""


def get_css() -> str:
    """Return the full CSS stylesheet for the UFC 8 sportsbook UI."""
    return """<style>
/* ===== GOOGLE FONT ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* ===== BASE LAYOUT ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #f7f3ec !important;
    font-family: 'Inter', sans-serif !important;
    color: #1a1a1a;
}

[data-testid="stHeader"] {
    background-color: #f7f3ec !important;
}

.main .block-container {
    max-width: 1200px;
    padding: 2rem;
}

/* ===== TYPOGRAPHY ===== */
h1 {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
    color: #1a1a1a !important;
}

h2, h3, h4 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

p, li {
    color: #2a2a2a;
    line-height: 1.7;
}

strong {
    color: #1a1a1a;
}

hr {
    border-color: #d20a0a !important;
    opacity: 0.4;
}

/* ===== TABS ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 10px;
    border: 2px solid #d20a0a;
    gap: 0;
    padding: 4px;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
    background: transparent !important;
    padding: 8px 20px;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: #ffffff !important;
    background: #d20a0a !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none;
}

/* ===== BUTTONS (default look) ===== */
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stButton"] > button {
    background-color: #d20a0a !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: 2px solid #d20a0a !important;
    transition: all 0.2s ease;
}

[data-testid="stButton"] > button:hover {
    background-color: #ffffff !important;
    color: #d20a0a !important;
}

/* ===== EXPANDERS ===== */
[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 2px solid #d20a0a !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

[data-testid="stExpander"] summary:hover {
    color: #d20a0a !important;
}

/* ===== TEXT INPUTS ===== */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;
    border: 2px solid #d20a0a !important;
    color: #1a1a1a !important;
    border-radius: 8px !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #1a1a1a !important;
    box-shadow: 0 0 0 2px rgba(210,10,10,0.25) !important;
}

[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stTextArea"] label {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ===== FIGHT CARD BANNER ===== */
.fight-card-banner {
    background: linear-gradient(135deg, #ffffff 0%, #fbf6ec 100%);
    border-left: 6px solid #d20a0a;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

/* ===== FIGHTER VS BLOCK ===== */
.fighter-vs-block {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 16px;
    align-items: center;
}

.fighter-slot {
    background: #ffffff;
    border: 2px solid #d20a0a;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.vs-divider {
    color: #d20a0a;
    font-size: 1.4rem;
    font-weight: 800;
    text-align: center;
}

/* ===== MONEYLINE PILL ===== */
.moneyline-pill {
    display: inline-block;
    background: #f7f3ec;
    border: 1px solid #d20a0a;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 800;
    font-size: 1.1rem;
    letter-spacing: 0.5px;
}

.moneyline-pill.positive { color: #0a8a3a; }
.moneyline-pill.negative { color: #d20a0a; }
.moneyline-pill.neutral  { color: #1a1a1a; }

/* ===== ODDS TABLE ===== */
.odds-table {
    width: 100%;
    border-collapse: collapse;
    background: #ffffff;
    border: 2px solid #d20a0a;
    border-radius: 10px;
    overflow: hidden;
}

.odds-table th {
    background: #d20a0a;
    color: #ffffff;
    text-transform: uppercase;
    font-size: 0.78rem;
    letter-spacing: 0.8px;
    padding: 12px 16px;
    text-align: left;
}

.odds-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #f0e6d2;
    color: #1a1a1a;
}

.odds-table tr:last-child td { border-bottom: none; }

.odds-table tr:hover td { background: #fbf6ec; }

.odds-table .best-line {
    color: #d20a0a;
    font-weight: 800;
}

/* ===== ARB BANNER ===== */
.arb-banner {
    background: #e9f9ef;
    border: 2px solid #0a8a3a;
    border-radius: 12px;
    padding: 18px 22px;
    color: #0a6a2a;
}

/* ===== NO-ARB BANNER ===== */
.no-arb-banner {
    background: #fdecec;
    border: 2px solid #d20a0a;
    border-radius: 12px;
    padding: 14px 18px;
    color: #8a0a0a;
}

/* ===== HEDGE RESULT CARD ===== */
.hedge-result-card {
    background: #ffffff;
    border: 2px solid #d20a0a;
    border-radius: 12px;
    padding: 22px;
}

.hedge-result-card .bet-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #f0e6d2;
    align-items: center;
}

.hedge-result-card .bet-row:last-of-type { border-bottom: none; }

.hedge-result-card .bet-book {
    color: #6a6a6a;
    font-size: 0.9rem;
}

.hedge-result-card .bet-amount {
    color: #d20a0a;
    font-weight: 800;
    font-size: 1.1rem;
}

.hedge-result-card .profit-line {
    color: #0a8a3a;
    font-weight: 800;
    font-size: 1.2rem;
    padding-top: 12px;
}

/* ===== ANALYSIS BLOCK ===== */
.analysis-block {
    background: #ffffff;
    border: 2px solid #d20a0a;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 16px;
}

.analysis-block, .analysis-block * { color: #1a1a1a; }

/* ===== SECTION LABEL ===== */
.section-label {
    border-left: 5px solid #d20a0a;
    padding-left: 12px;
    margin: 28px 0 14px 0;
    color: #1a1a1a;
    font-weight: 800;
    font-size: 1.15rem;
}

/* ===== BETTING REC BLOCK ===== */
.betting-rec-block {
    background: #fff8f8;
    border: 2px solid #d20a0a;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 16px;
}

.betting-rec-block, .betting-rec-block * { color: #1a1a1a; }

.betting-rec-block .rec-header {
    color: #d20a0a;
    font-weight: 800;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 12px;
}

/* ===== DEBUT BADGE ===== */
.debut-badge {
    background: #d20a0a;
    color: #ffffff;
    font-weight: 800;
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 0.72rem;
    display: inline-block;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f7f3ec; }
::-webkit-scrollbar-thumb { background: #d20a0a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #8a0a0a; }

/* ===== UFC POSTER-STYLE FIGHT GRID ===== */
.section-header {
    margin: 32px 0 18px 0;
    padding: 14px 24px;
    background: #d20a0a;
    border-top: 3px solid #1a1a1a;
    border-bottom: 3px solid #1a1a1a;
    color: #ffffff;
    font-weight: 800;
    font-size: 1.6rem;
    letter-spacing: 4px;
    text-align: center;
    text-transform: uppercase;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    border-radius: 4px;
}

/* ===== CLICKABLE FIGHT TILES ===== */
/* Each fight tile is a Streamlit button. Compact, white, red border. */
.fight-tile-row [data-testid="stButton"] > button {
    background: #ffffff !important;
    color: #1a1a1a !important;
    border: 2px solid #d20a0a !important;
    border-radius: 12px !important;
    height: 180px !important;
    width: 180px !important;
    max-width: 180px !important;
    margin: 0 auto !important;
    padding: 12px 8px !important;
    white-space: pre-line !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.82rem !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: all 0.15s ease;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.fight-tile-row { display: flex; justify-content: center; }

.fight-tile-row [data-testid="stButton"] > button:hover {
    background: #d20a0a !important;
    color: #ffffff !important;
    border-color: #1a1a1a !important;
    transform: translateY(-2px);
}

/* Main event badge + tile */
.main-event-badge {
    text-align: center;
    color: #ffffff;
    background: #1a1a1a;
    font-weight: 800;
    font-size: 0.85rem;
    letter-spacing: 4px;
    padding: 6px 0;
    margin: 18px auto 8px auto;
    max-width: 50%;
    border-radius: 4px;
    border: 2px solid #d20a0a;
}

.main-event-tile [data-testid="stButton"] > button {
    height: 200px !important;
    width: 200px !important;
    max-width: 200px !important;
    font-size: 0.95rem !important;
    border-width: 3px !important;
    box-shadow: 0 4px 14px rgba(210,10,10,0.18);
}

/* Pending analysis card */
.pending-card {
    background: #fff8f8;
    border: 2px dashed #d20a0a;
    border-radius: 12px;
    padding: 28px;
    text-align: center;
    color: #1a1a1a;
    margin: 18px 0;
}
.pending-card .pending-title {
    font-weight: 800;
    font-size: 1.25rem;
    color: #d20a0a;
    margin-bottom: 8px;
}

/* Back-to-card button */
.back-btn-wrap [data-testid="stButton"] > button {
    background: #ffffff !important;
    border: 2px solid #d20a0a !important;
    color: #d20a0a !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
}
.back-btn-wrap [data-testid="stButton"] > button:hover {
    background: #d20a0a !important;
    color: #ffffff !important;
}
</style>"""
