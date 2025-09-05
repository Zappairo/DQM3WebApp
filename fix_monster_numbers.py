#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les incohérences entre monster ID et number dans les fichiers JSON
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

def analyze_inconsistencies():
    """Analyse les incohérences entre monster2.json et monsters.json"""
    
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
    
    # Créer un mapping par nom et identifier pour monster2.json
    monster2_by_name = {}
    monster2_by_identifier = {}
    
    for monster in monster2_data:
        if monster.get("Name"):
            monster2_by_name[monster["Name"].lower()] = monster
        if monster.get("Identifier"):
            monster2_by_identifier[monster["Identifier"]] = monster
    
    print(f"\nMapping créé avec {len(monster2_by_name)} noms et {len(monster2_by_identifier)} identifiants")
    
    # Analyser les incohérences entre les champs "number"
    inconsistencies = []
    matches_found = 0
    
    for monster_key, monster_data in monsters_data.items():
        current_number = monster_data.get("number")
        monster_name = monster_data.get("name", "")
        
        # Chercher par nom d'abord, puis par identifier
        match = None
        if monster_name.lower() in monster2_by_name:
            match = monster2_by_name[monster_name.lower()]
        elif monster_key in monster2_by_identifier:
            match = monster2_by_identifier[monster_key]
        
        if match:
            matches_found += 1
            monster2_number = match.get("Number")
            
            # Comparer les champs "number" et "Number"
            if monster2_number is not None and current_number != monster2_number:
                inconsistencies.append({
                    "key": monster_key,
                    "name": monster_name,
                    "current_number": current_number,
                    "correct_number": monster2_number,
                    "identifier": match.get("Identifier")
                })
    
    print(f"\nCorrespondances trouvées: {matches_found}")
    print(f"Incohérences détectées: {len(inconsistencies)}")
    
    if inconsistencies:
        print("\n=== INCOHÉRENCES DÉTECTÉES ===")
        for inc in inconsistencies[:10]:  # Afficher les 10 premières
            print(f"Clé: {inc['key']}")
            print(f"  Nom: {inc['name']}")
            print(f"  Number actuel dans monsters.json: {inc['current_number']}")
            print(f"  Number correct dans monster2.json: {inc['correct_number']}")
            print(f"  Identifier: {inc['identifier']}")
            print()
        
        if len(inconsistencies) > 10:
            print(f"... et {len(inconsistencies) - 10} autres incohérences")
    
    return inconsistencies, monsters_data

def fix_inconsistencies(inconsistencies, monsters_data):
    """Corrige les incohérences en mettant à jour les numbers"""
    
    if not inconsistencies:
        print("Aucune incohérence à corriger.")
        return
    
    print(f"\nCorrection de {len(inconsistencies)} incohérences...")
    
    # Créer une sauvegarde
    backup_path = "data/monsters.json.backup"
    if not os.path.exists(backup_path):
        print("Création d'une sauvegarde...")
        save_json_file(backup_path, monsters_data)
    
    # Appliquer les corrections
    corrections_applied = 0
    for inc in inconsistencies:
        monster_key = inc["key"]
        correct_number = inc["correct_number"]
        
        if monster_key in monsters_data:
            old_number = monsters_data[monster_key]["number"]
            monsters_data[monster_key]["number"] = correct_number
            print(f"Corrigé {monster_key}: {old_number} → {correct_number}")
            corrections_applied += 1
    
    print(f"\n{corrections_applied} corrections appliquées.")
    
    # Sauvegarder le fichier corrigé
    if save_json_file("data/monsters.json", monsters_data):
        print("Fichier monsters.json mis à jour avec succès!")
    else:
        print("Erreur lors de la sauvegarde du fichier corrigé.")

def main():
    """Fonction principale"""
    print("=== ANALYSE ET CORRECTION DES MONSTER NUMBERS ===\n")
    
    inconsistencies, monsters_data = analyze_inconsistencies()
    
    if inconsistencies:
        response = input(f"\nVoulez-vous corriger ces {len(inconsistencies)} incohérences? (y/N): ")
        if response.lower() in ['y', 'yes', 'o', 'oui']:
            fix_inconsistencies(inconsistencies, monsters_data)
        else:
            print("Correction annulée.")
    else:
        print("Aucune incohérence trouvée!")

if __name__ == "__main__":
    main()
