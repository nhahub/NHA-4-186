import streamlit as st


def inject_theme_js():
    theme = st.session_state.get("theme", "light")
    js = f"""<script>
try{{document.documentElement.setAttribute('data-theme','{theme}');document.documentElement.style.colorScheme='{theme}'}}catch(e){{}}
</script>"""
    try:
        st.components.v1.html(js, width=0, height=0)
    except Exception:
        pass


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&display=swap');

:root {
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

/* =========================================================
   LIGHT THEME (default)
   ========================================================= */
:root {
    --main-header-bg: linear-gradient(135deg, #2E86AB 0%, #1B4965 100%);
    --page-bg: #FFFFFF;
    --card-bg: #FFFFFF;
    --card-shadow: 0 2px 8px rgba(0,0,0,0.06);
    --card-border: 1px solid #E0E4E8;
    --sidebar-bg: #F8FAFC;
    --sidebar-border: 1px solid #E0E4E8;
    --text-primary: #262730;
    --text-secondary: #6B7280;
    --text-muted: #888;
    --accent: #2E86AB;
    --accent-cyan: #2E86AB;
    --border: #E0E4E8;
    --input-bg: #FFFFFF;
    --input-border: 1px solid #D1D5DB;
    --metric-bg: #FFFFFF;
    --metric-border: #E0E4E8;
    --dataframe-header: #F8FAFC;
    --dataframe-header-text: #374151;
    --dataframe-border: 1px solid #E0E4E8;
    --tab-border: #E0E4E8;
    --tab-active: #2E86AB;
    --tab-inactive: #6B7280;
    --form-bg: #FFFFFF;
    --form-border: #E0E4E8;
    --badge-critical-bg: #fde8e8;
    --badge-critical-text: #c0392b;
    --badge-warning-bg: #fef3cd;
    --badge-warning-text: #b9770e;
    --badge-healthy-bg: #d5f5e3;
    --badge-healthy-text: #1e8449;
    --status-healthy-bg: #E8F5E9;
    --status-healthy-text: #2E7D32;
    --status-warning-bg: #FFF3E0;
    --status-warning-text: #E65100;
    --status-critical-bg: #FFEBEE;
    --status-critical-text: #C62828;
    --status-pending-bg: #F3E5F5;
    --status-pending-text: #7B1FA2;
    --status-completed-bg: #E8F5E9;
    --status-completed-text: #2E7D32;
    --role-admin-bg: #FFEBEE;
    --role-admin-text: #C62828;
    --role-engineer-bg: #E3F2FD;
    --role-engineer-text: #1565C0;
    --engine-critical-bg: #fff5f5;
    --engine-warning-bg: #fffdf5;
    --engine-healthy-bg: #f5fff8;
    --rul-bar-bg: #eee;
    --section-title-color: #1B4965;
    --sidebar-user-bg: #FFFFFF;
    --sidebar-user-border: #E0E4E8;
    --stat-value-color: #1B4965;
    --stat-label-color: #6B7280;
    --btn-shadow: 0 4px 10px rgba(0,0,0,0.1);
    --scrollbar-bg: #f1f1f1;
    --scrollbar-thumb: #c1c1c1;
    --kpi-critical: #e74c3c;
    --kpi-warning: #f39c12;
    --kpi-success: #2ecc71;
    --kpi-info: #3498db;
    --engine-critical-border: #e74c3c;
    --engine-warning-border: #f39c12;
    --engine-healthy-border: #2ecc71;
    --stat-card-border-left: #3498db;
}

/* =========================================================
   DARK THEME
   ========================================================= */
html[data-theme="dark"] {
    --main-header-bg: linear-gradient(135deg, #0d2137 0%, #050a12 100%);
    --page-bg: #0a0e17;
    --card-bg: #111827;
    --card-shadow: 0 4px 16px rgba(0,0,0,0.2);
    --card-border: 1px solid rgba(255,255,255,0.06);
    --sidebar-bg: #0d1117;
    --sidebar-border: 1px solid rgba(0,229,255,0.08);
    --text-primary: #e2e8f0;
    --text-secondary: #9CA3AF;
    --text-muted: #8892a4;
    --accent: #00e5ff;
    --accent-cyan: #00e5ff;
    --border: rgba(255,255,255,0.06);
    --input-bg: rgba(255,255,255,0.04);
    --input-border: 1px solid rgba(255,255,255,0.1);
    --metric-bg: #111827;
    --metric-border: rgba(255,255,255,0.06);
    --dataframe-header: rgba(0,229,255,0.05);
    --dataframe-header-text: #00e5ff;
    --dataframe-border: 1px solid rgba(255,255,255,0.06);
    --tab-border: rgba(255,255,255,0.06);
    --tab-active: #00e5ff;
    --tab-inactive: #8892a4;
    --form-bg: #111827;
    --form-border: rgba(255,255,255,0.06);
    --badge-critical-bg: rgba(255,45,85,0.15);
    --badge-critical-text: #ff2d55;
    --badge-warning-bg: rgba(255,179,0,0.15);
    --badge-warning-text: #ffb300;
    --badge-healthy-bg: rgba(0,255,136,0.15);
    --badge-healthy-text: #00ff88;
    --status-healthy-bg: rgba(0,255,136,0.12);
    --status-healthy-text: #00ff88;
    --status-warning-bg: rgba(255,179,0,0.12);
    --status-warning-text: #ffb300;
    --status-critical-bg: rgba(255,45,85,0.12);
    --status-critical-text: #ff2d55;
    --status-pending-bg: rgba(0,229,255,0.12);
    --status-pending-text: #00e5ff;
    --status-completed-bg: rgba(0,255,136,0.12);
    --status-completed-text: #00ff88;
    --role-admin-bg: rgba(255,45,85,0.15);
    --role-admin-text: #ff2d55;
    --role-engineer-bg: rgba(0,229,255,0.15);
    --role-engineer-text: #00e5ff;
    --engine-critical-bg: rgba(255,45,85,0.04);
    --engine-warning-bg: rgba(255,179,0,0.04);
    --engine-healthy-bg: rgba(0,255,136,0.04);
    --rul-bar-bg: rgba(255,255,255,0.06);
    --section-title-color: #00e5ff;
    --sidebar-user-bg: rgba(17,24,39,0.65);
    --sidebar-user-border: rgba(255,255,255,0.06);
    --stat-value-color: #e2e8f0;
    --stat-label-color: #8892a4;
    --btn-shadow: 0 0 16px rgba(0,229,255,0.25);
    --scrollbar-bg: #1a1f2e;
    --scrollbar-thumb: #2d3748;
    --kpi-critical: #ff2d55;
    --kpi-warning: #ffb300;
    --kpi-success: #00ff88;
    --kpi-info: #00e5ff;
    --engine-critical-border: #ff2d55;
    --engine-warning-border: #ffb300;
    --engine-healthy-border: #00ff88;
    --stat-card-border-left: #00e5ff;
}

/* =========================================================
   PAGE BACKGROUND
   ========================================================= */
body, #root, .stApp, section[data-testid="stMain"] {
    background: var(--page-bg) !important;
}
section[data-testid="stMain"] .block-container {
    background: var(--page-bg) !important;
}
[data-testid="stAppViewContainer"] {
    background: var(--page-bg);
}

/* Scan-line overlay (dark only) */
html[data-theme="dark"] [data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,229,255,0.012) 2px, rgba(0,229,255,0.012) 4px
    );
    pointer-events: none;
    z-index: 999999;
}

/* =========================================================
   MAIN HEADER
   ========================================================= */
.main-header {
    background: var(--main-header-bg);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
}
html[data-theme="dark"] .main-header { box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
html[data-theme="dark"] .main-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(0,229,255,0.06), transparent 60%);
    pointer-events: none;
}
.main-header h1 {
    color: #FFFFFF;
    font-weight: 700;
    margin: 0;
    font-size: 1.8rem;
    position: relative;
    z-index: 1;
}
html[data-theme="dark"] .main-header h1 {
    text-shadow: 0 0 16px rgba(0,229,255,0.3);
}
.main-header p {
    color: rgba(255,255,255,0.85);
    margin: 0.3rem 0 0 0;
    font-size: 0.95rem;
    position: relative;
    z-index: 1;
}

/* =========================================================
   KPI CARDS
   ========================================================= */
.kpi-card {
    background: var(--card-bg);
    box-shadow: var(--card-shadow);
    border: var(--card-border);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1);
    border-left: 4px solid var(--accent);
}
.kpi-card.critical { border-left-color: var(--kpi-critical); }
.kpi-card.warning  { border-left-color: var(--kpi-warning); }
.kpi-card.success  { border-left-color: var(--kpi-success); }
.kpi-card.info     { border-left-color: var(--kpi-info); }
html[data-theme="dark"] .kpi-card:hover { box-shadow: 0 8px 24px rgba(0,229,255,0.08); }
html[data-theme="dark"] .kpi-card.critical { box-shadow: 0 0 16px rgba(255,45,85,0.05); }

.kpi-value {
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0;
    font-family: var(--font-mono);
    color: var(--stat-value-color);
}
html[data-theme="dark"] .kpi-value {
    text-shadow: 0 0 8px rgba(0,229,255,0.3);
}
html[data-theme="dark"] .kpi-card.critical .kpi-value { color: var(--kpi-critical); text-shadow: 0 0 8px rgba(255,45,85,0.4); }
html[data-theme="dark"] .kpi-card.warning .kpi-value { color: var(--kpi-warning); text-shadow: 0 0 8px rgba(255,179,0,0.4); }
html[data-theme="dark"] .kpi-card.success .kpi-value { color: var(--kpi-success); text-shadow: 0 0 8px rgba(0,255,136,0.4); }
html[data-theme="dark"] .kpi-card.info .kpi-value { color: var(--kpi-info); text-shadow: 0 0 8px rgba(0,229,255,0.4); }

.kpi-label {
    color: var(--stat-label-color);
    font-size: 0.82rem;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* =========================================================
   STATUS BADGES
   ========================================================= */
.status-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-align: center;
    transition: all 0.2s ease;
}
.status-badge.healthy { background: var(--status-healthy-bg); color: var(--status-healthy-text); }
.status-badge.warning { background: var(--status-warning-bg); color: var(--status-warning-text); }
.status-badge.critical { background: var(--status-critical-bg); color: var(--status-critical-text); }
.status-badge.pending { background: var(--status-pending-bg); color: var(--status-pending-text); }
.status-badge.completed { background: var(--status-completed-bg); color: var(--status-completed-text); }
html[data-theme="dark"] .status-badge {
    box-shadow: 0 0 8px color-mix(in srgb, currentColor 15%, transparent);
}

/* =========================================================
   ROLE BADGES
   ========================================================= */
.role-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.role-badge.admin { background: var(--role-admin-bg); color: var(--role-admin-text); }
.role-badge.engineer { background: var(--role-engineer-bg); color: var(--role-engineer-text); }

/* =========================================================
   ENGINE CARDS
   ========================================================= */
.engine-card {
    background: var(--card-bg);
    border: var(--card-border);
    box-shadow: var(--card-shadow);
    border-radius: 12px;
    padding: 1rem;
    border-left: 5px solid #ccc;
    margin-bottom: 0.6rem;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1);
}
.engine-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
html[data-theme="dark"] .engine-card:hover { box-shadow: 0 4px 20px rgba(0,229,255,0.1); }
.engine-card.critical { border-left-color: var(--engine-critical-border); background: var(--engine-critical-bg); }
.engine-card.warning  { border-left-color: var(--engine-warning-border); background: var(--engine-warning-bg); }
.engine-card.healthy  { border-left-color: var(--engine-healthy-border); background: var(--engine-healthy-bg); }

/* =========================================================
   BADGES
   ========================================================= */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
}
.badge-critical { background: var(--badge-critical-bg); color: var(--badge-critical-text); }
.badge-warning  { background: var(--badge-warning-bg); color: var(--badge-warning-text); }
.badge-healthy  { background: var(--badge-healthy-bg); color: var(--badge-healthy-text); }
html[data-theme="dark"] .badge { box-shadow: 0 0 6px color-mix(in srgb, currentColor 20%, transparent); }

/* =========================================================
   RUL BAR
   ========================================================= */
.rul-bar-container {
    width: 100%;
    height: 8px;
    background: var(--rul-bar-bg);
    border-radius: 4px;
    overflow: hidden;
}
.rul-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}
html[data-theme="dark"] .engine-card.critical .rul-bar-fill { background: linear-gradient(90deg, #ff2d55, #ff6680) !important; }
html[data-theme="dark"] .engine-card.warning .rul-bar-fill { background: linear-gradient(90deg, #ffb300, #ffcc66) !important; }
html[data-theme="dark"] .engine-card.healthy .rul-bar-fill { background: linear-gradient(90deg, #00ff88, #66ffb3) !important; }

/* =========================================================
   SECTION TITLE
   ========================================================= */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    color: var(--section-title-color);
    border-bottom: 2px solid var(--border);
}

/* =========================================================
   STAT CARDS
   ========================================================= */
.stat-card {
    background: var(--card-bg);
    box-shadow: var(--card-shadow);
    border: var(--card-border);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    border-left: 4px solid var(--stat-card-border-left);
}
.stat-card.critical { border-left-color: var(--kpi-critical); }
.stat-card.warning  { border-left-color: var(--kpi-warning); }
.stat-card.success  { border-left-color: var(--kpi-success); }
.stat-card.info     { border-left-color: var(--kpi-info); }
.stat-value {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    font-family: var(--font-mono);
    color: var(--stat-value-color);
}
.stat-label {
    font-size: 0.82rem;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--stat-label-color);
}

/* =========================================================
   BUTTONS
   ========================================================= */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: var(--btn-shadow);
}
html[data-theme="dark"] .stButton > button {
    border-radius: 50px !important;
}
html[data-theme="dark"] .stButton > button {
    border: 1px solid rgba(0,229,255,0.3) !important;
    background: rgba(0,229,255,0.08) !important;
    color: var(--accent-cyan) !important;
    transition: all 0.25s ease !important;
}
html[data-theme="dark"] .stButton > button:hover {
    background: rgba(0,229,255,0.15) !important;
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 16px rgba(0,229,255,0.25) !important;
}
html[data-theme="dark"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-cyan), #0098b0) !important;
    border: none !important;
    color: #0a0e17 !important;
    font-weight: 700 !important;
}
html[data-theme="dark"] .stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(0,229,255,0.35) !important;
}
html[data-theme="dark"] .stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: var(--text-primary) !important;
}

html[data-theme="dark"] .stDownloadButton > button {
    border-radius: 50px !important;
    border: 1px solid rgba(0,229,255,0.3) !important;
    background: rgba(0,229,255,0.08) !important;
    color: var(--accent-cyan) !important;
}
html[data-theme="dark"] .stDownloadButton > button:hover {
    background: rgba(0,229,255,0.15) !important;
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 16px rgba(0,229,255,0.25) !important;
}

/* =========================================================
   SIDEBAR
   ========================================================= */
div[data-testid="stSidebar"] {
    background: var(--sidebar-bg);
    border-right: var(--sidebar-border);
}
html[data-theme="dark"] div[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(to bottom, transparent, rgba(0,229,255,0.3), transparent);
}

.sidebar-user {
    background: var(--sidebar-user-bg);
    border: 1px solid var(--sidebar-user-border);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    text-align: center;
}
html[data-theme="dark"] .sidebar-user {
    backdrop-filter: blur(12px);
}
.sidebar-user .avatar { font-size: 2.5rem; margin-bottom: 0.4rem; }
.sidebar-user .name { font-weight: 700; font-size: 0.95rem; color: var(--section-title-color); }
.sidebar-user .username { font-size: 0.8rem; color: var(--text-secondary); }

.sidebar-footer {
    font-size: 0.7rem;
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
}

/* =========================================================
   TABS
   ========================================================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    border-bottom: 2px solid var(--tab-border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 0.5rem 1rem;
    font-weight: 500;
    color: var(--tab-inactive);
}
.stTabs [aria-selected="true"] {
    font-weight: 600;
    color: var(--tab-active);
}
html[data-theme="dark"] .stTabs [data-baseweb="tab"]::after {
    content: '';
    position: absolute;
    bottom: 0; left: 50%;
    width: 0; height: 2px;
    background: var(--accent-cyan);
    transition: all 0.3s ease;
    transform: translateX(-50%);
}
html[data-theme="dark"] .stTabs [data-baseweb="tab"][aria-selected="true"]::after { width: 80%; }

/* =========================================================
   FORMS
   ========================================================= */
.stForm {
    background: var(--form-bg);
    border: 1px solid var(--form-border);
    border-radius: 10px;
    padding: 1.2rem;
}

/* =========================================================
   METRICS
   ========================================================= */
div[data-testid="stMetric"] {
    background: var(--metric-bg) !important;
    border: 1px solid var(--metric-border) !important;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
div[data-testid="stMetric"] > div { gap: 0.2rem; }
div[data-testid="stMetric"] label {
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-secondary) !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--section-title-color) !important;
}
html[data-theme="dark"] div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: var(--font-mono);
    color: var(--accent-cyan) !important;
}

/* =========================================================
   DATA FRAME
   ========================================================= */
div[data-testid="stDataFrame"] {
    border: var(--dataframe-border);
    border-radius: 8px;
    overflow: hidden;
}
div[data-testid="stDataFrame"] thead tr th {
    background: var(--dataframe-header) !important;
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--dataframe-header-text) !important;
}
html[data-theme="dark"] div[data-testid="stDataFrame"] tbody tr td {
    color: var(--text-primary) !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
}
html[data-theme="dark"] div[data-testid="stDataFrame"] tbody tr:hover td {
    background: rgba(0,229,255,0.02) !important;
}

/* =========================================================
   INPUT FIELDS
   ========================================================= */
.stTextInput input, .stNumberInput input, .stSelectbox > div,
.stTextArea textarea, .stDateInput input {
    background: var(--input-bg) !important;
    border: var(--input-border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 15%, transparent) !important;
}

/* =========================================================
   ALERTS
   ========================================================= */
.stAlert {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}
.stAlert [data-testid="stMarkdownContainer"] {
    color: var(--text-primary) !important;
}

/* =========================================================
   TEXT / LABELS
   ========================================================= */
.stMarkdown, .stMarkdown p, label,
.stSelectbox label, .stNumberInput label,
.stTextInput label, .stTextArea label, .stDateInput label {
    color: var(--text-primary) !important;
}

/* =========================================================
   EXPANDER
   ========================================================= */
[data-testid="stExpander"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
}

/* =========================================================
   DIVIDER
   ========================================================= */
hr { border-color: var(--border) !important; }

/* =========================================================
   STATUS DOT (pulsing)
   ========================================================= */
.status-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    vertical-align: middle;
}
.status-dot.critical { background: var(--kpi-critical); }
.status-dot.warning { background: var(--kpi-warning); }
.status-dot.healthy { background: var(--kpi-success); }
html[data-theme="dark"] .status-dot.critical { box-shadow: 0 0 6px var(--kpi-critical), 0 0 12px rgba(255,45,85,0.4); animation: pulse-critical 1.5s ease-in-out infinite; }
html[data-theme="dark"] .status-dot.warning { box-shadow: 0 0 6px var(--kpi-warning), 0 0 12px rgba(255,179,0,0.4); animation: pulse-warning 2s ease-in-out infinite; }
html[data-theme="dark"] .status-dot.healthy { box-shadow: 0 0 6px var(--kpi-success), 0 0 12px rgba(0,255,136,0.4); animation: pulse-healthy 2.5s ease-in-out infinite; }

@keyframes pulse-critical {
    0%, 100% { box-shadow: 0 0 4px var(--kpi-critical), 0 0 8px rgba(255,45,85,0.25); }
    50% { box-shadow: 0 0 12px var(--kpi-critical), 0 0 24px rgba(255,45,85,0.5); }
}
@keyframes pulse-warning {
    0%, 100% { box-shadow: 0 0 4px var(--kpi-warning), 0 0 8px rgba(255,179,0,0.25); }
    50% { box-shadow: 0 0 12px var(--kpi-warning), 0 0 24px rgba(255,179,0,0.5); }
}
@keyframes pulse-healthy {
    0%, 100% { box-shadow: 0 0 4px var(--kpi-success), 0 0 8px rgba(0,255,136,0.25); }
    50% { box-shadow: 0 0 12px var(--kpi-success), 0 0 24px rgba(0,255,136,0.5); }
}

/* =========================================================
   UTILITY
   ========================================================= */
.text-muted { color: var(--text-muted); }
.text-sm { font-size: 0.78rem; }
.text-xs { font-size: 0.72rem; }
.text-critical { color: var(--kpi-critical) !important; }
.fw-800 { font-weight: 800; }

html[data-theme="dark"] .color-scheme { color-scheme: dark; }

/* =========================================================
   SCROLLBAR (dark only)
   ========================================================= */
html[data-theme="dark"] ::-webkit-scrollbar { width: 8px; }
html[data-theme="dark"] ::-webkit-scrollbar-track { background: var(--scrollbar-bg); }
html[data-theme="dark"] ::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 4px; }

/* =========================================================
   EXTRA DARK EFFECTS
   ========================================================= */
html[data-theme="dark"] .neon-text { color: var(--accent-cyan); text-shadow: 0 0 8px rgba(0,229,255,0.5), 0 0 16px rgba(0,229,255,0.2); }
html[data-theme="dark"] .neon-text.critical { color: var(--kpi-critical); text-shadow: 0 0 8px rgba(255,45,85,0.5), 0 0 16px rgba(255,45,85,0.2); }
html[data-theme="dark"] .neon-text.warning { color: var(--kpi-warning); text-shadow: 0 0 8px rgba(255,179,0,0.5), 0 0 16px rgba(255,179,0,0.2); }
html[data-theme="dark"] .neon-text.healthy { color: var(--kpi-success); text-shadow: 0 0 8px rgba(0,255,136,0.5), 0 0 16px rgba(0,255,136,0.2); }

html[data-theme="dark"] .glass-panel { background: rgba(17,24,39,0.65); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.06); }

html[data-theme="dark"] .glow-border { position: relative; border: 1px solid transparent !important; background: var(--card-bg); background-clip: padding-box; }
html[data-theme="dark"] .glow-border::before {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: inherit;
    background: linear-gradient(135deg, var(--accent-cyan), var(--kpi-critical), var(--kpi-warning), var(--accent-cyan));
    background-size: 300% 300%;
    animation: rotate-gradient 4s ease infinite;
    z-index: -1;
    opacity: 0.7;
}
@keyframes rotate-gradient {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

html[data-theme="dark"] .gauge {
    width: 90px; height: 90px;
    border-radius: 50%;
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
}
html[data-theme="dark"] .gauge::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(var(--gauge-color, var(--accent-cyan)) 0deg var(--gauge-deg, 0deg), var(--bg-elevated, #1a1f2e) var(--gauge-deg, 0deg) 360deg);
    mask: radial-gradient(circle, transparent 58%, black 60%);
    -webkit-mask: radial-gradient(circle, transparent 58%, black 60%);
}
html[data-theme="dark"] .gauge-value { font-family: var(--font-mono); font-size: 1.4rem; font-weight: 800; z-index: 1; }
</style>
"""

import streamlit as st

import streamlit as st


def inject_global_css():

    if st.session_state.get("theme", "dark") == "dark":

        st.markdown("""
        <style>

        /* ===========================
           Main Background
        ============================ */
        .stApp{
            background:#0F172A;
            color:#F8FAFC;
        }

        .main{
            background:#0F172A;
            color:#F8FAFC;
        }

        /* ===========================
           Sidebar
        ============================ */

        section[data-testid="stSidebar"]{
            background:#111827;
            border-right:1px solid #334155;
        }

        .sidebar-user{
            background:#1E293B;
            color:white;
            border-radius:15px;
            padding:18px;
            margin-bottom:15px;
            text-align:center;
            border:1px solid #334155;
        }

        .sidebar-footer{
            color:#94A3B8;
            text-align:center;
            margin-top:20px;
            font-size:13px;
        }

        /* ===========================
           HEADINGS
        ============================ */

        h1,h2,h3,h4,h5,h6{
            color:#F8FAFC !important;
        }

        p,label,span,div{
            color:#F8FAFC;
        }

        /* ===========================
           Metric Cards
        ============================ */

        div[data-testid="stMetric"]{
            background:#1E293B;
            border:1px solid #334155;
            border-radius:15px;
            padding:15px;
        }

        div[data-testid="stMetric"] label{
            color:#CBD5E1 !important;
        }

        div[data-testid="stMetricValue"]{
            color:white !important;
        }

        /* ===========================
           Buttons
        ============================ */

        .stButton>button{
            width:100%;
            background:#2563EB;
            color:white;
            border:none;
            border-radius:10px;
            padding:10px;
        }

        .stButton>button:hover{
            background:#1D4ED8;
            color:white;
        }

        /* ===========================
           Inputs
        ============================ */

        .stTextInput input,
        .stNumberInput input,
        textarea{
            background:#1E293B !important;
            color:white !important;
            border:1px solid #334155;
        }

        .stSelectbox div[data-baseweb="select"]{
            background:#1E293B !important;
            color:white !important;
        }

        /* ===========================
           DataFrames
        ============================ */

        div[data-testid="stDataFrame"]{
            border-radius:15px;
            border:1px solid #334155;
        }

        /* ===========================
           Tabs
        ============================ */

        button[data-baseweb="tab"]{
            color:#CBD5E1 !important;
            background:#1E293B;
            border-radius:10px;
        }

        button[data-baseweb="tab"][aria-selected="true"]{
            color:white !important;
            background:#2563EB !important;
        }

        /* ===========================
           Markdown Containers
        ============================ */

        div[data-testid="stMarkdownContainer"] *{
            color:#F8FAFC !important;
        }

        /* ===========================
           Info / Warning / Success
        ============================ */

        div[data-testid="stAlert"]{
            border-radius:12px;
        }

        </style>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <style>

        .stApp{
            background:#F8FAFC;
            color:#1F2937;
        }

        .main{
            background:#F8FAFC;
            color:#1F2937;
        }

        section[data-testid="stSidebar"]{
            background:#FFFFFF;
            border-right:1px solid #E5E7EB;
        }

        .sidebar-user{
            background:white;
            border-radius:15px;
            padding:18px;
            margin-bottom:15px;
            text-align:center;
            border:1px solid #E5E7EB;
        }

        .sidebar-footer{
            color:#6B7280;
            text-align:center;
            margin-top:20px;
            font-size:13px;
        }

        h1,h2,h3,h4,h5,h6{
            color:#111827;
        }

        p,label,span,div{
            color:#1F2937;
        }

        div[data-testid="stMetric"]{
            background:white;
            border:1px solid #E5E7EB;
            border-radius:15px;
            padding:15px;
        }

        .stButton>button{
            width:100%;
            background:#2563EB;
            color:white;
            border:none;
            border-radius:10px;
            padding:10px;
        }

        .stButton>button:hover{
            background:#1D4ED8;
            color:white;
        }

        div[data-testid="stDataFrame"]{
            border-radius:15px;
            border:1px solid #E5E7EB;
        }

        button[data-baseweb="tab"]{
            border-radius:10px;
        }

        button[data-baseweb="tab"][aria-selected="true"]{
            background:#2563EB !important;
            color:white !important;
        }

        </style>
        """, unsafe_allow_html=True)
   # inject_theme_js()
   # st.markdown(CSS, unsafe_allow_html=True)


def status_badge_html(status):
    cls = status.lower().replace(" ", "-")
    if cls in ("healthy", "good"):
        cls = "healthy"
    elif cls in ("warning", "fair", "poor"):
        cls = "warning"
    elif cls in ("critical", "high-risk"):
        cls = "critical"
    return f'<span class="status-badge {cls}">{status}</span>'


def role_badge_html(role):
    cls = role.lower()
    return f'<span class="role-badge {cls}">{role}</span>'


def dot_html(status):
    cls = status.lower()
    return f'<span class="status-dot {cls}"></span>'
