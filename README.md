# project_facture_ia

## Description

`project_facture_ia` est une application web permettant d'utiliser l'intelligence artificielle pour traiter et analyser des factures.

L'objectif du projet est de mettre en place une application capable de recevoir les informations nécessaires concernant une facture, de les transmettre à une intelligence artificielle pour analyse, puis de récupérer et d'afficher le résultat de manière structurée.

Le projet est composé de trois parties principales :

* **Une interface web** permettant à l'utilisateur d'interagir avec l'application ;
* **Un backend Python avec Flask** chargé de gérer les requêtes, le traitement des données et la communication avec l'intelligence artificielle ;
* **Une intelligence artificielle** chargée d'analyser les données de la facture et de produire les informations demandées.

Le fonctionnement général est le suivant :

```text
Utilisateur
     │
     ▼
┌─────────────────┐
│    Page Web     │
│   HTML/CSS/JS   │
└────────┬────────┘
         │
         │ Requête HTTP
         ▼
┌─────────────────┐
│ Backend Flask   │
│     Python      │
└────────┬────────┘
         │
         │ Données / Prompt
         ▼
┌─────────────────┐
│       IA        │
│   OpenAI API    │
└────────┬────────┘
         │
         │ Résultat
         ▼
┌─────────────────┐
│ Backend Flask   │
│     Python      │
└────────┬────────┘
         │
         │ Résultat final
         ▼
┌─────────────────┐
│    Page Web     │
│ Affichage       │
└─────────────────┘
```

## Fonctionnement

L'utilisateur commence par accéder à l'interface web de l'application.

Il fournit ensuite les informations nécessaires au traitement de la facture à travers l'interface.

La page web envoie une requête au backend Flask.

Le backend Python reçoit les données, les prépare et construit la requête destinée à l'intelligence artificielle.

Les données ainsi que les instructions nécessaires sont ensuite transmises à l'API d'intelligence artificielle.

L'intelligence artificielle analyse les informations reçues et retourne une réponse.

Le backend Flask récupère cette réponse et effectue, si nécessaire, les traitements complémentaires permettant de préparer le résultat final.

Enfin, le résultat est transmis à l'interface web et présenté à l'utilisateur.

Le flux principal de l'application est donc :

```text
Page Web
    ↓
Flask / Python
    ↓
OpenAI API
    ↓
Flask / Python
    ↓
Page Web
```

## Structure du projet

```text
project_facture_ia/
│
├── app.py
│
├── test_api.py
├── test_ai.py
│
├── static/
│   ├── style.css
│   └── app.js
│
├── templates/
│   └── index.html
│
├── uploads/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Principaux éléments

| Élément            | Description                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `app.py`           | Application principale Flask et logique du backend                                        |
| `test_api.py`      | Fichier utilisé pour tester le fonctionnement de l'API                                    |
| `test_ai.py`       | Fichier utilisé pour tester la communication avec l'IA                                    |
| `templates/`       | Contient les pages HTML de l'application                                                  |
| `static/`          | Contient les fichiers CSS et JavaScript                                                   |
| `uploads/`         | Répertoire utilisé pour les fichiers transmis à l'application lorsque cela est nécessaire |
| `.env`             | Contient les variables d'environnement et informations sensibles                          |
| `.gitignore`       | Définit les fichiers qui ne doivent pas être envoyés vers Git                             |
| `requirements.txt` | Contient les dépendances Python du projet                                                 |
| `README.md`        | Documentation du projet                                                                   |

## Technologies utilisées

Le projet utilise principalement les technologies suivantes :

* **Python** pour le développement du backend ;
* **Flask** pour créer le serveur web et gérer les requêtes ;
* **HTML** pour la structure de l'interface ;
* **CSS** pour la mise en forme de l'application ;
* **JavaScript** pour les interactions côté client ;
* **OpenAI API** pour communiquer avec le modèle d'intelligence artificielle ;
* **JSON** pour structurer et échanger les données ;
* **Git** pour le contrôle de version ;
* **GitHub** pour l'hébergement du code source.

## Prérequis

Avant de lancer le projet, les éléments suivants doivent être installés :

* Python 3 ;
* pip ;
* Git ;
* un navigateur web ;
* une clé API permettant d'utiliser le service d'intelligence artificielle.

Pour vérifier l'installation de Python :

```bash
python --version
```

ou :

```bash
python3 --version
```

Pour vérifier l'installation de pip :

```bash
pip --version
```

Pour vérifier Git :

```bash
git --version
```

## Installation

### 1. Cloner le projet

Cloner le dépôt GitHub :

```bash
git clone <URL_DU_REPOSITORY>
```

Entrer ensuite dans le dossier du projet :

```bash
cd project_facture_ia
```

### 2. Créer un environnement virtuel

Sous Windows :

```bash
python -m venv venv
```

Activer l'environnement virtuel :

```bash
venv\Scripts\activate
```

Sous Linux/macOS :

```bash
python3 -m venv venv
```

Puis :

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

Installer les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

## Configuration

L'application utilise une clé API pour communiquer avec le service d'intelligence artificielle.

Créer un fichier `.env` à la racine du projet :

```text
OPENAI_API_KEY=<VOTRE_CLE_API>
```

La clé API doit rester privée.

Elle ne doit jamais être écrite directement dans le code source ni publiée dans un dépôt GitHub public.

Le fichier `.env` doit être ajouté au fichier `.gitignore` :

```text
.env
venv/
__pycache__/
uploads/
```

## Lancement

Une fois l'installation et la configuration terminées, activer l'environnement virtuel puis lancer l'application Flask :

```bash
python app.py
```

Le serveur Flask démarre alors localement.

L'application est généralement accessible à l'adresse :

```text
http://127.0.0.1:5000
```

ou :

```text
http://localhost:5000
```

Ouvrir l'une de ces adresses dans un navigateur pour accéder à l'application.

## Utilisation

Une fois l'application lancée :

1. Ouvrir l'interface web ;
2. Fournir les informations nécessaires concernant la facture ;
3. Valider la demande ;
4. La page web envoie les données au backend Flask ;
5. Flask prépare les données et construit la requête destinée à l'IA ;
6. Le backend transmet les informations à l'API OpenAI ;
7. L'intelligence artificielle analyse les données ;
8. L'API retourne la réponse au backend ;
9. Flask traite la réponse ;
10. Le résultat final est envoyé à l'interface web ;
11. Le résultat est affiché à l'utilisateur.

## Architecture

L'architecture de `project_facture_ia` repose sur une séparation entre l'interface utilisateur, le backend Python et le service d'intelligence artificielle.

```text
┌──────────────────────────┐
│        Utilisateur       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        Interface Web     │
│       HTML / CSS / JS    │
└────────────┬─────────────┘
             │
             │ Requête HTTP
             ▼
┌──────────────────────────┐
│       Backend Flask      │
│          Python          │
│  Traitement / Logique    │
└────────────┬─────────────┘
             │
             │ API Request
             ▼
┌──────────────────────────┐
│    Service IA / OpenAI   │
│ Analyse et traitement    │
└────────────┬─────────────┘
             │
             │ Réponse
             ▼
┌──────────────────────────┐
│       Backend Flask      │
│     Traitement résultat  │
└────────────┬─────────────┘
             │
             │ Réponse HTTP
             ▼
┌──────────────────────────┐
│        Interface Web     │
│    Affichage résultat    │
└──────────────────────────┘
```

## Communication entre les composants

La communication entre les différentes parties de l'application peut être représentée comme suit :

```text
Client Web
    │
    │ HTTP Request
    ▼
Flask
    │
    │ Données + Prompt
    ▼
OpenAI API
    │
    │ Réponse IA
    ▼
Flask
    │
    │ HTTP Response
    ▼
Client Web
```

Le backend Flask joue donc le rôle d'intermédiaire entre l'utilisateur et le service d'intelligence artificielle.

Cette organisation permet de séparer clairement :

* la présentation ;
* la logique applicative ;
* la communication avec l'IA.

## Gestion des données

Les données échangées entre le frontend et le backend sont structurées afin de faciliter leur traitement.

Le format JSON peut notamment être utilisé pour transmettre les informations entre les différents composants.

Exemple de structure :

```json
{
    "invoice_number": "INV-001",
    "date": "2026-08-19",
    "supplier": "Example Company",
    "total": 1500,
    "currency": "MAD"
}
```

La structure exacte des données dépend des informations demandées par l'application.

## Gestion de l'intelligence artificielle

L'intelligence artificielle est utilisée pour analyser les informations fournies au système.

Le backend Python prépare les données et les instructions avant de les envoyer au modèle.

Le résultat retourné par l'IA est ensuite récupéré par Flask afin d'être traité et présenté à l'utilisateur.

Cette architecture permet de modifier ou d'améliorer la logique de traitement côté backend sans modifier directement l'interface utilisateur.

## Gestion des erreurs

En cas de problème, vérifier les éléments suivants :

1. que Python est correctement installé ;
2. que l'environnement virtuel est activé ;
3. que les dépendances sont installées ;
4. que le fichier `.env` existe ;
5. que la clé API est correctement configurée ;
6. que la connexion au service d'IA fonctionne ;
7. que le backend Flask est correctement lancé ;
8. que l'adresse et le port utilisés sont corrects ;
9. les messages d'erreur affichés dans le terminal.

Les erreurs liées à l'API peuvent également être dues à une clé invalide, à des restrictions de compte ou à des limites d'utilisation du service.

## Tests

Le projet contient des fichiers permettant de tester différents composants de l'application.

### Test de l'API

Le fichier :

```text
test_api.py
```

permet de vérifier le fonctionnement de la communication avec l'API.

Il peut être exécuté avec :

```bash
python test_api.py
```

### Test de l'intelligence artificielle

Le fichier :

```text
test_ai.py
```

permet de tester la communication avec le modèle d'intelligence artificielle.

Il peut être exécuté avec :

```bash
python test_ai.py
```

Ces tests permettent d'identifier plus facilement les problèmes liés à la configuration ou à la communication avec les services externes.

## Sécurité

Les informations sensibles doivent être protégées.

Les clés API ne doivent jamais être intégrées directement dans le code source.

Il est recommandé d'utiliser des variables d'environnement :

```text
OPENAI_API_KEY=<VOTRE_CLE_API>
```

Le fichier `.env` doit être exclu du dépôt Git :

```text
.env
```

Il est également recommandé de ne pas publier dans un dépôt public des données réelles ou confidentielles provenant de factures.

## Améliorations possibles

Le projet peut être amélioré par l'ajout de plusieurs fonctionnalités :

* amélioration de l'interface utilisateur ;
* amélioration de la gestion des erreurs ;
* ajout d'une validation des résultats générés par l'IA ;
* prise en charge de différents formats et structures de factures ;
* ajout d'une base de données ;
* conservation de l'historique des traitements ;
* export des résultats dans différents formats ;
* ajout d'un système d'authentification ;
* ajout d'un système de gestion des utilisateurs ;
* amélioration de la sécurité ;
* déploiement de l'application sur un serveur ;
* optimisation des prompts utilisés avec l'intelligence artificielle.

## Conclusion

`project_facture_ia` permet de mettre en œuvre une architecture combinant une interface web, un backend Python/Flask et un service d'intelligence artificielle.

Le backend constitue le lien entre l'utilisateur et l'intelligence artificielle. Il reçoit les données provenant de l'interface, les prépare, communique avec l'API d'IA, récupère la réponse et la transmet ensuite à l'utilisateur.

Le projet permet ainsi de mettre en pratique plusieurs concepts importants du développement d'applications modernes, notamment les applications web avec Flask, les API, les échanges de données JSON, l'intégration d'un service d'intelligence artificielle et la gestion d'un projet avec Git et GitHub.

## Auteur

**Projet :** `project_facture_ia`
**Auteur :** Oumaima Jallouli
**Date :** 19/08/2026

## Licence

Ce projet est réalisé dans le cadre d'un projet de formation / stage.

Les conditions d'utilisation et de distribution du projet peuvent être définies selon les exigences de l'organisme d'accueil.
