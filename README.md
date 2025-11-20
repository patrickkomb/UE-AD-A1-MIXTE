# UE-AD-A1-MIXTE

Projet réalisé par Evan RUNEMBERG et Noé JOUAN.

---

Ce projet contient 4 microservices :
- Movie (GraphQL)
- Booking (GraphQL)
- User (REST)
- Schedule (gRPC)

## Structure du projet

```
.
├── booking/
│   ├── data/bookings.json
│   ├── booking.graphql
│   ├── Dockerfile
│   ├── booking.py
│   ├── env.py
│   ├── repository.py
│   └── resolvers.py
├── movie/
│   ├── data/
│   │    ├── movies.json
│   │    └── actors.json
│   ├── movie.graphql
│   ├── Dockerfile
│   ├── movie.py
│   ├── env.py
│   ├── repository.py
│   └── resolvers.py
├── schedule/
│   ├── data/times.json
│   ├── Dockerfile
│   ├── schedule.proto
│   ├── schedule.py
│   └── ....
├── user/
│   ├── data/users.json
│   ├── Dockerfile
│   ├── env.py
│   ├── repository.py
│   └── user.py
├── requirements.txt
├── docker-compose.yml
├── .env
└── .env.local
```

## Prérequis
- Python >= 3.10
- Docker et Docker Compose

## Variables d'environnement

Le projet utilise **deux fichiers** ``.env`` :

- ``.env`` **— pour Docker** :

Contient les variables utilisées par tous les microservices dans le cas d'une exécution via **Docker**.

Par exemple :
```
USERS_SERVICE_URL=http://user:3203/users
SCHEDULE_SERVICE_URL=http://schedule:3202/schedules
MOVIES_SERVICE_URL=http://movie:3200/graphql
BOOKING_SERVICE_URL=http://booking:3201/graphql
MONGO_URL=mongodb://user:pwd@mongo:27017/cinema?authSource=admin
USE_MONGO=true
```

- ``.env.local`` **— pour local** :

Contient les variables utilisées par tous les microservices dans le cas d'une exécution **locale**.

Par exemple :
```
USERS_SERVICE_URL=http://localhost:3203/users
SCHEDULE_SERVICE_URL=http://localhost:3202/schedules
MOVIES_SERVICE_URL=http://localhost:3200/graphql
BOOKING_SERVICE_URL=http://localhost:3201/graphql
MONGO_URL=mongodb://user:pwd@localhost:27017/cinema?authSource=admin
USE_MONGO=true
```

## Gestion des données Mongo / JSON

Chaque microservice possède des données JSON d’origine :

- booking/data/bookings.json

- movie/data/movies.json

- … etc.

**Deux modes sont possibles :**

### Mode données JSON (``USE_MONGO=false``)

- Ce mode est choisi si la variable d'environnement ``USE_MONGO`` est définie à ``false``.

- Les données seront lues et écrites directement dans les fichiers JSON de chaque microservice.

### Mode données MongoDB (``USE_MONGO=true``)

- Ce mode est choisi si la variable d'environnement ``USE_MONGO`` est définie à ``true``.

- Les données seront stockées dans MongoDB.

- Les données JSON sont automatiquement importées dans MongoDB au premier lancement du projet, si les collections sont vides.

## Lancer le projet

### Lancer tous les microservices avec Docker Compose

Pour choisir la source de données (MongoDB ou fichier JSON), il suffit de modifier la variable d'environnement ``USE_MONGO`` dans le fichier ``.env``, en la passant à ``true`` ou ``false`` (mise à ``true`` par défaut).

Puis exécuter à la racine du projet, en ayant lancé Docker au préalable :
```
docker compose up -d --build
```

Les 4 microservices seront lancés ainsi que MongoDB et Mongo Express.

### Lancer tous les microservices en local

Pour choisir la source de données (MongoDB ou fichier JSON), il suffit de modifier la variable d'environnement ``USE_MONGO`` dans le fichier ``.env.local``, en la passant à ``true`` ou ``false`` (mise à ``true`` par défaut).

Toutes les dépendances à installer sont situées dans le fichier ``requirements.txt`` présent à la racine du projet.

Il faut ensuite lancer les microservices un à un, dans des terminaux séparés :

Pour ``booking/`` par exemple, depuis la racine du projet :

```
pip install -r requirements.txt
cd booking
python booking.py
```

**⚠️ Si vous avez choisi de lancer le projet avec les données MongoDB (``USE_MONGO=true``), il faut lancer le conteneur MongoDB avant de lancer les services :** 

En se plaçant à la racine du projet :
```
docker compose up -d --build mongo
```
