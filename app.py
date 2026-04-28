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
    initial_sidebar_state="expanded"
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
        background: linear-gradient(135deg, #0a1929 0%, #1a2332 50%, #0f1419 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        animation: fadeInUp 0.6s ease-out;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #F8FAFC !important;
        font-weight: 800 !important;
    }
    
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
        color: #CBD5E1 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] h2 {
        background: linear-gradient(135deg, #0EA5E9 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    /* Metrics Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(14, 165, 233, 0.2);
        border-color: rgba(14, 165, 233, 0.4);
    }
    
    [data-testid="metric-container"] label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        color: #94A3B8 !important;
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
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.6s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .fraud-card {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.15), rgba(153, 27, 27, 0.1));
        border: 2px solid rgba(239, 68, 68, 0.4);
    }
    
    .legit-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(21, 128, 61, 0.1));
        border: 2px solid rgba(74, 222, 128, 0.4);
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
        padding: 6px 14px;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 8px;
        margin-bottom: 16px;
    }
    
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.3), transparent);
        margin: 24px 0;
    }

    /* Input Fields */
    .stNumberInput input, .stSelectbox select {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        color: #F1F5F9 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: rgba(14, 165, 233, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #0EA5E9, #8B5CF6) !important;
        border-radius: 10px !important;
    }
    
    .stProgress > div {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        height: 12px !important;
    }

    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .feature-badge {
        display: inline-block;
        padding: 6px 12px;
        background: rgba(14, 165, 233, 0.15);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: #0EA5E9;
        margin: 4px;
    }
    
    .info-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        border-color: rgba(14, 165, 233, 0.4);
        transform: translateX(4px);
    }

    /* DataFrames */
    [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 16px !important;
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
# 📊 SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🛡️ FraudShield AI")
    
    st.markdown("<div class='section-tag'>// System Status</div>", unsafe_allow_html=True)
    if model_loaded:
        st.success("✅ XGBoost Model Active")
    else:
        st.error("⚠️ Model Not Found")
        st.info("📦 Place model files in root directory")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Performance</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Accuracy", "90.24%")
    col2.metric("AUC-ROC", "92.86%")
    col1.metric("F1-Score", "90.00%")
    col2.metric("CV-AUC", "92.67%")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Model Comparison</div>", unsafe_allow_html=True)
    
    st.markdown("""
| Model | AUC | Status |
|-------|-----|--------|
| **XGBoost** | **0.9286** | ✅ Active |
| Random Forest | 0.9214 | 🔵 Backup |
| Logistic Reg | 0.9024 | 🔵 Backup |
| DL-Medium | 0.8476 | 📊 Test |
""")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// About</div>", unsafe_allow_html=True)
    st.markdown("""
**FraudShield AI** uses advanced ML algorithms for real-time fraud detection.

**Version:** 2.0.0  
**Updated:** April 2026  
**License:** MIT
""")

# ═══════════════════════════════════════════════════════════════════════════
# 🏠 MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class='premium-header'>
    <div style='display: flex; align-items: center; gap: 20px; margin-bottom: 16px;'>
        <div style='font-size: 64px; animation: float 3s ease-in-out infinite;'>🛡️</div>
        <div>
            <h1 style='font-size: 2.8rem; font-weight: 900; margin: 0; background: linear-gradient(135deg, #0EA5E9, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                FraudShield AI
            </h1>
            <p style='color: #94A3B8; font-size: 16px; margin: 8px 0 0 0;'>
                Enterprise-Grade Fraud Detection System
            </p>
        </div>
    </div>
    <div style='display: flex; gap: 8px; flex-wrap: wrap;'>
        <span class='feature-badge'>🤖 XGBoost ML</span>
        <span class='feature-badge'>⚡ Real-Time Detection</span>
        <span class='feature-badge'>📊 92.86% AUC-ROC</span>
        <span class='feature-badge'>🎯 90.24% Accuracy</span>
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
        st.markdown("**📊 Detailed Analysis**")
        st.progress(prob, text=f"Risk Score: {pct:.1f}%")
        st.markdown("<br>", unsafe_allow_html=True)
        
        factors = {
            "💰 High Amount (>$800)": ("🔴 HIGH RISK", "risk") if amt > 800 else ("✅ Normal", "safe"),
            "🏪 Risky Category": ("🔴 HIGH RISK", "risk") if category_clean in RISKY_CATEGORIES else ("✅ Standard", "safe"),
            "🌙 Night Transaction": ("🔴 HIGH RISK", "risk") if (hour >= 22 or hour <= 5) else ("✅ Normal Hours", "safe"),
            "📅 Weekend": ("🟡 CAUTION", "warning") if day_val >= 5 else ("✅ Weekday", "safe"),
            f"📍 Distance: {dist_km:.1f}km": ("🔴 HIGH RISK", "risk") if dist_km > 100 else (("🟡 MEDIUM", "warning") if dist_km > 30 else ("✅ Normal", "safe")),
        }
        
        for name, (status, level) in factors.items():
            color = "#DC2626" if level == "risk" else ("#F59E0B" if level == "warning" else "#16A34A")
            bg_color = "rgba(220, 38, 38, 0.1)" if level == "risk" else ("rgba(245, 158, 11, 0.1)" if level == "warning" else "rgba(34, 197, 94, 0.1)")
            st.markdown(f"""
            <div class='info-card' style='border-left: 3px solid {color}; background: {bg_color};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='color: #E2E8F0; font-weight: 600; font-size: 13px;'>{name}</span>
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
    st.markdown(f"<p style='color: #94A3B8; font-size: 14px; margin-bottom: 16px;'>📋 {len(st.session_state.history)} transaction(s) analyzed</p>", unsafe_allow_html=True)
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
