# project_facture_ia

## Description

`project_facture_ia` est une application permettant d’utiliser l’intelligence artificielle pour traiter et analyser des factures.

Le projet est composé de trois parties principales :

* **Une page web** permettant à l’utilisateur d’interagir avec l’application.
* **Un backend Python** chargé de recevoir les données, de gérer le traitement et de communiquer avec l’IA.
* **Une intelligence artificielle** chargée d’analyser les informations provenant des factures et de générer le résultat attendu.

Le fonctionnement général est le suivant :

```text
Utilisateur
     │
     ▼
┌─────────────────┐
│     Page Web    │
└────────┬────────┘
         │
         │ Requête
         ▼
┌─────────────────┐
│ Python Backend  │
└────────┬────────┘
         │
         │ Données / Prompt
         ▼
┌─────────────────┐
│       IA        │
└────────┬────────┘
         │
         │ Résultat
         ▼
┌─────────────────┐
│ Python Backend  │
└────────┬────────┘
         │
         │ Résultat final
         ▼
┌─────────────────┐
│     Page Web    │
└─────────────────┘
```

## Fonctionnement

L'utilisateur commence par accéder à l'interface web et fournit les informations nécessaires au traitement de la facture.

La page web transmet ensuite la requête au backend Python.

Le backend Python prépare les données et les transmet à l'intelligence artificielle. L'IA analyse les informations reçues et retourne une réponse.

Python récupère cette réponse, effectue si nécessaire les traitements complémentaires, puis renvoie le résultat à la page web.

Enfin, le résultat est affiché à l'utilisateur.

Le flux de données est donc :

```text
Page Web
   ↓
Python
   ↓
IA
   ↓
Python
   ↓
Page Web
```

## Structure du projet

```text
project_facture_ia/
│
├── <fichier_python>.py
│
├── <dossier_web>/
│   ├── <fichier_html>
│   ├── <fichier_css>
│   └── <fichier_javascript>
│
├── requirements.txt
│
└── README.md
```

### Principaux éléments

| Élément            | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| Python             | Gère le backend et la logique de l'application.              |
| Page Web           | Permet à l'utilisateur d'interagir avec l'application.       |
| IA                 | Analyse les données et génère les résultats.                 |
| `requirements.txt` | Contient les dépendances Python nécessaires.                 |
| `README.md`        | Contient la documentation et les instructions d'utilisation. |

## Technologies utilisées

Le projet utilise principalement :

* **Python** pour le backend ;
* **HTML** pour la structure de la page web ;
* **CSS** pour la mise en forme ;
* **JavaScript** pour les interactions avec l'interface et le backend ;
* **Intelligence artificielle** pour l'analyse des factures.

## Prérequis

Avant de lancer le projet, il faut avoir installé :

* Python 3 ;
* pip ;
* un navigateur web ;
* les éventuelles clés API nécessaires au fonctionnement de l'IA.

Vérifier l'installation de Python :

```bash
python --version
```

ou :

```bash
python3 --version
```

## Installation

### 1. Cloner le projet

```bash
git clone <URL_DU_REPOSITORY>
```

Entrer ensuite dans le dossier :

```bash
cd project_facture_ia
```

### 2. Créer un environnement virtuel

Sous Windows :

```bash
python -m venv venv
venv\Scripts\activate
```

Sous Linux/macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

Installer les dépendances nécessaires avec :

```bash
pip install -r requirements.txt
```

## Configuration

Si le projet utilise une clé API pour communiquer avec le service d'intelligence artificielle, celle-ci doit être configurée avant le lancement.

Par exemple, créer un fichier `.env` :

```text
API_KEY=<VOTRE_CLE_API>
```

Ne jamais publier une clé API dans le code source ou dans un dépôt Git public.

Il est recommandé d'ajouter le fichier `.env` au `.gitignore` :

```text
.env
venv/
__pycache__/
```

## Lancement

Une fois l'installation terminée, lancer le backend Python :

```bash
python <fichier_python>.py
```

ou :

```bash
python3 <fichier_python>.py
```

Le serveur démarre alors localement.

L'adresse affichée dans le terminal peut être de la forme :

```text
http://localhost:<PORT>
```

Ouvrir cette adresse dans un navigateur pour accéder à l'application.

## Utilisation

Une fois l'application lancée :

1. Ouvrir l'interface web.
2. Fournir la facture ou les informations nécessaires.
3. Lancer le traitement.
4. La page web envoie les données au backend Python.
5. Python transmet les informations à l'IA.
6. L'IA analyse les données.
7. Le résultat est retourné au backend Python.
8. Le résultat final est affiché sur la page web.

## Architecture

L'architecture de `project_facture_ia` repose sur une séparation entre l'interface utilisateur, le backend et l'intelligence artificielle.

```text
┌──────────────────────┐
│      Utilisateur     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Page Web       │
│ HTML / CSS / JS      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Backend Python    │
│   Traitement / API   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────-----┐
│ Intelligence Artificielle │
│ Analyse des factures      │
└──────────┬───────────-----┘
           │
           ▼
┌──────────────────────┐
│    Backend Python    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Page Web       │
│ Affichage du résultat│
└──────────────────────┘
```

## Gestion des erreurs

En cas de problème, vérifier :

1. que Python est correctement installé ;
2. que l'environnement virtuel est activé ;
3. que les dépendances ont été installées ;
4. que les variables d'environnement ou clés API sont correctement configurées ;
5. que le backend Python est bien lancé ;
6. que l'adresse et le port utilisés sont corrects ;
7. les messages d'erreur affichés dans le terminal.

## Arrêter l'application

Pour arrêter le serveur, utiliser :

```text
Ctrl + C
```

dans le terminal où le serveur Python est exécuté.

## Sécurité

Les clés API et autres informations sensibles ne doivent jamais être intégrées directement au code source.

Utiliser des variables d'environnement pour stocker ces informations et ne pas publier le fichier `.env`.

## Améliorations possibles

Le projet peut être amélioré par l'ajout de fonctionnalités telles que :

* une meilleure interface utilisateur ;
* une meilleure gestion des erreurs ;
* la prise en charge de différents formats de factures ;
* l'extraction automatique des informations importantes ;
* l'ajout d'une base de données ;
* l'historique des factures traitées ;
* l'authentification des utilisateurs ;
* le déploiement de l'application sur un serveur.

## Auteur

**Projet :** `project_facture_ia`
**Auteur :** `<Jallouli / oumaima>`
**Date :** `<Date>`

## Licence

Ce projet est réalisé dans le cadre de `<formation /  projet personnel>`.