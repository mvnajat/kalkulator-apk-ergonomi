import streamlit as st
import pandas as pd
import math
import io
import re
import altair as alt
from urllib.parse import quote

# =====================================================================
# KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="IE Toolkit — Waktu Kerja & Ergonomi",
    page_icon="◆",
    layout="wide",
)


def H(s):
    """Rapatkan HTML jadi satu baris (hindari markdown menganggapnya code block)."""
    return re.sub(r"\n\s*", "", s.strip())


# =====================================================================
# IKON (SVG stroke 24x24)
# =====================================================================
ICONS = {
    "clock": "<circle cx='12' cy='12' r='9'/><path d='M12 7v5l3 2'/>",
    "timer": "<circle cx='12' cy='13' r='8'/><path d='M12 9v4l2.5 2M9 2.5h6'/>",
    "gauge": "<path d='M4 17a8 8 0 1 1 16 0'/><path d='M12 17l4-5'/>",
    "target": "<circle cx='12' cy='12' r='9'/><circle cx='12' cy='12' r='4.5'/><circle cx='12' cy='12' r='.8'/>",
    "bolt": "<path d='M13 3L5 14h6l-1 7 8-11h-6z'/>",
    "pulse": "<path d='M3 12h4l2-6 4 12 2-6h6'/>",
    "body": "<circle cx='12' cy='5' r='2.5'/><path d='M12 8v6M7 10l5 1 5-1M9.5 21l2.5-7 2.5 7'/>",
    "home": "<path d='M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z'/>",
    "stack": "<path d='M12 3l9 5-9 5-9-5z'/><path d='M3 13l9 5 9-5'/>",
}


def svg_icon(name, size=20, color="currentColor", stroke=1.6):
    return (
        f"<svg width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='{color}' "
        f"stroke-width='{stroke}' stroke-linecap='round' stroke-linejoin='round'>{ICONS[name]}</svg>"
    )


def mask_uri(name):
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' "
        f"stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'>{ICONS[name]}</svg>"
    )
    return 'url("data:image/svg+xml;utf8,' + quote(svg, safe="/ '=:,.-") + '")'


# =====================================================================
# DESIGN SYSTEM (CSS)
# =====================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&display=swap');

:root{
  --bg:#07080c; --ink:#e8eaf3; --mut:#8f94a8; --dim:#5e6275;
  --line:rgba(255,255,255,.07); --glass:rgba(255,255,255,.035);
  --up:#4ade80; --down:#f87171; --amber:#fbbf24; --blue:#7c8cff;
}
html, body, [class*="css"], .stApp{ font-family:'Geist','Inter',system-ui,sans-serif; color:var(--ink); }
.stApp{
  background:
    radial-gradient(1100px 520px at 12% -8%, rgba(104,100,190,.34), transparent 62%),
    radial-gradient(700px 380px at 95% -5%, rgba(80,90,160,.12), transparent 60%),
    var(--bg);
}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{ display:none !important; }
header[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:1.4rem; padding-bottom:4rem; max-width:1480px; }

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"][aria-expanded="true"]{ min-width:310px; width:310px; }
section[data-testid="stSidebar"]{ border-right:1px solid var(--line); }
section[data-testid="stSidebar"] > div:first-child{
  background:
    radial-gradient(520px 320px at 25% 0%, rgba(125,118,210,.30), transparent 70%),
    linear-gradient(180deg,#13141e 0%,#0b0c12 42%,#08090d 100%);
}
section[data-testid="stSidebar"] .block-container{ padding:1.6rem 1.2rem 2rem; }
.brand{ display:flex; align-items:center; gap:14px; }
.brand .nm{ font-size:19px; font-weight:500; color:#fff; letter-spacing:-.01em; line-height:1.15; }
.brand .sb{ font-size:13px; color:var(--mut); }
.hr{ height:1px; background:var(--line); margin:22px 0; }
.welcome{ font-size:32px; font-weight:500; line-height:1.08; letter-spacing:-.025em; color:#fff; }
.last{ color:var(--mut); font-size:14px; margin-top:12px; }
.grp-label{ color:var(--mut); font-size:14px; margin:6px 0 10px 2px; }
.idcard{ border:1px solid var(--line); background:var(--glass); border-radius:16px; padding:6px 16px; margin:4px 0 14px; }
.idcard .r{ display:flex; justify-content:space-between; gap:10px; padding:9px 0; font-size:13px; border-bottom:1px solid rgba(255,255,255,.05); }
.idcard .r:last-child{ border-bottom:none; }
.idcard .r span:first-child{ color:var(--mut); }
.idcard .r span:last-child{ color:#fff; text-align:right; }
.foot{ color:var(--dim); font-size:12px; margin-top:20px; font-family:'Geist Mono',monospace; }

/* navigasi (st.radio) */
section[data-testid="stSidebar"] div[role="radiogroup"]{ flex-direction:column; gap:4px; width:100%; }
section[data-testid="stSidebar"] label[data-baseweb="radio"]{
  position:relative; width:100%; margin:0; padding:14px 16px; gap:14px; align-items:center;
  border:1px solid transparent; border-radius:14px; color:#8f94a8; transition:all .15s;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-of-type{ display:none; }
section[data-testid="stSidebar"] label[data-baseweb="radio"] p{ color:inherit !important; font-size:16px; }
section[data-testid="stSidebar"] label[data-baseweb="radio"]::before{
  content:""; width:22px; height:22px; flex:none; background:currentColor;
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat; -webkit-mask-position:center; mask-position:center;
  -webkit-mask-size:contain; mask-size:contain;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"]:nth-of-type(1)::before{ -webkit-mask-image:__I1__; mask-image:__I1__; }
section[data-testid="stSidebar"] label[data-baseweb="radio"]:nth-of-type(2)::before{ -webkit-mask-image:__I2__; mask-image:__I2__; }
section[data-testid="stSidebar"] label[data-baseweb="radio"]:nth-of-type(3)::before{ -webkit-mask-image:__I3__; mask-image:__I3__; }
section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover{ color:#d8dbea; background:rgba(255,255,255,.03); }
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked){
  color:#fff; border-color:rgba(255,255,255,.13);
  background:linear-gradient(90deg,rgba(255,255,255,.08),rgba(255,255,255,.015) 70%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
}
section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked)::after{
  content:""; position:absolute; right:18px; top:50%; width:3px; height:16px; margin-top:-8px; background:#fff; border-radius:2px;
}
section[data-testid="stSidebar"] div[data-testid="stExpander"]{ background:transparent; border:1px solid var(--line) !important; border-radius:14px; }
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary{ font-size:15px; color:#b6bacb; }
.step{ display:flex; gap:12px; margin:10px 0; font-size:13px; line-height:1.5; color:#aab0c4; }
.step b{ font-family:'Geist Mono',monospace; font-weight:500; color:#fff; min-width:22px; }

/* ================= TOPBAR / TICKER / HERO ================= */
.topbar{ display:flex; align-items:center; justify-content:space-between; padding:2px 0 22px; border-bottom:1px solid var(--line); }
.crumb{ display:flex; align-items:center; gap:14px; font-size:20px; color:var(--mut); }
.crumb b{ color:#fff; font-weight:500; }
.crumb .sep{ color:var(--dim); }
.crumb svg{ color:#cfd2e0; }
.spill{ border:1px solid var(--line); background:var(--glass); border-radius:14px; padding:13px 22px; font-size:16px; color:var(--mut); }
.ticker{ overflow:hidden; white-space:nowrap; border-bottom:1px solid var(--line); padding:18px 0; margin-bottom:36px;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 4%,#000 96%,transparent); mask-image:linear-gradient(90deg,transparent,#000 4%,#000 96%,transparent); }
.track{ display:inline-flex; animation:mq 48s linear infinite; }
.tk{ display:inline-flex; align-items:center; gap:11px; padding:0 30px; border-right:1px solid rgba(255,255,255,.09); font-size:15px; color:var(--ink); }
.tk i{ width:24px; height:24px; border-radius:50%; display:grid; place-items:center; font-size:11px; font-style:normal; font-weight:700; color:#fff; }
.tk em{ font-style:normal; color:var(--mut); }
@keyframes mq{ to{ transform:translateX(-50%); } }
.eyebrow{ display:inline-flex; align-items:center; gap:12px; color:var(--mut); font-size:15px; }
.eyebrow .o{ width:24px; height:24px; border-radius:50%; background:rgba(255,255,255,.09); display:grid; place-items:center; }
.eyebrow .o:after{ content:""; width:8px; height:8px; border-radius:50%; background:#fff; }
.eyebrow b{ color:#fff; font-weight:500; }
.htitle{ font-size:58px; font-weight:500; line-height:.98; letter-spacing:-.035em; margin:18px 0 34px;
  background:linear-gradient(180deg,#fff 30%,#8a8ea3 110%); -webkit-background-clip:text; background-clip:text; color:transparent; }

/* ================= SECTION & CARD ================= */
div[data-testid="stVerticalBlockBorderWrapper"]{
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.012));
  border:1px solid var(--line) !important; border-radius:22px !important; padding:8px 10px;
}
.sec{ margin:6px 0 14px; }
.sec .ey{ display:flex; align-items:center; gap:9px; color:var(--mut); font-size:14px; }
.sec .tt{ font-size:26px; font-weight:500; color:#fff; letter-spacing:-.02em; margin-top:4px; }
.grp{ display:flex; align-items:center; justify-content:space-between; margin:4px 0 12px; }
.grp .t{ font-size:17px; font-weight:500; color:#fff; letter-spacing:-.01em; }
.grp .t span{ color:var(--mut); font-weight:400; margin-right:8px; font-family:'Geist Mono',monospace; font-size:13px; }
.grp .g{ font-size:12px; color:var(--dim); font-family:'Geist Mono',monospace; letter-spacing:.06em; }
.sub{ color:var(--mut); font-size:13px; margin:14px 0 6px; font-family:'Geist Mono',monospace; letter-spacing:.04em; }

/* ================= COIN CARD ================= */
.coin{ position:relative; overflow:hidden; border-radius:26px; padding:22px 24px 0; margin-bottom:14px; border:1px solid rgba(255,255,255,.085);
  background:
    radial-gradient(130% 80% at 0% 100%, color-mix(in srgb, var(--ac) 16%, transparent), transparent 62%),
    linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.012)); }
.coin:before{ content:""; position:absolute; left:0; top:46%; width:3px; height:36px; background:var(--ac); border-radius:0 3px 3px 0; }
.coin .hd{ display:flex; align-items:center; gap:14px; }
.coin .tile{ width:50px; height:50px; border-radius:15px; display:grid; place-items:center; color:var(--ac);
  background:color-mix(in srgb,var(--ac) 14%,#0b0c12); border:1px solid color-mix(in srgb,var(--ac) 38%,transparent); }
.coin .code{ font-size:14px; color:var(--mut); }
.coin .nm{ font-size:21px; font-weight:500; color:#fff; letter-spacing:-.01em; }
.coin .unit{ margin-left:auto; padding:10px 14px; border-radius:12px; border:1px solid var(--line); background:rgba(255,255,255,.03);
  font-family:'Geist Mono',monospace; font-size:12px; color:#cfd2e0; }
.coin .lbl{ margin-top:26px; color:var(--mut); font-size:15px; }
.coin .val{ font-size:46px; font-weight:500; letter-spacing:-.035em; line-height:1.12; color:#fff; }
.coin .val .dec{ color:#6a6e82; }
.coin .val small{ font-size:20px; color:var(--mut); margin-left:6px; letter-spacing:0; }
.coin .row{ display:flex; gap:8px; align-items:center; margin-top:14px; }
.trend{ min-width:44px; height:36px; padding:0 10px; border-radius:18px; display:grid; place-items:center; font-size:15px; border:1px solid transparent; }
.pill{ display:inline-flex; align-items:center; padding:7px 16px; border-radius:999px; font-size:14px; font-weight:500; border:1px solid transparent; }
.up{ background:rgba(74,222,128,.12); color:var(--up); border-color:rgba(74,222,128,.22); }
.down{ background:rgba(248,113,113,.12); color:var(--down); border-color:rgba(248,113,113,.22); }
.flat{ background:rgba(124,140,255,.12); color:#a9b4ff; border-color:rgba(124,140,255,.25); }
.warn{ background:rgba(251,191,36,.12); color:var(--amber); border-color:rgba(251,191,36,.25); }
.coin svg.sp{ display:block; margin:10px -24px 0; width:calc(100% + 48px); height:auto; }
.coin .bars{ display:flex; gap:4px; margin:20px 0 22px; }
.coin .bars i{ flex:1; height:10px; border-radius:3px; background:rgba(255,255,255,.07); }
.mini{ border-radius:20px; padding:16px 18px; border:1px solid var(--line); background:var(--glass); margin-bottom:14px; }
.mini .l{ color:var(--mut); font-size:13px; }
.mini .v{ font-size:30px; font-weight:500; color:#fff; letter-spacing:-.03em; margin:2px 0; }
.mini .s{ font-family:'Geist Mono',monospace; font-size:11.5px; color:#a9b4ff; }

/* ================= CALLOUT ================= */
.callout{ position:relative; border-radius:20px; padding:18px 20px 18px 22px; border:1px solid var(--line); height:100%;
  background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.01)); margin-bottom:6px; }
.callout:before{ content:""; position:absolute; left:0; top:22px; width:3px; height:30px; border-radius:0 3px 3px 0; background:var(--cc); }
.callout .tg{ display:inline-block; font-size:11.5px; letter-spacing:.08em; font-family:'Geist Mono',monospace; padding:4px 10px; border-radius:999px;
  color:var(--cc); background:color-mix(in srgb,var(--cc) 12%,transparent); border:1px solid color-mix(in srgb,var(--cc) 28%,transparent); }
.callout .ti{ font-size:17px; font-weight:500; color:#fff; margin:10px 0 4px; letter-spacing:-.01em; }
.callout .bd{ font-size:13.5px; color:var(--mut); line-height:1.55; }
.callout.ok{ --cc:#4ade80; } .callout.warn{ --cc:#fbbf24; } .callout.err{ --cc:#f87171; }
.callout.info{ --cc:#7c8cff; } .callout.rev{ --cc:#60a5fa; margin-bottom:14px; }

/* ================= TABLE ================= */
.tblwrap{ border:1px solid var(--line); border-radius:22px; overflow:hidden; background:rgba(255,255,255,.015); }
.tbl{ width:100%; border-collapse:collapse; font-size:14.5px; }
.tbl th{ text-align:left; font-weight:400; font-size:13.5px; color:var(--mut); padding:16px 20px; border-bottom:1px solid var(--line); }
.tbl td{ padding:16px 20px; color:#eceef6; border-bottom:1px solid rgba(255,255,255,.05); }
.tbl tr:last-child td{ border-bottom:none; }
.tbl td.no{ color:var(--dim); font-size:13px; width:64px; font-family:'Geist Mono',monospace; }
.tbl td.num{ font-family:'Geist Mono',monospace; font-size:13.5px; }
.tbl tr:hover td{ background:rgba(255,255,255,.02); }
.tbl .pill{ font-size:12.5px; padding:4px 12px; }

/* ================= WIDGET OVERRIDE ================= */
div[data-testid="stWidgetLabel"] p{ font-size:13.5px; color:#a4a9bd; }
.stTextArea textarea, .stNumberInput input, .stTextInput input{
  background:rgba(255,255,255,.04) !important; color:var(--ink) !important; border:1px solid var(--line) !important;
  border-radius:14px !important; font-family:'Geist Mono',monospace !important; font-size:13px !important; }
.stTextArea textarea:focus, .stNumberInput input:focus{ border-color:rgba(160,170,255,.6) !important; box-shadow:0 0 0 3px rgba(124,140,255,.12) !important; }
div[data-baseweb="select"] > div{ background:rgba(255,255,255,.04) !important; border:1px solid var(--line) !important; border-radius:14px !important; font-size:14px; }
div[data-baseweb="popover"] ul{ background:#12131b !important; border-radius:12px; }
.stCheckbox label p{ font-size:13.5px; color:#c3c7d8; }
.stRadio div[role="radiogroup"] label p{ font-size:13.5px; }
div[data-testid="stSlider"] [role="slider"]{ background:#a9b4ff !important; box-shadow:0 0 0 4px rgba(124,140,255,.2) !important; }
.stDownloadButton button{ width:100%; background:rgba(255,255,255,.05) !important; color:#fff !important; border:1px solid rgba(255,255,255,.14) !important;
  border-radius:16px !important; padding:.75rem 1rem; font-size:14.5px !important; font-weight:500; transition:all .15s; }
.stDownloadButton button:hover{ background:rgba(255,255,255,.11) !important; border-color:rgba(255,255,255,.28) !important; }
hr{ border-color:var(--line) !important; }
::-webkit-scrollbar{ width:8px; height:8px; } ::-webkit-scrollbar-thumb{ background:#23253a; border-radius:4px; }
</style>
"""
CSS = CSS.replace("__I1__", mask_uri("timer")).replace("__I2__", mask_uri("pulse")).replace("__I3__", mask_uri("body"))
st.markdown(CSS, unsafe_allow_html=True)


# =====================================================================
# HELPER KOMPONEN UI
# =====================================================================
def sec(eyebrow, title, icon="clock"):
    st.markdown(
        H(f"<div class='sec'><div class='ey'>{svg_icon(icon, 16)}{eyebrow}</div><div class='tt'>{title}</div></div>"),
        unsafe_allow_html=True,
    )


def grp(code, title, tag=""):
    st.markdown(
        H(f"<div class='grp'><div class='t'><span>{code}</span>{title}</div><div class='g'>{tag}</div></div>"),
        unsafe_allow_html=True,
    )


def sublabel(text):
    st.markdown(f"<div class='sub'>{text}</div>", unsafe_allow_html=True)


def callout(tone, tag, title, body):
    st.markdown(
        H(f"<div class='callout {tone}'><span class='tg'>{tag}</span><div class='ti'>{title}</div><div class='bd'>{body}</div></div>"),
        unsafe_allow_html=True,
    )


def pill(text, tone="flat"):
    return f"<span class='pill {tone}'>{text}</span>"


def split_val(s):
    ip, sep, dp = s.partition(".")
    return f"{ip}<span class='dec'>.{dp}</span>" if sep else ip


def spark(vals, color, uid, w=340, h=116):
    n = len(vals)
    if n < 2:
        return ""
    mn, mx = min(vals), max(vals)
    rng = (mx - mn) or 1
    pts = [(i * w / (n - 1), 26 + (1 - (v - mn) / rng) * (h - 58)) for i, v in enumerate(vals)]
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = line + f" L{w},{h} L0,{h} Z"
    imax = max(range(n), key=lambda i: vals[i])
    lx, ly = pts[-1]
    mx_x, mx_y = pts[imax]
    tx = min(max(mx_x - 14, 6), w - 44)
    return H(f"""
    <svg class='sp' viewBox='0 0 {w} {h}'>
      <defs><linearGradient id='g{uid}' x1='0' y1='0' x2='0' y2='1'>
        <stop offset='0' stop-color='{color}' stop-opacity='.34'/><stop offset='1' stop-color='{color}' stop-opacity='0'/>
      </linearGradient></defs>
      <path d='{area}' fill='url(#g{uid})'/>
      <path d='{line}' fill='none' stroke='{color}' stroke-opacity='.8' stroke-width='1.6' stroke-linejoin='round'/>
      <circle cx='{mx_x:.1f}' cy='{mx_y:.1f}' r='8' fill='{color}' opacity='.16'/>
      <circle cx='{mx_x:.1f}' cy='{mx_y:.1f}' r='3.6' fill='#0b0c12' stroke='#cfd3ff' stroke-width='1.5'/>
      <text x='{tx:.1f}' y='{max(mx_y - 14, 12):.1f}' fill='#cfd2e0' font-size='11' font-family='Geist Mono, monospace'>{mx:.2f}</text>
      <circle cx='{lx:.1f}' cy='{ly:.1f}' r='3.4' fill='#0b0c12' stroke='#cfd3ff' stroke-width='1.4'/>
    </svg>""")


def coin_card(uid, icon, code, name, label, value, unit, pill_txt, tone, glyph, color, vals):
    st.markdown(
        H(f"""
        <div class='coin' style='--ac:{color}'>
          <div class='hd'><div class='tile'>{svg_icon(icon, 24)}</div>
            <div><div class='code'>{code}</div><div class='nm'>{name}</div></div>
            <div class='unit'>{unit}</div></div>
          <div class='lbl'>{label}</div>
          <div class='val'>{split_val(value)}</div>
          <div class='row'><span class='trend {tone}'>{glyph}</span><span class='pill {tone}'>{pill_txt}</span></div>
          {spark(vals, color, uid)}
          <div style='height:8px'></div>
        </div>"""),
        unsafe_allow_html=True,
    )


def score_card(code, name, icon, value, vmax, tag, tone, color, sub):
    segs = "".join(
        f"<i style='background:{color};box-shadow:0 0 10px {color}66'></i>" if k < min(value, vmax) else "<i></i>"
        for k in range(vmax)
    )
    st.markdown(
        H(f"""
        <div class='coin' style='--ac:{color}'>
          <div class='hd'><div class='tile'>{svg_icon(icon, 24)}</div>
            <div><div class='code'>{code}</div><div class='nm'>{name}</div></div>
            <div class='unit'>maks {vmax}</div></div>
          <div class='lbl'>Skor akhir</div>
          <div class='val'>{value}<small>/ {vmax}</small></div>
          <div class='row'><span class='pill {tone}'>{tag}</span><span style='color:var(--mut);font-size:13px;margin-left:6px'>{sub}</span></div>
          <div class='bars'>{segs}</div>
        </div>"""),
        unsafe_allow_html=True,
    )


def mini(label, value, sub):
    st.markdown(
        H(f"<div class='mini'><div class='l'>{label}</div><div class='v'>{value}</div><div class='s'>{sub}</div></div>"),
        unsafe_allow_html=True,
    )


def html_table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for i, r in enumerate(rows, 1):
        tds = f"<td class='no'>#{i}</td>" + "".join(
            f"<td class='{'num' if j == len(r) - 1 else ''}'>{c}</td>" for j, c in enumerate(r)
        )
        body += f"<tr>{tds}</tr>"
    st.markdown(
        H(f"<div class='tblwrap'><table class='tbl'><thead><tr><th>No</th>{th}</tr></thead><tbody>{body}</tbody></table></div>"),
        unsafe_allow_html=True,
    )


# =====================================================================
# SIDEBAR
# =====================================================================
LOGO = H("""
<svg width='42' height='42' viewBox='0 0 42 42' fill='none'>
  <defs><linearGradient id='lg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#d9dcff'/><stop offset='1' stop-color='#6f74c9'/></linearGradient></defs>
  <path d='M8 30 L8 14 L21 6 L34 14 L34 30 L21 36 Z' fill='none' stroke='url(#lg)' stroke-width='2' stroke-linejoin='round'/>
  <path d='M14 27 L21 12 L28 27 Z' fill='url(#lg)' opacity='.9'/>
</svg>""")

PAGES = [
    "Modul 1 · Fisiologi", "Modul 2 · OWAS", "Waktu Baku",
    "RULA Assessment", "REBA Assessment", "Modul 4 · Antropometri",
    "Modul 5 · Antropometri Lanjutan", "Modul 6 · Temperatur",
    "Modul 7 · Kebisingan", "Modul 8 · Pencahayaan",
]

with st.sidebar:
    st.markdown(
        H(f"<div class='brand'>{LOGO}<div><div class='nm'>IE Toolkit</div><div class='sb'>Work Design &amp; Ergonomics</div></div></div>"),
        unsafe_allow_html=True,
    )
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown(
        H("<div class='welcome'>Welcome<br>Back, Munajat</div><div class='last'>Kelas J253B · Universitas Pelita Bangsa</div>"),
        unsafe_allow_html=True,
    )
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("<div class='grp-label'>Overview</div>", unsafe_allow_html=True)
    page = st.radio("Navigasi", PAGES, label_visibility="collapsed")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("<div class='grp-label'>Others</div>", unsafe_allow_html=True)
    st.markdown(
        H("""<div class='idcard'>
        <div class='r'><span>Prodi</span><span>Teknik Industri</span></div>
        <div class='r'><span>Author</span><span>Munajat</span></div>
        <div class='r'><span>Collab</span><span>Web Prak. APK &amp; Ergonomi</span></div></div>"""),
        unsafe_allow_html=True,
    )
    with st.expander("Panduan Singkat"):
        st.markdown(
            H("""
            <div class='step'><b>01</b><span><u>Fisiologi</u> — bandingkan kondisi normal dan setelah aktivitas.</span></div>
            <div class='step'><b>02</b><span><u>Postur</u> — gunakan OWAS, RULA, dan REBA sesuai postur yang diamati.</span></div>
            <div class='step'><b>03</b><span><u>Waktu kerja</u> — masukkan waktu observasi dalam detik dan evaluasi waktu baku.</span></div>
            <div class='step'><b>04–08</b><span><u>Antropometri &amp; lingkungan</u> — masukkan data pengukuran asli agar analisis dan ekspor relevan.</span></div>"""),
            unsafe_allow_html=True,
        )
    st.markdown("<div class='foot'>© 2026 · IE TOOLKIT PROJECT</div>", unsafe_allow_html=True)

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
# TOPBAR, TICKER & HERO (dinamis per halaman)
# =====================================================================
HERO = {
    "Modul 1 · Fisiologi": ("Pengukuran respons fisiologis operator", "Fisiologi<br>Kerja"),
    "Modul 2 · OWAS": ("Klasifikasi postur punggung, lengan, kaki dan beban", "OWAS<br>Assessment"),
    "Waktu Baku": ("Kalkulasi time study <b>real-time</b>", "Live Time Study<br>&amp; Uji Data"),
    "RULA Assessment": ("Penilaian anggota gerak atas · <b>Tabel A, B, C</b>", "Upper Limb<br>Assessment"),
    "REBA Assessment": ("Penilaian seluruh tubuh · <b>Tabel A, B, C</b>", "Entire Body<br>Assessment"),
    "Modul 4 · Antropometri": ("Dimensi tubuh dan rancangan stasiun kerja", "Antropometri<br>Dasar"),
    "Modul 5 · Antropometri Lanjutan": ("Uji statistik, keseragaman dan kecukupan data", "Antropometri<br>Lanjutan"),
    "Modul 6 · Temperatur": ("Perbandingan hasil kerja pada kondisi dingin dan panas", "Temperatur<br>&amp; Output"),
    "Modul 7 · Kebisingan": ("Perbandingan hasil kerja pada kondisi normal dan bising", "Kebisingan<br>&amp; Output"),
    "Modul 8 · Pencahayaan": ("Perbandingan hasil kerja pada kondisi normal dan gelap", "Pencahayaan<br>&amp; Output"),
}

st.markdown(
    H(f"""
    <div class='topbar'>
      <div class='crumb'>{svg_icon('home', 26)}<span>Overview</span><span class='sep'>/</span><b>{page}</b></div>
      <div class='spill'>Kelas J253B · UPB</div>
    </div>"""),
    unsafe_allow_html=True,
)

_tick = [
    ("#6366f1", "k", "CONF 99%", "k = 3"), ("#22c55e", "k", "CONF 95%", "k = 2"),
    ("#f59e0b", "k", "CONF 68%", "k = 1"), ("#3b82f6", "W", "WESTINGHOUSE", "4 faktor"),
    ("#ec4899", "R", "RULA", "skor 1–7"), ("#14b8a6", "B", "REBA", "skor 1–15"),
    ("#f97316", "Σ", "OUTPUT STD", "3600 / Wb"),
]
_items = "".join(f"<span class='tk'><i style='background:{c}'>{g}</i>{n} <em>{v}</em></span>" for c, g, n, v in _tick)
st.markdown(H(f"<div class='ticker'><div class='track'>{_items}{_items}</div></div>"), unsafe_allow_html=True)

_eb, _ti = HERO[page]
st.markdown(
    H(f"<div class='eyebrow'><span class='o'></span><span>{_eb}</span></div><div class='htitle'>{_ti}</div>"),
    unsafe_allow_html=True,
)


# =====================================================================
# HALAMAN 1: KALKULATOR WAKTU KERJA & UJI DATA
# =====================================================================
if page == "Waktu Baku":
    col_input, col_hasil = st.columns([1.0, 1.35], gap="large")

    with col_input:
        with st.container(border=True):
            grp("A", "Data Waktu Pengamatan", "INPUT")
            data_raw = st.text_area(
                "Masukkan data waktu pengamatan (detik), pisahkan dengan koma:",
                value="12.5, 13.0, 12.8, 12.4, 15.8, 12.7, 12.9, 12.5, 12.6, 13.0, 12.7, 12.8",
                help="Contoh di atas memiliki 1 data ekstrem (15.8) untuk menguji fitur outlier.",
                height=110,
            )

        with st.container(border=True):
            grp("B", "Parameter Uji Statistik", "CONFIG")
            u1, u2 = st.columns(2)
            with u1:
                konf_dict = {"99% (k = 3)": 3.0, "95% (k = 2)": 2.0, "68% (k = 1)": 1.0}
                k_label = st.selectbox("Tingkat Kepercayaan", list(konf_dict.keys()), index=1)
                k_val = konf_dict[k_label]

                pembagi_std = st.radio(
                    "Rumus Standar Deviasi",
                    ["Sampel (N - 1)", "Populasi (N)"],
                    horizontal=True
                )
            with u2:
                s_pct = st.number_input("Derajat Ketelitian / s (%)", min_value=1.0, max_value=25.0, value=5.0, step=0.5)
                s_val = s_pct / 100.0
                auto_revisi = st.checkbox("Otomatis buang data di luar BKA/BKB (Revisi Data)")

        with st.container(border=True):
            grp("C", "Faktor Penyesuaian · Westinghouse", "RATING")
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

        with st.container(border=True):
            grp("D", "Kelonggaran · Allowance", "ALLOW")
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

                # ---------- KARTU HASIL ----------
                sec("Live Updates", "Waktu Kerja & Output Standar", "timer")
                ra, rb = st.columns(2)
                with ra:
                    coin_card("ws", "timer", "Ws / N = %d" % n_data, "Waktu Siklus", "Rata-rata pengamatan",
                              f"{ws:.2f}", "detik", f"σ = {std_dev:.3f}", "flat", "≈", "#7c8cff", data_aktif)
                with rb:
                    coin_card("wn", "gauge", "Wn = Ws × p", "Waktu Normal", "Setelah rating Westinghouse",
                              f"{wn:.2f}", "detik", f"p = {p:.2f} ({(p - 1) * 100:+.1f}%)",
                              "up" if p >= 1 else "down", "↗" if p >= 1 else "↘", "#a78bfa", [x * p for x in data_aktif])
                rc, rd = st.columns(2)
                with rc:
                    coin_card("wb", "target", "Wb = Wn × (1 + allow)", "Waktu Baku", "Termasuk kelonggaran",
                              f"{wb:.2f}", "detik", f"+{allowance_pct:g}% allowance", "up", "↗", "#f7931a",
                              [x * p * (1 + allowance_pct / 100) for x in data_aktif])
                with rd:
                    coin_card("os", "bolt", "3600 / Wb", "Output Standar", "Kapasitas per jam",
                              f"{output_std:.1f}", "unit/jam", "kapasitas standar", "flat", "→", "#34d399",
                              [3600 / (x * p * (1 + allowance_pct / 100)) if x > 0 else 0 for x in data_aktif])

                # ---------- UJI DATA ----------
                status_seragam = "SERAGAM" if len(outliers) == 0 else "TIDAK SERAGAM"
                status_cukup = "CUKUP (N' <= N)" if n_aksen <= n_data else "BELUM CUKUP (N' > N)"

                sec("Validation", "Uji Keseragaman & Kecukupan", "stack")
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

                # ---------- GRAFIK ----------
                st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
                sec("Control Chart", "Peta Kontrol Keseragaman", "pulse")
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
                area = base.mark_area(
                    line=False,
                    color=alt.Gradient(
                        gradient="linear", x1=1, x2=1, y1=1, y2=0,
                        stops=[alt.GradientStop(color="rgba(124,140,255,0)", offset=0),
                               alt.GradientStop(color="rgba(124,140,255,0.30)", offset=1)],
                    ),
                ).encode(y=alt.Y("Waktu (detik):Q", scale=alt.Scale(zero=False), title="Waktu (detik)"))
                line_data = base.mark_line(color="#9aa6ff", strokeWidth=1.8).encode(
                    y=alt.Y("Waktu (detik):Q", scale=alt.Scale(zero=False))
                )
                points_data = base.mark_point(size=100, filled=True, opacity=1, stroke="#0b0c12", strokeWidth=1.5).encode(
                    y="Waktu (detik):Q",
                    color=alt.Color(
                        "Status:N",
                        scale=alt.Scale(domain=["Normal", "Outlier (Di Luar Batas)"], range=["#c9ceff", "#f87171"]),
                        legend=alt.Legend(orient="top", title=None),
                    ),
                    tooltip=["Pengamatan Ke", "Waktu (detik)", "Status", "BKA", "Rata-rata (Ws)", "BKB"]
                )
                rule_bka = alt.Chart(df_chart).mark_rule(color="#f87171", strokeDash=[6, 5], size=1.4, opacity=.8).encode(y="mean(BKA):Q")
                rule_ws = alt.Chart(df_chart).mark_rule(color="#4ade80", strokeDash=[3, 4], size=1.4, opacity=.8).encode(y="mean(Rata-rata (Ws)):Q")
                rule_bkb = alt.Chart(df_chart).mark_rule(color="#f87171", strokeDash=[6, 5], size=1.4, opacity=.8).encode(y="mean(BKB):Q")

                chart_final = (
                    (area + line_data + points_data + rule_bka + rule_ws + rule_bkb)
                    .properties(height=300)
                    .configure(background="transparent")
                    .configure_view(strokeOpacity=0)
                    .configure_axis(
                        labelColor="#8f94a8", titleColor="#8f94a8", gridColor="rgba(255,255,255,0.05)",
                        domainColor="rgba(255,255,255,0.08)", tickColor="rgba(255,255,255,0.08)",
                        labelFont="Geist Mono", titleFont="Geist", labelFontSize=11, titleFontSize=12,
                    )
                    .configure_legend(labelColor="#c3c7d8", labelFont="Geist", labelFontSize=12)
                )
                with st.container(border=True):
                    st.altair_chart(chart_final, use_container_width=True)
                    st.caption("BKA / BKB: garis putus merah · Ws: garis putus hijau · titik merah = outlier")

                # ---------- TABEL RINGKASAN ----------
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

                st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
                sec("Live Updates", "Parameter Overview", "clock")
                _rows = []
                for nm_, val_ in zip(df_summary["Parameter"], df_summary["Nilai"]):
                    if nm_ == "Status Uji Keseragaman":
                        cell = pill(val_, "up" if val_ == "SERAGAM" else "down")
                    elif nm_ == "Status Uji Kecukupan":
                        cell = pill(val_, "up" if n_aksen <= n_data else "warn")
                    else:
                        cell = str(val_)
                    _rows.append([nm_, cell])
                html_table(["Parameter", "Nilai"], _rows)

                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
                excel_buffer_1 = io.BytesIO()
                with pd.ExcelWriter(excel_buffer_1, engine="openpyxl") as writer:
                    df_summary.to_excel(writer, sheet_name="Ringkasan_Perhitungan", index=False)
                    df_chart.to_excel(writer, sheet_name="Data_Pengamatan", index=False)

                st.download_button(
                    label="Unduh Laporan Waktu Baku & Uji Data (.xlsx)",
                    data=excel_buffer_1.getvalue(),
                    file_name="Laporan_Waktu_Baku_APK.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        except ValueError:
            callout("err", "INPUT ERROR", "Format data tidak valid",
                    "Pastikan data pengamatan hanya berisi angka dan dipisahkan dengan tanda koma (,).")


    # Pelengkap Modul 3: perbandingan faktor rating dan waktu baku.
    with st.container(border=True):
        grp("D", "Perbandingan Metode Rating Modul 3", "SCHUMMARD · WESTINGHOUSE · OBJEKTIF")
        st.caption("Masukkan waktu observasi rata-rata dan nilai rating berdasarkan tabel praktikum. Nilai tabel Schummard/Objective harus diverifikasi dengan lembar modul yang digunakan.")
        c1,c2,c3=st.columns(3)
        obs_mean=c1.number_input("Waktu observasi rata-rata (detik)",0.01,100000.0,12.8,step=0.1,key="m3_obs")
        allowance=c2.number_input("Allowance (%)",0.0,90.0,15.5,step=0.5,key="m3_allow")/100
        sch_score=c3.number_input("Skor Schummard",0.0,120.0,60.0,step=1.0,key="m3_sch_score")
        c1,c2,c3=st.columns(3)
        west_rating=c1.number_input("Rating Westinghouse total (desimal)",-0.5,0.5,0.0,step=0.01,key="m3_west")
        obj_total=c2.number_input("Total faktor kesulitan Objective (%)",-90.0,300.0,0.0,step=1.0,key="m3_obj")
        obj_p1=c3.number_input("P1 Objective (Schummard / 60)",0.1,2.0,1.0,step=0.01,key="m3_obj_p1")
        rating_sch=sch_score/60
        rating_west=1+west_rating
        rating_obj=obj_p1*(1+obj_total/100)
        normal_sch=obs_mean*rating_sch; normal_west=obs_mean*rating_west; normal_obj=obs_mean*rating_obj
        denom=max(0.01,1-allowance)
        result_methods=pd.DataFrame([
            {"Metode":"Schummard","Faktor rating":rating_sch,"Waktu normal (detik)":normal_sch,"Waktu baku (detik)":normal_sch/denom,"Output teoritis (unit/jam)":3600/(normal_sch/denom)},
            {"Metode":"Westinghouse","Faktor rating":rating_west,"Waktu normal (detik)":normal_west,"Waktu baku (detik)":normal_west/denom,"Output teoritis (unit/jam)":3600/(normal_west/denom)},
            {"Metode":"Objective","Faktor rating":rating_obj,"Waktu normal (detik)":normal_obj,"Waktu baku (detik)":normal_obj/denom,"Output teoritis (unit/jam)":3600/(normal_obj/denom)},
        ])
        st.dataframe(result_methods,use_container_width=True)
        st.caption("Perhitungan aplikasi: rating Schummard = skor/60; Westinghouse = 1 + total rating; Objective = P1 × [1 + total faktor kesulitan/100]. Waktu baku dihitung Wn/(1−allowance) dan output = 3600/Wb. Sesuaikan konvensi dengan instruksi dosen/modul.")
        b=io.BytesIO()
        with pd.ExcelWriter(b,engine="openpyxl") as w: result_methods.to_excel(w,index=False,sheet_name="Perbandingan_Metode")
        st.download_button("Unduh perbandingan Modul 3 (.xlsx)",b.getvalue(),"Laporan_Modul_3_Perbandingan_Metode.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# =====================================================================
# MODUL TAMBAHAN 1, 2, 4, 5, 6, 7, 8
# =====================================================================
elif page == "Modul 1 · Fisiologi":
    st.caption("Isi hasil pengukuran nyata. CVL dihitung dari denyut jantung; rumus ECPT/ECPM pada dokumen praktikum tidak terbaca sebagai teks, jadi tidak dibuat-buat di sini.")
    with st.container(border=True):
        grp("A", "Identitas Praktikum", "METADATA")
        m1, m2, m3 = st.columns(3)
        kelas = m1.text_input("Kelas", key="fis_kelas")
        kelompok = m2.text_input("Kelompok", key="fis_kelompok")
        tanggal = m3.date_input("Tanggal", key="fis_tanggal")
        operator = st.text_input("Nama / kode operator", key="fis_operator")
        a1, a2, a3 = st.columns(3)
        usia = a1.number_input("Usia (tahun)", 1, 100, 20, key="fis_usia")
        berat = a2.number_input("Berat badan (kg)", 1.0, 300.0, 60.0, key="fis_berat")
        suhu = a3.number_input("Suhu tubuh (°C)", 30.0, 45.0, 36.5, step=0.1, key="fis_suhu")
    with st.container(border=True):
        grp("B", "Pengukuran Fisiologis", "HEART RATE")
        st.write("Masukkan denyut jantung dalam bpm pada kondisi normal dan setelah aktivitas fisik.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Kondisi normal**")
            hr_rest = st.number_input("Denyut jantung istirahat (bpm)", 30, 220, 75, key="fis_hr_rest")
            tekanan_rest = st.text_input("Tekanan darah (opsional)", placeholder="Contoh: 120/80", key="fis_bp_rest")
            tulisan_rest = st.text_area("Catatan / hasil tulisan kondisi normal", key="fis_write_rest")
        with c2:
            st.markdown("**Setelah aktivitas fisik**")
            hr_work = st.number_input("Denyut jantung setelah aktivitas (bpm)", 30, 240, 110, key="fis_hr_work")
            tekanan_work = st.text_input("Tekanan darah setelah aktivitas (opsional)", placeholder="Contoh: 135/85", key="fis_bp_work")
            tulisan_work = st.text_area("Catatan / hasil tulisan setelah aktivitas", key="fis_write_work")
        st.markdown("**ECPT / ECPM**")
        st.caption("Rumus ECPT/ECPM pada file modul berada pada elemen visual yang tidak terbaca dalam ekstraksi teks. Isi hasil perhitungan dari rumus di lembar praktikum agar tidak menggunakan rumus pengganti yang belum terverifikasi.")
        ecpt = st.number_input("ECPT hasil hitung manual (sesuai satuan modul)", 0.0, 100000.0, 0.0, key="fis_ecpt")
        ecpm = st.number_input("ECPM hasil hitung manual (sesuai satuan modul)", 0.0, 100000.0, 0.0, key="fis_ecpm")
    hr_max = max(1, 220 - usia)
    cvl = max(0.0, (hr_work - hr_rest) / max(1, hr_max - hr_rest) * 100) if hr_max > hr_rest else 0.0
    c1, c2, c3 = st.columns(3)
    c1.metric("Denyut jantung maksimum estimasi", f"{hr_max} bpm")
    c2.metric("Selisih denyut jantung", f"{hr_work - hr_rest} bpm")
    c3.metric("CVL", f"{cvl:.2f}%")
    st.caption("CVL menggunakan pendekatan umum: (HR kerja − HR istirahat) / (HR maksimum − HR istirahat) × 100%, dengan HR maksimum estimasi 220 − usia. Pastikan rumus ini sesuai arahan dosen/modul Anda.")
    st.text_area("Analisis, kesimpulan, dan saran", key="fis_analisis")
    df = pd.DataFrame([{"Item":"Kelas","Nilai":kelas},{"Item":"Kelompok","Nilai":kelompok},{"Item":"Tanggal","Nilai":str(tanggal)},{"Item":"Operator","Nilai":operator},{"Item":"Usia (tahun)","Nilai":usia},{"Item":"Berat badan (kg)","Nilai":berat},{"Item":"Suhu tubuh (°C)","Nilai":suhu},{"Item":"HR istirahat (bpm)","Nilai":hr_rest},{"Item":"HR setelah aktivitas (bpm)","Nilai":hr_work},{"Item":"Tekanan darah normal","Nilai":tekanan_rest},{"Item":"Tekanan darah setelah aktivitas","Nilai":tekanan_work},{"Item":"CVL (%)","Nilai":round(cvl,2)},{"Item":"ECPT hasil hitung manual","Nilai":ecpt},{"Item":"ECPM hasil hitung manual","Nilai":ecpm},{"Item":"Catatan normal","Nilai":tulisan_rest},{"Item":"Catatan setelah aktivitas","Nilai":tulisan_work},{"Item":"Analisis/kesimpulan/saran","Nilai":st.session_state.get('fis_analisis','')}])
    buf=io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w: df.to_excel(w, index=False, sheet_name="Fisiologi")
    st.download_button("Unduh laporan Modul 1 (.xlsx)", buf.getvalue(), "Laporan_Modul_1_Fisiologi.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif page == "Modul 2 · OWAS":
    with st.container(border=True):
        grp("A", "Identitas & Aktivitas", "POSTURE OBSERVATION")
        c1,c2,c3=st.columns(3)
        operator= c1.text_input("Operator", key="ow_operator")
        aktivitas= c2.text_input("Aktivitas / stasiun", key="ow_activity", value="Menulis")
        beban_kg= c3.number_input("Beban (kg)",0.0,200.0,0.0,step=0.5,key="ow_load")
        c1,c2=st.columns(2)
        back = c1.selectbox("Punggung (Back)",[(1,"1 — Tegak"),(2,"2 — Membungkuk"),(3,"3 — Memutar / miring"),(4,"4 — Membungkuk dan memutar")],format_func=lambda x:x[1],key="ow_back")[0]
        arms = c2.selectbox("Lengan (Arms)",[(1,"1 — Kedua lengan di bawah bahu"),(2,"2 — Satu lengan di atas bahu"),(3,"3 — Kedua lengan di atas bahu")],format_func=lambda x:x[1],key="ow_arms")[0]
        legs = st.selectbox("Kaki (Legs)",[(1,"1 — Duduk"),(2,"2 — Berdiri dengan dua kaki lurus"),(3,"3 — Berdiri dengan satu kaki lurus"),(4,"4 — Berdiri / jongkok dengan dua lutut ditekuk"),(5,"5 — Berdiri / jongkok dengan satu lutut ditekuk"),(6,"6 — Berlutut pada satu/dua lutut"),(7,"7 — Berjalan / bergerak")],format_func=lambda x:x[1],key="ow_legs")[0]
        loadcat=st.selectbox("Kategori beban OWAS",[(1,"1 — ≤ 10 kg"),(2,"2 — 10–20 kg"),(3,"3 — > 20 kg")],format_func=lambda x:x[1],key="ow_loadcat")[0]
        st.caption("Kode postur di atas mengikuti kategori OWAS umum. Skor tindakan OWAS resmi berasal dari kombinasi 4 kode; tabel matriks lengkap tidak tersedia sebagai teks pada dokumen yang diunggah, sehingga hasil tindakan di bawah merupakan skrining awal, bukan pengganti tabel matriks resmi.")
    # Skrining konservatif untuk membantu interpretasi, bukan skor matriks OWAS resmi.
    severity = (back in (3,4)) + (arms == 3) + (legs in (4,5,6)) + (loadcat == 3)
    if severity == 0: action, advice = "Perlu konfirmasi matriks OWAS", "Postur relatif lebih netral; cocokkan kode 4 digit dengan tabel OWAS resmi."
    elif severity <= 2: action, advice = "Perlu ditinjau", "Tinjau postur dan durasi paparan; verifikasi kategori tindakan menggunakan tabel OWAS resmi."
    else: action, advice = "Prioritaskan evaluasi", "Kombinasi postur/beban menunjukkan faktor yang perlu segera dievaluasi; verifikasi skor tindakan pada tabel resmi."
    st.metric("Kode postur OWAS", f"{back}-{arms}-{legs}-{loadcat}")
    callout("warn", "SCREENING", action, advice)
    catatan=st.text_area("Catatan observasi dan usulan perbaikan",key="ow_notes")
    df=pd.DataFrame([{"Operator":operator,"Aktivitas":aktivitas,"Punggung":back,"Lengan":arms,"Kaki":legs,"Kategori beban":loadcat,"Beban aktual (kg)":beban_kg,"Kode OWAS":f"{back}-{arms}-{legs}-{loadcat}","Skrining":action,"Catatan":catatan}])
    buf=io.BytesIO()
    with pd.ExcelWriter(buf,engine="openpyxl") as w: df.to_excel(w,index=False,sheet_name="OWAS")
    st.download_button("Unduh laporan OWAS (.xlsx)",buf.getvalue(),"Laporan_Modul_2_OWAS.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif page == "Modul 4 · Antropometri":
    dimensi = ["Tinggi badan tegak","Tinggi mata berdiri","Tinggi bahu berdiri","Tinggi siku berdiri","Panjang lengan bawah","Tinggi lutut","Jangkauan tangan","Rentang tangan","Tinggi dada tegak","Tinggi mata duduk","Tinggi badan duduk","Tinggi siku duduk","Tinggi pundak","Tinggi olecranon","Panjang pergelangan ke olecranon","Panjang kaki luar","Lebar pinggul","Lebar bahu","Panjang kepala","Lebar kepala","Diameter maksimum dari dagu","Dagu ke puncak kepala","Telinga ke puncak kepala","Telinga ke belakang kepala","Antara dua telinga","Mata ke puncak kepala","Mata ke belakang kepala","Antara dua pupil mata","Hidung ke puncak kepala","Hidung ke belakang kepala","Mulut ke puncak kepala","Lebar mulut"]
    with st.container(border=True):
        grp("A","Identitas Sampel & Dimensi Stasiun Kerja","DATA INPUT")
        c1,c2,c3=st.columns(3)
        kelas=c1.text_input("Kelas",key="ant_kelas"); kelompok=c2.text_input("Kelompok",key="ant_kelompok"); operator=c3.text_input("Kode responden",key="ant_resp")
        st.markdown("**Dimensi tubuh (cm)**")
        values={}
        for i in range(0,len(dimensi),2):
            c=st.columns(2)
            for j in range(2):
                idx=i+j
                if idx < len(dimensi): values[dimensi[idx]]=c[j].number_input(dimensi[idx],0.0,300.0,0.0,step=0.1,key=f"ant_dim_{idx}")
        st.markdown("**Dimensi fasilitas (cm)**")
        furn={}
        fc=["Panjang pintu","Lebar pintu","Tinggi pintu","Tebal pintu","Panjang meja","Lebar meja","Tinggi meja","Tebal meja","Tinggi kursi","Lebar kursi","Tinggi sandaran tangan","Sudut sandaran punggung"]
        cols=st.columns(3)
        for i,n in enumerate(fc): furn[n]=cols[i%3].number_input(n,0.0,500.0,0.0,step=0.5,key=f"ant_f_{i}")
    st.info("Masukkan ukuran yang benar-benar diukur. Nilai 0 berarti belum diisi dan tidak akan ditafsirkan sebagai ukuran aktual.")
    st.text_area("Analisis kesesuaian pintu, meja, kursi, rancangan/usulan, kesimpulan",key="ant_notes")
    df1=pd.DataFrame([{"Dimensi tubuh":k,"Ukuran (cm)":v} for k,v in values.items() if v>0])
    df2=pd.DataFrame([{"Fasilitas":k,"Ukuran (cm)":v} for k,v in furn.items() if v>0])
    buf=io.BytesIO()
    with pd.ExcelWriter(buf,engine="openpyxl") as w:
        df1.to_excel(w,index=False,sheet_name="Dimensi_Tubuh"); df2.to_excel(w,index=False,sheet_name="Dimensi_Fasilitas")
    st.download_button("Unduh laporan Antropometri (.xlsx)",buf.getvalue(),"Laporan_Modul_4_Antropometri.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif page == "Modul 5 · Antropometri Lanjutan":
    st.write("Tempel data antropometri sebagai CSV: baris pertama adalah nama dimensi, setiap baris berikutnya satu responden. Contoh: `Tinggi_Badan,Lebar_Pinggul,Jangkauan`.")
    raw=st.text_area("Data CSV",value="Tinggi_Badan,Lebar_Pinggul,Jangkauan\n160,34,65\n165,36,68\n170,37,70\n172,38,72\n168,35,69\n175,40,74\n163,34,66\n180,42,78\n158,33,64\n169,37,70",height=220,key="ant5_csv")
    confidence=st.selectbox("Tingkat kepercayaan untuk batas kontrol",["95% (k=2)","99% (k=3)"],key="ant5_conf")
    k=2 if confidence.startswith("95") else 3
    precision=st.number_input("Ketelitian uji kecukupan s (%)",1.0,25.0,5.0,step=0.5,key="ant5_precision")/100
    try:
        data=pd.read_csv(io.StringIO(raw)).apply(pd.to_numeric,errors="coerce").dropna(axis=1,how="all")
        if data.empty or len(data)<2: st.warning("Masukkan setidaknya dua baris sampel numerik.")
        else:
            summaries=[]; outliers={}
            for col in data.columns:
                x=data[col].dropna().astype(float); n=len(x); mean=float(x.mean()); sd=float(x.std(ddof=1)) if n>1 else 0.0
                bka=mean+k*sd; bkb=mean-k*sd; sumx=float(x.sum()); sumx2=float((x*x).sum())
                n_req=((k/precision)*math.sqrt(max(0,n*sumx2-sumx**2))/abs(sumx))**2 if sumx else float("inf")
                vals={f"P{q}":float(x.quantile(q/100)) for q in (5,10,50,90,95)}
                outside=[int(i+1) for i,v in enumerate(x.tolist()) if v>bka or v<bkb]
                outliers[col]=outside
                summaries.append({"Dimensi":col,"N":n,"Rata-rata":mean,"SD sampel":sd,"BKA":bka,"BKB":bkb,"Min":float(x.min()),"Max":float(x.max()),"N' kecukupan":math.ceil(n_req) if math.isfinite(n_req) else None,"Status kecukupan":"Cukup" if n_req<=n else "Tidak cukup",**vals})
            sdf=pd.DataFrame(summaries)
            st.dataframe(sdf,use_container_width=True)
            for col in data.columns:
                with st.expander(f"Grafik kontrol — {col}"):
                    chart=pd.DataFrame({"Sampel":range(1,len(data[col].dropna())+1),"Nilai":data[col].dropna().tolist()})
                    st.line_chart(chart.set_index("Sampel"))
                    row=sdf[sdf["Dimensi"]==col].iloc[0]
                    st.caption(f"BKA={row['BKA']:.2f}; BKB={row['BKB']:.2f}. Indeks baris di luar batas: {outliers[col] or 'tidak ada'}.")
            st.caption("Catatan: uji kecukupan menggunakan bentuk umum N' = [(k/s)·√(NΣx²−(Σx)²)/Σx]². Kuantil dihitung dari data empiris; ini bukan uji normalitas formal.")
            buf=io.BytesIO()
            with pd.ExcelWriter(buf,engine="openpyxl") as w:
                data.to_excel(w,index=False,sheet_name="Data_Mentah"); sdf.to_excel(w,index=False,sheet_name="Statistik")
            st.download_button("Unduh analisis Antropometri Lanjutan (.xlsx)",buf.getvalue(),"Laporan_Modul_5_Antropometri_Lanjutan.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"CSV belum dapat diproses: {e}. Pastikan format CSV valid dan angka memakai titik desimal.")

elif page in ("Modul 6 · Temperatur", "Modul 7 · Kebisingan", "Modul 8 · Pencahayaan"):
    is_temp=page.startswith("Modul 6")
    is_noise=page.startswith("Modul 7")
    module_no=6 if is_temp else (7 if is_noise else 8)
    label_a,label_b=("Dingin","Panas") if is_temp else (("Normal","Bising") if is_noise else ("Normal","Gelap"))
    measure_label="Temperatur (°C)" if is_temp else ("Kebisingan (dB, opsional)" if is_noise else "Pencahayaan (lux, opsional)")
    with st.container(border=True):
        grp("A","Identitas & Kondisi Lingkungan","EXPERIMENT")
        c1,c2,c3=st.columns(3)
        operator=c1.text_input("Operator",key=f"env{module_no}_op")
        kelas=c2.text_input("Kelas / kelompok",key=f"env{module_no}_class")
        durasi=c3.number_input("Durasi percobaan (menit)",1,60,2,key=f"env{module_no}_duration")
        c1,c2=st.columns(2)
        with c1:
            st.markdown(f"**Kondisi {label_a}**")
            measure_a=st.number_input(f"{measure_label} — {label_a}",0.0,2000.0,20.0 if is_temp else 0.0,step=0.5,key=f"env{module_no}_measure_a")
            out_a=[st.number_input(f"Output percobaan {i} — {label_a}",0,10000,0,key=f"env{module_no}_out_a_{i}") for i in range(1,4)]
            err_a=[st.number_input(f"Kesalahan percobaan {i} — {label_a}",0,10000,0,key=f"env{module_no}_err_a_{i}") for i in range(1,4)]
        with c2:
            st.markdown(f"**Kondisi {label_b}**")
            measure_b=st.number_input(f"{measure_label} — {label_b}",0.0,2000.0,30.0 if is_temp else 0.0,step=0.5,key=f"env{module_no}_measure_b")
            out_b=[st.number_input(f"Output percobaan {i} — {label_b}",0,10000,0,key=f"env{module_no}_out_b_{i}") for i in range(1,4)]
            err_b=[st.number_input(f"Kesalahan percobaan {i} — {label_b}",0,10000,0,key=f"env{module_no}_err_b_{i}") for i in range(1,4)]
    def env_stats(outputs, errors):
        avg=float(sum(outputs)/len(outputs)); err=float(sum(errors)/len(errors)); err_pct=(err/avg*100) if avg>0 else 0.0
        good=max(0.0,avg-err); efficiency=(good/avg*100) if avg>0 else 0.0
        return avg,err,err_pct,efficiency
    sa=env_stats(out_a,err_a); sb=env_stats(out_b,err_b)
    st.markdown("### Ringkasan hasil")
    c1,c2,c3,c4=st.columns(4)
    c1.metric(f"Rata-rata output {label_a}",f"{sa[0]:.2f}")
    c2.metric(f"Rata-rata output {label_b}",f"{sb[0]:.2f}")
    c3.metric(f"Kesalahan rata-rata {label_a}",f"{sa[2]:.2f}%")
    c4.metric(f"Kesalahan rata-rata {label_b}",f"{sb[2]:.2f}%")
    compare=pd.DataFrame({"Kondisi":[label_a,label_b],"Percobaan 1":[out_a[0],out_b[0]],"Percobaan 2":[out_a[1],out_b[1]],"Percobaan 3":[out_a[2],out_b[2]],"Rata-rata output":[sa[0],sb[0]],"Rata-rata kesalahan":[sa[1],sb[1]],"Kesalahan (%)":[sa[2],sb[2]],"Efisiensi (%)":[sa[3],sb[3]],measure_label:[measure_a,measure_b]})
    st.bar_chart(compare.set_index("Kondisi")[["Rata-rata output","Kesalahan (%)","Efisiensi (%)"]])
    st.dataframe(compare,use_container_width=True)
    st.caption("Kesalahan (%) = rata-rata kesalahan / rata-rata output × 100. Efisiensi operasional di sini didefinisikan sebagai (rata-rata output − rata-rata kesalahan) / rata-rata output × 100; ini definisi analisis aplikasi, bukan rumus eksplisit yang tercetak pada modul.")
    notes=st.text_area("Analisis hasil, kesimpulan dan saran",key=f"env{module_no}_notes")
    buf=io.BytesIO()
    with pd.ExcelWriter(buf,engine="openpyxl") as w:
        compare.to_excel(w,index=False,sheet_name=f"Modul_{module_no}")
        pd.DataFrame([{"Operator":operator,"Kelas/kelompok":kelas,"Durasi (menit)":durasi,"Analisis":notes}]).to_excel(w,index=False,sheet_name="Metadata")
    st.download_button(f"Unduh laporan Modul {module_no} (.xlsx)",buf.getvalue(),f"Laporan_Modul_{module_no}.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# =====================================================================
# HALAMAN 2: SKORING POSTUR KERJA RULA
# =====================================================================
elif page == "RULA Assessment":
    col_ra, col_rb, col_rres = st.columns([1.05, 1.05, 1.0], gap="large")

    with col_ra:
        with st.container(border=True):
            grp("A", "Grup A · Lengan & Pergelangan", "UPPER LIMB")
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

            sublabel("OTOT &amp; BEBAN · GRUP A")
            rula_muscle_a = 1 if st.checkbox("Postur Grup A statis >1 menit atau repetitif >4x/menit (+1)", key="rula_ma") else 0
            rula_force_a = st.selectbox("Beban / Gaya Grup A (Force/Load)", [
                (0, "0 : Beban < 2 kg (intermiten)"),
                (1, "1 : Beban 2 - 10 kg (intermiten)"),
                (2, "2 : Beban 2 - 10 kg (statis / repetitif)"),
                (3, "3 : Beban > 10 kg atau beban kejut")
            ], format_func=lambda x: x[1], key="rula_fa")[0]

    with col_rb:
        with st.container(border=True):
            grp("B", "Grup B · Leher, Punggung & Kaki", "TRUNK / LEGS")
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

            sublabel("OTOT &amp; BEBAN · GRUP B")
            rula_muscle_b = 1 if st.checkbox("Postur Grup B statis >1 menit atau repetitif >4x/menit (+1)", key="rula_mb") else 0
            rula_force_b = st.selectbox("Beban / Gaya Grup B (Force/Load)", [
                (0, "0 : Beban < 2 kg (intermiten)"),
                (1, "1 : Beban 2 - 10 kg (intermiten)"),
                (2, "2 : Beban 2 - 10 kg (statis / repetitif)"),
                (3, "3 : Beban > 10 kg atau beban kejut")
            ], format_func=lambda x: x[1], key="rula_fb")[0]

    with col_rres:
        score_table_a = RULA_TABLE_A[rula_ua - 1][rula_la - 1][rula_wr - 1][rula_wt - 1]
        score_c = score_table_a + rula_muscle_a + rula_force_a

        score_table_b = RULA_TABLE_B[rula_nk - 1][rula_tr - 1][rula_legs - 1]
        score_d = score_table_b + rula_muscle_b + rula_force_b

        idx_c = min(score_c, 8) - 1
        idx_d = min(score_d, 7) - 1
        rula_grand = RULA_TABLE_C[idx_c][idx_d]

        if rula_grand in [1, 2]:
            tone, pt, color, tag = "ok", "up", "#4ade80", "Level 1 · Rendah"
            rula_kat = "Action Level 1 (Risiko Rendah - Dapat Diterima)"
            body = "Postur kerja dapat diterima jika tidak dipertahankan dalam waktu lama."
        elif rula_grand in [3, 4]:
            tone, pt, color, tag = "warn", "warn", "#fbbf24", "Level 2 · Sedang"
            rula_kat = "Action Level 2 (Risiko Sedang - Perlu Investigasi)"
            body = "Diperlukan investigasi lebih lanjut dan perubahan posisi kerja mungkin dibutuhkan."
        elif rula_grand in [5, 6]:
            tone, pt, color, tag = "err", "down", "#fb923c", "Level 3 · Tinggi"
            rula_kat = "Action Level 3 (Risiko Tinggi - Segera Perbaiki)"
            body = "Investigasi dan perubahan desain stasiun kerja harus segera dilakukan dalam waktu dekat."
        else:
            tone, pt, color, tag = "err", "down", "#f87171", "Level 4 · Kritis"
            rula_kat = "Action Level 4 (Risiko Sangat Tinggi - Perbaiki Sekarang!)"
            body = "Kondisi kritis! Perbaikan postur dan stasiun kerja harus dilakukan SEKARANG JUGA."

        score_card("RULA · Tabel C", "Skor Akhir", "pulse", rula_grand, 7, tag, pt, color, f"C={score_c} · D={score_d}")
        m1, m2 = st.columns(2)
        with m1:
            mini("Skor C · Grup A", score_c, f"Tabel A = {score_table_a}")
        with m2:
            mini("Skor D · Grup B", score_d, f"Tabel B = {score_table_b}")
        callout(tone, tag.upper(), rula_kat, body)

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

    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    sec("Live Updates", "Rincian Skoring RULA", "clock")
    _rows = [[a, pill(b, pt) if a == "Kategori Action Level" else b]
             for a, b in zip(df_rula["Komponen Evaluasi RULA"], df_rula["Nilai / Skor"])]
    html_table(["Komponen Evaluasi", "Nilai / Skor"], _rows)

    excel_buffer_rula = io.BytesIO()
    with pd.ExcelWriter(excel_buffer_rula, engine="openpyxl") as writer:
        df_rula.to_excel(writer, sheet_name="Hasil_Skoring_RULA", index=False)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.download_button(
        label="Unduh Laporan RULA (.xlsx)",
        data=excel_buffer_rula.getvalue(),
        file_name="Laporan_Ergonomi_RULA.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


# =====================================================================
# HALAMAN 3: SKORING POSTUR KERJA REBA
# =====================================================================
elif page == "REBA Assessment":
    col_eba, col_ebb, col_ebres = st.columns([1.05, 1.05, 1.0], gap="large")

    with col_eba:
        with st.container(border=True):
            grp("A", "Grup A · Punggung, Leher & Kaki", "TRUNK / LEGS")
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
        with st.container(border=True):
            grp("B", "Grup B · Lengan & Pergelangan", "UPPER LIMB")
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

            sublabel("9 · SKOR AKTIVITAS (ACTIVITY SCORE)")
            act1 = 1 if st.checkbox("1 atau lebih bagian tubuh statis > 1 menit (+1)", key="reba_act1") else 0
            act2 = 1 if st.checkbox("Gerakan berulang > 4x per menit (+1)", key="reba_act2") else 0
            act3 = 1 if st.checkbox("Perubahan postur besar secara cepat / tidak stabil (+1)", key="reba_act3") else 0
            reba_activity = act1 + act2 + act3

    with col_ebres:
        eb_table_a = REBA_TABLE_A[reba_tr - 1][reba_nk - 1][reba_legs - 1]
        reba_score_a = min(eb_table_a + reba_total_load, 12)

        eb_table_b = REBA_TABLE_B[reba_ua - 1][reba_la - 1][reba_wr - 1]
        reba_score_b = min(eb_table_b + reba_coupling, 12)

        reba_score_c = REBA_TABLE_C[reba_score_a - 1][reba_score_b - 1]
        reba_final = reba_score_c + reba_activity

        if reba_final == 1:
            tone, pt, color, tag = "ok", "up", "#4ade80", "Level 0 · Sangat Rendah"
            reba_kat = "Action Level 0 (Risiko Sangat Rendah - Tidak Perlu Tindakan)"
            body = "Postur kerja aman dan tidak memerlukan tindakan perbaikan."
        elif reba_final in [2, 3]:
            tone, pt, color, tag = "info", "flat", "#7c8cff", "Level 1 · Rendah"
            reba_kat = "Action Level 1 (Risiko Rendah - Mungkin Perlu Perbaikan)"
            body = "Risiko rendah, perubahan postur mungkin diperlukan ke depannya."
        elif reba_final in [4, 5, 6, 7]:
            tone, pt, color, tag = "warn", "warn", "#fbbf24", "Level 2 · Sedang"
            reba_kat = "Action Level 2 (Risiko Sedang - Perlu Tindakan)"
            body = "Perlu investigasi lebih lanjut dan tindakan perbaikan postur kerja."
        elif reba_final in [8, 9, 10]:
            tone, pt, color, tag = "err", "down", "#fb923c", "Level 3 · Tinggi"
            reba_kat = "Action Level 3 (Risiko Tinggi - Segera Perbaiki)"
            body = "Risiko cedera tinggi! Perlu tindakan perbaikan sesegera mungkin."
        else:
            tone, pt, color, tag = "err", "down", "#f87171", "Level 4 · Kritis"
            reba_kat = "Action Level 4 (Risiko Sangat Tinggi - Perbaiki Saat Ini Juga!)"
            body = "Kondisi berbahaya! Tindakan perbaikan mutlak dilakukan SAAT INI JUGA."

        score_card("REBA · Tabel C", "Skor Akhir", "body", min(reba_final, 15), 15, tag, pt, color,
                   f"C={reba_score_c} + akt. {reba_activity}")
        m1, m2 = st.columns(2)
        with m1:
            mini("Skor A · Grup A", reba_score_a, f"Tabel A = {eb_table_a}")
        with m2:
            mini("Skor B · Grup B", reba_score_b, f"Tabel B = {eb_table_b}")
        callout(tone, tag.upper(), reba_kat, body)

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

    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    sec("Live Updates", "Rincian Skoring REBA", "clock")
    _rows = [[a, pill(b, pt) if a == "Kategori Action Level" else b]
             for a, b in zip(df_reba["Komponen Evaluasi REBA"], df_reba["Nilai / Skor"])]
    html_table(["Komponen Evaluasi", "Nilai / Skor"], _rows)

    excel_buffer_reba = io.BytesIO()
    with pd.ExcelWriter(excel_buffer_reba, engine="openpyxl") as writer:
        df_reba.to_excel(writer, sheet_name="Hasil_Skoring_REBA", index=False)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.download_button(
        label="Unduh Laporan REBA (.xlsx)",
        data=excel_buffer_reba.getvalue(),
        file_name="Laporan_Ergonomi_REBA.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
