from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r

PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)

# Elements for Ariadne
type_defs = load_schema_from_path('booking.graphql')
query = QueryType()
mutation = MutationType()
booking = ObjectType('Booking')
booking_date = ObjectType('BookingDate')
movie_booking_result = ObjectType('MovieBookingsResult')
user_booking = ObjectType('UserBooking')
movie_detail = ObjectType('MovieDetail')
booking_mutation_response = ObjectType('BookingMutationResponse')

query.set_field("bookings_for_user", r.bookings_for_user)
query.set_field("users_for_movie", r.users_for_movie)
mutation.set_field("add_booking", r.add_booking)
mutation.set_field("delete_booking", r.delete_booking)

schema = make_executable_schema(type_defs, query, mutation, booking, booking_date, movie_booking_result, user_booking, movie_detail, booking_mutation_response)

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Booking service!</h1>",200)

# graphql entry points
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value={"request": request},
                        debug=app.debug
                    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)