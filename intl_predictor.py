import math

# ICC Men's Cricket World Rankings & Elo Baseline Ratings
ICC_RATINGS = {
    'T20I': {
        'India': 268, 'Australia': 256, 'England': 253, 'South Africa': 250,
        'West Indies': 248, 'New Zealand': 247, 'Pakistan': 241, 'Sri Lanka': 232,
        'Bangladesh': 224, 'Afghanistan': 222, 'Ireland': 195, 'Zimbabwe': 190,
        'Netherlands': 185, 'Scotland': 184, 'Namibia': 178, 'USA': 175,
        'Nepal': 170, 'UAE': 165, 'Oman': 158, 'Canada': 150
    },
    'ODI': {
        'India': 122, 'Australia': 118, 'South Africa': 112, 'Pakistan': 108,
        'New Zealand': 105, 'England': 102, 'Sri Lanka': 98, 'Bangladesh': 91,
        'Afghanistan': 88, 'West Indies': 84, 'Ireland': 68, 'Zimbabwe': 60,
        'Scotland': 58, 'Netherlands': 55, 'Namibia': 48, 'USA': 42,
        'Nepal': 40, 'Canada': 36, 'UAE': 34, 'Oman': 30
    },
    'TEST': {
        'India': 120, 'Australia': 124, 'England': 108, 'South Africa': 104,
        'New Zealand': 98, 'Pakistan': 86, 'Sri Lanka': 84, 'West Indies': 76,
        'Bangladesh': 66, 'Zimbabwe': 35, 'Ireland': 28, 'Afghanistan': 30
    }
}

# Major International Venues & Home Advantage Profiles
VENUES_CONFIG = {
    'Wankhede Stadium, Mumbai': {'country': 'India', 'pitch': 'Batting Friendly', 'par_t20': 185, 'par_odi': 295},
    'Eden Gardens, Kolkata': {'country': 'India', 'pitch': 'Balanced / Spin', 'par_t20': 180, 'par_odi': 280},
    'Narendra Modi Stadium, Ahmedabad': {'country': 'India', 'pitch': 'Balanced', 'par_t20': 178, 'par_odi': 275},
    'Melbourne Cricket Ground (MCG), Melbourne': {'country': 'Australia', 'pitch': 'Pace & Bounce', 'par_t20': 170, 'par_odi': 270},
    'Sydney Cricket Ground (SCG), Sydney': {'country': 'Australia', 'pitch': 'Spin & Batting', 'par_t20': 175, 'par_odi': 280},
    "Lord's Cricket Ground, London": {'country': 'England', 'pitch': 'Swing & Seam', 'par_t20': 168, 'par_odi': 260},
    'The Oval, London': {'country': 'England', 'pitch': 'True Bounce & Batting', 'par_t20': 180, 'par_odi': 285},
    'Newlands, Cape Town': {'country': 'South Africa', 'pitch': 'Seam & Bounce', 'par_t20': 165, 'par_odi': 255},
    'SuperSport Park, Centurion': {'country': 'South Africa', 'pitch': 'High Altitude & Pace', 'par_t20': 185, 'par_odi': 290},
    'Eden Park, Auckland': {'country': 'New Zealand', 'pitch': 'Short Boundaries', 'par_t20': 182, 'par_odi': 280},
    'Gaddafi Stadium, Lahore': {'country': 'Pakistan', 'pitch': 'Flat / High Scoring', 'par_t20': 185, 'par_odi': 300},
    'R. Premadasa Stadium, Colombo': {'country': 'Sri Lanka', 'pitch': 'Spin Friendly', 'par_t20': 160, 'par_odi': 250},
    'Kensington Oval, Bridgetown, Barbados': {'country': 'West Indies', 'pitch': 'Balanced', 'par_t20': 165, 'par_odi': 265},
    'Sher-e-Bangla National Stadium, Mirpur': {'country': 'Bangladesh', 'pitch': 'Slow & Turning', 'par_t20': 148, 'par_odi': 240},
    'Dubai International Cricket Stadium': {'country': 'UAE (Neutral)', 'pitch': 'Chasing Advantage', 'par_t20': 168, 'par_odi': 260},
    'Sharjah Cricket Stadium': {'country': 'UAE (Neutral)', 'pitch': 'Short & Spin', 'par_t20': 172, 'par_odi': 265}
}

def sigmoid(x):
    return 1 / (1 + math.exp(-max(min(x, 15), -15)))

def predict_international_t20_odi(format_type, team1, team2, venue, target, current_score, balls_bowled, wickets_fallen):
    """
    High-accuracy Bayesian/Logit probability model for T20I and ODI chases.
    Incorporates:
    - Team ICC strength difference
    - Home ground advantage
    - Current vs Required Run Rate differential
    - Non-linear resource decay based on wickets in hand
    - Balls remaining pressure
    """
    total_balls = 120 if format_type == 'T20I' else 300
    balls_left = total_balls - balls_bowled
    runs_needed = target - current_score
    wickets_in_hand = 10 - wickets_fallen
    
    # 1. Rating baseline
    ratings = ICC_RATINGS.get(format_type, ICC_RATINGS['T20I'])
    r1 = ratings.get(team1, 200 if format_type == 'T20I' else 80)
    r2 = ratings.get(team2, 200 if format_type == 'T20I' else 80)
    rating_diff = r1 - r2
    
    # Format-calibrated rating scale factor
    scale_factor = 25.0 if format_type == 'T20I' else 18.0
    baseline_logit = (rating_diff / scale_factor)
    
    # 2. Home Ground Advantage
    venue_info = VENUES_CONFIG.get(venue, {'country': 'Neutral'})
    if venue_info['country'] == team1:
        baseline_logit += 0.25
    elif venue_info['country'] == team2:
        baseline_logit -= 0.25

    # 3. Dynamic match match-state pressure
    effective_overs_bowled = max(balls_bowled / 6.0, 0.1)
    crr = current_score / effective_overs_bowled
    rrr = (runs_needed * 6.0) / max(balls_left, 1)
    
    # Rate difference (Positive means batting comfortably above RRR)
    rate_diff = crr - rrr
    
    # Wicket penalty exponential weight (as wickets fall, each wicket hurts harder)
    # Wickets in hand exponent (Duckworth-Lewis resource inspired)
    resource_pct = (wickets_in_hand / 10.0) ** 1.35 * (balls_left / float(total_balls)) ** 0.85
    
    # Pressure coefficient
    run_pressure = (runs_needed / max(balls_left, 1))
    pressure_logit = (rate_diff * 0.45) + (wickets_in_hand * 0.42) - (run_pressure * 2.2)
    
    # Combined log-odds
    final_logit = (0.28 * baseline_logit) + (0.72 * pressure_logit)
    
    # Bound into calibrated probability
    chasing_win_prob = sigmoid(final_logit)
    defending_win_prob = 1.0 - chasing_win_prob
    
    return {
        'chasing_win': round(chasing_win_prob * 100, 1),
        'defending_win': round(defending_win_prob * 100, 1),
        'crr': round(crr, 2),
        'rrr': round(rrr, 2),
        'runs_needed': runs_needed,
        'balls_left': balls_left,
        'wickets_in_hand': wickets_in_hand,
        'resource_pct': round(resource_pct * 100, 1)
    }

def predict_test_match(team1, team2, venue, day, overs_left_today, lead_or_target, wickets_in_hand_4th):
    """
    Multinomial outcome model (Team 1 Win, Team 2 Win, Draw) for 5-Day Test Matches.
    """
    ratings = ICC_RATINGS.get('TEST', {})
    r1 = ratings.get(team1, 90)
    r2 = ratings.get(team2, 90)
    diff = r1 - r2
    
    # Estimate total overs remaining in the Test
    days_left = max(5 - day, 0)
    total_overs_remaining = (days_left * 90) + overs_left_today
    
    if day >= 4 and lead_or_target > 0:
        # 4th innings run chase scenario
        rrr = (lead_or_target / max(total_overs_remaining, 1))
        # Likelihood of chasing target
        chase_ability = (diff * 0.02) + (wickets_in_hand_4th * 0.4) - (lead_or_target / 55.0)
        t1_win = sigmoid(chase_ability) * 0.88
        
        # Draw probability depends on surviving overs
        draw_prob = (1.0 - t1_win) * min(total_overs_remaining / 140.0, 0.65) * (wickets_in_hand_4th / 10.0)
        t2_win = max(1.0 - t1_win - draw_prob, 0.02)
    else:
        # General match position
        advantage = (diff * 0.03) + (lead_or_target / 120.0)
        t1_win = sigmoid(advantage) * (1.0 - (total_overs_remaining / 450.0) * 0.45)
        draw_prob = max((total_overs_remaining / 450.0) * 0.4, 0.05)
        t2_win = max(1.0 - t1_win - draw_prob, 0.05)
        
    tot = t1_win + t2_win + draw_prob
    return {
        'team1_win': round((t1_win / tot) * 100, 1),
        'team2_win': round((t2_win / tot) * 100, 1),
        'draw': round((draw_prob / tot) * 100, 1),
        'overs_remaining': total_overs_remaining
    }
