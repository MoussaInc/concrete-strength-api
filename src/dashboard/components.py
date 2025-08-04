# src/dashboard/components.py

import os
import streamlit as st
import requests
# Fonction utilitaire pour encoder l'image en base64
import base64


def load_custom_css(css_path="src/dashboard/static/style.css"):
    """
    Chargement et injection du CSS personnalisé dans l'app Streamlit.
    """

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Fichier CSS non trouvé à : {css_path}")

def display_logo(path="src/dashboard/static/images/logo.png", width=100, cv_url="https://www.poussaim.org"):
    """
    Affiche le logo cliquable (lien vers mon site perso) si le chemin est valide, sinon affiche un warning.
    """
    if path and os.path.exists(path):
        # Utiliser HTML pour afficher une image cliquable
        logo_html = f"""
        <a href="{cv_url}" target="_blank">
            <img src="data:image/png;base64,{get_base64_of_bin_file(path)}" width="{width}">
        </a>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.warning("Logo non trouvé.")



def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_header():
    """
    Affiche le header avec le titre et le lien vers le site mon site perso poussaim.org.
    """
    st.markdown("""
    <div style="text-align: center; max-width: 700px; margin: auto; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <h1 style="color: #2E3B4E; font-weight: 700; letter-spacing: 1.2px; margin-bottom: 0.2rem;">
            Concrete Strength Predictor
        </h1>
        <h4 style="color: #4a5a70; font-weight: 500; font-style: italic; margin-top: 0; margin-bottom: 1rem;">
            Prédiction de la résistance en compression simple du béton (MPa) <br>
            selon sa composition et sa durée de cure
        </h4>
    </div>
    <hr style="border-top: 3px solid #f68b1e; width: 50%; margin: 1.5rem auto 2rem auto; border-radius: 2px;" />
    """, unsafe_allow_html=True)

def display_footer():
    """
    Affiche le footer avec copyright.
    """
    st.markdown("""
    <hr style="border-top: 2px solid #2E3B4E"/>
    <div style="text-align:center; color:gray; font-size: 0.9rem;">
        © 2025 <a href="https://poussaim.org" target="_blank">Moussa MBALLO</a> — Tous droits réservés.
    </div>
    """, unsafe_allow_html=True)

def create_input_form(input_names):
    """
    Crée un formulaire responsive avec 4 colonnes pour saisir les features.
    Calcule et ajoute les features dérivées (water_cement_ratio, binder, fine_to_coarse_ratio).

    Args:
        input_names (list[str]): Noms des features de base.

    Returns:
        list[float]: Liste des valeurs des features de base + features dérivées.
    """

    cols = st.columns(4)
    inputs = []
    for i, name in enumerate(input_names):
        val = cols[i % 4].number_input(name.replace("_", " ").capitalize(), value=0.0, format="%.2f")
        inputs.append(val)

    cement, slag, fly_ash, water, superplasticizer, coarse, fine, age = inputs
    binder = cement + slag + fly_ash
    wcr = water / (binder + 1e-6)
    f2c = fine / (coarse + 1e-6)

    return inputs + [wcr, binder, f2c]

def call_prediction_api(api_url, features):
    """
    Envoie une requête POST à l'API pour une prédiction unique.

    Args:
        api_url (str): URL de base de l'API.
        features (list): Liste des features (avec dérivées).

    Returns:
        dict: {success: bool, value/message: str}
    """

    try:
        response = requests.post(f"{api_url}/predict", json={"features": features})
        if response.status_code == 200:
            return {"success": True, "value": response.json()["predicted_strength_MPa"]}
        else:
            return {"success": False, "message": response.json().get("detail", "Erreur API")}
    except Exception as e:
        return {"success": False, "message": str(e)}

def call_batch_prediction_api(api_url, file):
    """
    Envoie un fichier CSV à l'API pour une prédiction batch.

    Args:
        api_url (str): URL de base de l'API.
        file (UploadedFile): Fichier CSV uploadé via Streamlit.

    Returns:
        dict: {success: bool, predictions/message: list/str}
    """

    try:
        files = {"file": (file.name, file.getvalue(), "text/csv")}
        response = requests.post(f"{api_url}/predict-batch", files=files)
        if response.status_code == 200:
            return {"success": True, "predictions": response.json()["predicted_strengths_MPa"]}
        else:
            return {"success": False, "message": response.json().get("detail", "Erreur API")}
    except Exception as e:
        return {"success": False, "message": str(e)}

def show_input_instructions():
    st.markdown("""
    ### 🧾 Paramètres attendus pour la prédiction :

    Le modèle prend en compte les 8 paramètres suivants (unité : kg/m³ sauf âge en jours) :

    - **cement** : quantité de ciment   
    - **slag** : laitier de haut fourneau  
    - **fly_ash** : cendres volantes  
    - **water** : quantité d’eau  
    - **superplasticizer** : adjuvant  
    - **coarse_aggregate** : granulats grossiers  
    - **fine_aggregate** : granulats fins  
    - **age** : durée de cure du béton (en jours)

    Ces colonnes doivent être présentes dans le fichier CSV pour les prédictions en lot.
    """)
