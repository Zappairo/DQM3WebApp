import streamlit as st
from PIL import Image
import os

def get_maxstats(monstre_name, maxstats_data):
    """Obtenir les statistiques maximales d'un monstre"""
    for monster in maxstats_data:
        if monster["name"].lower() == monstre_name.lower():
            return monster["stats"]
    return None

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

def show_synthesis_images(synthesis_items):
    """Afficher les images de synthèse"""
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
                # Afficher la famille
                st.info(f"Famille: {item['name']}")

def show(donnees):
    st.title("Recherche de Monstres")
    
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
            
            # Informations de base
            family_name = donnees["families"].get(monstre.get("family", ""), {}).get("name", "Inconnue")
            
            col_base1, col_base2, col_base3 = st.columns(3)
            with col_base1:
                st.metric("Numéro", monstre.get('number', '?'))
            with col_base2:
                st.metric("Rang", monstre.get('rank', '?'))
            with col_base3:
                st.metric("Famille", family_name)
            
            # Description
            if monstre.get('description'):
                st.write("**Description:**")
                st.write(monstre['description'])

        # Gain de statistiques par niveau
        st.subheader("Gain de statistiques par niveau")
        growth = monstre.get("growth", {})
        if growth is not None:
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("HP", growth.get('hp', '?'))
            with col2:
                st.metric("MP", growth.get('mp', '?'))
            with col3:
                st.metric("ATK", growth.get('atk', '?'))
            with col4:
                st.metric("DEF", growth.get('def', '?'))
            with col5:
                st.metric("AGI", growth.get('agi', '?'))
            with col6:
                st.metric("WIS", growth.get('wis', '?'))
        else:
            st.info("Données de croissance non disponibles")
        
        # Statistiques maximales
        st.subheader("Statistiques maximales")
        maxstats = get_maxstats(monstre["name"], donnees.get("maxstats", []))
        if maxstats:
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("HP Max", maxstats.get('hp', '?'), 
                         help="Points de vie maximum")
            with col2:
                st.metric("MP Max", maxstats.get('mp', '?'), 
                         help="Points de magie maximum")
            with col3:
                st.metric("ATK Max", maxstats.get('attack', '?'), 
                         help="Attaque maximum")
            with col4:
                st.metric("DEF Max", maxstats.get('defense', '?'), 
                         help="Défense maximum")
            with col5:
                st.metric("AGI Max", maxstats.get('agility', '?'), 
                         help="Agilité maximum")
            with col6:
                st.metric("WIS Max", maxstats.get('wisdom', '?'), 
                         help="Sagesse maximum")
        else:
            st.info("Statistiques maximales non disponibles pour ce monstre")
        
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
            resistance_data = []
            for res_key, value in resistances.items():
                res_name = donnees["resistances"].get(res_key, {}).get("name", res_key)
                symbol = "+" if value > 0 else ""
                color = "[+]" if value > 0 else "[-]" if value < 0 else "[=]"
                resistance_data.append([f"{color} {res_name}", f"{symbol}{value}%"])
            
            # Afficher en colonnes
            cols = st.columns(4)
            for i, (name, value) in enumerate(resistance_data):
                with cols[i % 4]:
                    st.write(f"{name}: **{value}**")
        else:
            st.info("Données de résistances non disponibles")
        
        # Drops
        st.subheader("Drops")
        drops = monstre.get("drops", {})
        if drops is not None:
            col_normal, col_rare = st.columns(2)
            with col_normal:
                st.write(f"**Normal:** {drops.get('normal', 'Aucun')}")
            with col_rare:
                st.write(f"**Rare:** {drops.get('rare', 'Aucun')}")
        else:
            st.info("Aucun drop disponible")
        
        # Synthèse
        st.subheader("Informations de synthèse")
        synthesis_info, synthesis_items = get_synthesis_info(monstre, donnees["families"], donnees["monstres"])
        
        if synthesis_items:
            st.write(synthesis_info)
            show_synthesis_images(synthesis_items)
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
