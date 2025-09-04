import streamlit as st
import pandas as pd

def get_maxstats_for_monster(monster_name, maxstats_data):
    """Obtenir les statistiques maximales d'un monstre"""
    if not maxstats_data:
        print(f"DEBUG: maxstats_data est vide pour {monster_name}")
        return None
    
    # Debug: afficher les premières entrées
    if len(maxstats_data) > 0 and isinstance(maxstats_data[0], dict):
        pass  # Données OK
    else:
        print(f"DEBUG: format de maxstats_data incorrect: {type(maxstats_data[0]) if maxstats_data else 'vide'}")
        return None
    
    for monster in maxstats_data:
        if monster["name"].lower() == monster_name.lower():
            return monster["stats"]
    
    # Debug: si pas trouvé
    print(f"DEBUG: {monster_name} pas trouvé dans maxstats")
    return None

def show(donnees):
    st.title("Base de Données")
    
    st.markdown("Explorez tous les monstres disponibles dans la base de données.")
    
    # Filtres
    st.subheader("Filtres")
    col1, col2, col3 = st.columns(3)
    
    # Préparer les données pour les filtres
    families_list = ["Tous"] + [f["name"] for f in donnees["families"].values()]
    ranks_list = ["Tous"] + sorted(list(set([m.get("rank", "?") for m in donnees["monstres"].values() if m.get("rank")])))
    
    with col1:
        selected_family = st.selectbox("Famille", families_list)
    
    with col2:
        selected_rank = st.selectbox("Rang", ranks_list)
    
    with col3:
        search_name = st.text_input("Recherche par nom")
    
    # Préparer les données des monstres
    monsters_data = []
    for key, monster in donnees["monstres"].items():
        if monster.get("name"):
            family_name = donnees["families"].get(monster.get("family", ""), {}).get("name", "Inconnue")
            growth = monster.get("growth", {})
            
            # Obtenir les statistiques maximales
            maxstats = get_maxstats_for_monster(monster["name"], donnees.get("maxstats", []))
            
            monster_data = {
                "Nom": monster["name"],
                "Numéro": monster.get("number", "?"),
                "Rang": monster.get("rank", "?"),
                "Famille": family_name,
                "HP Growth": growth.get("hp", "?") if growth else "?",
                "MP Growth": growth.get("mp", "?") if growth else "?",
                "ATK Growth": growth.get("atk", "?") if growth else "?",
                "DEF Growth": growth.get("def", "?") if growth else "?",
                "AGI Growth": growth.get("agi", "?") if growth else "?",
                "WIS Growth": growth.get("wis", "?") if growth else "?"
            }
            
            # Ajouter les stats maximales si disponibles
            if maxstats:
                monster_data.update({
                    "HP Max": maxstats.get("hp", "?"),
                    "MP Max": maxstats.get("mp", "?"),
                    "ATK Max": maxstats.get("attack", "?"),
                    "DEF Max": maxstats.get("defense", "?"),
                    "AGI Max": maxstats.get("agility", "?"),
                    "WIS Max": maxstats.get("wisdom", "?")
                })
            else:
                monster_data.update({
                    "HP Max": "?",
                    "MP Max": "?",
                    "ATK Max": "?",
                    "DEF Max": "?",
                    "AGI Max": "?",
                    "WIS Max": "?"
                })
            
            monsters_data.append(monster_data)
    
    # Créer DataFrame
    df = pd.DataFrame(monsters_data)
    
    # Appliquer les filtres
    if selected_family != "Tous":
        df = df[df["Famille"] == selected_family]
    
    if selected_rank != "Tous":
        df = df[df["Rang"] == selected_rank]
    
    if search_name:
        df = df[df["Nom"].str.contains(search_name, case=False, na=False)]
    
    # Afficher les résultats
    st.subheader(f"Résultats ({len(df)} monstres)")
    
    if len(df) > 0:
        # Options d'affichage
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            show_growth = st.checkbox("Stats croissance", value=True)
        with col3:
            show_maxstats = st.checkbox("Stats maximales", value=False)
        
        # Définir les colonnes à afficher
        base_columns = ["Nom", "Numéro", "Rang", "Famille"]
        growth_columns = ["HP Growth", "MP Growth", "ATK Growth", "DEF Growth", "AGI Growth", "WIS Growth"]
        max_columns = ["HP Max", "MP Max", "ATK Max", "DEF Max", "AGI Max", "WIS Max"]
        
        columns_to_show = base_columns.copy()
        if show_growth:
            columns_to_show.extend(growth_columns)
        if show_maxstats:
            columns_to_show.extend(max_columns)
        
        # Afficher le DataFrame avec les colonnes sélectionnées
        st.dataframe(
            df[columns_to_show],
            use_container_width=True,
            height=400
        )        # Statistiques
        st.subheader("Statistiques")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total monstres", len(df))
        with col2:
            family_counts = df["Famille"].value_counts()
            st.metric("Famille la plus représentée", family_counts.index[0] if len(family_counts) > 0 else "N/A")
        with col3:
            rank_counts = df["Rang"].value_counts()
            st.metric("Rang le plus courant", rank_counts.index[0] if len(rank_counts) > 0 else "N/A")
        with col4:
            st.metric("Familles uniques", df["Famille"].nunique())
    
    else:
        st.warning("Aucun monstre trouvé avec ces filtres.")
        st.info("Essayez de modifier vos critères de recherche.")
