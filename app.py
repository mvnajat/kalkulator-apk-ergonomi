import streamlit as st
import pandas as pd
import math
import io
import altair as alt

# =====================================================================
# KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="IE//TOOLKIT — Waktu Kerja & Ergonomi",
    page_icon="◢",
    layout="wide",
)

# =====================================================================
# DESIGN SYSTEM (CSS)
# =====================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root{
  --bg:#070b11; --panel:#0d141d; --panel2:#111b27; --line:#1c2a3a;
  --cyan:#22d3ee; --lime:#a3e635; --amber:#fbbf24; --red:#f87171; --blue:#60a5fa;
  --text:#d5e1ee; --muted:#6c8097;
  --mono:'JetBrains Mono',ui-monospace,monospace; --sans:'Space Grotesk',system-ui,sans-serif;
}

html, body, [class*="css"], .stApp { font-family: var(--sans); color: var(--text); }
.stApp{
  background-color: var(--bg);
  background-image:
    linear-gradient(rgba(34,211,238,.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34,211,238,.045) 1px, transparent 1px);
  background-size: 36px 36px;
}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{ display:none !important; }
header[data-testid="stHeader"]{ background: transparent; }
.block-container{ padding-top: 1.6rem; max-width: 1500px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{ background: #090e15; border-right: 1px solid var(--line); }
section[data-testid="stSidebar"] .block-container{ padding-top: 1.2rem; }
.sb-brand{ display:flex; align-items:center; gap:12px; margin-bottom:6px; }
.sb-brand .t1{ font-family:var(--mono); font-weight:700; font-size:15px; letter-spacing:.08em; color:#fff; }
.sb-brand .t2{ font-family:var(--mono); font-size:10px; color:var(--muted); letter-spacing:.14em; text-transform:uppercase; }
.sb-box{ border:1px solid var(--line); background:var(--panel); padding:12px 14px; border-radius:6px; margin:10px 0; }
.sb-box .row{ display:flex; justify-content:space-between; font-family:var(--mono); font-size:11.5px; padding:3px 0; }
.sb-box .row span:first-child{ color:var(--muted); }
.sb-box .row span:last-child{ color:var(--text); text-align:right; }
.sb-h{ font-family:var(--mono); font-size:10.5px; letter-spacing:.18em; color:var(--cyan); text-transform:uppercase; margin:18px 0 8px; }
.sb-step{ display:flex; gap:10px; margin:9px 0; font-size:12.5px; line-height:1.45; color:#a9bacc; }
.sb-step b{ font-family:var(--mono); color:var(--cyan); font-weight:500; min-width:22px; }
.sb-foot{ font-family:var(--mono); font-size:10px; color:var(--muted); margin-top:22px; letter-spacing:.06em; }

/* ---------- Hero ---------- */
.hero{ border:1px solid var(--line); background:linear-gradient(135deg,#0d1621 0%,#0a1119 60%,#0b1a1f 100%);
  border-radius:8px; padding:22px 26px; margin-bottom:18px; position:relative; overflow:hidden; }
.hero:before{ content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(var(--cyan),var(--lime)); }
.hero .status{ font-family:var(--mono); font-size:11px; letter-spacing:.16em; color:var(--lime); text-transform:uppercase; }
.hero .dot{ display:inline-block; width:7px; height:7px; background:var(--lime); border-radius:50%; margin-right:8px;
  box-shadow:0 0 0 0 rgba(163,230,53,.7); animation:pulse 2s infinite; }
@keyframes pulse{ 70%{ box-shadow:0 0 0 8px rgba(163,230,53,0);} 100%{ box-shadow:0 0 0 0 rgba(163,230,53,0);} }
.hero h1{ font-family:var(--sans); font-weight:700; font-size:30px; letter-spacing:-.01em; margin:8px 0 4px; color:#fff; padding:0; }
.hero h1 em{ font-style:normal; color:var(--cyan); }
.hero p{ color:var(--muted); font-size:13.5px; margin:0 0 12px; }
.chips{ display:flex; gap:8px; flex-wrap:wrap; }
.chip{ font-family:var(--mono); font-size:10.5px; letter-spacing:.08em; padding:3px 9px; border:1px solid var(--line);
  color:#9db2c7; border-radius:3px; background:rgba(255,255,255,.02); }

/* ---------- Tabs ---------- */
div[data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--line); }
button[data-baseweb="tab"]{ font-family:var(--mono) !important; font-size:12px !important; letter-spacing:.06em;
  text-transform:uppercase; color:var(--muted) !important; padding:10px 18px !important; background:transparent !important; }
button[data-baseweb="tab"][aria-selected="true"]{ color:var(--cyan) !important; }
div[data-baseweb="tab-highlight"]{ background-color:var(--cyan) !important; height:2px !important; }
div[data-baseweb="tab-border"]{ background:transparent !important; }

/* ---------- Section headers ---------- */
.sec{ display:flex; align-items:center; gap:10px; font-family:var(--mono); font-size:12px; letter-spacing:.14em;
  text-transform:uppercase; color:#fff; margin:20px 0 10px; padding-bottom:8px; border-bottom:1px dashed var(--line); }
.sec .idx{ color:var(--bg); background:var(--cyan); font-weight:700; padding:1px 7px; border-radius:2px; font-size:11px; }
.sec .sub{ margin-left:auto; color:var(--muted); font-size:10.5px; letter-spacing:.08em; }
.panel-title{ font-size:20px; font-weight:600; color:#fff; margin:6px 0 2px; }
.panel-cap{ font-family:var(--mono); font-size:11px; color:var(--muted); margin-bottom:10px; letter-spacing:.04em; }

/* ---------- KPI cards ---------- */
.kpi{ border:1px solid var(--line); background:var(--panel); border-radius:6px; padding:12px 14px; position:relative; height:100%; }
.kpi:before{ content:""; position:absolute; top:0; left:0; width:100%; height:2px; background:var(--accent,var(--cyan)); opacity:.9; }
.kpi .k-l{ font-family:var(--mono); font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
.kpi .k-v{ font-family:var(--mono); font-size:25px; font-weight:700; color:#fff; margin-top:6px; line-height:1.1; }
.kpi .k-u{ font-size:11px; font-weight:400; color:var(--muted); margin-left:5px; }
.kpi .k-s{ font-family:var(--mono); font-size:10.5px; color:var(--accent,var(--cyan)); margin-top:6px; }
.kpi.cyan{ --accent:var(--cyan);} .kpi.lime{ --accent:var(--lime);} .kpi.amber{ --accent:var(--amber);}
.kpi.red{ --accent:var(--red);} .kpi.blue{ --accent:var(--blue);}

/* ---------- Callouts ---------- */
.callout{ border:1px solid var(--line); border-left:3px solid var(--accent); background:var(--panel); border-radius:4px;
  padding:11px 14px; height:100%; }
.callout .c-tag{ font-family:var(--mono); font-size:10px; letter-spacing:.16em; color:var(--accent); text-transform:uppercase; }
.callout .c-title{ font-weight:600; color:#fff; margin:3px 0 4px; font-size:14.5px; }
.callout .c-body{ font-size:12.5px; color:#9fb2c6; line-height:1.5; }
.callout.ok{ --accent:var(--lime);} .callout.warn{ --accent:var(--amber);}
.callout.err{ --accent:var(--red);} .callout.info{ --accent:var(--cyan);}
.callout.rev{ --accent:var(--blue); margin-bottom:10px; }

/* ---------- Score bar ---------- */
.sbar{ display:flex; gap:3px; margin:10px 0 2px; }
.sbar i{ flex:1; height:9px; background:#16212e; border-radius:1px; }
.sbar-l{ display:flex; justify-content:space-between; font-family:var(--mono); font-size:10px; color:var(--muted); margin-bottom:12px; }

/* ---------- Widgets ---------- */
label, .stMarkdown p{ color:var(--text); }
div[data-testid="stWidgetLabel"] p{ font-size:12.5px; color:#a9bacc; }
.stTextArea textarea, .stNumberInput input, .stTextInput input{
  background:var(--panel2) !important; color:var(--text) !important; border:1px solid var(--line) !important;
  font-family:var(--mono) !important; font-size:12.5px !important; border-radius:4px !important; }
.stTextArea textarea:focus, .stNumberInput input:focus{ border-color:var(--cyan) !important; box-shadow:0 0 0 1px var(--cyan) !important; }
div[data-baseweb="select"] > div{ background:var(--panel2) !important; border:1px solid var(--line) !important; border-radius:4px !important; font-size:12.5px; }
div[data-baseweb="popover"] ul{ background:var(--panel2) !important; }
.stCheckbox label span{ font-size:12.5px; }
div[data-testid="stSlider"] [role="slider"]{ background:var(--cyan) !important; }
div[data-testid="stExpander"]{ border:1px solid var(--line) !important; background:var(--panel); border-radius:6px; }
div[data-testid="stExpander"] summary{ font-family:var(--mono); font-size:12px; letter-spacing:.05em; }

.stDownloadButton button{ width:100%; background:transparent !important; color:var(--cyan) !important;
  border:1px solid var(--cyan) !important; border-radius:4px !important; font-family:var(--mono) !important;
  font-size:12px !important; letter-spacing:.08em; text-transform:uppercase; padding:.6rem 1rem; transition:all .15s; }
.stDownloadButton button:hover{ background:var(--cyan) !important; color:var(--bg) !important; box-shadow:0 0 18px rgba(34,211,238,.35); }

div[data-testid="stDataFrame"]{ border:1px solid var(--line); border-radius:6px; }
hr{ border-color:var(--line) !important; }
::-webkit-scrollbar{ width:8px; height:8px;} ::-webkit-scrollbar-thumb{ background:#1f3042; border-radius:4px;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =====================================================================
# HELPER KOMPONEN UI
# =====================================================================
def sec(idx, text, sub=""):
    st.markdown(
        f'<div class="sec"><span class="idx">{idx}</span>{text}<span class="sub">{sub}</span></div>',
        unsafe_allow_html=True,
    )


def kpi(label, value, unit="", sub="", tone="cyan"):
    return (
        f'<div class="kpi {tone}"><div class="k-l">{label}</div>'
        f'<div class="k-v">{value}<span class="k-u">{unit}</span></div>'
        f'<div class="k-s">{sub}</div></div>'
    )


def callout(tone, tag, title, body):
    st.markdown(
        f'<div class="callout {tone}"><div class="c-tag">{tag}</div>'
        f'<div class="c-title">{title}</div><div class="c-body">{body}</div></div>',
        unsafe_allow_html=True,
    )


def score_bar(value, max_value, color):
    segs = "".join(
        f'<i style="background:{color};box-shadow:0 0 8px {color}66"></i>' if k < min(value, max_value)
        else "<i></i>"
        for k in range(max_value)
    )
    st.markdown(
        f'<div class="sbar">{segs}</div><div class="sbar-l"><span>0</span><span>SKOR {value}</span><span>{max_value}</span></div>',
        unsafe_allow_html=True,
    )


# =====================================================================
# SIDEBAR
# =====================================================================
LOGO_SVG = """
<svg width="38" height="38" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="36" height="36" rx="6" fill="#0d141d" stroke="#22d3ee" stroke-width="1.4"/>
  <path d="M9 27 L19 9 L29 27 Z" fill="none" stroke="#22d3ee" stroke-width="1.8"/>
  <circle cx="19" cy="21" r="3" fill="#a3e635"/>
</svg>
"""

with st.sidebar:
    st.markdown(
        f'<div class="sb-brand">{LOGO_SVG}<div><div class="t1">IE//TOOLKIT</div>'
        f'<div class="t2">v1.0 · Work Design</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="sb-box">
        <div class="row"><span>PRODI</span><span>Teknik Industri</span></div>
        <div class="row"><span>KAMPUS</span><span>Univ. Pelita Bangsa</span></div>
        <div class="row"><span>KELAS</span><span>J253B</span></div>
        <div class="row"><span>AUTHOR</span><span>Munajat</span></div>
        <div class="row"><span>COLLAB</span><span>Web Prak. APK &amp; Ergonomi</span></div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sb-h">// Panduan Singkat</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sb-step"><b>01</b><span><u>Waktu Baku</u> — input data detik (pisah koma), atur Westinghouse, lihat grafik &amp; unduh Excel.</span></div>
        <div class="sb-step"><b>02</b><span><u>RULA</u> — pilih postur sesuai kondisi nyata untuk melihat <i>Action Level</i>.</span></div>
        <div class="sb-step"><b>03</b><span><u>REBA</u> — evaluasi seluruh tubuh secara komprehensif.</span></div>
        <div class="sb-foot">© 2026 · IE TOOLKIT PROJECT</div>
        """,
        unsafe_allow_html=True,
    )

# =====================================================================
# MATRIKS LOOKUP TABLE RESMI RULA & REBA
# =====================================================================

# --- 1. MATRIKS RULA (McAtamney & Corlett, 1993) ---
RULA_TABLE_A = [
    # Upper Arm = 1
    [[[1, 2], [2, 2], [2, 3], [3, 3]], [[2, 2], [2, 2], [3, 3], [3, 3]], [[2, 3], [3, 3], [3, 3], [4, 4]]],
    # Upper Arm = 2
    [[[2, 3], [3, 3], [3, 4], [4, 4]], [[3, 3], [3, 3], [3, 4], [4, 4]], [[3, 4], [4, 4], [4, 4], [5, 5]]],
    # Upper Arm = 3
    [[[3, 3], [4, 4], [4, 4], [5, 5]], [[3, 4], [4, 4], [4, 4], [5, 5]], [[4, 4], [4, 4], [4, 5], [5, 5]]],
    # Upper Arm = 4
    [[[4, 4], [4, 4], [4, 5], [5, 5]], [[4, 4], [4, 4], [4, 5], [5, 5]], [[4, 4], [4, 5], [5, 5], [6, 6]]],
    # Upper Arm = 5
    [[[5, 5], [5, 5], [5, 6], [6, 7]], [[5, 6], [6, 6], [6, 7], [7, 7]], [[6, 6], [6, 7], [7, 7], [7, 8]]],
    # Upper Arm = 6
    [[[7, 7], [7, 7], [7, 8], [8, 9]], [[8, 8], [8, 8], [8, 9], [9, 9]], [[9, 9], [9, 9], [9, 9], [9, 9]]]
]

RULA_TABLE_B = [
    [[1, 3], [2, 3], [3, 4], [5, 5], [6, 6], [7, 7]],  # Neck = 1
    [[2, 3], [2, 3], [4, 5], [5, 5], [6, 7], [7, 7]],  # Neck = 2
    [[3, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 7]],  # Neck = 3
    [[5, 5], [5, 6], [6, 7], [7, 7], [7, 7], [8, 8]],  # Neck = 4
    [[7, 7], [7, 7], [7, 8], [8, 8], [8, 8], [8, 8]],  # Neck = 5
    [[8, 8], [8, 8], [8, 8], [8, 9], [9, 9], [9, 9]]   # Neck = 6
]

RULA_TABLE_C = [
    [1, 2, 3, 3, 4, 5, 5],  # Score C = 1
    [2, 2, 3, 4, 4, 5, 5],  # Score C = 2
    [3, 3, 3, 4, 4, 5, 6],  # Score C = 3
    [3, 3, 3, 4, 5, 6, 6],  # Score C = 4
    [4, 4, 4, 5, 6, 7, 7],  # Score C = 5
    [4, 4, 5, 6, 6, 7, 7],  # Score C = 6
    [5, 5, 6, 6, 7, 7, 7],  # Score C = 7
    [5, 5, 6, 7, 7, 7, 7]   # Score C >= 8
]

# --- 2. MATRIKS REBA (Hignett & McAtamney, 2000) ---
REBA_TABLE_A = [
    [[1, 2, 3, 4], [1, 2, 3, 4], [3, 3, 5, 6]],  # Trunk = 1
    [[2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]],  # Trunk = 2
    [[2, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8]],  # Trunk = 3
    [[3, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9]],  # Trunk = 4
    [[4, 6, 7, 8], [6, 7, 8, 9], [7, 8, 9, 9]]   # Trunk = 5
]

REBA_TABLE_B = [
    [[1, 2, 2], [1, 2, 3]],  # Upper Arm = 1
    [[1, 2, 3], [2, 3, 4]],  # Upper Arm = 2
    [[3, 4, 5], [4, 5, 5]],  # Upper Arm = 3
    [[4, 5, 5], [5, 6, 7]],  # Upper Arm = 4
    [[6, 7, 8], [7, 8, 8]],  # Upper Arm = 5
    [[7, 8, 8], [8, 9, 9]]   # Upper Arm = 6
]

REBA_TABLE_C = [
    [1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7],
    [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8],
    [2, 3, 3, 3, 4, 5, 6, 7, 7, 8, 8, 8],
    [3, 4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9],
    [4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9, 9],
    [6, 6, 6, 7, 8, 8, 9, 9, 10, 10, 10, 10],
    [7, 7, 7, 8, 9, 9, 9, 10, 10, 11, 11, 11],
    [8, 8, 8, 9, 10, 10, 10, 10, 10, 11, 11, 11],
    [9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12],
    [10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 12],
    [11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12],
    [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
]


# =====================================================================
# HERO HEADER & NAVIGASI TAB
# =====================================================================
st.markdown(
    """
    <div class="hero">
      <div class="status"><span class="dot"></span>System online · Analysis engine ready</div>
      <h1>Pengukuran Waktu Kerja <em>&amp;</em> Ergonomi</h1>
      <p>Aplikasi web Teknik Industri — Analisis Perancangan Kerja (APK) &amp; Ergonomi</p>
      <div class="chips">
        <span class="chip">TIME STUDY</span><span class="chip">WESTINGHOUSE</span>
        <span class="chip">CONTROL CHART</span><span class="chip">RULA</span><span class="chip">REBA</span>
        <span class="chip">EXPORT .XLSX</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "01 · Waktu Baku & Uji Data",
    "02 · RULA",
    "03 · REBA",
])


# =====================================================================
# TAB 1: KALKULATOR WAKTU KERJA & UJI DATA
# =====================================================================
with tab1:
    st.markdown('<div class="panel-title">Waktu Baku, Uji Keseragaman & Kecukupan Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-cap">MODULE: TIME_STUDY · INPUT → PROCESS → OUTPUT</div>', unsafe_allow_html=True)

    col_input, col_hasil = st.columns([1.1, 1.3], gap="large")

    with col_input:
        sec("A", "Data Waktu Pengamatan", "INPUT")
        data_raw = st.text_area(
            "Masukkan data waktu pengamatan (detik), pisahkan dengan koma:",
            value="12.5, 13.0, 12.8, 12.4, 15.8, 12.7, 12.9, 12.5, 12.6, 13.0, 12.7, 12.8",
            help="Contoh di atas memiliki 1 data ekstrem (15.8) untuk menguji fitur outlier.",
            height=110,
        )

        sec("B", "Parameter Uji Statistik", "CONFIG")
        u1, u2 = st.columns(2)
        with u1:
            konf_dict = {"99% (k = 3)": 3.0, "95% (k = 2)": 2.0, "68% (k = 1)": 1.0}
            k_label = st.selectbox("Tingkat Kepercayaan", list(konf_dict.keys()), index=1)
            k_val = konf_dict[k_label]

            pembagi_std = st.radio(
                "Rumus Standar Deviasi",
                ["Sampel (N - 1)", "Populasi (N)"],
                horizontal=True,
            )
        with u2:
            s_pct = st.number_input("Derajat Ketelitian / s (%)", min_value=1.0, max_value=25.0, value=5.0, step=0.5)
            s_val = s_pct / 100.0
            auto_revisi = st.checkbox("Otomatis buang data di luar BKA/BKB (Revisi Data)")

        sec("C", "Faktor Penyesuaian · Westinghouse", "RATING")
        skill_dict = {
            "Superskill (A1) [+0.15]": 0.15, "Superskill (A2) [+0.13]": 0.13,
            "Excellent (B1) [+0.11]": 0.11, "Excellent (B2) [+0.08]": 0.08,
            "Good (C1) [+0.06]": 0.06, "Good (C2) [+0.03]": 0.03,
            "Average (D) [0.00]": 0.00,
            "Fair (E1) [-0.05]": -0.05, "Fair (E2) [-0.10]": -0.10,
            "Poor (F1) [-0.16]": -0.16, "Poor (F2) [-0.22]": -0.22
        }
        effort_dict = {
            "Excessive (A1) [+0.13]": 0.13, "Excessive (A2) [+0.12]": 0.12,
            "Excellent (B1) [+0.10]": 0.10, "Excellent (B2) [+0.08]": 0.08,
            "Good (C1) [+0.05]": 0.05, "Good (C2) [+0.02]": 0.02,
            "Average (D) [0.00]": 0.00,
            "Fair (E1) [-0.04]": -0.04, "Fair (E2) [-0.08]": -0.08,
            "Poor (F1) [-0.12]": -0.12, "Poor (F2) [-0.17]": -0.17
        }
        cond_dict = {
            "Ideal (A) [+0.06]": 0.06, "Excellent (B) [+0.04]": 0.04,
            "Good (C) [+0.02]": 0.02, "Average (D) [0.00]": 0.00,
            "Fair (E) [-0.03]": -0.03, "Poor (F) [-0.07]": -0.07
        }
        cons_dict = {
            "Perfect (A) [+0.04]": 0.04, "Excellent (B) [+0.03]": 0.03,
            "Good (C) [+0.01]": 0.01, "Average (D) [0.00]": 0.00,
            "Fair (E) [-0.02]": -0.02, "Poor (F) [-0.04]": -0.04
        }

        c1, c2 = st.columns(2)
        with c1:
            s_w = skill_dict[st.selectbox("Keterampilan (Skill)", list(skill_dict.keys()), index=6)]
            e_w = effort_dict[st.selectbox("Usaha (Effort)", list(effort_dict.keys()), index=6)]
        with c2:
            cd_w = cond_dict[st.selectbox("Kondisi Kerja (Condition)", list(cond_dict.keys()), index=3)]
            cs_w = cons_dict[st.selectbox("Konsistensi (Consistency)", list(cons_dict.keys()), index=3)]

        sec("D", "Kelonggaran · Allowance", "ALLOW")
        allowance_pct = st.slider("Total Persentase Allowance (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.5)

    with col_hasil:
        try:
            data_awal = [float(x.strip()) for x in data_raw.split(",") if x.strip() != ""]

            if len(data_awal) < 2:
                callout("warn", "WARNING", "Data tidak cukup", "Masukkan minimal 2 data pengamatan untuk menghitung standar deviasi.")
            else:
                def hitung_statistik(data_arr):
                    n = len(data_arr)
                    rata2 = sum(data_arr) / n
                    pembagi = (n - 1) if pembagi_std == "Sampel (N - 1)" else n
                    variansi = sum((x - rata2) ** 2 for x in data_arr) / pembagi
                    std_dev = math.sqrt(variansi)
                    bka_val = rata2 + (k_val * std_dev)
                    bkb_val = rata2 - (k_val * std_dev)

                    sum_x = sum(data_arr)
                    sum_x2 = sum(x ** 2 for x in data_arr)
                    pembilang_n = (k_val / s_val) * math.sqrt(max((n * sum_x2) - (sum_x ** 2), 0))
                    n_aksen = (pembilang_n / sum_x) ** 2 if sum_x > 0 else 0
                    return n, rata2, std_dev, bka_val, bkb_val, n_aksen

                n_data, ws, std_dev, bka, bkb, n_aksen = hitung_statistik(data_awal)
                outliers = [x for x in data_awal if x > bka or x < bkb]
                data_aktif = data_awal

                if auto_revisi and len(outliers) > 0:
                    data_aktif = [x for x in data_awal if bkb <= x <= bka]
                    if len(data_aktif) >= 2:
                        callout(
                            "rev", "REVISI DATA AKTIF", f"{len(outliers)} data ekstrem dihapus",
                            f"Data dibuang: {outliers}. Batas kontrol dihitung ulang.",
                        )
                        n_data, ws, std_dev, bka, bkb, n_aksen = hitung_statistik(data_aktif)
                        outliers = [x for x in data_aktif if x > bka or x < bkb]

                p = 1.0 + (s_w + e_w + cd_w + cs_w)
                wn = ws * p
                wb = wn * (1 + (allowance_pct / 100))
                output_std = 3600 / wb if wb > 0 else 0

                sec("01", "Waktu Kerja & Output Standar", "RESULT")
                m1, m2, m3, m4 = st.columns(4)
                m1.markdown(kpi("Waktu Siklus · Ws", f"{ws:.2f}", "dtk", f"N = {n_data}", "blue"), unsafe_allow_html=True)
                m2.markdown(kpi("Waktu Normal · Wn", f"{wn:.2f}", "dtk", f"p = {p:.2f}", "cyan"), unsafe_allow_html=True)
                m3.markdown(kpi("Waktu Baku · Wb", f"{wb:.2f}", "dtk", f"allow. {allowance_pct}%", "lime"), unsafe_allow_html=True)
                m4.markdown(kpi("Output Standar", f"{output_std:.1f}", "unit/jam", "3600 / Wb", "amber"), unsafe_allow_html=True)

                sec("02", "Uji Keseragaman & Kecukupan Data", "VALIDATION")
                status_seragam = "SERAGAM" if len(outliers) == 0 else "TIDAK SERAGAM"
                status_cukup = "CUKUP (N' <= N)" if n_aksen <= n_data else "BELUM CUKUP (N' > N)"

                u_col1, u_col2 = st.columns(2)
                with u_col1:
                    if len(outliers) == 0:
                        callout("ok", "PASS · KESERAGAMAN", "Data SERAGAM",
                                f"Seluruh {n_data} data berada di rentang BKB ({bkb:.2f}) s/d BKA ({bka:.2f}).")
                    else:
                        callout("err", "FAIL · KESERAGAMAN", "Data TIDAK SERAGAM",
                                f"{len(outliers)} data di luar batas kontrol: <b>{outliers}</b>")
                with u_col2:
                    if n_aksen <= n_data:
                        callout("ok", "PASS · KECUKUPAN", "Data CUKUP (N' ≤ N)",
                                f"N' = <b>{n_aksen:.2f}</b> (dibulatkan {math.ceil(n_aksen)}), sedangkan N = {n_data}.")
                    else:
                        kurang = math.ceil(n_aksen) - n_data
                        callout("warn", "FAIL · KECUKUPAN", "Data BELUM CUKUP (N' > N)",
                                f"N' = <b>{n_aksen:.2f}</b> (N = {n_data}). Kurang minimal <b>{kurang}</b> data lagi.")

                # --- GRAFIK PETA KONTROL ---
                sec("03", "Peta Kontrol Keseragaman Data", "CONTROL CHART")
                df_chart = pd.DataFrame({
                    "Pengamatan Ke": list(range(1, n_data + 1)),
                    "Waktu (detik)": data_aktif,
                    "Kuadrat Waktu (x²)": [round(x ** 2, 4) for x in data_aktif],
                    "BKA": [round(bka, 3)] * n_data,
                    "Rata-rata (Ws)": [round(ws, 3)] * n_data,
                    "BKB": [round(bkb, 3)] * n_data,
                    "Status": ["Normal" if bkb <= x <= bka else "Outlier (Di Luar Batas)" for x in data_aktif]
                })

                base = alt.Chart(df_chart).encode(x=alt.X("Pengamatan Ke:O", title="Pengamatan ke-"))
                area = base.mark_area(color="#22d3ee", opacity=0.07).encode(
                    y=alt.Y("Waktu (detik):Q", scale=alt.Scale(zero=False), title="Waktu (detik)")
                )
                line_data = base.mark_line(color="#22d3ee", strokeWidth=1.8).encode(
                    y=alt.Y("Waktu (detik):Q", scale=alt.Scale(zero=False))
                )
                points_data = base.mark_point(size=90, filled=True, opacity=1).encode(
                    y="Waktu (detik):Q",
                    color=alt.Color(
                        "Status:N",
                        scale=alt.Scale(domain=["Normal", "Outlier (Di Luar Batas)"], range=["#22d3ee", "#f87171"]),
                        legend=alt.Legend(orient="top", title=None),
                    ),
                    tooltip=["Pengamatan Ke", "Waktu (detik)", "Status", "BKA", "Rata-rata (Ws)", "BKB"]
                )
                rule_bka = alt.Chart(df_chart).mark_rule(color="#f87171", strokeDash=[6, 4], size=1.5).encode(y="mean(BKA):Q")
                rule_ws = alt.Chart(df_chart).mark_rule(color="#a3e635", strokeDash=[3, 3], size=1.5).encode(y="mean(Rata-rata (Ws)):Q")
                rule_bkb = alt.Chart(df_chart).mark_rule(color="#f87171", strokeDash=[6, 4], size=1.5).encode(y="mean(BKB):Q")

                chart_final = (
                    (area + line_data + points_data + rule_bka + rule_ws + rule_bkb)
                    .properties(height=290)
                    .configure(background="transparent")
                    .configure_view(strokeOpacity=0)
                    .configure_axis(
                        labelColor="#6c8097", titleColor="#6c8097", gridColor="#162231",
                        domainColor="#1c2a3a", tickColor="#1c2a3a",
                        labelFont="JetBrains Mono", titleFont="JetBrains Mono", labelFontSize=10, titleFontSize=10,
                    )
                    .configure_legend(labelColor="#9db2c7", labelFont="JetBrains Mono", labelFontSize=10)
                )
                st.altair_chart(chart_final, use_container_width=True)
                st.markdown(
                    '<div class="panel-cap">— BKA / BKB (merah putus-putus) · Ws (hijau titik) · outlier ditandai merah</div>',
                    unsafe_allow_html=True,
                )

                # --- TABEL RINGKASAN & UNDUH EXCEL ---
                df_summary = pd.DataFrame({
                    "Parameter": [
                        "Jumlah Pengamatan Aktif (N)",
                        "Total Waktu Pengamatan (Σx)",
                        "Total Kuadrat Waktu (Σx²)",
                        "Waktu Siklus Rata-rata (Ws)",
                        "Standar Deviasi (σ)",
                        "Batas Kontrol Atas (BKA)",
                        "Batas Kontrol Bawah (BKB)",
                        "Status Uji Keseragaman",
                        "Jumlah Pengamatan Minimum (N')",
                        "Status Uji Kecukupan",
                        "Faktor Penyesuaian Westinghouse (p)",
                        "Waktu Normal (Wn)",
                        "Allowance (%)",
                        "Waktu Baku (Wb)",
                        "Kapasitas Output Standar (unit/jam)"
                    ],
                    "Nilai": [
                        n_data,
                        round(sum(data_aktif), 4),
                        round(sum(x ** 2 for x in data_aktif), 4),
                        round(ws, 4),
                        round(std_dev, 4),
                        round(bka, 4),
                        round(bkb, 4),
                        status_seragam,
                        round(n_aksen, 4),
                        status_cukup,
                        round(p, 2),
                        round(wn, 4),
                        allowance_pct,
                        round(wb, 4),
                        round(output_std, 2)
                    ]
                })

                excel_buffer_1 = io.BytesIO()
                with pd.ExcelWriter(excel_buffer_1, engine="openpyxl") as writer:
                    df_summary.to_excel(writer, sheet_name="Ringkasan_Perhitungan", index=False)
                    df_chart.to_excel(writer, sheet_name="Data_Pengamatan", index=False)

                st.download_button(
                    label="⤓ Unduh Laporan Waktu Baku & Uji Data (.xlsx)",
                    data=excel_buffer_1.getvalue(),
                    file_name="Laporan_Waktu_Baku_APK.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                with st.expander("Tabel Ringkasan Parameter Lengkap"):
                    st.dataframe(df_summary, use_container_width=True, hide_index=True)

        except ValueError:
            callout("err", "INPUT ERROR", "Format data tidak valid",
                    "Pastikan data pengamatan hanya berisi angka dan dipisahkan dengan tanda koma (,).")


# =====================================================================
# TAB 2: SKORING POSTUR KERJA RULA
# =====================================================================
with tab2:
    st.markdown('<div class="panel-title">RULA · Rapid Upper Limb Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-cap">LOOKUP: TABEL A · B · C — McAtamney &amp; Corlett (1993)</div>', unsafe_allow_html=True)

    col_ra, col_rb, col_rres = st.columns([1.1, 1.1, 1], gap="large")

    with col_ra:
        sec("A", "Grup A · Lengan & Pergelangan", "UPPER LIMB")
        ua_base = st.selectbox("1. Posisi Lengan Atas (Upper Arm)", [
            (1, "1 : Sudut -20° s/d 20° (Netral)"),
            (2, "2 : Ekstensi >20° atau Fleksi 20°-45°"),
            (3, "3 : Fleksi 45°-90°"),
            (4, "4 : Fleksi >90°")
        ], format_func=lambda x: x[1], key="rula_ua")[0]
        ua_sh = 1 if st.checkbox("Bahu terangkat (+1)", key="rula_ua_sh") else 0
        ua_ab = 1 if st.checkbox("Lengan atas abduksi / menjauhi tubuh (+1)", key="rula_ua_ab") else 0
        ua_sp = -1 if st.checkbox("Lengan ditopang / bersandar (-1)", key="rula_ua_sp") else 0
        rula_ua = max(1, min(ua_base + ua_sh + ua_ab + ua_sp, 6))

        la_base = st.selectbox("2. Posisi Lengan Bawah (Lower Arm)", [
            (1, "1 : Fleksi 60° - 100°"),
            (2, "2 : Fleksi <60° atau >100°")
        ], format_func=lambda x: x[1], key="rula_la")[0]
        la_mid = 1 if st.checkbox("Bekerja melewati garis tengah / keluar sisi tubuh (+1)", key="rula_la_mid") else 0
        rula_la = max(1, min(la_base + la_mid, 3))

        wr_base = st.selectbox("3. Posisi Pergelangan Tangan (Wrist)", [
            (1, "1 : Posisi Netral (0°)"),
            (2, "2 : Fleksi / Ekstensi 0° - 15°"),
            (3, "3 : Fleksi / Ekstensi > 15°")
        ], format_func=lambda x: x[1], key="rula_wr")[0]
        wr_dev = 1 if st.checkbox("Deviasi radial / ulnar (belok ke samping) (+1)", key="rula_wr_dev") else 0
        rula_wr = max(1, min(wr_base + wr_dev, 4))

        rula_wt = st.selectbox("4. Putaran Pergelangan (Wrist Twist)", [
            (1, "1 : Berputar di rentang tengah (Mid-range)"),
            (2, "2 : Berputar di dekat / batas akhir (End-range)")
        ], format_func=lambda x: x[1], key="rula_wt")[0]

        st.markdown('<div class="panel-cap" style="margin-top:12px">OTOT &amp; BEBAN · GRUP A</div>', unsafe_allow_html=True)
        rula_muscle_a = 1 if st.checkbox("Postur Grup A statis >1 menit atau repetitif >4x/menit (+1)", key="rula_ma") else 0
        rula_force_a = st.selectbox("Beban / Gaya Grup A (Force/Load)", [
            (0, "0 : Beban < 2 kg (intermiten)"),
            (1, "1 : Beban 2 - 10 kg (intermiten)"),
            (2, "2 : Beban 2 - 10 kg (statis / repetitif)"),
            (3, "3 : Beban > 10 kg atau beban kejut")
        ], format_func=lambda x: x[1], key="rula_fa")[0]

    with col_rb:
        sec("B", "Grup B · Leher, Punggung & Kaki", "TRUNK / LEGS")
        nk_base = st.selectbox("5. Posisi Leher (Neck)", [
            (1, "1 : Fleksi 0° - 10°"),
            (2, "2 : Fleksi 10° - 20°"),
            (3, "3 : Fleksi > 20°"),
            (4, "4 : Ekstensi (Mendongak)")
        ], format_func=lambda x: x[1], key="rula_nk")[0]
        nk_tw = 1 if st.checkbox("Leher terputar / menoleh (+1)", key="rula_nk_tw") else 0
        nk_sb = 1 if st.checkbox("Leher miring ke samping (+1)", key="rula_nk_sb") else 0
        rula_nk = max(1, min(nk_base + nk_tw + nk_sb, 6))

        tr_base = st.selectbox("6. Posisi Punggung (Trunk)", [
            (1, "1 : Duduk tegak & ditopang baik (0°)"),
            (2, "2 : Fleksi (Membungkuk) 0° - 20°"),
            (3, "3 : Fleksi 20° - 60°"),
            (4, "4 : Fleksi > 60°")
        ], format_func=lambda x: x[1], key="rula_tr")[0]
        tr_tw = 1 if st.checkbox("Punggung terputar (+1)", key="rula_tr_tw") else 0
        tr_sb = 1 if st.checkbox("Punggung miring ke samping (+1)", key="rula_tr_sb") else 0
        rula_tr = max(1, min(tr_base + tr_tw + tr_sb, 6))

        rula_legs = st.selectbox("7. Posisi Kaki (Legs)", [
            (1, "1 : Kaki tertopang seimbang / duduk"),
            (2, "2 : Kaki tidak tertopang / tumpuan 1 kaki")
        ], format_func=lambda x: x[1], key="rula_legs")[0]

        st.markdown('<div class="panel-cap" style="margin-top:12px">OTOT &amp; BEBAN · GRUP B</div>', unsafe_allow_html=True)
        rula_muscle_b = 1 if st.checkbox("Postur Grup B statis >1 menit atau repetitif >4x/menit (+1)", key="rula_mb") else 0
        rula_force_b = st.selectbox("Beban / Gaya Grup B (Force/Load)", [
            (0, "0 : Beban < 2 kg (intermiten)"),
            (1, "1 : Beban 2 - 10 kg (intermiten)"),
            (2, "2 : Beban 2 - 10 kg (statis / repetitif)"),
            (3, "3 : Beban > 10 kg atau beban kejut")
        ], format_func=lambda x: x[1], key="rula_fb")[0]

    with col_rres:
        sec("OUT", "Hasil Matriks RULA", "RESULT")
        score_table_a = RULA_TABLE_A[rula_ua - 1][rula_la - 1][rula_wr - 1][rula_wt - 1]
        score_c = score_table_a + rula_muscle_a + rula_force_a

        score_table_b = RULA_TABLE_B[rula_nk - 1][rula_tr - 1][rula_legs - 1]
        score_d = score_table_b + rula_muscle_b + rula_force_b

        idx_c = min(score_c, 8) - 1
        idx_d = min(score_d, 7) - 1
        rula_grand = RULA_TABLE_C[idx_c][idx_d]

        r1, r2 = st.columns(2)
        r1.markdown(kpi("Skor C · Grup A", score_c, "", f"Tabel A = {score_table_a}", "blue"), unsafe_allow_html=True)
        r2.markdown(kpi("Skor D · Grup B", score_d, "", f"Tabel B = {score_table_b}", "blue"), unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if rula_grand in [1, 2]:
            tone, color, tag = "ok", "#a3e635", "LEVEL 1 · RENDAH"
            rula_kat = "Action Level 1 (Risiko Rendah - Dapat Diterima)"
            body = "Postur kerja dapat diterima jika tidak dipertahankan dalam waktu lama."
        elif rula_grand in [3, 4]:
            tone, color, tag = "warn", "#fbbf24", "LEVEL 2 · SEDANG"
            rula_kat = "Action Level 2 (Risiko Sedang - Perlu Investigasi)"
            body = "Diperlukan investigasi lebih lanjut dan perubahan posisi kerja mungkin dibutuhkan."
        elif rula_grand in [5, 6]:
            tone, color, tag = "err", "#fb923c", "LEVEL 3 · TINGGI"
            rula_kat = "Action Level 3 (Risiko Tinggi - Segera Perbaiki)"
            body = "Investigasi dan perubahan desain stasiun kerja harus segera dilakukan dalam waktu dekat."
        else:
            tone, color, tag = "err", "#f87171", "LEVEL 4 · KRITIS"
            rula_kat = "Action Level 4 (Risiko Sangat Tinggi - Perbaiki Sekarang!)"
            body = "Kondisi kritis! Perbaikan postur dan stasiun kerja harus dilakukan SEKARANG JUGA."

        st.markdown(kpi("Skor Akhir RULA", rula_grand, "/ 7", "Tabel C", tone if tone != "err" else "red"),
                    unsafe_allow_html=True)
        score_bar(min(rula_grand, 7), 7, color)
        callout(tone, tag, rula_kat, body)

        df_rula = pd.DataFrame({
            "Komponen Evaluasi RULA": [
                "Skor Lengan Atas (Upper Arm)", "Skor Lengan Bawah (Lower Arm)",
                "Skor Pergelangan Tangan (Wrist)", "Skor Putaran Pergelangan (Wrist Twist)",
                "Skor Postur Tabel A", "Skor Otot & Beban Grup A", "Skor C (Total Grup A)",
                "Skor Leher (Neck)", "Skor Punggung (Trunk)", "Skor Kaki (Legs)",
                "Skor Postur Tabel B", "Skor Otot & Beban Grup B", "Skor D (Total Grup B)",
                "Skor Akhir RULA (Tabel C)", "Kategori Action Level"
            ],
            "Nilai / Skor": [
                rula_ua, rula_la, rula_wr, rula_wt,
                score_table_a, (rula_muscle_a + rula_force_a), score_c,
                rula_nk, rula_tr, rula_legs,
                score_table_b, (rula_muscle_b + rula_force_b), score_d,
                rula_grand, rula_kat
            ]
        })
        df_rula["Nilai / Skor"] = df_rula["Nilai / Skor"].astype(str)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.dataframe(df_rula, use_container_width=True, hide_index=True, height=280)

        excel_buffer_rula = io.BytesIO()
        with pd.ExcelWriter(excel_buffer_rula, engine="openpyxl") as writer:
            df_rula.to_excel(writer, sheet_name="Hasil_Skoring_RULA", index=False)

        st.download_button(
            label="⤓ Unduh Laporan RULA (.xlsx)",
            data=excel_buffer_rula.getvalue(),
            file_name="Laporan_Ergonomi_RULA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# =====================================================================
# TAB 3: SKORING POSTUR KERJA REBA
# =====================================================================
with tab3:
    st.markdown('<div class="panel-title">REBA · Rapid Entire Body Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-cap">LOOKUP: TABEL A · B · C — Hignett &amp; McAtamney (2000)</div>', unsafe_allow_html=True)

    col_eba, col_ebb, col_ebres = st.columns([1.1, 1.1, 1], gap="large")

    with col_eba:
        sec("A", "Grup A · Punggung, Leher & Kaki", "TRUNK / LEGS")
        eb_tr_base = st.selectbox("1. Posisi Punggung (Trunk)", [
            (1, "1 : Tegak / Netral (0°)"),
            (2, "2 : Fleksi / Ekstensi 0° - 20°"),
            (3, "3 : Fleksi 20° - 60° atau Ekstensi > 20°"),
            (4, "4 : Fleksi > 60°")
        ], format_func=lambda x: x[1], key="reba_tr")[0]
        eb_tr_mod = 1 if st.checkbox("Punggung terputar atau miring ke samping (+1)", key="reba_tr_mod") else 0
        reba_tr = max(1, min(eb_tr_base + eb_tr_mod, 5))

        eb_nk_base = st.selectbox("2. Posisi Leher (Neck)", [
            (1, "1 : Fleksi 0° - 20°"),
            (2, "2 : Fleksi > 20° atau Ekstensi (Mendongak)")
        ], format_func=lambda x: x[1], key="reba_nk")[0]
        eb_nk_mod = 1 if st.checkbox("Leher terputar atau miring ke samping (+1)", key="reba_nk_mod") else 0
        reba_nk = max(1, min(eb_nk_base + eb_nk_mod, 3))

        eb_leg_base = st.selectbox("3. Posisi Kaki (Legs)", [
            (1, "1 : Tumpuan 2 kaki seimbang / jalan / duduk"),
            (2, "2 : Tumpuan 1 kaki / postur tidak stabil")
        ], format_func=lambda x: x[1], key="reba_leg")[0]
        eb_leg_knee = st.selectbox("Tekukan Lutut (Knee Flexion)", [
            (0, "0 : Lutut lurus (< 30°)"),
            (1, "+1 : Lutut menekuk 30° - 60°"),
            (2, "+2 : Lutut menekuk > 60°")
        ], format_func=lambda x: x[1], key="reba_knee")[0]
        reba_legs = max(1, min(eb_leg_base + eb_leg_knee, 4))

        reba_load = st.selectbox("4. Beban / Gaya (Load / Force)", [
            (0, "0 : Beban < 5 kg"),
            (1, "1 : Beban 5 - 10 kg"),
            (2, "2 : Beban > 10 kg")
        ], format_func=lambda x: x[1], key="reba_load")[0]
        reba_shock = 1 if st.checkbox("Ada beban kejut / pengerahan gaya mendadak (+1)", key="reba_shock") else 0
        reba_total_load = reba_load + reba_shock

    with col_ebb:
        sec("B", "Grup B · Lengan & Pergelangan", "UPPER LIMB")
        eb_ua_base = st.selectbox("5. Posisi Lengan Atas (Upper Arm)", [
            (1, "1 : Fleksi / Ekstensi -20° s/d 20°"),
            (2, "2 : Ekstensi >20° atau Fleksi 20° - 45°"),
            (3, "3 : Fleksi 45° - 90°"),
            (4, "4 : Fleksi > 90°")
        ], format_func=lambda x: x[1], key="reba_ua")[0]
        eb_ua_sh = 1 if st.checkbox("Bahu terangkat (+1)", key="reba_ua_sh") else 0
        eb_ua_ab = 1 if st.checkbox("Lengan abduksi / diputar (+1)", key="reba_ua_ab") else 0
        eb_ua_sp = -1 if st.checkbox("Lengan ditopang / bersandar (-1)", key="reba_ua_sp") else 0
        reba_ua = max(1, min(eb_ua_base + eb_ua_sh + eb_ua_ab + eb_ua_sp, 6))

        reba_la = st.selectbox("6. Posisi Lengan Bawah (Lower Arm)", [
            (1, "1 : Fleksi 60° - 100°"),
            (2, "2 : Fleksi < 60° atau > 100°")
        ], format_func=lambda x: x[1], key="reba_la")[0]

        eb_wr_base = st.selectbox("7. Posisi Pergelangan Tangan (Wrist)", [
            (1, "1 : Fleksi / Ekstensi 0° - 15°"),
            (2, "2 : Fleksi / Ekstensi > 15°")
        ], format_func=lambda x: x[1], key="reba_wr")[0]
        eb_wr_mod = 1 if st.checkbox("Pergelangan tangan terputar / deviasi (+1)", key="reba_wr_mod") else 0
        reba_wr = max(1, min(eb_wr_base + eb_wr_mod, 3))

        reba_coupling = st.selectbox("8. Pegangan (Coupling Score)", [
            (0, "0 : Good (Pegangan pas dan kuat)"),
            (1, "1 : Fair (Pegangan masih bisa diterima)"),
            (2, "2 : Poor (Pegangan sulit / tidak nyaman)"),
            (3, "3 : Unacceptable (Tidak ada pegangan / tidak aman)")
        ], format_func=lambda x: x[1], key="reba_coup")[0]

        st.markdown('<div class="panel-cap" style="margin-top:12px">9 · SKOR AKTIVITAS (ACTIVITY SCORE)</div>', unsafe_allow_html=True)
        act1 = 1 if st.checkbox("1 atau lebih bagian tubuh statis > 1 menit (+1)", key="reba_act1") else 0
        act2 = 1 if st.checkbox("Gerakan berulang > 4x per menit (+1)", key="reba_act2") else 0
        act3 = 1 if st.checkbox("Perubahan postur besar secara cepat / tidak stabil (+1)", key="reba_act3") else 0
        reba_activity = act1 + act2 + act3

    with col_ebres:
        sec("OUT", "Hasil Matriks REBA", "RESULT")
        eb_table_a = REBA_TABLE_A[reba_tr - 1][reba_nk - 1][reba_legs - 1]
        reba_score_a = min(eb_table_a + reba_total_load, 12)

        eb_table_b = REBA_TABLE_B[reba_ua - 1][reba_la - 1][reba_wr - 1]
        reba_score_b = min(eb_table_b + reba_coupling, 12)

        reba_score_c = REBA_TABLE_C[reba_score_a - 1][reba_score_b - 1]
        reba_final = reba_score_c + reba_activity

        eb1, eb2 = st.columns(2)
        eb1.markdown(kpi("Skor A · Grup A", reba_score_a, "", f"Tabel A = {eb_table_a}", "blue"), unsafe_allow_html=True)
        eb2.markdown(kpi("Skor B · Grup B", reba_score_b, "", f"Tabel B = {eb_table_b}", "blue"), unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if reba_final == 1:
            tone, color, tag = "ok", "#a3e635", "LEVEL 0 · SANGAT RENDAH"
            reba_kat = "Action Level 0 (Risiko Sangat Rendah - Tidak Perlu Tindakan)"
            body = "Postur kerja aman dan tidak memerlukan tindakan perbaikan."
        elif reba_final in [2, 3]:
            tone, color, tag = "info", "#22d3ee", "LEVEL 1 · RENDAH"
            reba_kat = "Action Level 1 (Risiko Rendah - Mungkin Perlu Perbaikan)"
            body = "Risiko rendah, perubahan postur mungkin diperlukan ke depannya."
        elif reba_final in [4, 5, 6, 7]:
            tone, color, tag = "warn", "#fbbf24", "LEVEL 2 · SEDANG"
            reba_kat = "Action Level 2 (Risiko Sedang - Perlu Tindakan)"
            body = "Perlu investigasi lebih lanjut dan tindakan perbaikan postur kerja."
        elif reba_final in [8, 9, 10]:
            tone, color, tag = "err", "#fb923c", "LEVEL 3 · TINGGI"
            reba_kat = "Action Level 3 (Risiko Tinggi - Segera Perbaiki)"
            body = "Risiko cedera tinggi! Perlu tindakan perbaikan sesegera mungkin."
        else:
            tone, color, tag = "err", "#f87171", "LEVEL 4 · KRITIS"
            reba_kat = "Action Level 4 (Risiko Sangat Tinggi - Perbaiki Saat Ini Juga!)"
            body = "Kondisi berbahaya! Tindakan perbaikan mutlak dilakukan SAAT INI JUGA."

        kpi_tone = {"ok": "lime", "info": "cyan", "warn": "amber", "err": "red"}[tone]
        st.markdown(kpi("Skor Akhir REBA", reba_final, "/ 15", f"Tabel C = {reba_score_c} + aktivitas {reba_activity}", kpi_tone),
                    unsafe_allow_html=True)
        score_bar(min(reba_final, 15), 15, color)
        callout(tone, tag, reba_kat, body)

        df_reba = pd.DataFrame({
            "Komponen Evaluasi REBA": [
                "Skor Punggung (Trunk)", "Skor Leher (Neck)", "Skor Kaki (Legs)",
                "Skor Postur Tabel A", "Skor Beban / Force", "Skor A (Total Grup A)",
                "Skor Lengan Atas (Upper Arm)", "Skor Lengan Bawah (Lower Arm)", "Skor Pergelangan (Wrist)",
                "Skor Postur Tabel B", "Skor Pegangan (Coupling)", "Skor B (Total Grup B)",
                "Skor Tabel C", "Skor Aktivitas (Activity)", "Skor Akhir REBA", "Kategori Action Level"
            ],
            "Nilai / Skor": [
                reba_tr, reba_nk, reba_legs,
                eb_table_a, reba_total_load, reba_score_a,
                reba_ua, reba_la, reba_wr,
                eb_table_b, reba_coupling, reba_score_b,
                reba_score_c, reba_activity, reba_final, reba_kat
            ]
        })
        df_reba["Nilai / Skor"] = df_reba["Nilai / Skor"].astype(str)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.dataframe(df_reba, use_container_width=True, hide_index=True, height=280)

        excel_buffer_reba = io.BytesIO()
        with pd.ExcelWriter(excel_buffer_reba, engine="openpyxl") as writer:
            df_reba.to_excel(writer, sheet_name="Hasil_Skoring_REBA", index=False)

        st.download_button(
            label="⤓ Unduh Laporan REBA (.xlsx)",
            data=excel_buffer_reba.getvalue(),
            file_name="Laporan_Ergonomi_REBA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
