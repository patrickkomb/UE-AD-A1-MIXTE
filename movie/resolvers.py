import json

MOVIE_FILE = "{}/data/movies.json"
ACTOR_FILE = "{}/data/actors.json"


# TODO: Ajouter vérification user est admin pour les routes admin

# -- UTILS --
def load_movies():
    with open(MOVIE_FILE.format("."), "r") as file:
        return json.load(file)["movies"]

def save_movies(movies):
    with open(MOVIE_FILE.format("."), "w") as file:
        json.dump({"movies": movies}, file)

def load_actors():
    with open(ACTOR_FILE.format("."), "r") as file:
        return json.load(file)["actors"]

def save_actors(actors):
    with open(ACTOR_FILE.format("."), "w") as file:
        json.dump({"actors": actors}, file)

# -- QUERIES --

# Movie
def movie_with_id(_, info, _id):
    for movie in load_movies():
        if movie["id"] == _id:
            return movie
    return None

def all_movies(_, info):
    return load_movies()

def movie_with_title(_, info, _title):
    for movie in load_movies():
        if movie["title"].lower() == _title.lower():
            return movie
    return None

def resolve_actors_in_movie(movie, info):
    actors = load_actors()
    return [actor for actor in actors if movie["id"] in actor["films"]]

# Actor
def actor_with_id(_, info, _id):
    for actor in load_actors():
        if actor["id"] == _id:
            return actor
    return None

def all_actors(_, info):
    return load_actors()

# -- MUTATIONS -- #

# Movie
def update_movie_rate(_, info, _id, _rate):
    movies = load_movies()
    for movie in movies:
        if movie["id"] == _id:
            movie["rating"] = _rate
            save_movies(movies)
            return movie
    return None

def add_movie(_, info, _id, _title, _director, _rating):
    movies = load_movies()

    for movie in movies:
        if str(movie["id"]) == str(_id):
            raise Exception("Movie ID already exists")

    new_movie = {
        "id": _id,
        "title": _title,
        "director": _director,
        "rating" : _rating
    }

    movies.append(new_movie)
    save_movies(movies)
    return new_movie

def delete_movie(_, info, _id):
    movies = load_movies()

    for movie in movies:
        if str(movie["id"]) == str(_id):
            movies.remove(movie)
            save_movies(movies)
            return movie
    return None

# Actor
def add_actor(_, info, _id, _firstname, _lastname, _birthyear):
    actors = load_actors()

    for actor in actors:
        if str(actor["id"]) == str(_id):
            raise Exception("Actor ID already exists")

    new_actor = {
        "id": _id,
        "firstname": _firstname,
        "lastname": _lastname,
        "birthyear": _birthyear,
        "films": []
    }

    actors.append(new_actor)
    save_actors(actors)
    return new_actor

def add_movie_to_actor(_, info, _movie_id, _actor_id):
    actors = load_actors()
    movie = movie_with_id(_, info, _movie_id)

    if movie is None:
        raise Exception("Movie ID does not exist")

    for actor in actors:
        if str(actor["id"]) == str(_actor_id):
            if _movie_id not in actor["films"]:
                actor["films"].append(_movie_id)
                save_actors(actors)
            return actor
    return None

def delete_actor(_, info, _id):
    actors = load_actors()

    for actor in actors:
        if str(actor["id"]) == str(_id):
            actors.remove(actor)
            save_actors(actors)
            return actor
    return None