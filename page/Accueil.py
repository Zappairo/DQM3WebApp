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
    - Interface responsive
    - Images des monstres
    - Données complètes
    - Recherche rapide
    - Informations de synthèse
    
    """)
    
    # Statistiques rapides
    st.markdown("### Statistiques rapides")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monstres", "500+", delta="Complet")
    with col2:
        st.metric("Familles", "8", delta="Toutes")
    with col3:
        st.metric("Compétences", "200+", delta="Détaillées")
    with col4:
        st.metric("Traits", "100+", delta="Décrits")
    
    st.markdown("---")
    st.markdown("*Créé pour les fans de Dragon Quest Monsters*")
