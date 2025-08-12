import os
import pandas as pd
import streamlit as st
from components import (load_custom_css, display_logo, display_header, display_footer,\
                        create_input_form, call_prediction_api, call_batch_prediction_api,
)

# Configuration de la page
st.set_page_config(
    page_title="Concrete Strength Predictor",
    layout="wide",
    page_icon=" 🧱 "
)

# Initialisation
load_custom_css()
display_logo()
display_header()

# Configuration API
#API_URL = os.getenv("API_URL", "http://api:8000")
API_URL = os.getenv("API_URL")
#st.sidebar.markdown(f"🌐 API URL: `{API_URL}`")

# Liste des paramètres 
INPUT_NAMES = ["cement", "slag", "fly_ash", "water", "superplasticizer", "coarse_aggregate", "fine_aggregate", "age"]

# Instructions
st.markdown("""
Pour réaliser une prédiction en batch, veuillez charger un fichier **CSV** contenant les colonnes suivantes :

- `cement` : quantité de ciment (kg/m³)  
- `slag` : quantité de laitier (kg/m³)  
- `fly_ash` : quantité de cendre volante (kg/m³)  
- `water` : quantité d'eau (kg/m³)  
- `superplasticizer` : adjuvant superplastifiant (kg/m³)  
- `coarse_aggregate` : granulats grossiers (kg/m³)  
- `fine_aggregate` : granulats fins (kg/m³)  
- `age` : âge du béton (en jours)
""")

# Onglets principaux
tab1, tab2 = st.tabs(["Prédiction individuelle", "Prédiction en batch"])

with tab1:
    st.subheader("Entrez les paramètres du béton")
    features = create_input_form(INPUT_NAMES)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Prédire la résistance"):
            if all(v == 0 for v in features[:8]): 
                st.error("Veuillez entrer des valeurs non nulles")
            else:
                with st.spinner("Calcul en cours..."):
                    result = call_prediction_api(API_URL, features)
                
                if result["success"]:
                    try:
                        value = float(result['value'])
                        st.success(f"Résistance prédite: {value:.3f} MPa")
                        if result.get("source") == "business_rule":
                            st.info(result.get("message", "Règle métier appliquée"))
                    except (ValueError, TypeError):
                        st.error("Format de prédiction invalide")
                else:
                    st.error(f"Erreur: {result['message']}")

with tab2:
    st.subheader("Import d'un fichier CSV")
    uploaded = st.file_uploader("Chargez un fichier CSV", type="csv")

    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.success(f"Fichier chargé ({len(df)} lignes)")
            st.dataframe(df.head())

            # Vérification des colonnes
            missing_cols = [col for col in INPUT_NAMES if col not in df.columns]
            if missing_cols:
                st.error(f"Colonnes manquantes: {', '.join(missing_cols)}")
            elif st.button("Lancer la prédiction batch"):
                with st.spinner(f"Traitement de {len(df)} échantillons..."):
                    result = call_batch_prediction_api(API_URL, uploaded)
                
                if result["success"]:
                    df["predicted_strength_MPa"] = result["predictions"]
                    st.success("Prédictions terminées")
                    st.dataframe(df)
                    
                    # Téléchargement des résultats
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Télécharger les résultats", csv, "predictions.csv", "text/csv", key='download-csv')
                else:
                    st.error(f"Erreur: {result['message']}")

        except Exception as e:
            st.error(f"Erreur de lecture: {str(e)}")

# Pied de page
display_footer()