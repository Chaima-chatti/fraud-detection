import warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
import math
import os
from datetime import datetime

st.set_page_config(
    page_title="FraudShield AI — Enterprise Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Chaima-chatti/fraud-detection',
        'Report a bug': 'https://github.com/Chaima-chatti/fraud-detection/issues',
        'About': '# FraudShield AI\nEnterprise-grade fraud detection powered by XGBoost ML'
    }
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* ═══════════════════════════════════════════════════════════════════════════
       🎨 GLOBAL STYLES & ANIMATIONS
    ═══════════════════════════════════════════════════════════════════════════ */
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🌐 BASE LAYOUT
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .stApp {
        background: linear-gradient(135deg, #0a1929 0%, #1a2332 50%, #0f1419 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        z-index: 1;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #F8FAFC !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }
    
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
        color: #CBD5E1 !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🎯 SIDEBAR - PREMIUM GLASS MORPHISM
    ═══════════════════════════════════════════════════════════════════════════ */
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] h2 {
        background: linear-gradient(135deg, #0EA5E9 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem !important;
        margin-bottom: 1.5rem !important;
        animation: slideInRight 0.5s ease-out;
    }
    
    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stError,
    [data-testid="stSidebar"] .stInfo {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        padding: 12px 16px !important;
        animation: slideInRight 0.6s ease-out;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       📊 METRICS - MODERN CARDS WITH GLOW
    ═══════════════════════════════════════════════════════════════════════════ */
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 
            0 4px 24px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.5s ease-out;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.03), transparent);
        transition: left 0.5s;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 8px 32px rgba(14, 165, 233, 0.2),
            0 0 0 1px rgba(14, 165, 233, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-color: rgba(14, 165, 233, 0.4);
    }
    
    [data-testid="metric-container"]:hover::before {
        left: 100%;
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
        font-family: 'Inter', sans-serif !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #0EA5E9 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🔘 BUTTONS - PREMIUM INTERACTIVE
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .stButton button {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 50%, #0369A1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        padding: 18px 36px !important;
        width: 100% !important;
        box-shadow: 
            0 4px 20px rgba(14, 165, 233, 0.4),
            0 0 0 1px rgba(14, 165, 233, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 
            0 8px 32px rgba(14, 165, 233, 0.6),
            0 0 0 1px rgba(14, 165, 233, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        background: linear-gradient(135deg, #06B6D4 0%, #0EA5E9 50%, #0284C7 100%) !important;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🎴 RESULT CARDS - ANIMATED & PREMIUM
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .fraud-card {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(153, 27, 27, 0.1) 100%);
        border: 2px solid rgba(239, 68, 68, 0.4);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(220, 38, 38, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .fraud-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .legit-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(21, 128, 61, 0.1) 100%);
        border: 2px solid rgba(74, 222, 128, 0.4);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(34, 197, 94, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .legit-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(74, 222, 128, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    .fraud-card .icon, .legit-card .icon {
        font-size: 72px;
        margin-bottom: 16px;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🏷️ SECTION TAGS & DIVIDERS
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .section-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 2.5px;
        color: #0EA5E9;
        text-transform: uppercase;
        margin-bottom: 16px;
        font-weight: 700;
        display: inline-block;
        padding: 6px 14px;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 8px;
        animation: slideInRight 0.5s ease-out;
    }
    
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.3), transparent);
        margin: 24px 0;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       📝 INPUT FIELDS - MODERN DESIGN
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .stNumberInput input, .stSelectbox select, .stSlider {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        color: #F1F5F9 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: rgba(14, 165, 233, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }
    
    .stNumberInput label, .stSelectbox label, .stSlider label {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       📊 PROGRESS BAR - ANIMATED
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #0EA5E9, #8B5CF6) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.5) !important;
    }
    
    .stProgress > div {
        background: rgba(30, 41, 59, 0.6) !important;
        border-radius: 10px !important;
        height: 12px !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       📋 DATAFRAME - PREMIUM TABLE
    ═══════════════════════════════════════════════════════════════════════════ */
    
    [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stDataFrame"] table {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: rgba(14, 165, 233, 0.15) !important;
        color: #0EA5E9 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        letter-spacing: 1px !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🎭 RADIO BUTTONS
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .stRadio > label {
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }
    
    .stRadio [role="radiogroup"] label {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        margin: 4px !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio [role="radiogroup"] label:hover {
        border-color: rgba(14, 165, 233, 0.5) !important;
        background: rgba(14, 165, 233, 0.1) !important;
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       🎨 CUSTOM COMPONENTS
    ═══════════════════════════════════════════════════════════════════════════ */
    
    .premium-header {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.5s ease-out;
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
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        border-color: rgba(14, 165, 233, 0.4);
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.2);
        transform: translateX(4px);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    try:
        model  = joblib.load('xgb_model.pkl')
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
    'grocery_net': 3,  'grocery_pos': 4, 'health_fitness': 5,
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
    dist_km      = haversine(inp['lat'], inp['lon'], inp['merch_lat'], inp['merch_lon'])
    amt_log      = math.log1p(inp['amt'])
    city_pop_log = math.log1p(inp['city_pop'])
    row = {
        'amt': inp['amt'], 'amt_log': amt_log,
        'hour': inp['hour'], 'day': inp['day'], 'month': inp['month'],
        'age': inp['age'], 'is_male': inp['gender'],
        'city_pop': inp['city_pop'], 'city_pop_log': city_pop_log,
        'dist_km': dist_km,
        'is_high_amt':  1 if inp['amt'] > 800 else 0,
        'is_risky_cat': 1 if inp['category'] in RISKY_CATEGORIES else 0,
        'is_weekend':   1 if inp['day'] >= 5 else 0,
        'is_night':     1 if (inp['hour'] >= 22 or inp['hour'] <= 5) else 0,
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
        # ✅ FIX FLOAT32 : conversion explicite en float Python natif
        prob = float(model.predict_proba(df_scaled)[0][1])
    else:
        score = (-1.8 + math.log1p(inputs['amt'])*0.38
                 + (0.75 if inputs['category'] in RISKY_CATEGORIES else 0)
                 + (0.65 if inputs['hour'] >= 22 or inputs['hour'] <= 5 else 0)
                 + (0.9  if inputs['amt'] > 800 else 0)
                 + dist_km * 0.008)
        prob = float(1 / (1 + math.exp(-score)))
    return prob >= 0.45, prob, dist_km


# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 🛡️ FraudShield AI")
    st.markdown("<div class='section-tag'>// Statut Système</div>", unsafe_allow_html=True)
    if model_loaded:
        st.success("✅ Modèle XGBoost Opérationnel")
        st.markdown("""
        <div style='background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 12px; margin-top: 8px;'>
            <div style='font-size: 11px; color: #86EFAC; font-weight: 600;'>🔒 SYSTÈME SÉCURISÉ</div>
            <div style='font-size: 10px; color: #86EFAC; margin-top: 4px;'>Tous les composants chargés</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Modèle Non Trouvé")
        st.info("📦 Placez `xgb_model.pkl`, `scaler.pkl` et `feature_names.json` dans le dossier racine")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Performances ML</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Accuracy", "90.24%", delta="↑ 2.1%", delta_color="normal")
    c2.metric("AUC-ROC",  "92.86%", delta="↑ 1.8%", delta_color="normal")
    c1.metric("F1-Score", "90.00%", delta="↑ 3.2%", delta_color="normal")
    c2.metric("CV-AUC",   "92.67%", delta="↑ 1.5%", delta_color="normal")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Comparaison Modèles</div>", unsafe_allow_html=True)
    st.markdown("""
<div style='background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 16px; backdrop-filter: blur(10px);'>
    
| Modèle | AUC | Status |
|--------|-----|--------|
| **XGBoost** | **0.9286** | ✅ **Actif** |
| Random Forest | 0.9214 | 🔵 Backup |
| Logistic Reg. | 0.9024 | 🔵 Backup |
| DL-Medium | 0.8476 | 📊 Test |
| DL-FocalLoss | 0.8143 | 📊 Test |
| DL-Shallow | 0.8024 | 📊 Test |

</div>
""", unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// À Propos</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size: 12px; color: #94A3B8; line-height: 1.6;'>
        <strong style='color: #0EA5E9;'>FraudShield AI</strong> utilise des algorithmes de Machine Learning avancés pour détecter les transactions frauduleuses en temps réel.
        <br><br>
        <strong>Version:</strong> 2.0.0<br>
        <strong>Dernière MAJ:</strong> Avril 2026<br>
        <strong>Licence:</strong> MIT
    </div>
    """, unsafe_allow_html=True)


# ── PREMIUM HEADER ──
st.markdown("""
<div class='premium-header'>
    <div style='display: flex; align-items: center; gap: 20px; margin-bottom: 16px;'>
        <div style='font-size: 64px; animation: float 3s ease-in-out infinite;'>🛡️</div>
        <div>
            <h1 style='font-size: 2.8rem; font-weight: 900; margin: 0; background: linear-gradient(135deg, #0EA5E9 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
                FraudShield AI
            </h1>
            <p style='color: #94A3B8; font-size: 16px; margin: 8px 0 0 0; font-weight: 500;'>
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


# ── FORMULAIRE ──
st.markdown("<div class='section-tag'>// Paramètres de la transaction</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**💳 Informations Financières**")
    amt = st.number_input("Montant (USD)", min_value=0.01, max_value=50000.0, value=245.50, step=0.01, format="%.2f", help="Montant de la transaction en dollars américains")
    category = st.selectbox("Catégorie Marchande", options=[
        'grocery_pos','gas_transport','food_dining','entertainment','health_fitness',
        'personal_care','home','kids_pets',
        'shopping_net ⚠️','misc_net ⚠️','grocery_net ⚠️','travel ⚠️','shopping_pos ⚠️','misc_pos ⚠️'
    ], help="Catégories avec ⚠️ sont considérées à risque élevé")
    category_clean = category.replace(' ⚠️','')

with col2:
    st.markdown("**⏰ Données Temporelles**")
    now   = datetime.now()
    hour  = st.slider("Heure de la Transaction", 0, 23, now.hour, format="%dh", help="Transactions nocturnes (22h-5h) sont plus risquées")
    day   = st.selectbox("Jour de la Semaine",
                         ["Lundi (0)","Mardi (1)","Mercredi (2)","Jeudi (3)",
                          "Vendredi (4)","Samedi (5) ⚠️","Dimanche (6) ⚠️"],
                         index=now.weekday(), help="Week-ends présentent un risque accru")
    day_val = int(day.split("(")[1][0])
    month = st.slider("Mois", 1, 12, now.month)

with col3:
    st.markdown("**👤 Profil du Titulaire**")
    age      = st.slider("Âge du Titulaire", 18, 80, 35, help="Âge du détenteur de la carte")
    gender   = st.radio("Genre", ["Masculin (1)","Féminin (0)"], index=1, horizontal=True)
    gender_val = 1 if "Masculin" in gender else 0
    city_pop = st.number_input("Population de la Ville", min_value=100, max_value=5000000, value=50000, step=1000, help="Population de la ville du titulaire")

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("**📍 Coordonnées GPS**")
st.markdown("<p style='color: #94A3B8; font-size: 13px; margin-bottom: 16px;'>Distance importante entre titulaire et marchand = risque accru</p>", unsafe_allow_html=True)
g1, g2, g3, g4 = st.columns(4)
lat       = g1.number_input("Lat. Titulaire",  value=36.8065, format="%.4f", help="Latitude du titulaire")
lon       = g2.number_input("Lon. Titulaire",  value=10.1815, format="%.4f", help="Longitude du titulaire")
merch_lat = g3.number_input("Lat. Marchand",   value=36.8500, format="%.4f", help="Latitude du marchand")
merch_lon = g4.number_input("Lon. Marchand",   value=10.2500, format="%.4f", help="Longitude du marchand")
st.markdown("<br>", unsafe_allow_html=True)


# ── ANALYSE ──
if st.button("🔍 Analyser la Transaction"):
    inputs = {
        'amt': amt, 'category': category_clean, 'hour': hour,
        'day': day_val, 'month': month, 'age': age, 'gender': gender_val,
        'city_pop': city_pop, 'lat': lat, 'lon': lon,
        'merch_lat': merch_lat, 'merch_lon': merch_lon,
    }
    with st.spinner("⏳ Analyse en cours..."):
        import time; time.sleep(0.5)
        is_fraud, prob, dist_km = predict(inputs)

    pct = prob * 100
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Résultat de l'analyse</div>", unsafe_allow_html=True)

    r1, r2 = st.columns([1.2, 1])
    with r1:
        if is_fraud:
            st.markdown(f"""
            <div class='fraud-card'>
                <div class='icon'>🚨</div>
                <div style='font-size:32px;font-weight:900;color:#DC2626;font-family:Inter,sans-serif;margin-bottom:12px;letter-spacing:-0.02em;'>
                    FRAUDE DÉTECTÉE
                </div>
                <div style='font-size:16px;color:#991B1B;font-weight:600;margin-bottom:16px;'>
                    Probabilité de fraude : <span style='font-size:24px;font-weight:800;'>{pct:.1f}%</span>
                </div>
                <div style='margin-top:16px;padding:12px;background:rgba(220,38,38,0.2);border-radius:12px;'>
                    <div style='font-size:13px;color:#FCA5A5;font-weight:600;'>⚠️ TRANSACTION BLOQUÉE</div>
                    <div style='font-size:12px;color:#FCA5A5;margin-top:4px;'>Vérification manuelle requise</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='legit-card'>
                <div class='icon'>✅</div>
                <div style='font-size:32px;font-weight:900;color:#16A34A;font-family:Inter,sans-serif;margin-bottom:12px;letter-spacing:-0.02em;'>
                    TRANSACTION LÉGITIME
                </div>
                <div style='font-size:16px;color:#15803D;font-weight:600;margin-bottom:16px;'>
                    Probabilité de fraude : <span style='font-size:24px;font-weight:800;'>{pct:.1f}%</span>
                </div>
                <div style='margin-top:16px;padding:12px;background:rgba(34,197,94,0.2);border-radius:12px;'>
                    <div style='font-size:13px;color:#86EFAC;font-weight:600;'>✓ TRANSACTION AUTORISÉE</div>
                    <div style='font-size:12px;color:#86EFAC;margin-top:4px;'>Aucune action requise</div>
                </div>
            </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("**📊 Analyse Détaillée**")
        st.progress(prob, text=f"Score de Risque : {pct:.1f}%")
        st.markdown("<br>", unsafe_allow_html=True)
        
        factors = {
            "💰 Montant élevé (>800$)":      ("🔴 RISQUE ÉLEVÉ", "risk")    if amt > 800                                  else ("✅ Normal", "safe"),
            "🏪 Catégorie à risque":          ("🔴 RISQUE ÉLEVÉ", "risk")    if category_clean in RISKY_CATEGORIES         else ("✅ Standard", "safe"),
            "🌙 Transaction nocturne":        ("🔴 RISQUE ÉLEVÉ", "risk")    if (hour >= 22 or hour <= 5)                  else ("✅ Horaire normal", "safe"),
            "📅 Week-end":                    ("🟡 ATTENTION", "warning") if day_val >= 5                               else ("✅ Semaine", "safe"),
            f"📍 Distance: {dist_km:.1f}km": ("🔴 RISQUE ÉLEVÉ", "risk")    if dist_km > 100 else (("🟡 MOYEN", "warning") if dist_km > 30 else ("✅ Normale", "safe")),
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

    st.markdown("<br><div class='section-tag'>// Métriques de Prédiction</div>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Probabilité", f"{pct:.2f}%", delta=f"{pct-45:.1f}% vs seuil" if pct > 45 else f"{45-pct:.1f}% sous seuil", delta_color="inverse")
    c2.metric("Verdict",            "🚨 FRAUDE" if is_fraud else "✅ LÉGITIME")
    c3.metric("Seuil Optimal",      "45.0%")
    c4.metric("Modèle",             "XGBoost")
    c5.metric("Distance GPS",       f"{dist_km:.1f} km")

    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        'Heure': f"{hour:02d}h", 'Montant': f"${amt:.2f}",
        'Catégorie': category_clean, 'Distance': f"{dist_km:.1f} km",
        'Probabilité': f"{pct:.1f}%", 'Verdict': "🚨 FRAUDE" if is_fraud else "✅ LÉGITIME"
    })


# ── HISTORIQUE ──
if 'history' in st.session_state and len(st.session_state.history) > 0:
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Historique de la Session</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94A3B8; font-size: 14px; margin-bottom: 16px;'>📋 {len(st.session_state.history)} transaction(s) analysée(s)</p>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history[::-1]), use_container_width=True, hide_index=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        if st.button("🗑️ Effacer l'Historique"):
            st.session_state.history = []
            st.rerun()
    with col_btn2:
        if st.button("📥 Exporter CSV"):
            csv = pd.DataFrame(st.session_state.history).to_csv(index=False)
            st.download_button("⬇️ Télécharger", csv, "fraud_history.csv", "text/csv")