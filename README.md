# Dragon Quest Monsters - App Dex

Application web Streamlit pour Dragon Quest Monsters : Le Prince des Ténèbres.

## Fonctionnalitées disponibles

- **Recherche de Monstres** : Recherche détaillée avec statistiques, talents, traits et synthèse
- **Base de Données** : Liste en WIP de tout les monstres, talents et skills
- **Synthèse** : Calculateur et guide de synthèse

## Déploiement sur Streamlit Cloud

### Structure du projet
```
DQM Testouille la frippouille/
├── app.py                    # Application principale
├── requirements.txt          # Dépendances
├── page/
│   ├── __init__.py
│   ├── __pycache__.py
│   ├── accueil.py            # Page d'accueil
│   ├── recherche_monstres.py # Recherche de monstres
│   ├── base_donnees.py       # Base de données
│   └── synthese.py           # Synthèse
└── data/
    ├── monsters.json         # Données des monstres
    ├── talents.json          # Données des talents
    ├── skills.json           # Données des compétences
    ├── traits.json           # Données des traits
    ├── families.json         # Données des familles
    ├── resistances.json      # Données des résistances
    └── MonsterImages/        # Images des monstres
        ├── Slime.1.jpg
        ├── Goonache_Goodie.1.jpg
        └── ...
```

### Instructions de déploiement

1. **Préparation du repository GitHub**
   ```bash
   git add .
   git commit -m "DQM3WebApp"
   git push origin main
   ```

2. **Déploiement sur Streamlit Cloud**
   - Allez sur [share.streamlit.io](https://share.streamlit.io)
   - Connectez votre compte GitHub
   - Sélectionnez le repository
   - Main file path: `streamlit_app.py`
   - Cliquez sur "Deploy"

3. **Configuration**
   - L'application se déploiera automatiquement
   - Les dépendances seront installées via `requirements.txt`

## 🎮 Utilisation

### Page d'Accueil
- Vue d'ensemble de l'application
- Statistiques générales
- Navigation guidée

### Recherche de Monstres
- Recherche par nom exact
- Affichage des statistiques complètes
- Visualisation des talents et compétences
- Informations de synthèse avec images

### Base de Données
- Liste complète des monstres
- Filtres par famille, rang et nom
- Tableaux interactifs
- Statistiques en temps réel

### Synthèse
- Recherche de combinaisons
- Liste des synthèses disponibles
- Guide interactif

## 🛠️ Technologies

- **Streamlit** : Framework web Python
- **Pillow** : Traitement d'images
- **Pandas** : Manipulation de données
- **JSON** : Base de données

## 📊 Données

L'application utilise des fichiers JSON contenant :
- 500+ monstres avec statistiques complètes
- 200+ compétences détaillées
- 100+ traits avec descriptions
- 8 familles de monstres
- Données de résistances et de synthèses

## 🌐 URL de déploiement

Pas encore déployé

## 🔧 Développement local

```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement de l'application
streamlit run streamlit_app.py
```
