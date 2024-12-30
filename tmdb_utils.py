import itertools
import re
from operator import itemgetter

import requests

from tmdb_config import TMDB_BEARER_TOKEN


# Set variables used for all calls to TMDB API
tmdb_base_url = "https://api.themoviedb.org/3"
tmdb_headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
}


# Define helper function to get unique movies from iterable
def tmdb_get_unique_movies(movies):
    # Initialise list of movie_ids to track uniqueness
    movie_ids = []
    # Iterate over movies
    for movie in movies:
        # Test if movie_id not in unique list
        if not movie["movie_id"] in movie_ids:
            # Append movie_id to unique list
            movie_ids.append(movie["movie_id"])
            # Yield unique movie
            yield movie


# Define helper function to filter movies from iterable
def tmdb_get_filtered_movies(movies, movie_ids_to_exclude):
    # Iterate over movies
    for movie in movies:
        # Test if movie_id not in exclude list
        if not movie["movie_id"] in movie_ids_to_exclude:
            # Yield movie not in exclude list
            yield movie


# Define function to get movie details for movie name
def tmdb_get_movie_for_movie_name(movie_name):
    # Initialise movie dictionary item to return
    movie = None
    # Try to get movie details from TMDB search endpoint
    try:
        # Set URL for TMDB search endpoint
        url = f"{tmdb_base_url}/search/movie?include_adult=false&language=en-GB&page=1&query="
        # Test if movie name ends with bracketed year
        if re.search(r"\(\d{4}\)$", movie_name):
            # Extract bracketed year and use stripped movie name in query parameter, with additional year parameter
            url += f"{movie_name[:-6].strip()}&year={movie_name[-5:-1]}"
        else:
            # Use full movie name in query parameter
            url += f"{movie_name}"
        # Call TMDB endpoint and capture movie_results from JSON response
        response = requests.get(url, headers=tmdb_headers)
        movie_results = response.json()["results"]
        # Test if movie_results populated
        if movie_results[0]:
            # Create movie dictionary item with required keys and values from first result
            movie = {"movie_id": movie_results[0]["id"],
                     "movie_name": movie_results[0]["title"],
                     "movie_overview": movie_results[0]["overview"],
                     "movie_popularity": movie_results[0]["popularity"],
                     "movie_release_date": movie_results[0]["release_date"]}
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the TMDB API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return movie dictionary item or None if no results returned
    return movie


# Define function to get movie recommendations for movie_id
def tmdb_get_movie_recommendations_for_movie_id(movie_id):
    # Initialise list of movie dictionary items to return
    movies = []
    # Try to get movie recommendations from TMDB recommendations endpoint
    try:
        # Set URL for TMDB recommendations endpoint for specified movie_id
        url = f"{tmdb_base_url}/movie/{str(movie_id)}/recommendations?language=en-GB&page=1"
        # Call TMDB endpoint and capture movie_results from JSON response
        response = requests.get(url, headers=tmdb_headers)
        movie_results = response.json()["results"]
        # Sort movie_results by descending popularity and slice top 10
        sorted_movie_results = list(itertools.islice(
            sorted(movie_results, key=itemgetter("popularity"), reverse=True), 10))
        # Iterate over sorted_movie_results
        for movie in sorted_movie_results:
            # Append movie dictionary item with required keys and values to movies list
            movies.append({"movie_id": movie["id"],
                           "movie_name": movie["title"],
                           "movie_overview": movie["overview"],
                           "movie_popularity": movie["popularity"],
                           "movie_release_date": movie["release_date"]})
    # Raise exception in event of requests error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the TMDB API: {e}")
    # Raise exception in event of any uncaught error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    # Return list of movie dictionary items or empty list if no results returned
    return movies
