import unittest
from unittest.mock import patch, MagicMock

from tmdb_config import TMDB_BEARER_TOKEN
from tmdb_utils import (tmdb_get_unique_movies, tmdb_get_filtered_movies, tmdb_get_movie_for_movie_name,
                        tmdb_get_movie_recommendations_for_movie_id)


class TestTmdbUtils(unittest.TestCase):

    def test_tmdb_get_unique_movies(self):
        # Define expected result
        expected_movie_ids = [1, 2]
        # Prepare test data
        test_movies = [
            {"movie_id": 1, "movie_name": "Shrek"},
            {"movie_id": 2, "movie_name": "Spy"},
            {"movie_id": 1, "movie_name": "Shrek"}
        ]
        # Execute test
        unique_movies = list(tmdb_get_unique_movies(test_movies))
        # Evaluate results
        self.assertEqual(len(unique_movies), len(expected_movie_ids))
        self.assertEqual(unique_movies[0]["movie_id"], expected_movie_ids[0])
        self.assertEqual(unique_movies[1]["movie_id"], expected_movie_ids[1])

    def test_tmdb_get_filtered_movies(self):
        # Define expected result
        expected_movie_ids = [1, 3]
        # Prepare test data
        test_movies = [
            {"movie_id": 1, "movie_name": "Shrek"},
            {"movie_id": 2, "movie_name": "Spy"},
            {"movie_id": 3, "movie_name": "Star Wars"},
            {"movie_id": 4, "movie_name": "Titanic"},
        ]
        test_movie_ids_to_exclude = [2, 4]
        # Execute test
        filtered_movies = list(tmdb_get_filtered_movies(test_movies, test_movie_ids_to_exclude))
        # Evaluate results
        self.assertEqual(len(filtered_movies), len(expected_movie_ids))
        self.assertEqual(filtered_movies[0]["movie_id"], expected_movie_ids[0])
        self.assertEqual(filtered_movies[1]["movie_id"], expected_movie_ids[1])

    @patch("tmdb_utils.requests.get")
    def test_tmdb_get_movie_for_movie_name(self, mock_get):
        # Define expected results
        expected_movie_id = 808
        expected_movie_name = "Shrek"
        expected_movie_overview = "It ain't easy being green ..."
        expected_movie_popularity = 144.817
        expected_movie_release_date = "2001-05-18"
        # Prepare test data
        test_movie_name = "Shrek"
        test_url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-GB&page=1&query=Shrek"
        test_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
        }
        test_movie_results = {
            "results": [{
                "id": expected_movie_id,
                "original_language": "en",
                "original_title": "Shrek",
                "title": expected_movie_name,
                "overview": expected_movie_overview,
                "popularity": expected_movie_popularity,
                "release_date": expected_movie_release_date
            }]
        }
        # Prepare mock function
        mock_response = MagicMock()
        mock_response.json.return_value = test_movie_results
        mock_get.return_value = mock_response
        # Execute test
        movie = tmdb_get_movie_for_movie_name(test_movie_name)
        # Evaluate results
        mock_get.assert_called_with(test_url, headers=test_headers)
        self.assertIsNotNone(movie)
        self.assertEqual(movie["movie_id"], expected_movie_id)
        self.assertEqual(movie["movie_name"], expected_movie_name)
        self.assertEqual(movie["movie_overview"], expected_movie_overview)
        self.assertEqual(movie["movie_popularity"], expected_movie_popularity)
        self.assertEqual(movie["movie_release_date"], expected_movie_release_date)

    @patch("tmdb_utils.requests.get")
    def test_tmdb_get_movie_recommendations_for_movie_id(self, mock_get):
        # Define expected results
        expected_movies = [
            {
                "movie_id": 808,
                "movie_name": "Shrek",
                "movie_overview": "It ain't easy being green ...",
                "movie_popularity": 144.817,
                "movie_release_date": "2001-05-18"
            },
            {
                "movie_id": 238713,
                "movie_name": "Spy",
                "movie_overview": "A desk-bound CIA analyst ...",
                "movie_popularity": 29.197,
                "movie_release_date": "2015-05-06"
            }
        ]
        # Prepare test data
        test_movie_id = 10192
        test_url = "https://api.themoviedb.org/3/movie/10192/recommendations?language=en-GB&page=1"
        test_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
        }
        test_movie_results = {
            "results": [
                {
                    "id": expected_movies[0]["movie_id"],
                    "original_language": "en",
                    "original_title": "Shrek",
                    "title": expected_movies[0]["movie_name"],
                    "overview": expected_movies[0]["movie_overview"],
                    "popularity": expected_movies[0]["movie_popularity"],
                    "release_date": expected_movies[0]["movie_release_date"]
                },
                {
                    "id": expected_movies[1]["movie_id"],
                    "original_language": "en",
                    "original_title": "Spy",
                    "title": expected_movies[1]["movie_name"],
                    "overview": expected_movies[1]["movie_overview"],
                    "popularity": expected_movies[1]["movie_popularity"],
                    "release_date": expected_movies[1]["movie_release_date"]
                }
            ]
        }
        # Prepare mock function
        mock_response = MagicMock()
        mock_response.json.return_value = test_movie_results
        mock_get.return_value = mock_response
        # Execute test
        movies = tmdb_get_movie_recommendations_for_movie_id(test_movie_id)
        # Evaluate results
        mock_get.assert_called_with(test_url, headers=test_headers)
        self.assertEqual(len(movies), len(expected_movies))
        self.assertEqual(movies[0]["movie_id"], expected_movies[0]["movie_id"])
        self.assertEqual(movies[0]["movie_name"], expected_movies[0]["movie_name"])
        self.assertEqual(movies[0]["movie_overview"], expected_movies[0]["movie_overview"])
        self.assertEqual(movies[0]["movie_popularity"], expected_movies[0]["movie_popularity"])
        self.assertEqual(movies[0]["movie_release_date"], expected_movies[0]["movie_release_date"])
        self.assertEqual(movies[1]["movie_id"], expected_movies[1]["movie_id"])
        self.assertEqual(movies[1]["movie_name"], expected_movies[1]["movie_name"])
        self.assertEqual(movies[1]["movie_overview"], expected_movies[1]["movie_overview"])
        self.assertEqual(movies[1]["movie_popularity"], expected_movies[1]["movie_popularity"])
        self.assertEqual(movies[1]["movie_release_date"], expected_movies[1]["movie_release_date"])


if __name__ == "__main__":
    unittest.main()
