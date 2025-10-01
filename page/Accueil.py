import streamlit as st
from PIL import Image
import os

def show():
    st.title("Accueil - Dragon Quest Monsters")
    
    # Image d'accueil (optionnelle)
    if os.path.exists("data/MonsterImages/Slime.1.jpg"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            img = Image.open("data/MonsterImages/Slime.1.jpg")
            st.image(img, width=300, caption="Bienvenue dans le monde de DQM!")
    
    st.markdown("""
    ## Bienvenue dans la web app Dragon Quest Monsters!
    
    Cette application vous permet de :
    
    ### Recherche de Monstres
    - Rechercher un monstre par son nom
    - Voir ses statistiques complètes
    - Consulter ses talents et compétences
    - Analyser ses résistances, points forts et faiblesses
    - Découvrir la synthèse d'un monstre donné
    
    ### Base de Données
    - Explorer d'un coup d'oeil tous les monstres disponibles
    - Filtrer par famille, rang ou type
    - Comparaison de statistiques
    
    ### Synthèse
    - Calculateur de synthèse
    - Combinaisons possibles
    - Optimisation d'équipe
    
    ---
    
    ### Comment utiliser l'application:
    
    1. **Navigation**: Utilisez le menu latéral pour naviguer entre les pages
    2. **Recherche**: Tapez le nom d'un monstre pour voir toutes ses informations
    3. **Synthèse**: Découvrez quels monstres peuvent être créés par synthèse
    
    ---
    
    ### Fonctionnalités:
    - Images des monstres
    - Données en WIP presque complète
    - Recherche rapide
    - Informations de synthèse
    
    """)
    
    st.markdown("---")
    st.markdown("*Créé par G.B - Zappairo*")
