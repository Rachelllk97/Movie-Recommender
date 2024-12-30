import json
import unittest
from unittest.mock import patch

from api_config import API_BASE_URL
from api_utils import (api_add_user, api_get_user, api_add_user_movie_top_5, api_get_quizzes, map_quiz_responses,
                       api_add_user_quiz_responses, api_get_user_movie_recommendations)


class TestApiUtils(unittest.TestCase):

    @patch("api_utils.requests.post")
    def test_api_add_user_success(self, mock_post):
        # Define expected result
        expected_user_id = 1
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_last_name = "Stubbs"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        test_user_data = {
            "user_first_name": test_user_first_name,
            "user_last_name": test_user_last_name,
            "user_email": test_user_email,
            "user_password": test_user_password
        }
        test_status_code = 200
        # Prepare mock function
        mock_post.return_value.status_code = test_status_code
        mock_post.return_value.json.return_value = {"user_id": expected_user_id}
        # Execute test
        user_id = api_add_user(test_user_first_name, test_user_last_name, test_user_email, test_user_password)
        # Evaluate results
        mock_post.assert_called_with(f"{API_BASE_URL}/user",
                                     data=json.dumps(test_user_data),
                                     headers={"content-type": "application/json"})
        self.assertEqual(user_id, expected_user_id)

    @patch("api_utils.requests.post")
    def test_api_add_user_failure(self, mock_post):
        # Define expected result
        expected_user_id = None
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_last_name = "Stubbs"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        test_user_data = {
            "user_first_name": test_user_first_name,
            "user_last_name": test_user_last_name,
            "user_email": test_user_email,
            "user_password": test_user_password
        }
        test_status_code = 400
        # Prepare mock function
        mock_post.return_value.status_code = test_status_code
        mock_post.return_value.json.return_value = {"user_id": expected_user_id}
        # Execute test
        user_id = api_add_user(test_user_first_name, test_user_last_name, test_user_email, test_user_password)
        # Evaluate results
        mock_post.assert_called_with(f"{API_BASE_URL}/user",
                                     data=json.dumps(test_user_data),
                                     headers={"content-type": "application/json"})
        self.assertEqual(user_id, expected_user_id)

    @patch("api_utils.requests.get")
    def test_api_get_user_success(self, mock_get):
        # Define expected result
        expected_user_id = 1
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        test_user_data = {
            "user_email": test_user_email,
            "user_password": test_user_password
        }
        test_status_code = 200
        # Prepare mock function
        mock_get.return_value.status_code = test_status_code
        mock_get.return_value.json.return_value = {"user_id": expected_user_id}
        # Execute test
        user_id = api_get_user(test_user_email, test_user_password)
        # Evaluate results
        mock_get.assert_called_with(f"{API_BASE_URL}/user",
                                    data=json.dumps(test_user_data),
                                    headers={"content-type": "application/json"})
        self.assertEqual(user_id, expected_user_id)

    @patch("api_utils.requests.get")
    def test_api_get_user_failure(self, mock_get):
        # Define expected result
        expected_user_id = None
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        test_user_data = {
            "user_email": test_user_email,
            "user_password": test_user_password
        }
        test_status_code = 400
        # Prepare mock function
        mock_get.return_value.status_code = test_status_code
        mock_get.return_value.json.return_value = {"user_id": expected_user_id}
        # Execute test
        user_id = api_get_user(test_user_email, test_user_password)
        # Evaluate results
        mock_get.assert_called_with(f"{API_BASE_URL}/user",
                                    data=json.dumps(test_user_data),
                                    headers={"content-type": "application/json"})
        self.assertEqual(user_id, expected_user_id)

    @patch("api_utils.requests.post")
    def test_api_add_user_movie_top_5_success(self, mock_post):
        # Define expected result
        expected_update_count = 5
        # Prepare test data
        test_user_id = 1
        test_movie_names = "Shrek, Spy, Star Wars, Titanic, Top Gun"
        test_movie_data = {
            "movie_names": test_movie_names
        }
        test_status_code = 200
        # Prepare mock function
        mock_post.return_value.status_code = test_status_code
        mock_post.return_value.json.return_value = {"update_count": expected_update_count}
        # Execute test
        update_count = api_add_user_movie_top_5(test_user_id, test_movie_names)
        # Evaluate results
        mock_post.assert_called_with(f"{API_BASE_URL}/user/{test_user_id}/movie/top_5",
                                     data=json.dumps(test_movie_data),
                                     headers={"content-type": "application/json"})
        self.assertEqual(update_count, expected_update_count)

    @patch("api_utils.requests.post")
    def test_api_add_user_movie_top_5_failure(self, mock_post):
        # Define expected result
        expected_update_count = None
        # Prepare test data
        test_user_id = 1
        test_movie_names = "Shrek, Spy, Star Wars, Titanic, Top Gun"
        test_movie_data = {
            "movie_names": test_movie_names
        }
        test_status_code = 400
        # Prepare mock function
        mock_post.return_value.status_code = test_status_code
        mock_post.return_value.json.return_value = {"update_count": expected_update_count}
        # Execute test
        update_count = api_add_user_movie_top_5(test_user_id, test_movie_names)
        # Evaluate results
        mock_post.assert_called_with(f"{API_BASE_URL}/user/{test_user_id}/movie/top_5",
                                     data=json.dumps(test_movie_data),
                                     headers={"content-type": "application/json"})
        self.assertEqual(update_count, expected_update_count)

    @patch("api_utils.requests.get")
    def test_api_get_quizzes_success(self, mock_get):
        # Define expected result
        expected_quizzes = [
            {
                "quiz_id": 1,
                "quiz_prompts": [
                    {"quiz_prompt_id": 1, "quiz_prompt_text": "Quiz Prompt 1",
                     "quiz_prompt_options": [
                         {"quiz_prompt_option_id": 1, "quiz_prompt_option_text": "Quiz Prompt Option 1"},
                         {"quiz_prompt_option_id": 2, "quiz_prompt_option_text": "Quiz Prompt Option 2"}
                     ]
                     },
                    {"quiz_prompt_id": 2, "quiz_prompt_text": "Quiz Prompt 2",
                     "quiz_prompt_options": [
                         {"quiz_prompt_option_id": 3, "quiz_prompt_option_text": "Quiz Prompt Option 3"}
                     ]
                     }
                ]
            },
            {
                "quiz_id": 2,
                "quiz_prompts": [
                    {"quiz_prompt_id": 3, "quiz_prompt_text": "Quiz Prompt 3",
                     "quiz_prompt_options": [
                         {"quiz_prompt_option_id": 4, "quiz_prompt_option_text": "Quiz Prompt Option 4"}
                     ]
                     }
                ]
            }
        ]
        # Prepare test data
        test_status_code = 200
        # Prepare mock function
        mock_get.return_value.status_code = test_status_code
        mock_get.return_value.json.return_value = {"quizzes": expected_quizzes}
        # Execute test
        quizzes = api_get_quizzes()
        # Evaluate results
        mock_get.assert_called_with(f"{API_BASE_URL}/quizzes")
        self.assertEqual(quizzes, expected_quizzes)

    @patch("api_utils.requests.get")
    def test_api_get_quizzes_failure(self, mock_get):
        # Define expected result
        expected_quizzes = None
        # Prepare test data
        test_status_code = 400
        # Prepare mock function
        mock_get.return_value.status_code = test_status_code
        mock_get.return_value.json.return_value = {"quizzes": expected_quizzes}
        # Execute test
        quizzes = api_get_quizzes()
        # Evaluate results
        mock_get.assert_called_with(f"{API_BASE_URL}/quizzes")
        self.assertEqual(quizzes, expected_quizzes)

    def test_map_quiz_responses(self):
        # Define expected result
        expected_responses = [{"quiz_prompt_option_id": 1}, {"quiz_prompt_option_id": 2}]
        # Prepare test data
        test_quiz_responses = [1, 2]
        # Execute test
        mapped_responses = map_quiz_responses(test_quiz_responses)
        # Evaluate results
        self.assertEqual(mapped_responses, expected_responses)

    @patch("api_utils.requests.post")
    def test_api_add_user_quiz_responses_success(self, mock_post):
        # Define expected result
        expected_update_count = 2
        # Prepare test data
        test_user_id = 1
        test_quiz_id = 1
        test_quiz_responses = [1, 2]
        test_quiz_response_data = {"quiz_responses": [{"quiz_prompt_option_id": 1}, {"quiz_prompt_option_id": 2}]}
        test_status_code = 200
        # Prepare mock function
        mock_post.return_value.status_code = test_status_code
        mock_post.return_value.json.return_value = {"update_count": expected_update_count}
        # Execute test
        update_count = api_add_user_quiz_responses(test_user_id, test_quiz_id, test_quiz_responses)
        # Evaluate results
        mock_post.assert_called_with(f"{API_BASE_URL}/user/{test_user_id}/quiz/{test_quiz_id}",
                                     data=json.dumps(test_quiz_response_data),
                                     headers={"content-type": "application/json"})
        self.assertEqual(update_count, expected_update_count)

    @patch("api_utils.requests.post")
    def test_api_add_user_quiz_responses_failure(self, mock_post):
        # Define expected result
        expected_update_count = None
        # Prepare test data
        test_user_id = 1
        test_quiz_id = 1
        test_quiz_responses = [1, 2]
        test_quiz_response_data = {"quiz_responses": [{"quiz_prompt_option_id": 1}, {"quiz_prompt_option_id": 2}]}
        test_status_code = 400
        # Prepare mock function
        mock_post.return_value.status_code = test_status_code
        mock_post.return_value.json.return_value = {"update_count": expected_update_count}
        # Execute test
        update_count = api_add_user_quiz_responses(test_user_id, test_quiz_id, test_quiz_responses)
        # Evaluate results
        mock_post.assert_called_with(f"{API_BASE_URL}/user/{test_user_id}/quiz/{test_quiz_id}",
                                     data=json.dumps(test_quiz_response_data),
                                     headers={"content-type": "application/json"})
        self.assertEqual(update_count, expected_update_count)

    @patch("api_utils.requests.get")
    def test_api_get_user_movie_recommendations_success(self, mock_get):
        # Define expected result
        expected_movies = {"movies": [
            {"movie_id": 808,
             "movie_name": "Shrek",
             "movie_overview": "It ain't easy being green ...",
             "movie_popularity": 144.817,
             "movie_release_date": "2001-05-18"
             },
            {"movie_id": 238713,
             "movie_name": "Spy",
             "movie_overview": "A desk-bound CIA analyst ...",
             "movie_popularity": 29.197,
             "movie_release_date": "2015-05-06"
             }
        ]}
        # Prepare test data
        test_user_id = 1
        test_status_code = 200
        # Prepare mock function
        mock_get.return_value.status_code = test_status_code
        mock_get.return_value.json.return_value = {"movies": expected_movies}
        # Execute test
        movies = api_get_user_movie_recommendations(test_user_id)
        # Evaluate results
        mock_get.assert_called_with(f"{API_BASE_URL}/user/{test_user_id}/movie/recommendations")
        self.assertEqual(movies, expected_movies)

    @patch("api_utils.requests.get")
    def test_api_get_user_movie_recommendations_failure(self, mock_get):
        # Define expected result
        expected_movies = None
        # Prepare test data
        test_user_id = 1
        test_status_code = 400
        # Prepare mock function
        mock_get.return_value.status_code = test_status_code
        mock_get.return_value.json.return_value = {"movies": expected_movies}
        # Execute test
        movies = api_get_user_movie_recommendations(test_user_id)
        # Evaluate results
        mock_get.assert_called_with(f"{API_BASE_URL}/user/{test_user_id}/movie/recommendations")
        self.assertEqual(movies, expected_movies)


if __name__ == "__main__":
    unittest.main()
