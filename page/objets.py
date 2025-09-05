import streamlit as st
import json
import os
from urllib.parse import quote, unquote

def charger_donnees():
    """Charger les données des objets depuis le fichier JSON"""
    try:
        with open("data/items.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Fichier items.json introuvable")
        return {}
    except json.JSONDecodeError:
        st.error("Erreur lors du chargement du fichier items.json")
        return {}

def afficher_objet_detail(item_key, item_data):
    """Afficher les détails d'un objet"""
    item_name = item_data.get("name", item_key)
    st.subheader(f"📦 {item_name}")
    
    # Effet de l'objet (description)
    if "description" in item_data and item_data["description"]:
        st.write("**Description :**")
        st.info(item_data["description"])
    
    # Type/Catégorie
    if "type" in item_data:
        st.write(f"**Type :** {item_data['type']}")
    
    # Retour à la liste
    if st.button("🔙 Retour à la liste des objets"):
        st.session_state.selected_item = None
        st.rerun()

def main():
    st.title("📦 Base de données des objets")
    
    # Charger les données
    items_data = charger_donnees()
    
    if not items_data:
        return
    
    # Vérifier si un objet spécifique est sélectionné via URL
    if "selected_item" not in st.session_state:
        st.session_state.selected_item = None
    
    # Récupérer le paramètre d'URL si présent
    query_params = st.query_params
    if "item" in query_params and not st.session_state.selected_item:
        item_name = unquote(query_params["item"])
        if item_name in items_data:
            st.session_state.selected_item = item_name
    
    # Si un objet est sélectionné, afficher ses détails
    if st.session_state.selected_item:
        item_key = st.session_state.selected_item
        if item_key in items_data:
            afficher_objet_detail(item_key, items_data[item_key])
            return
        else:
            st.error(f"Objet '{item_key}' introuvable")
            st.session_state.selected_item = None
    
    # Organiser les objets par catégorie
    categories = {}
    for item_key, item_data in items_data.items():
        category = item_data.get("type", "Autres")
        if category not in categories:
            categories[category] = []
        categories[category].append((item_key, item_data))
    
    # Trier les catégories
    sorted_categories = sorted(categories.keys())
    
    # Afficher le sélecteur de catégorie
    selected_category = st.selectbox(
        "Choisir une catégorie :",
        ["Toutes les catégories"] + sorted_categories
    )
    
    # Barre de recherche
    search_term = st.text_input("🔍 Rechercher un objet :", placeholder="Nom de l'objet...")
    
    # Filtrer et afficher les objets
    if selected_category == "Toutes les catégories":
        items_to_show = []
        for category, items in categories.items():
            items_to_show.extend(items)
    else:
        items_to_show = categories.get(selected_category, [])
    
    # Appliquer le filtre de recherche
    if search_term:
        items_to_show = [
            (key, data) for key, data in items_to_show
            if search_term.lower() in data.get("name", key).lower()
        ]
    
    # Trier par nom
    items_to_show.sort(key=lambda x: x[1].get("name", x[0]))
    
    # Afficher les résultats
    if items_to_show:
        st.write(f"**{len(items_to_show)} objet(s) trouvé(s)**")
        
        # Afficher les objets en colonnes
        cols = st.columns(3)
        for i, (item_key, item_data) in enumerate(items_to_show):
            with cols[i % 3]:
                # Créer une carte pour chaque objet
                item_name = item_data.get("name", item_key)
                category = item_data.get("type", "Autres")
                description = item_data.get("description", "Aucune description disponible")
                
                # Limiter la longueur de la description affichée
                short_description = description[:100] + "..." if len(description) > 100 else description
                
                # Bouton pour sélectionner l'objet
                if st.button(
                    f"📦 {item_name}",
                    key=f"item_{i}",
                    help=short_description
                ):
                    st.session_state.selected_item = item_key
                    st.rerun()
                
                # Afficher la catégorie et un aperçu de la description
                st.caption(f"**{category}**")
                st.caption(short_description)
                st.markdown("---")
    else:
        if search_term:
            st.warning(f"Aucun objet trouvé pour '{search_term}'")
        else:
            st.info("Aucun objet dans cette catégorie")
    
    # Statistiques
    with st.expander("📊 Statistiques"):
        st.write(f"**Total des objets :** {len(items_data)}")
        st.write("**Objets par catégorie :**")
        for category, items in sorted(categories.items()):
            st.write(f"- {category}: {len(items)} objets")

if __name__ == "__main__":
    main()
