import streamlit as st
import pickle
import pandas as pd
import os

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="IPL Victory Predictor | Aditya Kumar",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Glassmorphic Custom Styling & Animation
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background Gradient with animated mesh vibe */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(26, 36, 63, 0.95), rgba(10, 15, 30, 0.98)),
                linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #030712 100%);
    background-attachment: fixed;
    color: #f1f5f9;
}

/* Glassmorphism Card Container */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    padding: 24px;
    margin-bottom: 24px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Header Glow Banner */
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #f43f5e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 25px;
}

.badge-dev {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.4);
    color: #c7d2fe;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Metrics and Chips */
.metric-box {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 14px;
    text-align: center;
}
.metric-box .val {
    font-size: 1.5rem;
    font-weight: 700;
    color: #38bdf8;
}
.metric-box .lbl {
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* Result Cards */
.result-card {
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}

.result-batting {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
    border: 1px solid rgba(34, 197, 94, 0.35);
    box-shadow: 0 8px 30px rgba(34, 197, 94, 0.2);
}

.result-bowling {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.05) 100%);
    border: 1px solid rgba(239, 68, 68, 0.35);
    box-shadow: 0 8px 30px rgba(239, 68, 68, 0.2);
}

.result-pct {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 10px 0;
}

.result-team {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.footer-text {
    text-align: center;
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}

/* Custom button styling */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    color: #ffffff;
    border: none;
    padding: 14px 28px;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 14px;
    width: 100%;
    cursor: pointer;
    box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.5);
    transition: all 0.3s ease;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px -5px rgba(236, 72, 153, 0.6);
    color: #ffffff;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
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

cities = [
    'Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein',
    'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack', 'Delhi',
    'Dharamsala', 'Durban', 'East London', 'Hyderabad', 'Indore', 'Jaipur',
    'Johannesburg', 'Kimberley', 'Kolkata', 'Mohali', 'Mumbai', 'Nagpur',
    'Port Elizabeth', 'Pune', 'Raipur', 'Ranchi', 'Sharjah', 'Visakhapatnam'
]

# ---------------------------------------------------------
# Sidebar - Developer Profile & Match Insights
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="font-size: 3rem;">⚡</div>
            <h2 style="margin: 0; color: #f8fafc; font-weight: 700;">IPL Win Predictor</h2>
            <p style="color: #94a3b8; font-size: 0.85rem;">Powered by Machine Learning</p>
            <span class="badge-dev">👨‍💻 Developed by Aditya Kumar</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 About the Model")
    st.info(
        "This application uses an **ensemble ColumnTransformer & Logistic Regression pipeline** "
        "trained on historical IPL ball-by-ball encounter records to estimate real-time chasing win probability."
    )
    
    st.markdown("### 🎯 Live Match Factors")
    st.markdown("""
    - **Current Run Rate (CRR)**
    - **Required Run Rate (RRR)**
    - **Wickets in Hand**
    - **Balls Remaining in Chase**
    - **Host Venue & Team Matchups**
    """)
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>"
        "© 2025-2026 Aditya Kumar<br>All Rights Reserved"
        "</div>", 
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
st.markdown("""
    <div style="text-align: center; margin-top: -15px; margin-bottom: 25px;">
        <h1 class="hero-title">🏏 IPL Match Win Probability Predictor</h1>
        <p class="hero-subtitle">
            Accurate in-game win predictions for 2nd innings run chases • 
            <span class="badge-dev">Crafted by Aditya Kumar</span>
        </p>
    </div>
""", unsafe_allow_html=True)

if pipe is None:
    st.error("❌ **Model file (`models/pipe.pkl`) not found!** Please ensure the trained model is uploaded.")
    st.stop()

# ---------------------------------------------------------
# Form Inputs: Match Setup
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 🏟️ Match Setup & Teams")

col_team1, col_team2, col_venue = st.columns([1, 1, 1])

with col_team1:
    batting_team = st.selectbox(
        '🏏 Batting Team (Chasing)',
        options=sorted(teams),
        index=sorted(teams).index('Mumbai Indians') if 'Mumbai Indians' in teams else 0,
        help="Select the team currently batting in the 2nd innings"
    )

with col_team2:
    # Filter out batting team to avoid accidental same-team selection
    available_bowling_teams = [t for t in sorted(teams) if t != batting_team]
    bowling_team = st.selectbox(
        '🎯 Bowling Team (Defending)',
        options=available_bowling_teams,
        index=available_bowling_teams.index('Chennai Super Kings') if 'Chennai Super Kings' in available_bowling_teams else 0,
        help="Select the team currently bowling/defending the target"
    )

with col_venue:
    selected_city = st.selectbox(
        '📍 Host City / Venue',
        options=sorted(cities),
        index=sorted(cities).index('Mumbai') if 'Mumbai' in cities else 0,
        help="Host city where the match is taking place"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Match Dynamics & Live Score
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### ⚡ 2nd Innings Live Match State")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    target = st.number_input(
        '🎯 Target Score (1st Innings Runs + 1)',
        min_value=1,
        max_value=350,
        value=180,
        step=1,
        help="Total runs the chasing team needs to reach for victory"
    )

with row1_col2:
    score = st.number_input(
        '🏏 Current Chasing Score',
        min_value=0,
        max_value=350,
        value=95,
        step=1,
        help="Runs scored so far in the 2nd innings"
    )

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    overs = st.number_input(
        '⏱️ Overs Completed (e.g. 10.2)',
        min_value=0.0,
        max_value=20.0,
        value=10.0,
        step=0.1,
        help="Overs bowled so far (valid balls: .0, .1, .2, .3, .4, .5)"
    )

with row2_col2:
    wickets = st.number_input(
        '🔴 Wickets Fallen',
        min_value=0,
        max_value=10,
        value=2,
        step=1,
        help="Total wickets lost by the chasing team"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Validation & Prediction Execution
# ---------------------------------------------------------
predict_btn = st.button('🔮 Calculate Win Probability', use_container_width=True)

if predict_btn:
    # Validate ball fractions in overs input (e.g., 10.6 is invalid, should be 11.0)
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
        
        # Immediate game termination checks
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
            # Safe calculation of Run Rates
            effective_overs = total_balls_bowled / 6.0
            crr = score / effective_overs
            rrr = (runs_left * 6.0) / balls_left

            # Prepare Data for Pipeline
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

            with st.spinner("Analyzing match dynamics with ML model..."):
                result = pipe.predict_proba(input_df)
                loss_prob = result[0][0]  # Bowling team win probability
                win_prob = result[0][1]   # Batting team win probability
                
                win_pct = round(win_prob * 100, 1)
                loss_pct = round(loss_prob * 100, 1)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Live Metrics Strip
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
                <div class="metric-box">
                    <div class="val">{runs_left}</div>
                    <div class="lbl">Runs Needed</div>
                </div>
                <div class="metric-box">
                    <div class="val">{balls_left}</div>
                    <div class="lbl">Balls Remaining</div>
                </div>
                <div class="metric-box">
                    <div class="val">{crr:.2f}</div>
                    <div class="lbl">Current Run Rate</div>
                </div>
                <div class="metric-box">
                    <div class="val">{rrr:.2f}</div>
                    <div class="lbl">Req. Run Rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Glassmorphism Result Displays
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.markdown(f"""
                <div class="result-card result-batting">
                    <div class="badge-dev" style="background: rgba(34, 197, 94, 0.2); border-color: rgba(34, 197, 94, 0.5); color: #86efac;">
                        CHASING TEAM
                    </div>
                    <div class="result-pct" style="color: #4ade80;">{win_pct}%</div>
                    <div class="result-team" style="color: #f0fdf4;">{batting_team}</div>
                    <p style="color: #86efac; font-size: 0.85rem; margin-top: 8px;">Estimated Win Probability</p>
                </div>
                """, unsafe_allow_html=True)

            with res_col2:
                st.markdown(f"""
                <div class="result-card result-bowling">
                    <div class="badge-dev" style="background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.5); color: #fca5a5;">
                        DEFENDING TEAM
                    </div>
                    <div class="result-pct" style="color: #f87171;">{loss_pct}%</div>
                    <div class="result-team" style="color: #fef2f2;">{bowling_team}</div>
                    <p style="color: #fca5a5; font-size: 0.85rem; margin-top: 8px;">Estimated Win Probability</p>
                </div>
                """, unsafe_allow_html=True)

            # Animated Progress Bar
            st.markdown("<br>", unsafe_allow_html=True)
            st.progress(win_prob)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("""
<div class="footer-text">
    IPL Win Predictor Web App • Engineered with Machine Learning & Streamlit<br>
    <strong>Designed & Developed by Aditya Kumar</strong> • Ready for Streamlit Cloud Deployment
</div>
""", unsafe_allow_html=True)