import streamlit as st
import pickle
import pandas as pd
import os
import urllib.request
import json

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="IPL Victory Predictor | Aditya Kumar",
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
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 1100px !important;
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

/* Live Score card badge */
.live-feed-banner {
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 14px;
    padding: 12px 18px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
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
    font-size: 3.8rem;
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
# Load Machine Learning Model (Cached)
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
# Supported Teams & Match Venues
# ---------------------------------------------------------
teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Kings XI Punjab',
    'Kolkata Knight Riders',
    'Mumbai Indians',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad',
    'Deccan Chargers',
    'Delhi Daredevils'
]

# Aliases mapping from ESPN / Cricbuzz naming to model training labels
TEAM_ALIAS_MAP = {
    'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
    'RCB': 'Royal Challengers Bangalore',
    'CSK': 'Chennai Super Kings',
    'MI': 'Mumbai Indians',
    'KKR': 'Kolkata Knight Riders',
    'SRH': 'Sunrisers Hyderabad',
    'RR': 'Rajasthan Royals',
    'DC': 'Delhi Capitals',
    'PBKS': 'Kings XI Punjab',
    'Punjab Kings': 'Kings XI Punjab',
}

cities = [
    'Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein',
    'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack', 'Delhi',
    'Dharamsala', 'Durban', 'East London', 'Hyderabad', 'Indore', 'Jaipur',
    'Johannesburg', 'Kimberley', 'Kolkata', 'Mohali', 'Mumbai', 'Nagpur',
    'Port Elizabeth', 'Pune', 'Raipur', 'Ranchi', 'Sharjah', 'Visakhapatnam'
]

# ---------------------------------------------------------
# Live ESPN / Cricinfo Cricket API Fetcher
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def fetch_espn_live_matches():
    """Fetch live or recent IPL scorecards from ESPN Cricinfo Sports API."""
    url = "https://site.api.espn.com/apis/site/v2/sports/cricket/8048/scoreboard"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            events = data.get('events', [])
            parsed_matches = []
            
            for ev in events:
                comp = ev.get('competitions', [{}])[0]
                competitors = comp.get('competitors', [])
                venue_data = comp.get('venue', {})
                venue_city = venue_data.get('address', {}).get('city', 'Mumbai')
                status_desc = comp.get('status', {}).get('summary', '') or ev.get('status', {}).get('type', {}).get('description', '')
                
                if len(competitors) >= 2:
                    team1_info = competitors[0].get('team', {})
                    team2_info = competitors[1].get('team', {})
                    
                    t1_name = team1_info.get('displayName', '')
                    t2_name = team2_info.get('displayName', '')
                    
                    # Normalize names
                    t1_norm = TEAM_ALIAS_MAP.get(t1_name, t1_name)
                    t2_norm = TEAM_ALIAS_MAP.get(t2_name, t2_name)
                    
                    # Check innings linescores
                    lines1 = competitors[0].get('linescores', [])
                    lines2 = competitors[1].get('linescores', [])
                    
                    # Default parsing
                    target_val = 180
                    score_val = 120
                    overs_val = 10.0
                    wickets_val = 3
                    batting_team = t2_norm if t2_norm in teams else teams[0]
                    bowling_team = t1_norm if t1_norm in teams else teams[1]
                    
                    # Look for 2nd innings
                    for line in lines1:
                        if line.get('period') == 1 and line.get('runs', 0) > 0:
                            target_val = int(line.get('runs')) + 1
                    for line in lines2:
                        if line.get('period') == 2 and line.get('runs', 0) > 0:
                            score_val = int(line.get('runs'))
                            overs_val = float(line.get('overs', 10.0))
                            wickets_val = int(line.get('wickets', 3))
                            batting_team = t2_norm
                            bowling_team = t1_norm
                            
                    parsed_matches.append({
                        'title': ev.get('name', f"{t1_name} vs {t2_name}"),
                        'short_name': ev.get('shortName', 'IPL Match'),
                        'status': status_desc,
                        'venue_city': venue_city if venue_city in cities else 'Ahmedabad',
                        'batting_team': batting_team if batting_team in teams else teams[0],
                        'bowling_team': bowling_team if bowling_team in teams else teams[1],
                        'target': target_val,
                        'score': score_val,
                        'overs': overs_val,
                        'wickets': wickets_val
                    })
            return parsed_matches
    except Exception:
        return []

# ---------------------------------------------------------
# Hero Title & Developer Attribution
# ---------------------------------------------------------
st.markdown("""
<div style="text-align: center; padding-top: 10px;">
    <h1 class="hero-title">🏏 IPL Match Win Predictor</h1>
    <div class="hero-subtitle">
        <span>Real-time chase probability engine</span>
        <span>•</span>
        <span class="badge-dev">👨‍💻 Developed by Aditya Kumar</span>
    </div>
</div>
""", unsafe_allow_html=True)

if pipe is None:
    st.error("❌ **Model file (`models/pipe.pkl`) not found!** Please ensure the trained model is uploaded.")
    st.stop()

# ---------------------------------------------------------
# Live Score API Integration (ESPN / Cricinfo)
# ---------------------------------------------------------
live_matches = fetch_espn_live_matches()

# Initialize session state for inputs if not present
if "batting_team_val" not in st.session_state:
    st.session_state.batting_team_val = 'Mumbai Indians'
if "bowling_team_val" not in st.session_state:
    st.session_state.bowling_team_val = 'Chennai Super Kings'
if "venue_val" not in st.session_state:
    st.session_state.venue_val = 'Mumbai'
if "target_val" not in st.session_state:
    st.session_state.target_val = 180
if "score_val" not in st.session_state:
    st.session_state.score_val = 120
if "overs_val" not in st.session_state:
    st.session_state.overs_val = 10.0
if "wickets_val" not in st.session_state:
    st.session_state.wickets_val = 3

with st.expander("📡 Live Match Score Fetcher (ESPN Sports API)", expanded=False):
    if live_matches:
        match_options = [f"{m['title']} ({m['status']})" for m in live_matches]
        sel_match_idx = st.selectbox(
            "Select active / recent IPL match to auto-fill state:",
            range(len(match_options)),
            format_func=lambda x: match_options[x]
        )
        if st.button("⚡ Sync Live Match Data to Predictor"):
            selected_match = live_matches[sel_match_idx]
            st.session_state.batting_team_val = selected_match['batting_team']
            st.session_state.bowling_team_val = selected_match['bowling_team']
            st.session_state.venue_val = selected_match['venue_city']
            st.session_state.target_val = selected_match['target']
            st.session_state.score_val = selected_match['score']
            st.session_state.overs_val = selected_match['overs']
            st.session_state.wickets_val = selected_match['wickets']
            st.toast(f"✅ Loaded live match state: {selected_match['title']}")
            st.rerun()
    else:
        st.info("ℹ️ No active live IPL match right now. Live matches will appear here automatically on game days via ESPN Cricinfo API.")

# ---------------------------------------------------------
# Match Setup & Teams (Smooth Border Line with Integrated Legend)
# ---------------------------------------------------------
st.markdown("""
<fieldset class="smooth-border-box">
    <legend class="smooth-legend">🏟️ Match Setup & Teams</legend>
""", unsafe_allow_html=True)

col_team1, col_team2, col_venue = st.columns([1, 1, 1])

# Safe index retrieval
bat_idx = sorted(teams).index(st.session_state.batting_team_val) if st.session_state.batting_team_val in teams else 0
with col_team1:
    batting_team = st.selectbox(
        '🏏 Batting Team (Chasing)',
        options=sorted(teams),
        index=bat_idx,
        key="bat_select"
    )

available_bowling_teams = [t for t in sorted(teams) if t != batting_team]
bowl_default = st.session_state.bowling_team_val if st.session_state.bowling_team_val in available_bowling_teams else available_bowling_teams[0]
bowl_idx = available_bowling_teams.index(bowl_default)

with col_team2:
    bowling_team = st.selectbox(
        '🎯 Bowling Team (Defending)',
        options=available_bowling_teams,
        index=bowl_idx,
        key="bowl_select"
    )

city_idx = sorted(cities).index(st.session_state.venue_val) if st.session_state.venue_val in cities else 0
with col_venue:
    selected_city = st.selectbox(
        '📍 Host City / Venue',
        options=sorted(cities),
        index=city_idx,
        key="city_select"
    )

st.markdown("</fieldset>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2nd Innings Live Match State (Smooth Border Line with Integrated Legend)
# ---------------------------------------------------------
st.markdown("""
<fieldset class="smooth-border-box">
    <legend class="smooth-legend">⚡ 2nd Innings Live Match State</legend>
""", unsafe_allow_html=True)

col_tgt, col_scr, col_ovr, col_wkt = st.columns(4)

with col_tgt:
    target = st.number_input(
        '🎯 Target Score',
        min_value=1,
        max_value=350,
        value=int(st.session_state.target_val),
        step=1,
        key="tgt_input"
    )

with col_scr:
    score = st.number_input(
        '🏏 Current Score',
        min_value=0,
        max_value=350,
        value=int(st.session_state.score_val),
        step=1,
        key="scr_input"
    )

with col_ovr:
    overs = st.number_input(
        '⏱️ Overs Bowled (e.g. 10.2)',
        min_value=0.0,
        max_value=20.0,
        value=float(st.session_state.overs_val),
        step=0.1,
        key="ovr_input"
    )

with col_wkt:
    wickets = st.number_input(
        '🔴 Wickets Fallen',
        min_value=0,
        max_value=10,
        value=int(st.session_state.wickets_val),
        step=1,
        key="wkt_input"
    )

st.markdown("</fieldset>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Prediction Button & Results
# ---------------------------------------------------------
predict_btn = st.button('🔮 Calculate Win Probability', use_container_width=True)

if predict_btn:
    full_overs = int(overs)
    fractional_part = round(overs - full_overs, 1)
    balls_in_over = int(round(fractional_part * 10))
    
    if balls_in_over > 5:
        st.warning(f"⚠️ Invalid overs value `{overs}`. An over has at most 5 completed balls after decimal (e.g., `{full_overs}.5`).")
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
            st.warning("⚠️ Overs bowled cannot be 0 when calculating dynamic chase run rates. Enter at least 1 legal ball (e.g. 0.1).")
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
            
            # Match Status Grid
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

            # Results Cards
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
    IPL Match Prediction Engine • Powered by Machine Learning<br>
    Crafted by <strong>Aditya Kumar</strong>
</div>
""", unsafe_allow_html=True)