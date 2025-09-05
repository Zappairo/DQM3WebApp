import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO
from urllib.parse import quote
import json

def get_maxstats(monstre_name, maxstats_data):
    """Obtenir les statistiques maximales d'un monstre"""
    for monster in maxstats_data:
        if monster["name"].lower() == monstre_name.lower():
            return monster["stats"]
    return None

def charger_items():
    """Charger les données des objets depuis le fichier JSON"""
    try:
        with open("data/items.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def objet_existe(item_name):
    """Vérifier si un objet existe dans la base de données"""
    items_data = charger_items()
    # Vérifier d'abord par clé, puis par nom
    if item_name in items_data:
        return True
    # Vérifier par nom d'affichage
    for key, data in items_data.items():
        if data.get("name", key) == item_name:
            return True
    return False

def obtenir_nom_objet(item_key):
    """Obtenir le nom d'affichage d'un objet à partir de sa clé"""
    items_data = charger_items()
    if item_key in items_data:
        return items_data[item_key].get("name", item_key)
    return item_key

def trouver_cle_objet(item_name):
    """Trouver la clé d'un objet à partir de son nom"""
    items_data = charger_items()
    # Vérifier d'abord par clé
    if item_name in items_data:
        return item_name
    # Vérifier par nom d'affichage
    for key, data in items_data.items():
        if data.get("name", key) == item_name:
            return key
    return None

def creer_lien_objet(item_name):
    """Créer un bouton cliquable vers la page des objets"""
    if item_name and item_name != "Aucun" and objet_existe(item_name):
        return f'<span style="color: #1f77b4; text-decoration: underline; cursor: pointer;" onclick="console.log(\'{item_name}\')">{item_name} 🔗</span>'
    return item_name

def afficher_objet_detail(item_key):
    """Afficher les détails d'un objet avec le format des résistances"""
    items_data = charger_items()
    if item_key in items_data:
        item_data = items_data[item_key]
        item_name = item_data.get("name", item_key)
        
        # Format similaire aux résistances avec icône
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px; padding: 15px; border: 2px solid #444; border-radius: 10px; background-color: rgba(255,255,255,0.05);">
            <span style="font-size: 30px; margin-right: 15px;">📦</span>
            <div style="flex: 1;">
                <div style="font-size: 20px; font-weight: bold; color: var(--text-color); margin-bottom: 5px;">{item_name}</div>
                <div style="color: #888; font-size: 14px;">Type: {item_data.get("type", "Inconnu")}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Description
        if "description" in item_data and item_data["description"]:
            st.write("**Description :**")
            st.info(item_data["description"])
        else:
            st.info("Aucune description disponible")
    else:
        st.error(f"Objet '{item_key}' introuvable")
    
    # Retour à la recherche
    if st.button("🔙 Retour à la recherche de monstres"):
        st.session_state.show_item_page = False
        st.session_state.selected_item = None
        st.rerun()

def get_monstre(nom, monstres):
    """Rechercher un monstre par son nom"""
    for key, m in monstres.items():
        if m["name"].lower() == nom.lower():
            return m
    return None

def get_skills(monstre, talents, skills):
    """Obtenir les talents et compétences d'un monstre"""
    talent_details = []
    
    talents_list = monstre.get("talents", [])
    if talents_list is None:
        return talent_details
    
    for talent_key in talents_list:
        talent = talents.get(talent_key)
        if talent:
            talent_name = talent.get("name", talent_key)
            talent_skills = []
            
            for skill_key, level in talent.get("skills", {}).items():
                skill = skills.get(skill_key)
                if skill:
                    skill_name = skill.get("name", skill_key)
                    mp_cost = skill.get("mp_cost", "?")
                    skill_type = skill.get("type", "Unknown")
                    skill_description = skill.get("description", "Aucune description disponible.")
                    
                    talent_skills.append({
                        "key": skill_key,
                        "name": skill_name,
                        "level": level,
                        "mp_cost": mp_cost,
                        "type": skill_type,
                        "description": skill_description
                    })
                    
            talent_details.append({
                "name": talent_name,
                "skills": talent_skills
            })
    
    return talent_details

def get_traits_info(monstre, traits_db):
    """Obtenir les informations sur les traits d'un monstre"""
    traits_info = {"small": [], "large": []}
    
    for size in ["small", "large"]:
        if size in monstre.get("traits", {}):
            traits_data = monstre["traits"][size]
            if traits_data is not None:
                for trait_key, level in traits_data.items():
                    trait = traits_db.get(trait_key)
                    trait_name = trait.get("name", trait_key) if trait else trait_key
                    trait_desc = trait.get("description", "Description non disponible") if trait else "Description non disponible"
                    traits_info[size].append({
                        "name": trait_name,
                        "level": level,
                        "description": trait_desc
                    })
    
    return traits_info

def get_synthesis_info(monstre, families, monstres):
    """Obtenir les informations de synthèse"""
    synthesis = monstre.get("synthesis")
    if not synthesis:
        return "Aucune synthèse disponible", []
    
    synthesis_items = []
    
    if isinstance(synthesis, list):
        info = "Synthèse :\n"
        for i, combination in enumerate(synthesis):
            if isinstance(combination, list):
                info += f"  Combinaison {i+1}: "
                for item_key in combination:
                    if item_key.startswith("_"):
                        # C'est une famille
                        family_name = families.get(item_key, {}).get("name", item_key)
                        info += f"{family_name} (famille) "
                        synthesis_items.append({"type": "family", "key": item_key, "name": family_name})
                    else:
                        # C'est un monstre
                        monster = monstres.get(item_key)
                        if monster:
                            monster_name = monster.get("name", item_key)
                            info += f"{monster_name} "
                            synthesis_items.append({"type": "monster", "key": item_key, "name": monster_name})
                        else:
                            info += f"{item_key} "
                            synthesis_items.append({"type": "unknown", "key": item_key, "name": item_key})
                info += "\n"
        return info, synthesis_items
    
    return f"Synthèse: {synthesis}", []

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

def get_family_icon(family_key):
    """Obtenir l'icône d'une famille"""
    if not family_key:
        return None
    
    # Enlever le préfixe _ si présent
    family_name = family_key.replace("_", "")
    
    icon_path = os.path.join("data/FamilyIcons", f"{family_name}.png")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    
    return None

def get_rank_icon(rank):
    """Obtenir l'icône d'un rang"""
    if not rank:
        return None
    
    icon_path = os.path.join("data/RankIcons", f"{rank}.png")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    
    return None

def get_resistance_icon(resistance_key):
    """Obtenir l'icône d'une résistance"""
    if not resistance_key:
        return None
    
    # Correspondance pour les noms d'icônes spéciaux
    icon_mapping = {
        "instant_death": "death"
    }
    
    icon_name = icon_mapping.get(resistance_key, resistance_key)
    icon_path = os.path.join("data/ResistanceIcons", f"{icon_name}.png")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    
    return None

def show_synthesis_images(synthesis_items, families_data):
    """Afficher les images de synthèse avec icônes"""
    if not synthesis_items:
        return
    
    st.subheader("Monstres de synthèse")
    
    # Organiser en colonnes
    cols = st.columns(min(len(synthesis_items), 6))
    
    for i, item in enumerate(synthesis_items[:6]):  # Limite à 6
        with cols[i]:
            if item["type"] == "monster":
                # Afficher l'image du monstre
                img = afficher_image_monstre(item["name"])
                if img:
                    st.image(img, width=100, caption=item["name"])
                else:
                    st.info(f"Image: {item['name']}")
            elif item["type"] == "family":
                # Afficher seulement l'icône de la famille
                family_icon = get_family_icon(item["key"])
                if family_icon:
                    st.image(family_icon, width=80, caption=f"Famille {item['name']}")
                else:
                    st.info(f"Famille: {item['name']}")

def show(donnees):
    st.title("Recherche de Monstres")
    
    # Vérifier si on doit afficher les détails d'un objet
    if 'show_item_page' in st.session_state and st.session_state.show_item_page:
        if 'selected_item' in st.session_state and st.session_state.selected_item:
            afficher_objet_detail(st.session_state.selected_item)
            return
    
    # Initialiser la session state pour la recherche
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    
    # Interface de recherche
    col1, col2 = st.columns([2, 1])
    
    with col1:
        nom_monstre = st.text_input("Nom du monstre", 
                                   value=st.session_state.search_query,
                                   placeholder="Ex: Slime, Goonache Goodie...")
        # Mettre à jour la session state si l'utilisateur tape quelque chose
        if nom_monstre != st.session_state.search_query:
            st.session_state.search_query = nom_monstre
    
    with col2:
        st.write("")  # Espacement
        rechercher = st.button("Rechercher", type="primary")
    
    if nom_monstre and (rechercher or nom_monstre):
        monstre = get_monstre(nom_monstre, donnees["monstres"])
        
        if not monstre:
            st.error(f"Monstre '{nom_monstre}' non trouvé.")
            st.info("Essayez avec un nom exact, par exemple: 'Slime', 'Goonache Goodie', 'Shell Slime'")
            return
        
        # Colonnes pour l'affichage
        col_img, col_info = st.columns([1, 2])
        
        # Image du monstre
        with col_img:
            img = afficher_image_monstre(monstre["name"])
            if img:
                st.image(img, width=250, caption=monstre["name"])
            else:
                st.info("Image non disponible")
        
        # Informations générales
        with col_info:
            st.subheader(f"{monstre['name']}")
            
            # Informations de base avec icônes en ligne
            family_key = monstre.get("family", "")
            family_name = donnees["families"].get(family_key, {}).get("name", "Inconnue")
            rank = monstre.get('rank', '?')
            
            # Obtenir les icônes
            family_icon = get_family_icon(family_key)
            rank_icon = get_rank_icon(rank)
            
            # Affichage compact en une seule ligne
            col_num, col_rank, col_family = st.columns([1, 1.5, 1.5])
            
            with col_num:
                st.metric("Numéro", monstre.get('number', '?'))
            
            with col_rank:
                # Afficher seulement l'icône du rang
                if rank_icon:
                    # Convertir l'image en base64 pour l'affichage HTML
                    buffered = BytesIO()
                    rank_icon.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 14px; color: var(--text-color); margin-bottom: 5px;">Rang</div>
                        <img src="data:image/png;base64,{img_str}" width="40" style="display: block; margin: 0 auto;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.metric("Rang", rank)
            
            with col_family:
                # Afficher seulement l'icône de la famille
                if family_icon:
                    # Convertir l'image en base64 pour l'affichage HTML
                    buffered = BytesIO()
                    family_icon.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 14px; color: var(--text-color); margin-bottom: 5px;">Famille</div>
                        <img src="data:image/png;base64,{img_str}" width="40" style="display: block; margin: 0 auto;">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.metric("Famille", family_name)
            
            # Description
            if monstre.get('description'):
                st.write("**Description:**")
                st.write(monstre['description'])

        # Statistiques - Max à gauche, Croissance à droite
        col_stats_max, col_stats_growth = st.columns(2)
        
        with col_stats_max:
            st.subheader("Statistiques maximales")
            maxstats = get_maxstats(monstre["name"], donnees.get("maxstats", []))
            if maxstats:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("HP Max", maxstats.get('hp', '?'), 
                             help="Points de vie maximum")
                    st.metric("ATK Max", maxstats.get('attack', '?'), 
                             help="Attaque maximum")
                with col2:
                    st.metric("MP Max", maxstats.get('mp', '?'), 
                             help="Points de magie maximum")
                    st.metric("DEF Max", maxstats.get('defense', '?'), 
                             help="Défense maximum")
                with col3:
                    st.metric("AGI Max", maxstats.get('agility', '?'), 
                             help="Agilité maximum")
                    st.metric("WIS Max", maxstats.get('wisdom', '?'), 
                             help="Sagesse maximum")
            else:
                st.info("Statistiques maximales non disponibles pour ce monstre")

        with col_stats_growth:
            st.subheader("Gain par niveau")
            growth = monstre.get("growth", {})
            if growth is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("HP", growth.get('hp', '?'))
                    st.metric("ATK", growth.get('atk', '?'))
                with col2:
                    st.metric("MP", growth.get('mp', '?'))
                    st.metric("DEF", growth.get('def', '?'))
                with col3:
                    st.metric("AGI", growth.get('agi', '?'))
                    st.metric("WIS", growth.get('wis', '?'))
            else:
                st.info("Données de croissance non disponibles")
        
        # Talents et Skills
        st.subheader("Talents et Compétences")
        talent_details = get_skills(monstre, donnees["talents"], donnees["skills"])
        if talent_details:
            for talent in talent_details:
                with st.expander(f"{talent['name']}"):
                    for skill in talent['skills']:
                        # Créer des colonnes pour organiser l'affichage
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Affichage principal de la compétence
                            skill_display = f"**{skill['name']}** (Niveau {skill['level']}, MP: {skill['mp_cost']})"
                            st.write(f"• {skill_display}")
                            
                            # Badge pour le type de compétence
                            if skill['type'] == "Attack":
                                st.markdown("`Attaque`")
                            elif skill['type'] == "Healing":
                                st.markdown("`Soin`")
                            elif skill['type'] == "Status":
                                st.markdown("`Statut`")
                            else:
                                st.markdown(f"`{skill['type']}`")
                        
                        with col2:
                            # Bouton pour afficher la description
                            if st.button("Détails", key=f"skill_{skill['key']}_{talent['name']}"):
                                st.session_state[f"show_desc_{skill['key']}"] = not st.session_state.get(f"show_desc_{skill['key']}", False)
                        
                        # Afficher la description si le bouton a été cliqué
                        if st.session_state.get(f"show_desc_{skill['key']}", False):
                            st.info(f"**Description:** {skill['description']}")
                        
                        st.markdown("---")
        else:
            st.info("Aucun talent disponible")
        
        # Traits
        st.subheader("Traits")
        traits_info = get_traits_info(monstre, donnees["traits"])
        
        col_small, col_large = st.columns(2)
        
        with col_small:
            st.write("**Small Traits:**")
            if traits_info['small']:
                for trait in traits_info['small']:
                    with st.expander(f"{trait['name']} (Niv.{trait['level']})"):
                        st.write(trait['description'])
            else:
                st.info("Aucun trait small")
        
        with col_large:
            st.write("**Large Traits:**")
            if traits_info['large']:
                for trait in traits_info['large']:
                    with st.expander(f"{trait['name']} (Niv.{trait['level']})"):
                        st.write(trait['description'])
            else:
                st.info("Aucun trait large")
        
        # Résistances
        st.subheader("Résistances")
        resistances = monstre.get("resistances", {})
        if resistances is not None:
            # Organiser les résistances en deux colonnes
            resistance_items = list(resistances.items())
            
            # Créer deux colonnes principales
            col1, col2 = st.columns(2)
            
            # Diviser les résistances en deux groupes
            mid_point = len(resistance_items) // 2 + (len(resistance_items) % 2)
            left_resistances = resistance_items[:mid_point]
            right_resistances = resistance_items[mid_point:]
            
            # Colonne gauche
            with col1:
                resistance_html_left = ""
                for res_key, value in left_resistances:
                    res_name = donnees["resistances"].get(res_key, {}).get("name", res_key)
                    resistance_icon = get_resistance_icon(res_key)
                    
                    # Déterminer la couleur en fonction de la valeur
                    if value > 0:
                        color = "#4CAF50"  # Vert pour résistance positive
                        symbol = "+"
                    elif value < 0:
                        color = "#F44336"  # Rouge pour faiblesse
                        symbol = ""
                    else:
                        color = "#9E9E9E"  # Gris pour neutre
                        symbol = ""
                    
                    if resistance_icon:
                        # Convertir l'image en base64
                        buffered = BytesIO()
                        resistance_icon.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        resistance_html_left += f"""
                        <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 5px; border: 1px solid #444; border-radius: 5px;">
                            <img src="data:image/png;base64,{img_str}" width="24" style="margin-right: 10px;">
                            <span style="color: var(--text-color); flex: 1;">{res_name}</span>
                            <span style="font-weight: bold; color: {color}; background-color: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 3px;">{symbol}{value}</span>
                        </div>
                        """
                
                st.markdown(resistance_html_left, unsafe_allow_html=True)
            
            # Colonne droite
            with col2:
                resistance_html_right = ""
                for res_key, value in right_resistances:
                    res_name = donnees["resistances"].get(res_key, {}).get("name", res_key)
                    resistance_icon = get_resistance_icon(res_key)
                    
                    # Déterminer la couleur en fonction de la valeur
                    if value > 0:
                        color = "#4CAF50"  # Vert pour résistance positive
                        symbol = "+"
                    elif value < 0:
                        color = "#F44336"  # Rouge pour faiblesse
                        symbol = ""
                    else:
                        color = "#9E9E9E"  # Gris pour neutre
                        symbol = ""
                    
                    if resistance_icon:
                        # Convertir l'image en base64
                        buffered = BytesIO()
                        resistance_icon.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        resistance_html_right += f"""
                        <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 5px; border: 1px solid #444; border-radius: 5px;">
                            <img src="data:image/png;base64,{img_str}" width="24" style="margin-right: 10px;">
                            <span style="color: var(--text-color); flex: 1;">{res_name}</span>
                            <span style="font-weight: bold; color: {color}; background-color: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 3px;">{symbol}{value}</span>
                        </div>
                        """
                
                st.markdown(resistance_html_right, unsafe_allow_html=True)
        else:
            st.info("Données de résistances non disponibles")
        
        # Drops
        st.subheader("Drops")
        drops = monstre.get("drops", {})
        if drops is not None:
            col_normal, col_rare = st.columns(2)
            with col_normal:
                st.write("**Normal:**")
                normal_drop = drops.get('normal', 'Aucun')
                if normal_drop and normal_drop != "Aucun" and objet_existe(normal_drop):
                    # Obtenir le vrai nom de l'objet pour l'affichage
                    display_name = obtenir_nom_objet(normal_drop)
                    if st.button(f"📦 {display_name}", key=f"normal_drop_{normal_drop}"):
                        st.session_state.selected_item = normal_drop
                        st.session_state.show_item_page = True
                        st.rerun()
                else:
                    # Si l'objet n'existe pas, essayer d'afficher le nom quand même
                    display_name = obtenir_nom_objet(normal_drop)
                    st.write(display_name)
                    
            with col_rare:
                st.write("**Rare:**")
                rare_drop = drops.get('rare', 'Aucun')
                if rare_drop and rare_drop != "Aucun" and objet_existe(rare_drop):
                    # Obtenir le vrai nom de l'objet pour l'affichage
                    display_name = obtenir_nom_objet(rare_drop)
                    if st.button(f"📦 {display_name}", key=f"rare_drop_{rare_drop}"):
                        st.session_state.selected_item = rare_drop
                        st.session_state.show_item_page = True
                        st.rerun()
                else:
                    # Si l'objet n'existe pas, essayer d'afficher le nom quand même
                    display_name = obtenir_nom_objet(rare_drop)
                    st.write(display_name)
        else:
            st.info("Aucun drop disponible")
        
        # Synthèse
        st.subheader("Informations de synthèse")
        synthesis_info, synthesis_items = get_synthesis_info(monstre, donnees["families"], donnees["monstres"])
        
        if synthesis_items:
            st.write(synthesis_info)
            show_synthesis_images(synthesis_items, donnees["families"])
        else:
            st.info("Aucune synthèse disponible")
    
    else:
        # Page d'aide quand aucune recherche
        st.info("Entrez le nom d'un monstre pour voir ses informations complètes")
        
        # Suggestions
        st.subheader("Suggestions")
        col1, col2, col3 = st.columns(3)
        
        suggestions = ["Slime", "Goonache Goodie", "Shell Slime", "Metal Slime", "King Slime", "Bubble Slime"]
        
        for i, suggestion in enumerate(suggestions):
            with [col1, col2, col3][i % 3]:
                if st.button(f"{suggestion}", key=f"suggest_{i}"):
                    st.session_state.search_query = suggestion
                    st.rerun()
