import streamlit as st import datetime 
import sqlite3

# Page Configuration
st.set_page_config(
    page_title="RYL: Ran Your Life",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# SQLite Database Initialization for Persistent Sovereignty
def init_db():
    conn = sqlite3.connect('ryl_local.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ledger 
                 (date TEXT PRIMARY KEY, intent TEXT, nasigoreng_orders INT, github_pushes INT, notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, project TEXT, task_name TEXT, completed INT)''')
    conn.commit()
    return conn

db_conn = init_db()

def get_ledger_data(today_str):
    c = db_conn.cursor()
    c.execute("SELECT intent, nasigoreng_orders, github_pushes, notes FROM ledger WHERE date = ?", (today_str,))
    row = c.fetchone()
    if row:
        return {"intent": row[0], "nasigoreng_orders": row[1], "github_pushes": row[2], "notes": row[3]}
    else:
        return {"intent": "Khalifah - Sovereign Execution", "nasigoreng_orders": 0, "github_pushes": 0, "notes": ""}

def save_ledger_data(today_str, intent, orders, pushes, notes):
    c = db_conn.cursor()
    c.execute('''INSERT OR REPLACE INTO ledger (date, intent, nasigoreng_orders, github_pushes, notes) 
                 VALUES (?, ?, ?, ?, ?)''', (today_str, intent, orders, pushes, notes))
    db_conn.commit()

def get_tasks(today_str, project_name):
    c = db_conn.cursor()
    c.execute("SELECT id, task_name, completed FROM tasks WHERE date = ? AND project = ?", (today_str, project_name))
    return c.fetchall()

def init_default_tasks(today_str):
    c = db_conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks WHERE date = ?", (today_str,))
    if c.fetchone()[0] == 0:
        default_tasks = [
            ("Tidore Project", "Finalize Ministry of Culture proposal draft"),
            ("Tidore Project", "Review Dapur Inspirasi maritime logistics"),
            ("Nasi Goreng Garasi", "Verify pre-order batch ingredients & packaging"),
            ("Nasi Goreng Garasi", "Coordinate frozen delivery schedule"),
            ("GOD•MauL / TCG", "Test Commander deck (Living Death / Hearthul)"),
            ("GOD•MauL / TCG", "Manage Guild matchmaking & Star Chip standings"),
            ("Inverted-Pyramid", "Commit Python automation script updates to GitHub"),
            ("Inverted-Pyramid", "Run Al-Haqq digital watermark verification")
        ]
        for proj, tname in default_tasks:
            c.execute("INSERT INTO tasks (date, project, task_name, completed) VALUES (?, ?, ?, 0)", (today_str, proj, tname))
        db_conn.commit()

today_str = datetime.date.today().strftime("%Y-%m-%d")
init_default_tasks(today_str)

# Custom CSS Injection for Dark-Mode & Mobile Polish
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        letter-spacing: -0.02em;
    }
    .metric-card {
        background-color: #1a1f2c;
        border: 1px solid #2d3748;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff9f0a;
        color: #000000;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #ffb340;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "somatic_reset" not in st.session_state:
    st.session_state.somatic_reset = {"clothes": False, "hydration": False, "movement": False}

db_data = get_ledger_data(today_str)
if "daily_ledger" not in st.session_state:
    st.session_state.daily_ledger = db_data

if "watermark_input" not in st.session_state:
    st.session_state.watermark_input = ""

# Header & Real-time Progress Bar
st.markdown("### ⚡ RYL: Ran Your Life — Command Center", unsafe_allow_html=True)
st.markdown("**Sovereignty, Movement, and Grounded Community**")

somatic_score = sum(1 for v in st.session_state.somatic_reset.values() if v) / len(st.session_state.somatic_reset)
st.progress(somatic_score, text=f"Daily Somatic Baseline: {int(somatic_score * 100)}% Synchronized")

st.markdown("---")

# Navigation Tabs
tab_dash, tab_todos, tab_somatic, tab_ledger, tab_watermark, tab_export = st.tabs([
    "Dashboard", "Project To-Do", "Somatic Reset", "Daily Ledger", "Watermark", "Export & Sync"
])

with tab_dash:
    st.markdown("### Multi-Front Operational Dashboard")
    st.write("Real-time telemetry across sovereign initiatives:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <b>🔥 Nasi Goreng Garasi</b><br>
            Pre-Orders: <b>{st.session_state.daily_ledger['nasigoreng_orders']}</b><br>
            Status: Active Production
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <b>⚓ Tidore Expedition</b><br>
            Progress: <b>92%</b><br>
            Status: Proposal Active
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <b>💻 Inverted-Pyramid</b><br>
            GitHub Pushes: <b>{st.session_state.daily_ledger['github_pushes']}</b><br>
            Status: Protocol Synchronized
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <b>⚔️ GOD•MauL Guild</b><br>
            Status: <b>Tactical Command</b><br>
            Readiness: Optimal
        </div>
        """, unsafe_allow_html=True)

with tab_todos:
    st.markdown("### Sovereign Project Trackers & To-Do Lists")
    st.write("Interactive operational task lists saved locally:")

    projects = ["Tidore Project", "Nasi Goreng Garasi", "GOD•MauL / TCG", "Inverted-Pyramid"]
    
    for proj in projects:
        st.markdown(f"**📌 {proj}**")
        tasks = get_tasks(today_str, proj)
        for task_id, task_name, completed in tasks:
            is_checked = st.checkbox(task_name, value=bool(completed), key=f"task_{task_id}")
            if is_checked != bool(completed):
                c = db_conn.cursor()
                c.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if is_checked else 0, task_id))
                db_conn.commit()
        st.markdown("")

with tab_somatic:
    st.markdown("### Physical-Somatic Reset")
    st.write("Execute and verify foundational anchors:")
    
    st.session_state.somatic_reset["clothes"] = st.checkbox("Changed clothes & stepped outside", value=st.session_state.somatic_reset["clothes"])
    st.session_state.somatic_reset["hydration"] = st.checkbox("Hydration & joint mobility completed", value=st.session_state.somatic_reset["hydration"])
    st.session_state.somatic_reset["movement"] = st.checkbox("Engaged in shared movement session", value=st.session_state.somatic_reset["movement"])
    
    if all(st.session_state.somatic_reset.values()):
        st.success("Somatic baseline secured. Sovereign clarity locked in.")

with tab_ledger:
    st.markdown("### Operational Daily Ledger (SQLite Persistence)")
    intent_val = st.text_input("Core Driving Intent", value=st.session_state.daily_ledger.get("intent", ""))
    nasigoreng_val = st.number_input("Nasi Goreng Garasi Pre-Orders", min_value=0, value=int(st.session_state.daily_ledger.get("nasigoreng_orders", 0)), step=1)
    github_val = st.number_input("Inverted-Pyramid / GitHub Pushes", min_value=0, value=int(st.session_state.daily_ledger.get("github_pushes", 0)), step=1)
    notes_val = st.text_area("Operational Notes & Directives", value=st.session_state.daily_ledger.get("notes", ""))
    
    if st.button("Commit & Save to Database"):
        st.session_state.daily_ledger["intent"] = intent_val
        st.session_state.daily_ledger["nasigoreng_orders"] = nasigoreng_val
        st.session_state.daily_ledger["github_pushes"] = github_val
        st.session_state.daily_ledger["notes"] = notes_val
        
        save_ledger_data(today_str, intent_val, nasigoreng_val, github_val, notes_val)
        st.success("Ledger entry permanently committed to local database.")

with tab_watermark:
    st.markdown("### Al-Haqq Digital Watermark Generator")
    st.write("Embed the authentic collaborative digital watermark into your writings.")
    
    raw_text = st.text_area("Input Text / Draft Article", placeholder="Paste your draft writing or notes here...", height=150)
    
    if st.button("Generate Watermarked Content"):
        if raw_text.strip():
            st.session_state.watermark_input = f"{raw_text.strip()}\n\n---\n*Cap Digital Kolaborasi Pemikiran & Penyempurnaan Bersama ICAM/Syams Maulana — Al-Haqq Protocol & Inverted-Pyramid Framework.*"
            st.success("Digital watermark successfully embedded.")
        else:
            st.warning("Please insert text to watermark.")
            
    if st.session_state.watermark_input:
        st.text_area("Watermarked Output (Ready to Copy)", value=st.session_state.watermark_input, height=180)

with tab_export:
    st.markdown("### Operational Summary & Export")
    st.write("Generate a clean markdown report of your daily metrics.")
    
    export_text = f"""### RYL Daily Report — {today_str}
- **Intent:** {st.session_state.daily_ledger.get('intent')}
- **Somatic Baseline:** {int(somatic_score * 100)}% Complete
- **Nasi Goreng Garasi Orders:** {st.session_state.daily_ledger.get('nasigoreng_orders')}
- **GitHub Pushes:** {st.session_state.daily_ledger.get('github_pushes')}
- **Notes:** {st.session_state.daily_ledger.get('notes')}
---
*Cap Digital Kolaborasi Pemikiran & Penyempurnaan Bersama ICAM/Syams Maulana — Al-Haqq Protocol & Inverted-Pyramid Framework.*"""

    st.text_area("Copy Report Markdown", value=export_text, height=200)

st.markdown("---")
st.caption("Cap Digital Kolaborasi Pemikiran & Penyempurnaan Bersama ICAM/Syams Maulana — Al-Haqq Protocol & Inverted-Pyramid Framework.")
