#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour importer les données manquantes de monster2.json vers monsters.json
"""

import json
import os

def load_json_file(filepath):
    """Charge un fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement de {filepath}: {e}")
        return None

def save_json_file(filepath, data):
    """Sauvegarde un fichier JSON"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de {filepath}: {e}")
        return False

def get_rank_name(rank_id):
    """Convertit RankId en nom de rang"""
    rank_mapping = {
        1: "G",
        2: "F", 
        3: "E",
        4: "D",
        5: "C",
        6: "B",
        7: "A",
        8: "S",
        9: "SS",
        10: "???"
    }
    return rank_mapping.get(rank_id, "Unknown")

def get_family_name(family_id):
    """Convertit FamilyId en nom de famille"""
    family_mapping = {
        1: "_slime",
        2: "_dragon", 
        3: "_nature",
        4: "_beast",
        5: "_material",
        6: "_demon",
        7: "_undead",
        8: "_special"
    }
    return family_mapping.get(family_id, "_unknown")

def import_monster_data():
    """Importe les données de monster2.json vers monsters.json"""
    
    # Chemins des fichiers
    monsters_path = "data/monsters.json"
    monster2_path = "data/monster2.json"
    
    # Chargement des données
    print("Chargement des fichiers JSON...")
    monsters_data = load_json_file(monsters_path)
    monster2_data = load_json_file(monster2_path)
    
    if not monsters_data or not monster2_data:
        print("Impossible de charger les fichiers JSON")
        return
    
    print(f"Nombre de monstres dans monsters.json: {len(monsters_data)}")
    print(f"Nombre d'entrées dans monster2.json: {len(monster2_data)}")
    
    # Créer un mapping par Number pour monster2.json
    monster2_by_number = {}
    for monster in monster2_data:
        number = monster.get("Number")
        if number is not None:
            monster2_by_number[number] = monster
    
    print(f"Mapping créé avec {len(monster2_by_number)} monstres ayant un Number")
    
    # Analyser les données à importer
    updates_needed = []
    stats_to_check = ['HP', 'MP', 'Att', 'Def', 'Agi', 'Wis']
    max_stats_to_check = ['MaxHP', 'MaxMP', 'MaxAtt', 'MaxDef', 'MaxAgi', 'MaxWis']
    
    for monster_key, monster_data in monsters_data.items():
        monster_number = monster_data.get("number")
        
        if monster_number in monster2_by_number:
            monster2_entry = monster2_by_number[monster_number]
            updates = {}
            
            # 1. Rang (rank)
            rank_id = monster2_entry.get("RankId")
            if rank_id is not None:
                new_rank = get_rank_name(rank_id)
                current_rank = monster_data.get("rank")
                if current_rank != new_rank:
                    updates['rank'] = {'old': current_rank, 'new': new_rank}
            
            # 2. Famille (family)
            family_id = monster2_entry.get("FamilyId")
            if family_id is not None:
                new_family = get_family_name(family_id)
                current_family = monster_data.get("family")
                if current_family != new_family:
                    updates['family'] = {'old': current_family, 'new': new_family}
            
            # 3. Nom français
            french_name = monster2_entry.get("FrenchName")
            if french_name and french_name.strip():
                updates['french_name'] = {'old': None, 'new': french_name}
            
            # 4. Trivia (dans description)
            trivia = monster2_entry.get("Trivia")
            current_description = monster_data.get("description") or ""
            if trivia and trivia.strip():
                # Ajouter la trivia à la description existante
                new_description = current_description
                if current_description and not current_description.endswith('.'):
                    new_description += ". "
                elif current_description:
                    new_description += " "
                new_description += f"Trivia: {trivia}"
                updates['description'] = {'old': current_description, 'new': new_description}
            
            # 5. Growth stats
            growth_updates = {}
            stat_mapping = {'HP': 'hp', 'MP': 'mp', 'Att': 'atk', 'Def': 'def', 'Agi': 'agi', 'Wis': 'wis'}
            
            for monster2_stat, monsters_stat in stat_mapping.items():
                monster2_value = monster2_entry.get(monster2_stat)
                if monster2_value is not None:
                    current_growth = monster_data.get("growth") or {}
                    current_value = current_growth.get(monsters_stat) if isinstance(current_growth, dict) else None
                    if current_value != monster2_value:
                        growth_updates[monsters_stat] = {'old': current_value, 'new': monster2_value}
            
            if growth_updates:
                updates['growth'] = growth_updates
            
            # 6. Max stats (créer une nouvelle section)
            max_stats = {}
            max_stat_mapping = {'MaxHP': 'max_hp', 'MaxMP': 'max_mp', 'MaxAtt': 'max_atk', 
                               'MaxDef': 'max_def', 'MaxAgi': 'max_agi', 'MaxWis': 'max_wis'}
            
            for monster2_stat, monsters_stat in max_stat_mapping.items():
                monster2_value = monster2_entry.get(monster2_stat)
                if monster2_value is not None:
                    max_stats[monsters_stat] = monster2_value
            
            if max_stats:
                updates['max_stats'] = {'old': None, 'new': max_stats}
            
            if updates:
                updates_needed.append({
                    'key': monster_key,
                    'name': monster_data.get('name'),
                    'number': monster_number,
                    'updates': updates
                })
    
    print(f"\nMonstres nécessitant des mises à jour: {len(updates_needed)}")
    
    if updates_needed:
        print("\n=== APERÇU DES MISES À JOUR ===")
        for i, update in enumerate(updates_needed[:5]):  # Afficher les 5 premiers
            print(f"Monster: {update['name']} (#{update['number']})")
            for field, change in update['updates'].items():
                if field == 'growth':
                    print(f"  Growth stats: {len(change)} modifications")
                elif field == 'max_stats':
                    print(f"  Max stats: {len(change['new'])} nouvelles valeurs")
                else:
                    print(f"  {field}: {change['old']} → {change['new']}")
            print()
        
        if len(updates_needed) > 5:
            print(f"... et {len(updates_needed) - 5} autres monstres")
    
    return updates_needed, monsters_data

def apply_updates(updates_needed, monsters_data):
    """Applique les mises à jour aux données des monstres"""
    
    if not updates_needed:
        print("Aucune mise à jour à appliquer.")
        return
    
    print(f"\nApplication de {len(updates_needed)} mises à jour...")
    
    # Créer une sauvegarde
    backup_path = "data/monsters.json.backup2"
    if not os.path.exists(backup_path):
        print("Création d'une sauvegarde...")
        save_json_file(backup_path, monsters_data)
    
    # Appliquer les mises à jour
    updates_applied = 0
    
    for update in updates_needed:
        monster_key = update['key']
        monster_updates = update['updates']
        
        if monster_key in monsters_data:
            monster = monsters_data[monster_key]
            
            # Appliquer chaque mise à jour
            for field, change in monster_updates.items():
                if field == 'rank':
                    monster['rank'] = change['new']
                elif field == 'family':
                    monster['family'] = change['new']
                elif field == 'french_name':
                    monster['french_name'] = change['new']
                elif field == 'description':
                    monster['description'] = change['new']
                elif field == 'growth':
                    if 'growth' not in monster or monster['growth'] is None:
                        monster['growth'] = {}
                    for stat, stat_change in change.items():
                        monster['growth'][stat] = stat_change['new']
                elif field == 'max_stats':
                    monster['max_stats'] = change['new']
            
            updates_applied += 1
            if updates_applied <= 5:  # Afficher les 5 premiers
                print(f"Mis à jour: {update['name']} (#{update['number']})")
    
    print(f"\n{updates_applied} mises à jour appliquées.")
    
    # Sauvegarder le fichier mis à jour
    if save_json_file("data/monsters.json", monsters_data):
        print("Fichier monsters.json mis à jour avec succès!")
    else:
        print("Erreur lors de la sauvegarde du fichier mis à jour.")

def main():
    """Fonction principale"""
    print("=== IMPORT DES DONNÉES DE MONSTER2.JSON ===\n")
    
    updates_needed, monsters_data = import_monster_data()
    
    if updates_needed:
        response = input(f"\nVoulez-vous appliquer ces {len(updates_needed)} mises à jour? (y/N): ")
        if response.lower() in ['y', 'yes', 'o', 'oui']:
            apply_updates(updates_needed, monsters_data)
        else:
            print("Mise à jour annulée.")
    else:
        print("Aucune mise à jour nécessaire!")

if __name__ == "__main__":
    main()
