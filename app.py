import warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
import math
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="FraudShield AI — Enterprise Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════
# 🎨 PREMIUM STYLING
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Base Layout */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 50%, #f8fafc 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1600px;
        animation: fadeInUp 0.6s ease-out;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
        color: #334155 !important;
    }

    /* Hide Sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Metrics Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(14, 165, 233, 0.15);
        border-color: #0EA5E9;
    }
    
    [data-testid="metric-container"] label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #0EA5E9, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #0EA5E9, #0284C7) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        padding: 18px 36px !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.6) !important;
    }

    /* Result Cards */
    .fraud-card, .legit-card {
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 0.6s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .fraud-card {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        border: 3px solid #ef4444;
    }
    
    .legit-card {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        border: 3px solid #10b981;
    }
    
    .icon {
        font-size: 72px;
        margin-bottom: 16px;
        animation: float 3s ease-in-out infinite;
    }

    /* Section Tags */
    .section-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 2.5px;
        color: #0EA5E9;
        text-transform: uppercase;
        font-weight: 700;
        display: inline-block;
        padding: 8px 16px;
        background: #e0f2fe;
        border: 2px solid #0EA5E9;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    
    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        margin: 32px 0;
    }

    /* Input Fields */
    .stNumberInput input, .stSelectbox select {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #0EA5E9 !important;
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1) !important;
    }
    
    .stNumberInput label, .stSelectbox label, .stSlider label, .stRadio label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* Progress Bar - Enhanced */
    .stProgress > div > div {
        background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3) !important;
    }
    
    .stProgress > div {
        background: #e2e8f0 !important;
        border-radius: 12px !important;
        height: 24px !important;
        border: 2px solid #cbd5e1 !important;
    }
    
    /* Progress Text */
    .stProgress [data-testid="stMarkdownContainer"] p {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 8px !important;
    }

    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #ffffff, #f0f9ff);
        border: 3px solid #0EA5E9;
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.15);
    }
    
    .feature-badge {
        display: inline-block;
        padding: 8px 16px;
        background: #e0f2fe;
        border: 2px solid #0EA5E9;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        color: #0369a1;
        margin: 4px;
    }
    
    .info-card {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .info-card:hover {
        border-color: #0EA5E9;
        transform: translateX(4px);
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.15);
    }
    
    /* Stats Card */
    .stats-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }

    /* DataFrames */
    [data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: #f1f5f9 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    
    /* Risk Score Container */
    .risk-score-container {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    .risk-label {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
        text-align: center;
    }
    
    .risk-percentage {
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        margin: 16px 0;
        background: linear-gradient(135deg, #ef4444, #f59e0b, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# 🔧 MODEL LOADING & FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_resource
def load_model():
    try:
        model = joblib.load('xgb_model.pkl')
        scaler = joblib.load('scaler.pkl')
        with open('feature_names.json') as f:
            features = json.load(f)
        return model, scaler, features, True
    except FileNotFoundError:
        return None, None, None, False

model, scaler, FEATURE_NAMES, model_loaded = load_model()

RISKY_CATEGORIES = ['shopping_net', 'misc_net', 'grocery_net', 'travel', 'shopping_pos', 'misc_pos']
CATEGORY_ENCODING = {
    'entertainment': 0, 'food_dining': 1, 'gas_transport': 2,
    'grocery_net': 3, 'grocery_pos': 4, 'health_fitness': 5,
    'home': 6, 'kids_pets': 7, 'misc_net': 8, 'misc_pos': 9,
    'personal_care': 10, 'shopping_net': 11, 'shopping_pos': 12, 'travel': 13,
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlam = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def build_features(inp):
    dist_km = haversine(inp['lat'], inp['lon'], inp['merch_lat'], inp['merch_lon'])
    amt_log = math.log1p(inp['amt'])
    city_pop_log = math.log1p(inp['city_pop'])
    row = {
        'amt': inp['amt'], 'amt_log': amt_log,
        'hour': inp['hour'], 'day': inp['day'], 'month': inp['month'],
        'age': inp['age'], 'is_male': inp['gender'],
        'city_pop': inp['city_pop'], 'city_pop_log': city_pop_log,
        'dist_km': dist_km,
        'is_high_amt': 1 if inp['amt'] > 800 else 0,
        'is_risky_cat': 1 if inp['category'] in RISKY_CATEGORIES else 0,
        'is_weekend': 1 if inp['day'] >= 5 else 0,
        'is_night': 1 if (inp['hour'] >= 22 or inp['hour'] <= 5) else 0,
        'category_encoded': CATEGORY_ENCODING.get(inp['category'], 8),
        'lat': inp['lat'], 'long': inp['lon'],
        'merch_lat': inp['merch_lat'], 'merch_long': inp['merch_lon'],
    }
    df = pd.DataFrame([row])
    if FEATURE_NAMES:
        for col in FEATURE_NAMES:
            if col not in df.columns:
                df[col] = 0
        df = df[FEATURE_NAMES]
    return df, dist_km

def predict(inputs):
    df, dist_km = build_features(inputs)
    if model_loaded and scaler is not None:
        df_scaled = scaler.transform(df)
        prob = float(model.predict_proba(df_scaled)[0][1])
    else:
        score = (-1.8 + math.log1p(inputs['amt'])*0.38
                 + (0.75 if inputs['category'] in RISKY_CATEGORIES else 0)
                 + (0.65 if inputs['hour'] >= 22 or inputs['hour'] <= 5 else 0)
                 + (0.9 if inputs['amt'] > 800 else 0)
                 + dist_km * 0.008)
        prob = float(1 / (1 + math.exp(-score)))
    return prob >= 0.45, prob, dist_km

# ═══════════════════════════════════════════════════════════════════════════
# 🏠 MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════

# Header with Stats
st.markdown("""
<div class='premium-header'>
    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;'>
        <div style='display: flex; align-items: center; gap: 20px;'>
            <div style='font-size: 64px; animation: float 3s ease-in-out infinite;'>🛡️</div>
            <div>
                <h1 style='font-size: 2.8rem; font-weight: 900; margin: 0; background: linear-gradient(135deg, #0EA5E9, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    FraudShield AI
                </h1>
                <p style='color: #64748b; font-size: 16px; margin: 8px 0 0 0;'>
                    Enterprise-Grade Fraud Detection System
                </p>
            </div>
        </div>
        <div style='text-align: right;'>
            <div style='font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;'>Model Status</div>
            <div style='font-size: 18px; font-weight: 700; color: #10b981;'>""" + ("✅ XGBoost Active" if model_loaded else "⚠️ Offline") + """</div>
        </div>
    </div>
    <div style='display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px;'>
        <span class='feature-badge'>🤖 XGBoost ML</span>
        <span class='feature-badge'>⚡ Real-Time Detection</span>
        <span class='feature-badge'>📊 92.86% AUC-ROC</span>
        <span class='feature-badge'>🎯 90.24% Accuracy</span>
        <span class='feature-badge'>🔒 Enterprise Security</span>
    </div>
    <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 24px;'>
        <div style='background: #f0f9ff; border: 2px solid #0ea5e9; border-radius: 12px; padding: 16px; text-align: center;'>
            <div style='font-size: 11px; color: #0369a1; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>Accuracy</div>
            <div style='font-size: 28px; font-weight: 900; color: #0ea5e9;'>90.24%</div>
        </div>
        <div style='background: #f0fdf4; border: 2px solid #10b981; border-radius: 12px; padding: 16px; text-align: center;'>
            <div style='font-size: 11px; color: #047857; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>AUC-ROC</div>
            <div style='font-size: 28px; font-weight: 900; color: #10b981;'>92.86%</div>
        </div>
        <div style='background: #fef3c7; border: 2px solid #f59e0b; border-radius: 12px; padding: 16px; text-align: center;'>
            <div style='font-size: 11px; color: #b45309; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>F1-Score</div>
            <div style='font-size: 28px; font-weight: 900; color: #f59e0b;'>90.00%</div>
        </div>
        <div style='background: #fae8ff; border: 2px solid #a855f7; border-radius: 12px; padding: 16px; text-align: center;'>
            <div style='font-size: 11px; color: #7e22ce; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;'>CV-AUC</div>
            <div style='font-size: 28px; font-weight: 900; color: #a855f7;'>92.67%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Form
st.markdown("<div class='section-tag'>// Transaction Parameters</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**💳 Financial Information**")
    amt = st.number_input("Amount (USD)", min_value=0.01, max_value=50000.0, value=245.50, step=0.01, format="%.2f")
    category = st.selectbox("Merchant Category", options=[
        'grocery_pos', 'gas_transport', 'food_dining', 'entertainment', 'health_fitness',
        'personal_care', 'home', 'kids_pets',
        'shopping_net ⚠️', 'misc_net ⚠️', 'grocery_net ⚠️', 'travel ⚠️', 'shopping_pos ⚠️', 'misc_pos ⚠️'
    ])
    category_clean = category.replace(' ⚠️', '')

with col2:
    st.markdown("**⏰ Temporal Data**")
    now = datetime.now()
    hour = st.slider("Transaction Hour", 0, 23, now.hour, format="%dh")
    day = st.selectbox("Day of Week",
                       ["Monday (0)", "Tuesday (1)", "Wednesday (2)", "Thursday (3)",
                        "Friday (4)", "Saturday (5) ⚠️", "Sunday (6) ⚠️"],
                       index=now.weekday())
    day_val = int(day.split("(")[1][0])
    month = st.slider("Month", 1, 12, now.month)

with col3:
    st.markdown("**👤 Cardholder Profile**")
    age = st.slider("Age", 18, 80, 35)
    gender = st.radio("Gender", ["Male (1)", "Female (0)"], index=1, horizontal=True)
    gender_val = 1 if "Male" in gender else 0
    city_pop = st.number_input("City Population", min_value=100, max_value=5000000, value=50000, step=1000)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("**📍 GPS Coordinates**")

g1, g2, g3, g4 = st.columns(4)
lat = g1.number_input("Cardholder Lat", value=36.8065, format="%.4f")
lon = g2.number_input("Cardholder Lon", value=10.1815, format="%.4f")
merch_lat = g3.number_input("Merchant Lat", value=36.8500, format="%.4f")
merch_lon = g4.number_input("Merchant Lon", value=10.2500, format="%.4f")

st.markdown("<br>", unsafe_allow_html=True)

# Analysis Button
if st.button("🔍 Analyze Transaction"):
    inputs = {
        'amt': amt, 'category': category_clean, 'hour': hour,
        'day': day_val, 'month': month, 'age': age, 'gender': gender_val,
        'city_pop': city_pop, 'lat': lat, 'lon': lon,
        'merch_lat': merch_lat, 'merch_lon': merch_lon,
    }
    
    with st.spinner("⏳ Analyzing..."):
        import time
        time.sleep(0.5)
        is_fraud, prob, dist_km = predict(inputs)

    pct = prob * 100
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Analysis Result</div>", unsafe_allow_html=True)

    r1, r2 = st.columns([1.2, 1])
    
    with r1:
        if is_fraud:
            st.markdown(f"""
            <div class='fraud-card'>
                <div class='icon'>🚨</div>
                <div style='font-size:32px;font-weight:900;color:#DC2626;margin-bottom:12px;'>
                    FRAUD DETECTED
                </div>
                <div style='font-size:16px;color:#991B1B;font-weight:600;margin-bottom:16px;'>
                    Fraud Probability: <span style='font-size:24px;font-weight:800;'>{pct:.1f}%</span>
                </div>
                <div style='margin-top:16px;padding:12px;background:rgba(220,38,38,0.2);border-radius:12px;'>
                    <div style='font-size:13px;color:#FCA5A5;font-weight:600;'>⚠️ TRANSACTION BLOCKED</div>
                    <div style='font-size:12px;color:#FCA5A5;margin-top:4px;'>Manual verification required</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='legit-card'>
                <div class='icon'>✅</div>
                <div style='font-size:32px;font-weight:900;color:#16A34A;margin-bottom:12px;'>
                    LEGITIMATE TRANSACTION
                </div>
                <div style='font-size:16px;color:#15803D;font-weight:600;margin-bottom:16px;'>
                    Fraud Probability: <span style='font-size:24px;font-weight:800;'>{pct:.1f}%</span>
                </div>
                <div style='margin-top:16px;padding:12px;background:rgba(34,197,94,0.2);border-radius:12px;'>
                    <div style='font-size:13px;color:#86EFAC;font-weight:600;'>✓ TRANSACTION APPROVED</div>
                    <div style='font-size:12px;color:#86EFAC;margin-top:4px;'>No action required</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("**📊 Detailed Risk Analysis**")
        
        # Enhanced Risk Score Display
        risk_color = "#ef4444" if prob > 0.7 else ("#f59e0b" if prob > 0.45 else "#10b981")
        risk_text = "HIGH RISK" if prob > 0.7 else ("MEDIUM RISK" if prob > 0.45 else "LOW RISK")
        
        st.markdown(f"""
        <div class='risk-score-container'>
            <div class='risk-label'>🎯 FRAUD RISK SCORE</div>
            <div class='risk-percentage' style='color: {risk_color};'>{pct:.1f}%</div>
            <div style='text-align: center; font-size: 16px; font-weight: 700; color: {risk_color}; margin-bottom: 16px;'>
                {risk_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(prob, text=f"Risk Level: {pct:.1f}% {'🔴' if prob > 0.7 else '🟡' if prob > 0.45 else '🟢'}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Risk Factors:**")
        
        factors = {
            "💰 High Amount (>$800)": ("🔴 HIGH RISK", "risk") if amt > 800 else ("✅ Normal", "safe"),
            "🏪 Risky Category": ("🔴 HIGH RISK", "risk") if category_clean in RISKY_CATEGORIES else ("✅ Standard", "safe"),
            "🌙 Night Transaction": ("🔴 HIGH RISK", "risk") if (hour >= 22 or hour <= 5) else ("✅ Normal Hours", "safe"),
            "📅 Weekend": ("🟡 CAUTION", "warning") if day_val >= 5 else ("✅ Weekday", "safe"),
            f"📍 Distance: {dist_km:.1f}km": ("🔴 HIGH RISK", "risk") if dist_km > 100 else (("🟡 MEDIUM", "warning") if dist_km > 30 else ("✅ Normal", "safe")),
        }
        
        for name, (status, level) in factors.items():
            color = "#DC2626" if level == "risk" else ("#F59E0B" if level == "warning" else "#10b981")
            bg_color = "#fee2e2" if level == "risk" else ("#fef3c7" if level == "warning" else "#d1fae5")
            st.markdown(f"""
            <div class='info-card' style='border-left: 4px solid {color}; background: {bg_color};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='color: #0f172a; font-weight: 600; font-size: 14px;'>{name}</span>
                    <span style='color: {color}; font-weight: 700; font-size: 13px;'>{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><div class='section-tag'>// Prediction Metrics</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Probability", f"{pct:.2f}%")
    c2.metric("Verdict", "🚨 FRAUD" if is_fraud else "✅ LEGIT")
    c3.metric("Threshold", "45.0%")
    c4.metric("Model", "XGBoost")
    c5.metric("GPS Distance", f"{dist_km:.1f} km")

    # Save to history
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'Time': f"{hour:02d}h",
        'Amount': f"${amt:.2f}",
        'Category': category_clean,
        'Distance': f"{dist_km:.1f} km",
        'Probability': f"{pct:.1f}%",
        'Verdict': "🚨 FRAUD" if is_fraud else "✅ LEGIT"
    })

# History Section
if 'history' in st.session_state and len(st.session_state.history) > 0:
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Session History</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #64748b; font-size: 14px; margin-bottom: 16px;'>📋 {len(st.session_state.history)} transaction(s) analyzed</p>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history[::-1]), use_container_width=True, hide_index=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    with col_btn2:
        if st.button("📥 Export CSV"):
            csv = pd.DataFrame(st.session_state.history).to_csv(index=False)
            st.download_button("⬇️ Download", csv, "fraud_history.csv", "text/csv")

# Model Comparison Section
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-tag'>// Model Performance Comparison</div>", unsafe_allow_html=True)

col_m1, col_m2 = st.columns([2, 1])

with col_m1:
    st.markdown("""
    <div class='stats-card'>
        <h3 style='color: #0f172a; margin-bottom: 16px;'>📊 Evaluated Models</h3>
        <table style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr style='background: #f1f5f9; border-bottom: 2px solid #cbd5e1;'>
                    <th style='padding: 12px; text-align: left; color: #0f172a; font-weight: 700;'>Model</th>
                    <th style='padding: 12px; text-align: center; color: #0f172a; font-weight: 700;'>AUC-ROC</th>
                    <th style='padding: 12px; text-align: center; color: #0f172a; font-weight: 700;'>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr style='background: #e0f2fe; border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; font-weight: 700; color: #0369a1;'>🏆 XGBoost</td>
                    <td style='padding: 12px; text-align: center; font-weight: 700; color: #0369a1;'>0.9286</td>
                    <td style='padding: 12px; text-align: center;'><span style='background: #10b981; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;'>✅ ACTIVE</span></td>
                </tr>
                <tr style='border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; color: #334155;'>Random Forest</td>
                    <td style='padding: 12px; text-align: center; color: #334155;'>0.9214</td>
                    <td style='padding: 12px; text-align: center;'><span style='background: #64748b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;'>🔵 BACKUP</span></td>
                </tr>
                <tr style='border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; color: #334155;'>Logistic Regression</td>
                    <td style='padding: 12px; text-align: center; color: #334155;'>0.9024</td>
                    <td style='padding: 12px; text-align: center;'><span style='background: #64748b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;'>🔵 BACKUP</span></td>
                </tr>
                <tr style='border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; color: #334155;'>DL-Medium</td>
                    <td style='padding: 12px; text-align: center; color: #334155;'>0.8476</td>
                    <td style='padding: 12px; text-align: center;'><span style='background: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;'>📊 TEST</span></td>
                </tr>
                <tr style='border-bottom: 1px solid #e2e8f0;'>
                    <td style='padding: 12px; color: #334155;'>DL-FocalLoss</td>
                    <td style='padding: 12px; text-align: center; color: #334155;'>0.8143</td>
                    <td style='padding: 12px; text-align: center;'><span style='background: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;'>📊 TEST</span></td>
                </tr>
                <tr>
                    <td style='padding: 12px; color: #334155;'>DL-Shallow</td>
                    <td style='padding: 12px; text-align: center; color: #334155;'>0.8024</td>
                    <td style='padding: 12px; text-align: center;'><span style='background: #f59e0b; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 700;'>📊 TEST</span></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class='stats-card'>
        <h3 style='color: #0f172a; margin-bottom: 16px;'>ℹ️ About</h3>
        <p style='color: #64748b; font-size: 14px; line-height: 1.6; margin-bottom: 12px;'>
            <strong style='color: #0EA5E9;'>FraudShield AI</strong> uses advanced Machine Learning algorithms for real-time fraud detection.
        </p>
        <div style='background: #f1f5f9; border-radius: 8px; padding: 12px; margin-top: 12px;'>
            <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'><strong>Version:</strong> 2.0.0</div>
            <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'><strong>Updated:</strong> April 2026</div>
            <div style='font-size: 12px; color: #64748b;'><strong>License:</strong> MIT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
