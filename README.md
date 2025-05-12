# Steam Scrapper

## Description

Cette application est un système de scraping et d'analyse de jeux Steam, composé de plusieurs parties :

### ETL Pipeline

- Un pipeline ETL (Extract, Transform, Load) qui :
- Extrait les données des jeux Steam via web scraping
- Transforme et nettoie les données récupérées
- Charge les données dans une base MongoDB

### Base de données

- MongoDB stockant les informations sur :
- Les jeux (titre, développeur, éditeur, etc.)
- Les configurations requises (CPU, GPU, RAM, etc.)
- Les systèmes d'exploitation supportés
- Les technologies utilisées

### API Flask

- Une API REST qui expose les données via différents endpoints
- Permet d'interroger la base pour obtenir :
  - La liste des jeux
  - Les détails d'un jeu spécifique
  - Les configurations requises

### Frontend

- Un frontend React qui permet de visualiser les données et de les filtrer
- Utilise l'API Flask pour obtenir les données
- Affiche les jeux dans un tableau et permet de les filtrer

### Steamscrapy

- Un script Python qui permet de scraper les données hardware (CPU, GPU, RAM, etc.)
- Utilise Scrapy pour scraper les données
- Utilise MongoDB pour stocker les données

## Prérequis

- Python 3.x
- MongoDB
- Les dépendances Python listées dans `requirements.txt`

## Installation

### 1. Cloner le repository

```sh
git clone https://github.com/SwerkF/SteamScraper
```

### 2. Créer un environnement virtuel

```sh
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```sh
pip install -r requirements.txt
```

### 4. Initialiser le frontend (./frontend)

#### 4.1 Installer les dépendances

```sh
cd frontend
npm install
```

#### 4.2 Créer un fichier .env avec les variables d'environnement

```env
VITE_API_BASE_URL="http://localhost:5000"
```

#### 4.3 Lancer le frontend

```sh
cd frontend
npm run dev
```

### 5. Initialiser le flask (./flask)

#### 5.1 Créer un fichier .env avec les variables d'environnement

```env
# MongoDB
MONGODB_ROOT_USERNAME=root
MONGODB_ROOT_PASSWORD=password
MONGODB_DATABASE=steam_games

# MongoDB Express
ME_CONFIG_MONGODB_ADMINUSERNAME=root
ME_CONFIG_MONGODB_ADMINPASSWORD=password
ME_CONFIG_MONGODB_SERVER=mongodb

#URI pour Atlas par exemple
MONGO_URI="mongodb://root:password@localhost:27017"
DB_NAME="steam_games"
```

#### 5.1.1 (optionnel) Lancer le docker pour MongoDB

```sh
docker compose up -d
```

#### 5.2 Lancer le flask

##### 5.2.1 (optionnel) Dumps

Des dumps sont disponibles dans le dossier `dumps` pour les jeux déjà scrapés.

Ordre d'imports: cpu > gpu > memory > os > games

##### 5.2.2 Lancer le flask

```sh
cd flask
flask --app main run
```

#### 6. Lancer le scrapper pour le hardware (./steamscrapy)

```sh
cd steamscrapy
scrapy crawl hardware
```

#### 7. Lancer le scrapper pour les jeux (./etl_pipeline)

##### 7.1 Méthode 1 : Lancer le scrapper pour les jeux

```sh
cd etl_pipeline
python run_etl.py
```

Ce processus est long, il peut prendre plusieurs heures. Si vous voulez scraper moins de jeux, vous devez modifier les fichiers:

- `etl_pipeline/etl/extract/steamDB_charts.py` > CTRL + F, et remplacer les valeurs "101" par le nombre de jeux que vous voulez scraper.
- `etl_pipeline/etl/extract/steamDB_config.py` > CTRL + F, et remplacer les valeurs "100" par le nombre de jeux que vous voulez scraper.
- `etl_pipeline/etl/extract/steamDB_games-details.py` > CTRL + F, et remplacer les valeurs "100" par le nombre de jeux que vous voulez scraper.

## Résultats

Les résultats sont stockés dans la base MongoDB.

## API

![API](./images/api.png)

![API2](./images/api-2.png)

![API3](./images/api-3.png)

## Frontend

![Frontend](./images/frontend.png)

![Frontend2](./images/frontend-2.png)

## ETL Pipeline

![ETL Pipeline](./images/scraping-games.png)

![ETL Pipeline](./images/scraping-games-details.png)

![Games](./images/game.png)

## Steamscrapy

![GPU](./images/gpu.png)

![GPU2](./images/gpus.png)

![CPU](./images/cpu.png)
