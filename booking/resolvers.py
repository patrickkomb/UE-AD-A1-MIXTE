import json
import requests
import os

SCHEDULE_SERVICE_URL =  os.getenv("SCHEDULE_SERVICE_URL", "http://localhost:3202/schedules")
MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "http://localhost:3200/graphql")
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:3203/users")

BOOKING_FILE = "{}/data/bookings.json"

# -- UTILS --
def load_bookings():
    with open(BOOKING_FILE.format("."), "r") as file:
        return json.load(file)["bookings"]

def save_bookings(bookings):
    with open(BOOKING_FILE.format("."), "w") as file:
        json.dump({"bookings": bookings}, file)

def is_admin(userid):
    try:
        user_resp = requests.get(f"{USERS_SERVICE_URL}/{userid}")
        if user_resp.status_code == 200:
            user_detail = user_resp.json()
            if user_detail["is_admin"]:
                return True
        else:
            return False
    except Exception as e:
        return False

# -- QUERIES --
def bookings_for_user(_, info, _userid):
    req = info.context["request"]
    current_userid = req.headers.get("X-User-Id")

    if not current_userid:
        raise Exception("Missing X-User-Id header")

    if current_userid != _userid and not is_admin(current_userid):
        raise Exception("Not authorized")

    bookings = load_bookings()

    for booking in bookings:
        if booking["userid"] == _userid:
            return booking
    return None

def users_for_movie(_, info, _movieid):
    current_userid = info.context["request"].headers.get("X-User-Id")
    if not current_userid:
        raise Exception("Missing X-User-Id header")
    if not is_admin(current_userid):
        raise Exception("Not authorized")

    # Check if movie exists
    query = f"""
    {{
      movie_with_id(_id: "{_movieid}") {{
        id
        title
        director
        rating
      }}
    }}
    """
    resp = requests.post(MOVIES_SERVICE_URL, json={"query": query})
    data = resp.json()
    movie_data = data.get("data", {}).get("movie_with_id")

    if not movie_data:
        return {"movie": None, "users": [], "error": "Movie ID not found"}

    bookings = load_bookings()
    users = []
    for user_booking in bookings:
        for booking_date in user_booking["dates"]:
            if _movieid in booking_date["movies"]:
                users.append({
                    "userid": user_booking["userid"],
                    "date": booking_date["date"]
                })

    return {
        "movie": movie_data,
        "users": users,
        "error": "No users found" if not users else None
    }

# -- MUTATIONS --
def add_booking(_, info, _userid, _date, _movieid):
    schedule_response = requests.get(f"{SCHEDULE_SERVICE_URL}/{_date}")
    schedule_response.raise_for_status()
    schedule_data = schedule_response.json()
    if _movieid not in schedule_data.get("movies"):
        return {"booking": None, "error": "Movie ID not found in schedule"}

    bookings = load_bookings()

    # Check user booking existence
    for user_booking in bookings:
        if user_booking["userid"] == _userid:

            # Search for the specific date
            for booking_date in user_booking["dates"]:
                if booking_date["date"] == _date:

                    # Check if movie already booked
                    if _movieid in booking_date["movies"]:
                        return {"booking": None, "error": "User already booked this movie on this date"}

                    # Add movie to existing date
                    booking_date["movies"].append(_movieid)
                    save_bookings(bookings)
                    return {"booking": user_booking, "error": None}

            # Date not found, add new date entry with movie
            user_booking["dates"].append({
                "date": _date,
                "movies": [_movieid]
            })
            save_bookings(bookings)
            return {"booking": user_booking, "error": None}

    # User not found, create new user booking
    bookings.append({"userid": _userid, "dates": [{"date": _date, "movies": [_movieid]}]})
    save_bookings(bookings)
    return {"booking": bookings[-1], "error": None}

def delete_booking(_, info, _userid, _date, _movieid):
    bookings = load_bookings()
    for user_booking in bookings:
        if user_booking["userid"] == _userid:
            for booking_date in user_booking["dates"]:
                if booking_date["date"] == _date and _movieid in booking_date["movies"]:
                    booking_date["movies"].remove(_movieid)
                    if not booking_date["movies"]:
                        user_booking["dates"].remove(booking_date)
                    save_bookings(bookings)
                    return {"booking": user_booking, "error": None}
    return {"booking": None, "error": "Booking not found"}

# TODO : modifier les retours au delete ? on renvoie le booking entier (mineur)