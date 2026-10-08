import streamlit as st
import pickle
import pandas as pd
import os
import urllib.request
import json
from datetime import datetime
import intl_predictor as ip

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cricket & IPL Match Center | Aditya Kumar",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Sleek, Modern Glassmorphism Styling
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 15% 10%, #1e1b4b 0%, #0f172a 45%, #020617 100%) fixed !important;
    color: #e2e8f0;
}

/* Page container */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1140px !important;
}

/* Clean fieldset border styling: title embedded on the line */
fieldset.smooth-border-box {
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 18px !important;
    padding: 18px 24px 20px 24px !important;
    margin: 15px 0 25px 0 !important;
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    box-shadow: 0 16px 36px -15px rgba(0, 0, 0, 0.5) !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

fieldset.smooth-border-box:hover {
    border-color: rgba(99, 102, 241, 0.35) !important;
    box-shadow: 0 20px 40px -12px rgba(99, 102, 241, 0.12) !important;
}

/* Legend placed directly on the border line */
legend.smooth-legend {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #e0e7ff !important;
    padding: 2px 14px !important;
    border-radius: 9999px !important;
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
    border: 1px solid rgba(129, 140, 248, 0.35) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    letter-spacing: 0.3px !important;
}

/* Hero Header styling */
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
    letter-spacing: -0.03em;
    line-height: 1.2;
}

.hero-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 0.92rem;
    font-weight: 400;
    margin-bottom: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.badge-dev {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 14px;
    border-radius: 9999px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(129, 140, 248, 0.25);
    color: #c7d2fe;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    backdrop-filter: blur(10px);
}

/* Live Score Header Card */
.live-header-box {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%);
    border: 1px solid rgba(129, 140, 248, 0.25);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;
    backdrop-filter: blur(16px);
}

/* Live Player Pitch Box */
.pitch-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

/* Ball-by-ball pill badges */
.ball-bubble {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 8px;
    margin-bottom: 6px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.ball-dot { background: #334155; color: #cbd5e1; }
.ball-runs { background: #1e3a8a; color: #93c5fd; }
.ball-four { background: #065f46; color: #6ee7b7; border: 1px solid #10b981; }
.ball-six { background: #701a75; color: #f0abfc; border: 1px solid #d946ef; }
.ball-wicket { background: #991b1b; color: #fca5a5; border: 1px solid #ef4444; }

/* Commentary items */
.comm-item {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 0.88rem;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.comm-over {
    font-weight: 800;
    color: #38bdf8;
    min-width: 40px;
}
.comm-text {
    color: #cbd5e1;
}

/* Stat & KPI Cards */
.stat-card {
    background: rgba(255, 255, 255, 0.025);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 16px 10px;
    text-align: center;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}
.stat-val {
    font-size: 1.65rem;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: -0.02em;
}
.stat-lbl {
    font-size: 0.72rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}

/* Prediction Result Cards */
.result-card {
    border-radius: 22px;
    padding: 28px 24px;
    text-align: center;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.3s ease;
}
.result-card:hover {
    transform: translateY(-3px);
}

.chasing-win {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.12) 0%, rgba(5, 150, 105, 0.02) 100%);
    border: 1px solid rgba(52, 211, 153, 0.25);
    box-shadow: 0 20px 40px -15px rgba(16, 185, 129, 0.2), inset 0 1px 0 rgba(52, 211, 153, 0.3);
}

.defending-win {
    background: linear-gradient(145deg, rgba(239, 68, 68, 0.12) 0%, rgba(185, 28, 28, 0.02) 100%);
    border: 1px solid rgba(248, 113, 113, 0.25);
    box-shadow: 0 20px 40px -15px rgba(239, 68, 68, 0.2), inset 0 1px 0 rgba(248, 113, 113, 0.3);
}

.draw-win {
    background: linear-gradient(145deg, rgba(234, 179, 8, 0.12) 0%, rgba(202, 138, 4, 0.02) 100%);
    border: 1px solid rgba(250, 204, 21, 0.25);
    box-shadow: 0 20px 40px -15px rgba(234, 179, 8, 0.2), inset 0 1px 0 rgba(250, 204, 21, 0.3);
}

.res-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.res-number {
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    margin: 14px 0 8px 0;
}

.res-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
}

/* Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    padding: 14px 28px !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    box-shadow: 0 12px 30px -8px rgba(124, 58, 237, 0.45) !important;
    transition: all 0.25s ease !important;
    margin-top: 6px !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 18px 36px -6px rgba(219, 39, 119, 0.55) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

/* Form Controls */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: rgba(15, 23, 42, 0.6) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #f1f5f9 !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover {
    border-color: rgba(99, 102, 241, 0.4) !important;
    background: rgba(15, 23, 42, 0.8) !important;
}

/* Streamlit Tabs */
div[data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    margin-bottom: 20px !important;
}

button[data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    color: #94a3b8 !important;
    padding: 10px 18px !important;
}

button[aria-selected="true"] {
    background: rgba(99, 102, 241, 0.25) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(129, 140, 248, 0.4) !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.custom-footer {
    text-align: center;
    color: #64748b;
    font-size: 0.82rem;
    margin-top: 40px;
    padding-top: 18px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load IPL Machine Learning Model (Cached)
# ---------------------------------------------------------
@st.cache_resource
def load_prediction_model():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'models', 'pipe.pkl'),
        os.path.join(os.path.dirname(__file__), 'pipe.pkl'),
        'models/pipe.pkl',
        'pipe.pkl'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
    return None

pipe = load_prediction_model()

# ---------------------------------------------------------
# Supported Teams & Venues
# ---------------------------------------------------------
ipl_teams = [
    'Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad',
    'Deccan Chargers', 'Delhi Daredevils'
]

ipl_cities = [
    'Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein',
    'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack', 'Delhi',
    'Dharamsala', 'Durban', 'East London', 'Hyderabad', 'Indore', 'Jaipur',
    'Johannesburg', 'Kimberley', 'Kolkata', 'Mohali', 'Mumbai', 'Nagpur',
    'Port Elizabeth', 'Pune', 'Raipur', 'Ranchi', 'Sharjah', 'Visakhapatnam'
]

# Top 20 International Cricket Nations
intl_top20_teams = [
    'India', 'Australia', 'England', 'South Africa', 'New Zealand',
    'Pakistan', 'West Indies', 'Sri Lanka', 'Bangladesh', 'Afghanistan',
    'Ireland', 'Zimbabwe', 'Netherlands', 'Scotland', 'Namibia',
    'USA', 'Nepal', 'UAE', 'Oman', 'Canada'
]

intl_venues = list(ip.VENUES_CONFIG.keys())

# ---------------------------------------------------------
# Global Live Cricket API Fetchers (ESPN Cricinfo Sports API)
# ---------------------------------------------------------
@st.cache_data(ttl=45)
def fetch_global_cricket_matches():
    """Fetch all active and scheduled cricket matches across International and Leagues."""
    url = "https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=cricket"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            sports = data.get('sports', [{}])[0]
            leagues = sports.get('leagues', [])
            all_matches = []
            
            for lg in leagues:
                lg_name = lg.get('name', 'Cricket')
                lg_id = lg.get('id', '')
                for ev in lg.get('events', []):
                    comp = ev.get('competitors', [])
                    status_desc = ev.get('status', {}).get('summary', '') or ev.get('status', {}).get('type', {}).get('description', '')
                    
                    t1_name = comp[0].get('displayName', comp[0].get('name', 'Team 1')) if len(comp) > 0 else 'Team 1'
                    t2_name = comp[1].get('displayName', comp[1].get('name', 'Team 2')) if len(comp) > 1 else 'Team 2'
                    
                    t1_score = comp[0].get('score', '') if len(comp) > 0 else ''
                    t2_score = comp[1].get('score', '') if len(comp) > 1 else ''
                    
                    all_matches.append({
                        'event_id': ev.get('id'),
                        'league_id': lg_id,
                        'league_name': lg_name,
                        'title': ev.get('name', f"{t1_name} v {t2_name}"),
                        't1_name': t1_name,
                        't2_name': t2_name,
                        't1_score': t1_score,
                        't2_score': t2_score,
                        'status': status_desc or ev.get('description', 'Scheduled'),
                        'date': ev.get('date', ''),
                        'location': ev.get('location', 'Stadium')
                    })
            return all_matches
    except Exception:
        return []

@st.cache_data(ttl=30)
def fetch_match_live_detail(league_id, event_id):
    """Fetch in-depth matchcard, batters on pitch, current bowlers, and ball commentary."""
    summary_url = f"https://site.api.espn.com/apis/site/v2/sports/cricket/{league_id}/summary?event={event_id}"
    pbp_url = f"https://site.api.espn.com/apis/site/v2/sports/cricket/{league_id}/playbyplay?event={event_id}"
    
    match_data = {'batting': [], 'bowling': [], 'balls': [], 'game_info': {}}
    
    try:
        req = urllib.request.Request(summary_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            match_data['game_info'] = data.get('gameInfo', {})
            
            for mc in data.get('matchcards', []):
                if mc.get('headline') == 'Batting':
                    match_data['batting'] = mc.get('playerDetails', [])
                elif mc.get('headline') == 'Bowling':
                    match_data['bowling'] = mc.get('playerDetails', [])
    except Exception:
        pass

    try:
        req_pbp = urllib.request.Request(pbp_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_pbp, timeout=5) as resp:
            pbp_data = json.loads(resp.read().decode('utf-8'))
            items = pbp_data.get('commentary', {}).get('items', [])
            match_data['balls'] = items[:15]
    except Exception:
        pass

    return match_data

# ---------------------------------------------------------
# Hero Title & Developer Attribution
# ---------------------------------------------------------
st.markdown("""
<div style="text-align: center; padding-top: 5px;">
    <h1 class="hero-title">🏏 Global Cricket & IPL Prediction Center</h1>
    <div class="hero-subtitle">
        <span>Live Ball-by-Ball Scores • Top 20 International Predictor (ODI, T20I, Test) • IPL ML Engine</span>
        <span>•</span>
        <span class="badge-dev">👨‍💻 Developed by Aditya Kumar</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabbed Navigation: 1. Live Match, 2. International Predictor, 3. IPL Predictor
# ---------------------------------------------------------
tab_live, tab_intl, tab_ipl = st.tabs([
    "🔴 Cricbuzz-Style Live Matches", 
    "🌍 International Predictor (ODI / T20 / Test)", 
    "🔮 IPL Win Predictor"
])

# =========================================================
# TAB 1: LIVE MATCH CENTER (Cricbuzz / ESPN Style)
# =========================================================
with tab_live:
    col_refresh, col_filter = st.columns([1, 3])
    with col_refresh:
        if st.button("🔄 Refresh Live Scores", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    matches = fetch_global_cricket_matches()
    
    if not matches:
        st.info("📡 Checking cricket feeds... Scheduled and live international fixtures will display here.")
    else:
        match_labels = [f"[{m['league_name']}] {m['title']} • {m['status']}" for m in matches]
        selected_idx = st.selectbox("🎯 Select Match to Inspect (Live or Upcoming):", range(len(matches)), format_func=lambda i: match_labels[i])
        cur_match = matches[selected_idx]
        
        st.markdown(f"""
        <div class="live-header-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <span class="badge-dev" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border-color: rgba(56, 189, 248, 0.3);">
                    🏆 {cur_match['league_name']}
                </span>
                <span style="color: #94a3b8; font-size: 0.82rem;">📍 {cur_match['location']}</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; text-align: center; gap: 20px;">
                <div style="text-align: left;">
                    <div style="font-size: 1.35rem; font-weight: 700; color: #f8fafc;">{cur_match['t1_name']}</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #38bdf8;">{cur_match['t1_score'] or 'Yet to Bat'}</div>
                </div>
                <div style="font-weight: 800; font-size: 1.2rem; color: #64748b;">VS</div>
                <div style="text-align: right;">
                    <div style="font-size: 1.35rem; font-weight: 700; color: #f8fafc;">{cur_match['t2_name']}</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #38bdf8;">{cur_match['t2_score'] or 'Yet to Bat'}</div>
                </div>
            </div>
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="color: #fbbf24; font-weight: 600; font-size: 0.92rem;">⚡ {cur_match['status']}</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">🕒 {cur_match['date'][:10]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        detail = fetch_match_live_detail(cur_match['league_id'], cur_match['event_id'])
        c_left, c_right = st.columns([1.2, 1])
        
        with c_left:
            st.markdown("""
            <fieldset class="smooth-border-box" style="margin-top: 0;">
                <legend class="smooth-legend">🏏 Batters on the Pitch</legend>
            """, unsafe_allow_html=True)
            
            if detail['batting']:
                active_batters = [b for b in detail['batting'] if 'not out' in b.get('dismissal', '').lower()][:2]
                if not active_batters:
                    active_batters = detail['batting'][:2]
                    
                for bat in active_batters:
                    st.markdown(f"""
                    <div class="pitch-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-weight: 700; font-size: 1.05rem; color: #f1f5f9;">{bat.get('playerName', 'Batter')}*</span>
                                <span style="color: #10b981; font-size: 0.75rem; margin-left: 8px;">({bat.get('dismissal', 'Batting')})</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="font-size: 1.3rem; font-weight: 800; color: #38bdf8;">{bat.get('runs', '0')}</span>
                                <span style="color: #94a3b8; font-size: 0.85rem;"> ({bat.get('ballsFaced', '0')}b)</span>
                            </div>
                        </div>
                        <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">
                            4s: <strong style="color: #cbd5e1;">{bat.get('fours', '0')}</strong> | 6s: <strong style="color: #cbd5e1;">{bat.get('sixes', '0')}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #94a3b8; font-size: 0.88rem;'>Batting scorecard will display when live innings begins.</p>", unsafe_allow_html=True)
                
            st.markdown("</fieldset>", unsafe_allow_html=True)
            
            st.markdown("""
            <fieldset class="smooth-border-box">
                <legend class="smooth-legend">🎯 Current Bowler</legend>
            """, unsafe_allow_html=True)
            
            if detail['bowling']:
                active_bowler = detail['bowling'][0]
                st.markdown(f"""
                <div class="pitch-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 700; font-size: 1.05rem; color: #f1f5f9;">{active_bowler.get('playerName', 'Bowler')}</span>
                            <span style="color: #f43f5e; font-size: 0.75rem; margin-left: 8px;">(Bowling)</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 1.2rem; font-weight: 800; color: #f43f5e;">{active_bowler.get('wickets', '0')}/{active_bowler.get('conceded', '0')}</span>
                            <span style="color: #94a3b8; font-size: 0.85rem;"> ({active_bowler.get('overs', '0')} ov)</span>
                        </div>
                    </div>
                    <div style="font-size: 0.78rem; color: #64748b; margin-top: 4px;">
                        Econ: <strong style="color: #cbd5e1;">{active_bowler.get('economyRate', '-')}</strong> | Maidens: <strong style="color: #cbd5e1;">{active_bowler.get('maidens', '0')}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #94a3b8; font-size: 0.88rem;'>Bowling scorecard available once live overs commence.</p>", unsafe_allow_html=True)
                
            st.markdown("</fieldset>", unsafe_allow_html=True)

        with c_right:
            st.markdown("""
            <fieldset class="smooth-border-box" style="margin-top: 0;">
                <legend class="smooth-legend">🎙️ Ball-by-Ball Commentary</legend>
            """, unsafe_allow_html=True)
            
            if detail['balls']:
                st.markdown("<div style='margin-bottom: 12px;'>", unsafe_allow_html=True)
                bubble_html = ""
                for ball in detail['balls'][:6]:
                    runs = ball.get('scoreValue', 0)
                    is_wicket = ball.get('dismissal', {}).get('dismissal', False)
                    
                    if is_wicket:
                        bubble_html += '<span class="ball-bubble ball-wicket">W</span>'
                    elif runs == 6:
                        bubble_html += '<span class="ball-bubble ball-six">6</span>'
                    elif runs == 4:
                        bubble_html += '<span class="ball-bubble ball-four">4</span>'
                    elif runs == 0:
                        bubble_html += '<span class="ball-bubble ball-dot">•</span>'
                    else:
                        bubble_html += f'<span class="ball-bubble ball-runs">{runs}</span>'
                st.markdown(bubble_html + "</div>", unsafe_allow_html=True)
                
                for item in detail['balls'][:6]:
                    over_num = item.get('over', {}).get('overs', '')
                    ball_txt = item.get('text', '') or item.get('shortText', '')
                    st.markdown(f"""
                    <div class="comm-item">
                        <span class="comm-over">{over_num}</span>
                        <span class="comm-text">{ball_txt}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #94a3b8; font-size: 0.88rem;'>Live ball-by-ball updates will stream here automatically during live overs.</p>", unsafe_allow_html=True)
                
            st.markdown("</fieldset>", unsafe_allow_html=True)

# =========================================================
# TAB 2: INTERNATIONAL PREDICTOR (ODI, T20I, TEST)
# =========================================================
with tab_intl:
    st.markdown("""
    <fieldset class="smooth-border-box">
        <legend class="smooth-legend">🌍 International Format & Teams</legend>
    """, unsafe_allow_html=True)
    
    col_fmt, col_t1, col_t2, col_ven = st.columns([1, 1, 1, 1.2])
    
    with col_fmt:
        intl_format = st.selectbox("🏆 Match Format", ["T20I", "ODI", "TEST"])
        
    with col_t1:
        team1_intl = st.selectbox(
            "🏏 Chasing / Batting Team" if intl_format != "TEST" else "🏏 Team 1 (Chasing/Batting 4th)",
            intl_top20_teams,
            index=intl_top20_teams.index("India")
        )
        
    with col_t2:
        available_t2 = [t for t in intl_top20_teams if t != team1_intl]
        team2_intl = st.selectbox(
            "🎯 Defending / Bowling Team" if intl_format != "TEST" else "🎯 Team 2 (Bowling 4th)",
            available_t2,
            index=available_t2.index("Australia") if "Australia" in available_t2 else 0
        )
        
    with col_ven:
        intl_venue = st.selectbox("📍 International Stadium / Venue", intl_venues)
        
    st.markdown("</fieldset>", unsafe_allow_html=True)
    
    # Format-Specific Match State Inputs
    if intl_format in ["T20I", "ODI"]:
        total_overs_limit = 20.0 if intl_format == "T20I" else 50.0
        default_target = 180 if intl_format == "T20I" else 280
        default_score = 110 if intl_format == "T20I" else 175
        default_overs = 10.0 if intl_format == "T20I" else 25.0
        
        st.markdown(f"""
        <fieldset class="smooth-border-box">
            <legend class="smooth-legend">⚡ {intl_format} 2nd Innings Live Match State</legend>
        """, unsafe_allow_html=True)
        
        i_col1, i_col2, i_col3, i_col4 = st.columns(4)
        with i_col1:
            target_intl = st.number_input('🎯 Target Score', min_value=1, max_value=500, value=default_target, step=1, key="intl_tgt")
        with i_col2:
            score_intl = st.number_input('🏏 Current Score', min_value=0, max_value=500, value=default_score, step=1, key="intl_scr")
        with i_col3:
            overs_intl = st.number_input(f'⏱️ Overs Bowled (max {int(total_overs_limit)})', min_value=0.0, max_value=total_overs_limit, value=default_overs, step=0.1, key="intl_ovr")
        with i_col4:
            wickets_intl = st.number_input('🔴 Wickets Fallen', min_value=0, max_value=10, value=3, step=1, key="intl_wkt")
            
        st.markdown("</fieldset>", unsafe_allow_html=True)
        
        intl_predict_btn = st.button(f'🔮 Predict {intl_format} Win Probability', use_container_width=True)
        
        if intl_predict_btn:
            full_overs = int(overs_intl)
            fractional_part = round(overs_intl - full_overs, 1)
            balls_in_over = int(round(fractional_part * 10))
            
            if balls_in_over > 5:
                st.warning(f"⚠️ Invalid overs value `{overs_intl}`. An over has at most 5 completed balls after decimal.")
            else:
                balls_bowled = (full_overs * 6) + balls_in_over
                total_balls = int(total_overs_limit * 6)
                
                if score_intl >= target_intl:
                    st.success(f"🎉 **{team1_intl}** has already chased the target and won!")
                elif wickets_intl >= 10:
                    st.error(f"🔴 **{team1_intl}** is all out! **{team2_intl}** has won!")
                elif balls_bowled == 0:
                    st.warning("⚠️ Overs bowled cannot be 0. Enter at least 1 legal ball.")
                elif (total_balls - balls_bowled) <= 0:
                    st.error(f"⏰ Overs finished! **{team2_intl}** won by {target_intl - score_intl} runs!")
                else:
                    res = ip.predict_international_t20_odi(
                        intl_format, team1_intl, team2_intl, intl_venue,
                        target_intl, score_intl, balls_bowled, wickets_intl
                    )
                    
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px;">
                        <div class="stat-card">
                            <div class="stat-val">{res['runs_needed']}</div>
                            <div class="stat-lbl">Runs Needed</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-val">{res['balls_left']}</div>
                            <div class="stat-lbl">Balls Remaining</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-val">{res['crr']}</div>
                            <div class="stat-lbl">Current Run Rate</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-val">{res['rrr']}</div>
                            <div class="stat-lbl">Required Run Rate</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    r1, r2 = st.columns(2)
                    with r1:
                        st.markdown(f"""
                        <div class="result-card chasing-win">
                            <span class="res-tag" style="background: rgba(16, 185, 129, 0.2); color: #6ee7b7;">Chasing Team</span>
                            <div class="res-number" style="color: #34d399;">{res['chasing_win']}%</div>
                            <div class="res-name">{team1_intl}</div>
                            <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 6px;">Win Probability</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with r2:
                        st.markdown(f"""
                        <div class="result-card defending-win">
                            <span class="res-tag" style="background: rgba(239, 68, 68, 0.2); color: #fca5a5;">Defending Team</span>
                            <div class="res-number" style="color: #f87171;">{res['defending_win']}%</div>
                            <div class="res-name">{team2_intl}</div>
                            <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 6px;">Win Probability</p>
                        </div>
                        """, unsafe_allow_html=True)
                    st.progress(res['chasing_win'] / 100.0)

    else:
        # TEST MATCH SIMULATOR
        st.markdown("""
        <fieldset class="smooth-border-box">
            <legend class="smooth-legend">⏳ 5-Day Test Match Situation</legend>
        """, unsafe_allow_html=True)
        
        t_col1, t_col2, t_col3, t_col4 = st.columns(4)
        with t_col1:
            test_day = st.slider("📅 Match Day", min_value=1, max_value=5, value=5)
        with t_col2:
            test_overs_today = st.number_input("⏱️ Overs Remaining Today", min_value=0, max_value=90, value=45)
        with t_col3:
            lead_or_target = st.number_input("🎯 4th Innings Runs Needed / Lead", min_value=1, max_value=600, value=140)
        with t_col4:
            wickets_in_hand_test = st.number_input("🔴 Wickets in Hand for Chasing Team", min_value=1, max_value=10, value=6)
            
        st.markdown("</fieldset>", unsafe_allow_html=True)
        
        test_predict_btn = st.button('🔮 Predict Test Match Outcome', use_container_width=True)
        
        if test_predict_btn:
            res_test = ip.predict_test_match(
                team1_intl, team2_intl, intl_venue,
                test_day, test_overs_today, lead_or_target, wickets_in_hand_test
            )
            
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            col_t_win1, col_t_draw, col_t_win2 = st.columns(3)
            
            with col_t_win1:
                st.markdown(f"""
                <div class="result-card chasing-win">
                    <span class="res-tag" style="background: rgba(16, 185, 129, 0.2); color: #6ee7b7;">Chasing Win</span>
                    <div class="res-number" style="color: #34d399;">{res_test['team1_win']}%</div>
                    <div class="res-name">{team1_intl}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_t_draw:
                st.markdown(f"""
                <div class="result-card draw-win">
                    <span class="res-tag" style="background: rgba(234, 179, 8, 0.2); color: #fde047;">Match Drawn</span>
                    <div class="res-number" style="color: #facc15;">{res_test['draw']}%</div>
                    <div class="res-name">Draw / Tie</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_t_win2:
                st.markdown(f"""
                <div class="result-card defending-win">
                    <span class="res-tag" style="background: rgba(239, 68, 68, 0.2); color: #fca5a5;">Defending Win</span>
                    <div class="res-number" style="color: #f87171;">{res_test['team2_win']}%</div>
                    <div class="res-name">{team2_intl}</div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# TAB 3: IPL WIN PREDICTOR (Machine Learning Model)
# =========================================================
with tab_ipl:
    if pipe is None:
        st.error("❌ **Model file (`models/pipe.pkl`) not found!** Please ensure the trained model is uploaded.")
        st.stop()

    st.markdown("""
    <fieldset class="smooth-border-box">
        <legend class="smooth-legend">🏟️ Match Setup & Teams</legend>
    """, unsafe_allow_html=True)

    col_team1, col_team2, col_venue = st.columns([1, 1, 1])

    with col_team1:
        batting_team = st.selectbox(
            '🏏 Batting Team (Chasing)',
            options=sorted(ipl_teams),
            index=sorted(ipl_teams).index('Mumbai Indians') if 'Mumbai Indians' in ipl_teams else 0,
            key="ipl_bat"
        )

    with col_team2:
        available_bowling_teams = [t for t in sorted(ipl_teams) if t != batting_team]
        bowling_team = st.selectbox(
            '🎯 Bowling Team (Defending)',
            options=available_bowling_teams,
            index=available_bowling_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in available_bowling_teams else 0,
            key="ipl_bowl"
        )

    with col_venue:
        selected_city = st.selectbox(
            '📍 Host City / Venue',
            options=sorted(ipl_cities),
            index=sorted(ipl_cities).index('Mumbai') if 'Mumbai' in ipl_cities else 0,
            key="ipl_city"
        )

    st.markdown("</fieldset>", unsafe_allow_html=True)

    st.markdown("""
    <fieldset class="smooth-border-box">
        <legend class="smooth-legend">⚡ 2nd Innings Live Match State</legend>
    """, unsafe_allow_html=True)

    col_tgt, col_scr, col_ovr, col_wkt = st.columns(4)

    with col_tgt:
        target = st.number_input('🎯 Target Score', min_value=1, max_value=350, value=180, step=1, key="ipl_tgt")

    with col_scr:
        score = st.number_input('🏏 Current Score', min_value=0, max_value=350, value=120, step=1, key="ipl_scr")

    with col_ovr:
        overs = st.number_input('⏱️ Overs Bowled (e.g. 10.2)', min_value=0.0, max_value=20.0, value=10.0, step=0.1, key="ipl_ovr")

    with col_wkt:
        wickets = st.number_input('🔴 Wickets Fallen', min_value=0, max_value=10, value=3, step=1, key="ipl_wkt")

    st.markdown("</fieldset>", unsafe_allow_html=True)

    predict_btn = st.button('🔮 Calculate IPL Win Probability', use_container_width=True)

    if predict_btn:
        full_overs = int(overs)
        fractional_part = round(overs - full_overs, 1)
        balls_in_over = int(round(fractional_part * 10))
        
        if balls_in_over > 5:
            st.warning(f"⚠️ Invalid overs value `{overs}`. An over has at most 5 completed balls after decimal.")
        else:
            total_balls_bowled = (full_overs * 6) + balls_in_over
            balls_left = 120 - total_balls_bowled
            runs_left = target - score
            wickets_in_hand = 10 - wickets
            
            if score >= target:
                st.success(f"🎉 **{batting_team}** has already chased down the target and won the match!")
            elif wickets >= 10:
                st.error(f"🔴 **{batting_team}** is all out! **{bowling_team}** has won the match!")
            elif total_balls_bowled == 0:
                st.warning("⚠️ Overs bowled cannot be 0 when calculating dynamic chase run rates. Enter at least 1 legal ball.")
            elif balls_left <= 0:
                if runs_left > 0:
                    st.error(f"⏰ Innings finished (20 overs completed)! **{bowling_team}** won by {runs_left} runs!")
                else:
                    st.info("🤝 Match tied!")
            else:
                effective_overs = total_balls_bowled / 6.0
                crr = score / effective_overs
                rrr = (runs_left * 6.0) / balls_left

                input_df = pd.DataFrame({
                    'batting_team': [batting_team],
                    'bowling_team': [bowling_team],
                    'city': [selected_city],
                    'runs_left': [runs_left],
                    'balls_left': [balls_left],
                    'wickets': [wickets_in_hand],
                    'total_runs_x': [target],
                    'crr': [crr],
                    'rrr': [rrr]
                })

                with st.spinner("Analyzing match state with ML pipeline..."):
                    result = pipe.predict_proba(input_df)
                    loss_prob = result[0][0]
                    win_prob = result[0][1]
                    
                    win_pct = round(win_prob * 100, 1)
                    loss_pct = round(loss_prob * 100, 1)

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px;">
                    <div class="stat-card">
                        <div class="stat-val">{runs_left}</div>
                        <div class="stat-lbl">Runs Needed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-val">{balls_left}</div>
                        <div class="stat-lbl">Balls Left</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-val">{crr:.2f}</div>
                        <div class="stat-lbl">Current Run Rate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-val">{rrr:.2f}</div>
                        <div class="stat-lbl">Required Run Rate</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2 = st.columns(2)

                with c1:
                    st.markdown(f"""
                    <div class="result-card chasing-win">
                        <span class="res-tag" style="background: rgba(16, 185, 129, 0.2); color: #6ee7b7;">Chasing Team</span>
                        <div class="res-number" style="color: #34d399;">{win_pct}%</div>
                        <div class="res-name">{batting_team}</div>
                        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 6px;">Win Probability</p>
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown(f"""
                    <div class="result-card defending-win">
                        <span class="res-tag" style="background: rgba(239, 68, 68, 0.2); color: #fca5a5;">Defending Team</span>
                        <div class="res-number" style="color: #f87171;">{loss_pct}%</div>
                        <div class="res-name">{bowling_team}</div>
                        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 6px;">Win Probability</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                st.progress(win_prob)

# ---------------------------------------------------------
# Clean Footer
# ---------------------------------------------------------
st.markdown("""
<div class="custom-footer">
    Global Cricket & IPL Match Center • Top 20 International & Franchise Predictions<br>
    Crafted by <strong>Aditya Kumar</strong>
</div>
""", unsafe_allow_html=True)