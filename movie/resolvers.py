import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.permissions import admin_required
from repository import get_movie_repository, get_actor_repository

movie_repo = get_movie_repository()
actor_repo = get_actor_repository()

# TODO: Ajouter vérification user est admin pour les routes admin
# -- QUERIES --

# Movie
def movie_with_id(_, info, _id):
    for movie in movie_repo.load():
        if movie["id"] == _id:
            return movie
    return None

def all_movies(_, info):
    return movie_repo.load()

def movie_with_title(_, info, _title):
    for movie in movie_repo.load():
        if movie["title"].lower() == _title.lower():
            return movie
    return None

def resolve_actors_in_movie(movie, info):
    actors = actor_repo.load()
    return [actor for actor in actors if movie["id"] in actor["films"]]

# Actor
def actor_with_id(_, info, _id):
    for actor in actor_repo.load():
        if actor["id"] == _id:
            return actor
    return None

def all_actors(_, info):
    return actor_repo.load()

# -- MUTATIONS -- #

# Movie
@admin_required
def update_movie_rate(_, info, _id, _rate):
    movies = movie_repo.load()
    for movie in movies:
        if movie["id"] == _id:
            movie["rating"] = _rate
            movie_repo.save(movies)
            return movie
    return None

@admin_required
def add_movie(_, info, _id, _title, _director, _rating):
    movies = movie_repo.load()

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
    movie_repo.save(movies)
    return new_movie

@admin_required
def delete_movie(_, info, _id):
    movies = movie_repo.load()

    for movie in movies:
        if str(movie["id"]) == str(_id):
            movies.remove(movie)
            movie_repo.save(movies)
            return movie
    return None

# Actor
@admin_required
def add_actor(_, info, _id, _firstname, _lastname, _birthyear):
    actors = actor_repo.load()

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
    actor_repo.save(actors)
    return new_actor

@admin_required
def add_movie_to_actor(_, info, _movie_id, _actor_id):
    actors = actor_repo.load()
    movie = movie_with_id(_, info, _movie_id)

    if movie is None:
        raise Exception("Movie ID does not exist")

    for actor in actors:
        if str(actor["id"]) == str(_actor_id):
            if _movie_id not in actor["films"]:
                actor["films"].append(_movie_id)
                actor_repo.save(actors)
            return actor
    return None

@admin_required
def delete_actor(_, info, _id):
    actors = actor_repo.load()

    for actor in actors:
        if str(actor["id"]) == str(_id):
            actors.remove(actor)
            actor_repo.save(actors)
            return actor
    return None