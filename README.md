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

## Architecture du projet

L'application est découpée en 4 microservices indépendants (Movie : GraphQL, Booking : GraphQL, User : REST, Schedule : gRPC) qui communiquent entre eux via des requêtes.

Le code contient plusieurs fichiers spécifiques et nécessaires au bon fonctionnement du projet peu importe l'environnement et le type du microservice :

### ``env.py``
Pour chaque microservice et pour le module `common`, ce fichier charge automatiquement la configuration adaptée à l'environnement (Docker ou local).

- Il détecte si l'application tourne en local (présence du fichier `.env.local`) ou sur Docker.
- Il définit les URLs pour contacter les autres microservices.
- Il détecte si l'application utilise MongoDB ou les fichiers JSON selon la variable d'environnement ``USE_MONGO``.

### ``repository.py``

Pour chaque microservice, ce fichier sert d'interface unique pour l'accès aux données et permet de gérer les 2 modes de stockage des données sans modifier le reste du code.

### ``resolvers.py`` (GraphQL)

Ce fichier contient les fonctions qui répondent précisément aux demandes envoyées à l'API GraphQL. Il fait le lien entre le schéma (la structure des données) et le repository (le stockage).

### Le schéma (GraphQL) (ex : ``booking.graphql``)

C'est le "contrat" de l'API. Il définit strictement ce que l'on peut demander ou modifier. Il contient les types définissant la structure des objets, les queries (lectures possibles) et les mutations (actions possibles).

### ``common/permissions.py``

La gestion des accès est centralisée dans ce fichier qui définit des décorateurs à utiliser sur les routes pour protéger l'accès à certains endpoints.

- Il vérifie l'identité via le header ``X-User-Id``.
- Il contacte le microservice User pour vérifier si l'utilisateur est admin (``@admin_required``) ou propriétaire de la donnée (``@owner_or_admin_required``).

### Les routes API (ex : ``nom_microservice.py``)

C'est le fichier principal de chaque service (ex: ``user.py``).
- Il lance le serveur Flask.
- Il définit les points d'entrée des APIs.

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
SCHEDULE_SERVICE_URL=schedule:3202
MOVIES_SERVICE_URL=http://movie:3200/graphql
BOOKING_SERVICE_URL=http://booking:3201/graphql
MONGO_URL=mongodb://root:example@mongo:27017/cinema?authSource=admin
USE_MONGO=true
```

- ``.env.local`` **— pour local** :

Contient les variables utilisées par tous les microservices dans le cas d'une exécution **locale**.

Par exemple :
```
USERS_SERVICE_URL=http://localhost:3203/users
SCHEDULE_SERVICE_URL=schedule:3202
MOVIES_SERVICE_URL=http://localhost:3200/graphql
BOOKING_SERVICE_URL=http://localhost:3201/graphql
MONGO_URL=mongodb://root:example@localhost:27017/cinema?authSource=admin
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

## Arrêter le projet

**⚠️ Il n'y a pas de persistance de données avec MongoDB, si le conteneur vient à être supprimé, les données seront donc perdues et remplacées par celles présentes dans les fichiers JSON à la recréation des conteneurs.**

### Stopper les conteneurs Docker
```
docker compose stop
```

### Stopper les microservices lancés en local

Dans les terminaux, faire ``Crtl + C``.