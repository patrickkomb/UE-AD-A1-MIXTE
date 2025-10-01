import json

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def actor_with_id(_,info,_id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor

def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

'''
Les variables newmovies et newmovie sont inutiles ?
Tester cette version du code :

def update_movie_rate(_,info,_id,_rate):
    #with open('./data/movies.json', "r") as rfile:
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
    for movie in movies['movies']:
        if movie['id'] == _id:
            movie['rating'] = _rate
            #with open('./data/movies.json', "w") as wfile:
            with open('{}/data/movies.json'.format("."), "w") as wfile:
                json.dump(movies, wfile)
            return movie
    return {}
'''

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result