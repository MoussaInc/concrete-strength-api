import json
import os
import streamlit as st
import requests
import base64
import pandas as pd
from typing import Dict, List, Optional


def load_custom_css(css_path="src/dashboard/static/style.css"):
    """Chargement du CSS"""
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_logo(path="src/dashboard/static/images/logo.png", width=100, cv_url="https://www.poussaim.org"):
    """Affichage du logo"""
    if path and os.path.exists(path):
        logo_html = f"""
        <a href="{cv_url}" target="_blank">
            <img src="data:image/png;base64,{get_base64_of_bin_file(path)}" width="{width}">
        </a>
        """
        st.markdown(logo_html, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def display_header():
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
    st.markdown("""
    <hr style="border-top: 2px solid #2E3B4E"/>
    <div style="text-align:center; color:gray; font-size: 0.9rem;">
        © 2025 <a href="https://poussaim.org" target="_blank">Moussa MBALLO</a> — Tous droits réservés.
    </div>
    """, unsafe_allow_html=True)


def create_input_form(input_names: List[str]) -> List[float]:
    """Formulaire avec validation des entrees"""
    cols = st.columns(4)
    inputs = []
    for i, name in enumerate(input_names):
        label = name.replace("_", " ").capitalize()
        val = cols[i % 4].number_input(label, value=0.0, format="%.2f")
        inputs.append(val)

    # Calcul des features dérivées avec gestion d'erreur
    try:
        cement, slag, fly_ash, water, superplasticizer, coarse, fine, age = inputs[:8]
        binder = cement + slag + fly_ash
        wcr = water / (binder or 1e-6)  # Évite division par zéro
        f2c = fine / (coarse or 1e-6)   # Évite division par zéro
        return inputs + [wcr, binder, f2c]
    except Exception:
        return inputs + [0.0, 0.0, 0.0]  # Valeurs par défaut en cas d'erreur


def call_prediction_api(api_url: str, features: List[float]) -> Dict:
    feature_names = [
        "cement", "slag", "fly_ash", "water", "superplasticizer",
        "coarse_aggregate", "fine_aggregate", "age",
        "water_cement_ratio", "binder", "fine_to_coarse_ratio"
    ]
    payload = {"features": dict(zip(feature_names, features))}
    try:
        response = requests.post(f"{api_url}/predict", json=payload, timeout=10)
        if not response.content:
            return {"success": False, "message": "Réponse vide de l'API"}
        data = response.json()
        return {
            "success": True,
            "value": float(data["predicted_strength_MPa"]),
            "source": data.get("source", "model"),
            "message": data.get("message")
        }
    except json.JSONDecodeError:
        return {"success": False, "message": "Réponse API non valide (JSON malformé)"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Erreur de connexion: {str(e)}"}
    except KeyError:
        return {"success": False, "message": "Format de réponse API inattendu"}
    except Exception as e:
        return {"success": False, "message": f"Erreur inattendue: {str(e)}"}


def call_batch_prediction_api(api_url: str, file) -> Dict:
    try:
        files = {"file": (file.name, file.getvalue(), "text/csv")}
        response = requests.post(f"{api_url}/predict-batch", files=files, timeout=30)
        if not response.content:
            return {"success": False, "message": "Réponse vide de l'API batch"}   
        data = response.json()
        return {
            "success": True,
            "predictions": data["predicted_strengths_MPa"],
            "messages": data.get("messages", []),
            "source": data.get("source", "model")
        }
    except json.JSONDecodeError:
        return {"success": False, "message": "Réponse batch non valide (JSON malformé)"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Erreur batch: {str(e)}"}
    except KeyError:
        return {"success": False, "message": "Format de réponse batch inattendu"}