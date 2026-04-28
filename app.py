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
    page_title="FraudShield — Détection de Fraude par IA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono&family=Syne:wght@400;600;700;800&display=swap');

    .stApp { background-color: #F5F7FA; }
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #0F4754 !important; }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * { color: #2D3748 !important; }

    [data-testid="metric-container"] {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 12px; padding: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="metric-container"] label {
        font-family: 'Space Mono', monospace !important;
        font-size: 11px !important; letter-spacing: 1px; color: #64748B !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-family: 'Space Mono', monospace !important;
        font-size: 26px !important; font-weight: 700 !important; color: #0F4754 !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #0F4754, #1a6b7a) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important; font-size: 16px !important;
        padding: 14px 32px !important; width: 100% !important;
        box-shadow: 0 2px 8px rgba(15,71,84,0.25) !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #1a6b7a, #0F4754) !important;
        box-shadow: 0 4px 16px rgba(15,71,84,0.35) !important;
    }

    .fraud-card {
        background: #FFF5F5; border: 2px solid #FC8181;
        border-radius: 16px; padding: 28px; text-align: center;
    }
    .legit-card {
        background: #F0FFF4; border: 2px solid #68D391;
        border-radius: 16px; padding: 28px; text-align: center;
    }
    .section-tag {
        font-family: 'Space Mono', monospace; font-size: 10px;
        letter-spacing: 2px; color: #0F4754; text-transform: uppercase;
        margin-bottom: 8px; font-weight: 600;
    }
    .divider { border: none; border-top: 1px solid #E2E8F0; margin: 16px 0; }
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
    st.markdown("## 🛡️ FraudShield")
    st.markdown("<div class='section-tag'>// Statut du modèle</div>", unsafe_allow_html=True)
    if model_loaded:
        st.success("✅ Modèle XGBoost chargé")
    else:
        st.error("⚠️ Modèle non trouvé")
        st.info("Place `xgb_model.pkl`, `scaler.pkl` et `feature_names.json` dans le même dossier que `app.py`")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Performances</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Accuracy", "90.24%")
    c2.metric("AUC-ROC",  "92.86%")
    c1.metric("F1-Score", "90.00%")
    c2.metric("CV-AUC",   "92.67%")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>// Modèles évalués</div>", unsafe_allow_html=True)
    st.markdown("""
| Modèle | AUC |
|--------|-----|
| **XGBoost ✓** | **0.9286** |
| Random Forest | 0.9214 |
| Logistic Reg. | 0.9024 |
| DL-Medium | 0.8476 |
| DL-FocalLoss | 0.8143 |
| DL-Shallow | 0.8024 |
""")


# ── TITRE ──
st.markdown("""
<h1 style='font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;color:#0F4754;margin-bottom:4px;'>
    🛡️ FraudShield — Détection de Fraude par IA
</h1>
<p style='color:#64748B;font-size:14px;margin-bottom:24px;'>
    Pipeline ML/DL · Credit Card Fraud Detection · XGBoost + Deep Learning
</p>
""", unsafe_allow_html=True)


# ── FORMULAIRE ──
st.markdown("<div class='section-tag'>// Paramètres de la transaction</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**💳 Informations financières**")
    amt = st.number_input("Montant (USD)", min_value=0.01, max_value=50000.0, value=245.50, step=0.01, format="%.2f")
    category = st.selectbox("Catégorie marchande", options=[
        'grocery_pos','gas_transport','food_dining','entertainment','health_fitness',
        'personal_care','home','kids_pets',
        'shopping_net ⚠️','misc_net ⚠️','grocery_net ⚠️','travel ⚠️','shopping_pos ⚠️','misc_pos ⚠️'
    ])
    category_clean = category.replace(' ⚠️','')

with col2:
    st.markdown("**⏰ Données temporelles**")
    now   = datetime.now()
    hour  = st.slider("Heure de la transaction", 0, 23, now.hour, format="%dh")
    day   = st.selectbox("Jour de la semaine",
                         ["Lundi (0)","Mardi (1)","Mercredi (2)","Jeudi (3)",
                          "Vendredi (4)","Samedi (5) ⚠️","Dimanche (6) ⚠️"],
                         index=now.weekday())
    day_val = int(day.split("(")[1][0])
    month = st.slider("Mois", 1, 12, now.month)

with col3:
    st.markdown("**👤 Profil du titulaire**")
    age      = st.slider("Âge du titulaire", 18, 80, 35)
    gender   = st.radio("Genre", ["Masculin (1)","Féminin (0)"], index=1)
    gender_val = 1 if "Masculin" in gender else 0
    city_pop = st.number_input("Population de la ville", min_value=100, max_value=5000000, value=50000, step=1000)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("**📍 Coordonnées GPS**")
g1, g2, g3, g4 = st.columns(4)
lat       = g1.number_input("Lat. titulaire",  value=36.8065, format="%.4f")
lon       = g2.number_input("Lon. titulaire",  value=10.1815, format="%.4f")
merch_lat = g3.number_input("Lat. marchand",   value=36.8500, format="%.4f")
merch_lon = g4.number_input("Lon. marchand",   value=10.2500, format="%.4f")
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
                <div style='font-size:56px;margin-bottom:10px;'>🚨</div>
                <div style='font-size:26px;font-weight:800;color:#C53030;font-family:Syne,sans-serif;margin-bottom:8px;'>FRAUDE DÉTECTÉE</div>
                <div style='font-size:14px;color:#742A2A;'>Probabilité de fraude : <strong>{pct:.1f}%</strong></div>
                <div style='margin-top:12px;font-size:12px;color:#E53E3E;'>⚠️ Transaction bloquée — Vérification recommandée</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='legit-card'>
                <div style='font-size:56px;margin-bottom:10px;'>✅</div>
                <div style='font-size:26px;font-weight:800;color:#276749;font-family:Syne,sans-serif;margin-bottom:8px;'>TRANSACTION LÉGITIME</div>
                <div style='font-size:14px;color:#276749;'>Probabilité de fraude : <strong>{pct:.1f}%</strong></div>
                <div style='margin-top:12px;font-size:12px;color:#38A169;'>✓ Transaction autorisée</div>
            </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("**📊 Détails de la prédiction**")
        # ✅ prob est un float Python natif — pas d'erreur float32
        st.progress(prob, text=f"Probabilité fraude : {pct:.1f}%")
        factors = {
            "Montant élevé (>800$)":      "🔴 RISQUE"    if amt > 800                                  else "✅ Normal",
            "Catégorie à risque":          "🔴 RISQUE"    if category_clean in RISKY_CATEGORIES         else "✅ Standard",
            "Transaction nocturne":        "🔴 RISQUE"    if (hour >= 22 or hour <= 5)                  else "✅ Horaire normal",
            "Week-end":                    "🟡 ATTENTION" if day_val >= 5                               else "✅ Semaine",
            f"Distance: {dist_km:.1f}km": "🔴 RISQUE"    if dist_km > 100 else ("🟡 MOYEN" if dist_km > 30 else "✅ Normale"),
        }
        for name, status in factors.items():
            st.markdown(f"`{name}` → **{status}**")

    st.markdown("<br><div class='section-tag'>// Informations de prédiction</div>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Probabilité fraude", f"{pct:.2f}%")
    c2.metric("Verdict",            "🚨 FRAUDE" if is_fraud else "✅ LÉGITIME")
    c3.metric("Seuil optimal",      "45.0%")
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
    st.markdown("<div class='section-tag'>// Historique de la session</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.history[::-1]), use_container_width=True, hide_index=True)
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.history = []
        st.rerun()