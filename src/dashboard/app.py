
# src/dashboard/app.py

import os
import pandas as pd
import streamlit as st
from components import (
    load_custom_css,
    display_logo,
    display_header,
    display_footer,
    create_input_form,
    call_prediction_api,
    call_batch_prediction_api
)

# --- Configuration de la page ---
st.set_page_config(
    page_title="Concrete Strength Predictor",
    layout="wide",
    page_icon="🧱"
)

# --- Initialisation ---
load_custom_css()
display_logo()
display_header()

API_URL = os.getenv("API_URL", "http://api:8000")

INPUT_NAMES = ["cement", "slag", "fly_ash", "water", "superplasticizer", "coarse_aggregate", "fine_aggregate", "age"]

# --- Onglets ---
tab1, tab2 = st.tabs(["Prédiction individuelle", "Prédiction en batch"])

with tab1:
    st.subheader("Entrez les paramètres du béton")
    features = create_input_form(INPUT_NAMES)

    if st.button("Prédire la résistance"):
        result = call_prediction_api(API_URL, features)
        if result["success"]:
            try:
                value = float(result['value'])
                st.success(f"Résistance prédite : {value:.2f} MPa")
            except (ValueError, TypeError):
                st.error("La prédiction reçue n'est pas un nombre valide.")
        else:
            st.error(result["message"])

with tab2:
    st.subheader("Import d’un fichier CSV pour prédiction en lot")
    st.markdown("Colonnes attendues : `" + ", ".join(INPUT_NAMES) + "`")

    uploaded = st.file_uploader("Chargez un fichier CSV", type="csv")

    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Erreur lecture CSV: {e}")
        else:
            if st.button("Lancer la prédiction batch"):
                result = call_batch_prediction_api(API_URL, uploaded)
                if result["success"]:
                    df["predicted_strength_MPa"] = result["predictions"]
                    st.success(f"{len(result['predictions'])} prédictions générées ✅")
                    st.dataframe(df)
                    st.download_button("Télécharger les résultats", df.to_csv(index=False), "predictions.csv", "text/csv")
                else:
                    st.error(result["message"])

display_footer()
