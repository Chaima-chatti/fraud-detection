# 🚀 Guide de Déploiement Streamlit Cloud

## ✅ Étapes Complétées

1. ✅ Streamlit CLI installé
2. ✅ Toutes les dépendances installées
3. ✅ Configuration Streamlit créée (`.streamlit/config.toml`)
4. ✅ `.gitignore` créé
5. ✅ README amélioré
6. ✅ Changements poussés vers GitHub

## 📋 Prochaines Étapes pour Déployer sur Streamlit Cloud

### 1. Accéder à Streamlit Cloud
- Allez sur: https://streamlit.io/cloud
- Cliquez sur "Sign up" ou "Sign in"
- Connectez-vous avec votre compte GitHub

### 2. Déployer l'Application
1. Cliquez sur "New app"
2. Sélectionnez votre repository: `Chaima-chatti/fraud-detection`
3. Branch: `main`
4. Main file path: `app.py`
5. Cliquez sur "Deploy!"

### 3. Configuration (Optionnel)
Si vous avez des secrets ou variables d'environnement:
- Allez dans "Settings" → "Secrets"
- Ajoutez vos variables au format TOML

### 4. URL de l'Application
Une fois déployée, votre app sera accessible à:
```
https://[votre-app-name].streamlit.app
```

## 🔧 Commandes Utiles

### Tester localement
```bash
streamlit run app.py
```

### Mettre à jour l'application
```bash
git add .
git commit -m "Update application"
git push origin main
```
L'application se redéploiera automatiquement sur Streamlit Cloud.

## 📊 Fichiers Requis (Tous Présents ✅)
- ✅ `app.py` - Application principale
- ✅ `requirements.txt` - Dépendances Python
- ✅ `xgb_model.pkl` - Modèle XGBoost
- ✅ `scaler.pkl` - Scaler
- ✅ `feature_names.json` - Noms des features
- ✅ `.streamlit/config.toml` - Configuration Streamlit

## 🎯 Votre Repository GitHub
https://github.com/Chaima-chatti/fraud-detection

## 💡 Conseils
- Le déploiement prend généralement 2-5 minutes
- Streamlit Cloud redéploie automatiquement à chaque push sur GitHub
- Vous pouvez voir les logs en temps réel pendant le déploiement
- L'application se réveille automatiquement quand quelqu'un y accède

## 🆘 Support
Si vous rencontrez des problèmes:
- Documentation: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Forum: https://discuss.streamlit.io/
