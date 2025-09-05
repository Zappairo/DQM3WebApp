import streamlit as st
from PIL import Image
import os

def afficher_image_monstre(nom):
    """Afficher l'image d'un monstre"""
    # Essayer plusieurs variations du nom de fichier
    variations = [
        nom,  # Nom original
        nom.replace(' ', '_'),  # Espaces -> underscores
        nom.replace('-', '_'),  # Tirets -> underscores
        nom.replace(' ', '_').replace('-', '_'),  # Les deux
    ]
    
    for variation in variations:
        img_path = os.path.join("data/MonsterImages", f"{variation}.1.jpg")
        if os.path.exists(img_path):
            return Image.open(img_path)
    
    return None

def get_synthesis_tree(monster_key, donnees, visited=None, depth=0):
    """Obtenir l'arbre de synthèse complet d'un monstre"""
    if visited is None:
        visited = set()
    
    # Éviter les boucles infinies
    if monster_key in visited or depth > 5:
        return None
    
    visited.add(monster_key)
    
    monster = donnees["monstres"].get(monster_key)
    if not monster:
        return None
    
    tree = {
        "key": monster_key,
        "name": monster.get("name", monster_key),
        "rank": monster.get("rank", "?"),
        "synthesis": monster.get("synthesis"),
        "parents": []
    }
    
    # Si ce monstre a des parents (synthèse), les ajouter récursivement
    synthesis = monster.get("synthesis")
    if synthesis and isinstance(synthesis, list):
        for combination in synthesis:
            if isinstance(combination, list):
                parent_combination = []
                for parent_key in combination:
                    if parent_key.startswith("_"):
                        # C'est une famille
                        family_name = donnees["families"].get(parent_key, {}).get("name", parent_key)
                        parent_combination.append({
                            "key": parent_key,
                            "name": f"{family_name} (Famille)",
                            "rank": "Famille",
                            "is_family": True,
                            "parents": []
                        })
                    else:
                        # C'est un monstre spécifique
                        parent_tree = get_synthesis_tree(parent_key, donnees, visited.copy(), depth + 1)
                        if parent_tree:
                            parent_combination.append(parent_tree)
                
                if parent_combination:
                    tree["parents"].append(parent_combination)
    
    return tree

def afficher_arbre_synthese_inverse(tree, donnees, etape_counter=None):
    """Afficher l'arbre de synthèse dans l'ordre chronologique (parents -> enfant)"""
    if not tree:
        return
    
    # Initialiser le compteur d'étapes si c'est le premier appel
    if etape_counter is None:
        etape_counter = {"count": 1}
    
    # D'abord afficher les parents (récursivement)
    if tree["parents"]:
        # Vérifier si cette combinaison nécessite seulement des familles
        has_only_families = True
        for combination in tree["parents"]:
            for parent in combination:
                if not parent.get("is_family", False) and parent.get("parents"):
                    has_only_families = False
                    break
            if not has_only_families:
                break
        
        # Afficher les étapes parents d'abord (seulement si ce ne sont pas que des familles)
        if not has_only_families:
            for comb_idx, combination in enumerate(tree["parents"]):
                for parent_idx, parent in enumerate(combination):
                    afficher_arbre_synthese_inverse(parent, donnees, etape_counter)
    
    # Ensuite afficher le monstre actuel
    etape_actuelle = etape_counter["count"]
    etape_counter["count"] += 1
    
    # Créer un identifiant unique
    unique_id = f"step_{etape_actuelle}_{tree['key']}"
    
    # Affichage du niveau actuel
    if tree.get("is_family", False):
        st.write(f"### Étape {etape_actuelle}: Capturer {tree['name']}")
    else:
        if tree["parents"]:
            st.write(f"### Étape {etape_actuelle}: Synthétiser {tree['name']}")
        else:
            st.write(f"### Étape {etape_actuelle}: Capturer {tree['name']} (monstre de base)")
    
    # Créer les colonnes pour l'affichage
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        # Afficher l'image
        if not tree.get("is_family", False):
            img = afficher_image_monstre(tree["name"])
            if img:
                st.image(img, width=80, caption=f"Rang {tree['rank']}")
            else:
                st.write(f"Pas d'image")
                st.caption(f"Rang {tree['rank']}")
        else:
            st.write("Famille")
            st.caption("Famille")
    
    with col2:
        # Nom et informations
        if tree.get("is_family", False):
            st.write(f"**{tree['name']}**")
            st.write(f"Capturez n'importe quel monstre de cette famille")
        else:
            st.write(f"**{tree['name']}**")
        
        # Bouton pour voir les détails du monstre (si ce n'est pas une famille)
        if not tree.get("is_family", False):
            try:
                if st.button(f"Voir détails", key=f"details_{unique_id}"):
                    st.session_state[f"show_monster_{tree['key']}"] = tree['key']
            except:
                # En cas de problème avec la clé, on n'affiche pas le bouton
                st.write("(Détails non disponibles)")
    
    with col3:
        # Informations sur la synthèse
        if tree["parents"]:
            st.write(f"**Obtenu par synthèse de:**")
            for i, combination in enumerate(tree["parents"]):
                combo_names = [parent["name"] for parent in combination]
                st.write(f"  • {' + '.join(combo_names)}")
        else:
            st.write(f"**Monstre de base** (à capturer directement)")
    
    st.markdown("---")

def afficher_arbre_synthese(tree, donnees, level=0, path="", max_depth=4):
    """Afficher l'arbre de synthèse de manière récursive"""
    if not tree or level > max_depth:
        if level > max_depth:
            st.info("... (arbre tronqué pour éviter la complexité excessive)")
        return
    
    # Créer un identifiant unique basé sur le chemin dans l'arbre
    unique_id = f"{path}_{tree['key']}_{level}" if path else f"{tree['key']}_{level}"
    
    # Indentation basée sur le niveau
    indent = "  " * level
    
    # Créer les colonnes pour l'affichage
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        # Afficher l'image
        if not tree.get("is_family", False):
            img = afficher_image_monstre(tree["name"])
            if img:
                st.image(img, width=80, caption=f"Rang {tree['rank']}")
            else:
                st.write(f"Pas d'image")
                st.caption(f"Rang {tree['rank']}")
        else:
            st.write("Famille")
            st.caption("Famille")
    
    with col2:
        # Nom et informations
        if tree.get("is_family", False):
            st.write(f"{indent}**{tree['name']}**")
        else:
            st.write(f"{indent}**{tree['name']}**")
        
        # Bouton pour voir les détails du monstre (si ce n'est pas une famille)
        if not tree.get("is_family", False):
            try:
                if st.button(f"Voir détails", key=f"details_{unique_id}"):
                    st.session_state[f"show_monster_{tree['key']}"] = tree['key']
            except:
                # En cas de problème avec la clé, on n'affiche pas le bouton
                st.write("(Détails non disponibles)")
    
    with col3:
        # Informations de synthèse
        if tree["parents"] and level < max_depth:
            st.write(f"{indent}**Synthèse nécessaire:**")
            for i, combination in enumerate(tree["parents"]):
                combo_names = [parent["name"] for parent in combination]
                st.write(f"{indent}  • {' + '.join(combo_names)}")
        else:
            st.write(f"{indent}**Monstre de base** (pas de synthèse)")
    
    # Afficher les parents de manière récursive (seulement si on n'a pas atteint la profondeur max)
    if tree["parents"] and level < max_depth:
        # Vérifier si cette combinaison nécessite seulement des familles (pas besoin d'afficher les étapes)
        has_only_families = True
        for combination in tree["parents"]:
            for parent in combination:
                if not parent.get("is_family", False) and parent.get("parents"):
                    has_only_families = False
                    break
            if not has_only_families:
                break
        
        # Si ce ne sont que des familles ou des monstres de base, pas besoin d'afficher l'arbre récursif
        if not has_only_families:
            st.markdown("---")
            for comb_idx, combination in enumerate(tree["parents"]):
                st.write(f"{indent}**Étape {level + 1}:** Combiner ces monstres ⬇️")
                for parent_idx, parent in enumerate(combination):
                    # Créer un chemin unique pour éviter les collisions de clés
                    new_path = f"{unique_id}_c{comb_idx}_p{parent_idx}"
                    afficher_arbre_synthese(parent, donnees, level + 1, new_path, max_depth)
                st.markdown("---")

def show(donnees):
    st.title("Synthèse")
    
    st.markdown("Calculateur de synthèse et informations sur les combinaisons de monstres.")
    
    # Recherche de synthèse
    st.subheader("Rechercher des combinaisons")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        target_monster = st.text_input("Monstre à créer", placeholder="Ex: Goonache Goodie")
    
    with col2:
        st.write("")  # Espacement
        search_synthesis = st.button("Rechercher", type="primary")
    
    if target_monster and search_synthesis:
        # Rechercher le monstre cible
        target = None
        target_key = None
        for key, monster in donnees["monstres"].items():
            if monster.get("name", "").lower() == target_monster.lower():
                target = monster
                target_key = key
                break
        
        if target:
            st.success(f"Synthèse trouvée pour {target['name']}")
            
            # Afficher l'image du monstre cible
            col1, col2 = st.columns([1, 3])
            with col1:
                img = afficher_image_monstre(target["name"])
                if img:
                    st.image(img, width=150, caption=f"{target['name']} (Rang {target.get('rank', '?')})")
                else:
                    st.info("Image non disponible")
            
            with col2:
                st.write(f"**Nom:** {target['name']}")
                st.write(f"**Rang:** {target.get('rank', '?')}")
                st.write(f"**Famille:** {donnees['families'].get(target.get('family', ''), {}).get('name', 'Inconnue')}")
                if target.get("description"):
                    st.write(f"**Description:** {target['description']}")
            
            st.markdown("---")
            
            # Obtenir et afficher l'arbre de synthèse complet
            synthesis_tree = get_synthesis_tree(target_key, donnees)
            
            if synthesis_tree and synthesis_tree["parents"]:
                st.subheader("Arbre de synthèse complet")
                st.write("Voici la route complète de synthèse avec tous les parents nécessaires :")
                
                # Afficher l'arbre
                st.write("**Plan de synthèse étape par étape :**")
                afficher_arbre_synthese_inverse(synthesis_tree, donnees)
                
                # Résumé des monstres de base nécessaires
                st.subheader("Résumé - Monstres de base nécessaires")
                base_monsters = set()
                
                def collect_base_monsters(tree):
                    if not tree["parents"]:  # Pas de parents = monstre de base
                        if not tree.get("is_family", False):
                            base_monsters.add(tree["name"])
                    else:
                        for combination in tree["parents"]:
                            for parent in combination:
                                collect_base_monsters(parent)
                
                collect_base_monsters(synthesis_tree)
                
                if base_monsters:
                    st.write("**Monstres de base à capturer/obtenir :**")
                    cols = st.columns(min(len(base_monsters), 4))
                    for i, monster_name in enumerate(sorted(base_monsters)):
                        with cols[i % len(cols)]:
                            img = afficher_image_monstre(monster_name)
                            if img:
                                st.image(img, width=100, caption=monster_name)
                            else:
                                st.write(f"{monster_name}")
                else:
                    st.info("Aucun monstre de base requis (peut utiliser des familles)")
            
            else:
                st.info("Ce monstre ne nécessite pas de synthèse (monstre de base) ou aucune information de synthèse disponible.")
        else:
            st.error(f"Monstre '{target_monster}' non trouvé.")
    
    # Liste des synthèses disponibles
    st.subheader("📋 Synthèses disponibles")
    
    synthesis_data = []
    for key, monster in donnees["monstres"].items():
        if monster.get("name") and monster.get("synthesis"):
            synthesis = monster["synthesis"]
            if isinstance(synthesis, list) and len(synthesis) > 0:
                combinations = []
                for combination in synthesis:
                    if isinstance(combination, list):
                        combo_names = []
                        for item_key in combination:
                            if item_key.startswith("_"):
                                family_name = donnees["families"].get(item_key, {}).get("name", item_key)
                                combo_names.append(f"{family_name} (Famille)")
                            else:
                                monster_combo = donnees["monstres"].get(item_key)
                                if monster_combo:
                                    combo_names.append(monster_combo.get("name", item_key))
                                else:
                                    combo_names.append(item_key)
                        combinations.append(" + ".join(combo_names))
                
                synthesis_data.append({
                    "key": key,
                    "Monstre": monster["name"],
                    "Rang": monster.get("rank") or "?",
                    "Famille": donnees["families"].get(monster.get("family", ""), {}).get("name", "Inconnue"),
                    "Combinaisons": " | ".join(combinations)
                })
    
    if synthesis_data:
        # Filtre par rang - filtrer les valeurs None et vides
        ranks = ["Tous"] + sorted(list(set([s["Rang"] for s in synthesis_data if s["Rang"] and s["Rang"] != "None"])))
        selected_rank_filter = st.selectbox("Filtrer par rang", ranks)
        
        if selected_rank_filter != "Tous":
            synthesis_data = [s for s in synthesis_data if s["Rang"] == selected_rank_filter]
        
        # Affichage sous forme de cartes avec images
        st.write("**Cliquez sur un monstre pour voir son arbre de synthèse complet**")
        
        # Affichage en grille
        cols_per_row = 3
        for i in range(0, len(synthesis_data), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j in range(cols_per_row):
                if i + j < len(synthesis_data):
                    monster_data = synthesis_data[i + j]
                    
                    with cols[j]:
                        # Carte pour chaque monstre
                        with st.container():
                            # Image
                            img = afficher_image_monstre(monster_data["Monstre"])
                            if img:
                                st.image(img, width=120)
                            else:
                                st.write("Pas d'image")
                            
                            # Informations
                            st.write(f"**{monster_data['Monstre']}**")
                            st.write(f"Rang: {monster_data['Rang']} | {monster_data['Famille']}")
                            
                            # Combinaisons (tronquées si trop longues)
                            combinaisons = monster_data['Combinaisons']
                            if len(combinaisons) > 50:
                                combinaisons = combinaisons[:50] + "..."
                            st.write(f"🔗 {combinaisons}")
                        
                        st.markdown("---")
        
        # Afficher l'arbre si un monstre a été sélectionné
        if 'show_tree_for' in st.session_state:
            selected_monster = st.session_state['show_tree_for']
            st.subheader(f"🌳 Arbre de synthèse pour {selected_monster}")
            
            # Trouver la clé du monstre
            target_key = None
            for key, monster in donnees["monstres"].items():
                if monster.get("name") == selected_monster:
                    target_key = key
                    break
            
            if target_key:
                synthesis_tree = get_synthesis_tree(target_key, donnees)
                if synthesis_tree:
                    st.write("📋 **Plan de synthèse étape par étape :**")
                    afficher_arbre_synthese_inverse(synthesis_tree, donnees)
                    
                    if st.button("❌ Fermer l'arbre"):
                        del st.session_state['show_tree_for']
                        st.rerun()
        
        st.info(f"{len(synthesis_data)} monstres avec synthèse disponible")
    else:
        st.warning("Aucune synthèse disponible dans la base de données.")
    
    # Guide de synthèse
    with st.expander("❓ Guide de synthèse"):
        st.markdown("""
        ### Comment fonctionne la synthèse ?
        
        1. **Combinaisons spécifiques** : Certains monstres nécessitent des monstres précis
        2. **Familles** : D'autres peuvent être créés avec n'importe quel monstre d'une famille donnée
        3. **Rangs** : Le rang des parents influence le résultat
        
        ### Conseils :
        - Utilisez la recherche pour trouver comment créer un monstre spécifique
        - Consultez la liste complète pour découvrir toutes les possibilités
        - Planifiez vos synthèses en fonction des monstres que vous possédez
        """)
