import streamlit as st
import json
import os
from PIL import Image
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="DQM Guide",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🐉 Dragon Quest Monsters - Guide")
st.markdown("---")

# Navigation
pages = {
    "🏠 Accueil": "accueil",
    "🔍 Recherche de Monstres": "recherche_monstres", 
    "📊 Base de Données": "base_donnees",
    "⚔️ Synthèse": "synthese"
}

# Sidebar pour la navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Choisir une page", list(pages.keys()))

# Fonction pour charger les données JSON
@st.cache_data
def charger_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Fichier non trouvé: {path}")
        return {}

# Chargement des données
@st.cache_data
def charger_donnees():
    return {
        "monstres": charger_json("data/monsters.json"),
        "talents": charger_json("data/talents.json"),
        "skills": charger_json("data/skills.json"),
        "traits": charger_json("data/traits.json"),
        "families": charger_json("data/families.json"),
        "resistances": charger_json("data/resistances.json"),
        "maxstats": charger_json("data/maxstats.json")
    }

# Chargement des données
donnees = charger_donnees()

# Router vers la page sélectionnée
if pages[selected_page] == "accueil":
    from page import accueil
    accueil.show()
elif pages[selected_page] == "recherche_monstres":
    from page import recherche_monstres
    recherche_monstres.show(donnees)
elif pages[selected_page] == "base_donnees":
    from page import base_donnees
    base_donnees.show(donnees)
elif pages[selected_page] == "synthese":
    from page import synthese
    synthese.show(donnees)
