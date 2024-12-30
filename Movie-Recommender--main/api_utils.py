import json

import requests

from api_config import API_BASE_URL


# Define function to call API endpoint to add user
def api_add_user(user_first_name, user_last_name, user_email, user_password):
    # Initialise user_id to return
    user_id = None
    # Create user data dictionary
    user_data = {
        "user_first_name": user_first_name,
        "user_last_name": user_last_name,
        "user_email": user_email,
        "user_password": user_password
    }
    # Try to call API endpoint to post user data
    try:
        # Send POST request to /user endpoint, passing user_data in JSON format
        api_response = requests.post(
            f"{API_BASE_URL}/user",
            data=json.dumps(user_data),
            headers={"content-type": "application/json"}
        )
        # Test if call to endpoint successful
        if api_response.status_code == 200:
            # Extract user_id from JSON response
            user_id = api_response.json().get("user_id", None)
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Movie Recommender API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return user_id or None if call to endpoint unsuccessful
    return user_id


# Define function to call API endpoint to get user
def api_get_user(user_email, user_password):
    # Initialise user_id to return
    user_id = None
    # Create user data dictionary
    user_data = {
        "user_email": user_email,
        "user_password": user_password
    }
    # Try to call API endpoint to get user data
    try:
        # Send GET request to /user endpoint, passing user_data in JSON format
        api_response = requests.get(
            f"{API_BASE_URL}/user",
            data=json.dumps(user_data),
            headers={"content-type": "application/json"}
        )
        # Test if call to endpoint successful
        if api_response.status_code == 200:
            # Extract user_id from JSON response
            user_id = api_response.json().get("user_id", None)
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Movie Recommender API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return user_id or None if call to endpoint unsuccessful
    return user_id


# Define function to call API endpoint to add user's top 5 movies
def api_add_user_movie_top_5(user_id, movie_names):
    # Initialise update_count to return
    update_count = None
    # Create movie data dictionary
    movie_data = {
        "movie_names": movie_names
    }
    # Try to call API endpoint to post movie data
    try:
        # Send POST request to /user/{user_id}/movie/top_5 endpoint, passing movie_data in JSON format
        api_response = requests.post(
            f"{API_BASE_URL}/user/{user_id}/movie/top_5",
            data=json.dumps(movie_data),
            headers={"content-type": "application/json"}
        )
        # Test if call to endpoint successful
        if api_response.status_code == 200:
            # Extract update_count from JSON response
            update_count = api_response.json().get("update_count", None)
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Movie Recommender API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return update_count or None if call to endpoint unsuccessful
    return update_count


# Define function to call API endpoint to get quizzes
def api_get_quizzes():
    # Initialise quizzes to return
    quizzes = None
    # Try to call API endpoint to get quizzes data
    try:
        # Send GET request to /quizzes endpoint
        api_response = requests.get(
            f"{API_BASE_URL}/quizzes"
        )
        # Test if call to endpoint successful
        if api_response.status_code == 200:
            # Extract quizzes from JSON response
            quizzes = api_response.json().get("quizzes", None)
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Movie Recommender API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return quizzes or None if call to endpoint unsuccessful
    return quizzes


# Define helper function to map quiz responses into list of dictionary items
def map_quiz_responses(quiz_responses):
    # Initialise list of quiz response dictionary items to return
    mapped_quiz_responses = []
    # Iterate over quiz responses
    for quiz_response in quiz_responses:
        # Create quiz response dictionary item
        quiz_response_item = {
            "quiz_prompt_option_id": quiz_response
        }
        # Append quiz response dictionary item to list
        mapped_quiz_responses.append(quiz_response_item)
    # Return list of quiz response dictionary items
    return mapped_quiz_responses


# Define function to call API endpoint to add user's quiz responses
def api_add_user_quiz_responses(user_id, quiz_id, quiz_responses):
    # Initialise update_count to return
    update_count = None
    # Create quiz response data dictionary
    quiz_response_data = {
        "quiz_responses": map_quiz_responses(quiz_responses)
    }
    # Try to call API endpoint to post quiz response data
    try:
        # Send POST request to /user/{user_id}/quiz/{quiz_id} endpoint, passing quiz_response_data in JSON format
        api_response = requests.post(
            f"{API_BASE_URL}/user/{user_id}/quiz/{quiz_id}",
            data=json.dumps(quiz_response_data),
            headers={"content-type": "application/json"}
        )
        # Test if call to endpoint successful
        if api_response.status_code == 200:
            # Extract update_count from JSON response
            update_count = api_response.json().get("update_count", None)
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Movie Recommender API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return update_count or None if call to endpoint unsuccessful
    return update_count


# Define function to call API endpoint to get user's movie recommendations
def api_get_user_movie_recommendations(user_id):
    # Initialise movies to return
    movies = None
    # Try to call API endpoint to get movie recommendations
    try:
        # Send GET request to /user/{user_id}/movie/recommendations endpoint
        api_response = requests.get(
            f"{API_BASE_URL}/user/{user_id}/movie/recommendations"
        )
        # Test if call to endpoint successful
        if api_response.status_code == 200:
            # Extract movies from JSON response
            movies = api_response.json().get("movies", None)
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Movie Recommender API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return movies or None if call to endpoint unsuccessful
    return movies
