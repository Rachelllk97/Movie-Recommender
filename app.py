import itertools
from flask import Flask, jsonify, request
from operator import itemgetter

from db_utils import (db_add_user, db_get_user, db_add_user_movie_top_5, db_get_quizzes, db_add_user_quiz_responses,
                      db_get_movie_top_5_for_similar_users)
from tmdb_utils import (tmdb_get_movie_for_movie_name, tmdb_get_unique_movies, tmdb_get_filtered_movies,
                        tmdb_get_movie_recommendations_for_movie_id)


# Create instance of Flask class to host API endpoints
app = Flask(__name__)


# Define route to post user details and bind to function
@app.route("/user", methods=["POST"])
def app_post_user():
    # Initialise user_id to return
    user_id = None
    # Extract user data from request body in JSON format
    user_data = request.get_json()
    # Define mandatory keys
    mandatory_keys = ["user_first_name", "user_last_name", "user_email", "user_password"]
    # Test if all mandatory keys present in user_data
    if all(key in user_data for key in mandatory_keys):
        # Set user_id to return value of db_add_user called with mandatory key values
        user_id = db_add_user(
            user_data["user_first_name"],
            user_data["user_last_name"],
            user_data["user_email"],
            user_data["user_password"]
        )
        # Set status code to 200 to indicate successful request
        status_code = 200
    else:
        # Set status code to 400 to indicate bad request
        status_code = 400
    # Create dictionary item to return user_id
    api_response = {"user_id": user_id}
    # Return user_id as JSON response object, along with status code
    return jsonify(api_response), status_code


# Define route to get user details and bind to function
@app.route("/user", methods=["GET"])
def app_get_user():
    # Initialise user_id to return
    user_id = None
    # Extract user data from request body in JSON format
    user_data = request.get_json()
    # Define mandatory keys
    mandatory_keys = ["user_email", "user_password"]
    # Test if all mandatory keys present in user data
    if all(key in user_data for key in mandatory_keys):
        # Set user_id to return value of db_get_user called with mandatory key values
        user_id = db_get_user(
            user_data["user_email"],
            user_data["user_password"]
        )
        # Set status code to 200 to indicate successful request
        status_code = 200
    else:
        # Set status code to 400 to indicate bad request
        status_code = 400
    # Create dictionary item to return user_id
    api_response = {"user_id": user_id}
    # Return user_id as JSON response object, along with status code
    return jsonify(api_response), status_code
 

# Define route to post user's top 5 movies and bind to function, passing user_id
@app.route("/user/<int:user_id>/movie/top_5", methods=["POST"])
def app_post_user_movie_top_5(user_id):
    # Initialise update_count to return
    update_count = None
    # Extract movie data from request body in JSON format
    movie_data = request.get_json()
    # Test if "movie_names" key present in movie data
    if "movie_names" in movie_data:
        # Set update_count to return value of db_add_user_movie_top_5 called with user_id and "movie_names" key value
        update_count = db_add_user_movie_top_5(user_id, movie_data["movie_names"])
        # Set status code to 200 to indicate successful request
        status_code = 200
    else:
        # Set status code to 400 to indicate bad request
        status_code = 400
    # Create dictionary item to return update_count
    api_response = {"update_count": update_count}
    # Return update_count as JSON response object, along with status code
    return jsonify(api_response), status_code


# Define route to get quizzes and bind to function
@app.route("/quizzes", methods=["GET"])
def app_get_quizzes():
    # Set quizzes to return value of db_get_quizzes
    quizzes = db_get_quizzes()
    # Set status code to 200 to indicate successful request
    status_code = 200
    # Create dictionary item to return quizzes
    api_response = {"quizzes": quizzes}
    # Return quizzes as JSON response object, along with status code
    return jsonify(api_response), status_code


# Define route to post user quiz responses and bind to function, passing user_id and quiz_id
@app.route("/user/<int:user_id>/quiz/<int:quiz_id>", methods=["POST"])
def app_post_user_quiz(user_id, quiz_id):
    # Initialise update_count to return
    update_count = None
    # Extract quiz response data from request body in JSON format
    quiz_response_data = request.get_json()
    # Test if "quiz_responses" key present in quiz response data
    if "quiz_responses" in quiz_response_data:
        # Initialise list of quiz responses to build comma-separated list
        quiz_responses = []
        # Iterate over quiz response data
        for quiz_response in quiz_response_data["quiz_responses"]:
            # Append quiz_prompt_option_id selected by user to list of quiz responses
            quiz_responses.append(str(quiz_response["quiz_prompt_option_id"]))
        # Transform list of quiz responses into comma-separated string
        quiz_responses_str = ",".join(quiz_responses)
        # Set update_count to return value of db_add_user_quiz_responses called with user_id, quiz_id and
        # quiz_responses_str
        update_count = db_add_user_quiz_responses(user_id, quiz_id, quiz_responses_str)
        # Set status code to 200 to indicate successful request
        status_code = 200
    else:
        # Set status code to 400 to indicate bad request
        status_code = 400
    # Create dictionary item to return update_count
    api_response = {"update_count": update_count}
    # Return update_count as JSON response object, along with status code
    return jsonify(api_response), status_code


# Define route to get user's movie recommendations and bind to function, passing user_id
@app.route("/user/<int:user_id>/movie/recommendations", methods=["GET"])
def app_get_user_movie_recommendations(user_id):
    # Initialise list of movies to return
    movies = []
    # Initialise list to track movie_ids of specified user's top 5 movies
    user_movie_top_5_ids = []
    # Set top_5_movies to return value of db_get_movie_top_5_for_similar_users called with user_id
    top_5_movies = db_get_movie_top_5_for_similar_users(user_id)
    # Iterate over list of top 5 movies for specified user and all similar users
    for top_5_movie in top_5_movies:
        # Create movie dictionary item with result of calling tmdb_get_movie_for_movie_name with current movie name
        movie = tmdb_get_movie_for_movie_name(top_5_movie["movie_name"])
        # Test if movie in specified user's top 5
        if top_5_movie["user_top_5"] == 1:
            # Append movie_id to list for tracking specified user's top 5
            user_movie_top_5_ids.append(movie["movie_id"])
        else:
            # Add movie dictionary item to unique list of movies to return
            movies = list(tmdb_get_unique_movies(itertools.chain(movies, [movie])))
        # Retrieve recommendations for current movie_id
        recommendations = tmdb_get_movie_recommendations_for_movie_id(movie["movie_id"])
        # Add recommendations to unique list of movies to return
        movies = list(tmdb_get_unique_movies(itertools.chain(movies, recommendations)))
    # Exclude from list of movies any of specified user's top 5
    movies = tmdb_get_filtered_movies(movies, user_movie_top_5_ids)
    # Sort movies by descending popularity and slice top 25
    movies = list(itertools.islice(sorted(movies, key=itemgetter("movie_popularity"), reverse=True), 25))
    # Set status code to 200 to indicate successful request
    status_code = 200
    # Create dictionary item to return movies
    api_response = {"movies": movies}
    # Return movies as JSON response object, along with status code
    return jsonify(api_response), status_code


if __name__ == "__main__":
    app.run(debug=True)
