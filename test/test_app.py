import unittest
from unittest.mock import patch, call

from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        # Create app test client
        self.app = app.test_client()
        self.app.testing = True

    @patch("app.db_add_user")
    def test_app_post_user_success(self, mock_db_add_user):
        # Define expected results
        expected_user_id = 1
        expected_status_code = 200
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_last_name = "Stubbs"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function
        mock_db_add_user.return_value = expected_user_id
        # Execute test
        response = self.app.post(
            "/user",
            json={"user_first_name": test_user_first_name,
                  "user_last_name": test_user_last_name,
                  "user_email": test_user_email,
                  "user_password": test_user_password}
        )
        # Evaluate results
        mock_db_add_user.assert_called_with(test_user_first_name, test_user_last_name, test_user_email,
                                            test_user_password)
        self.assertEqual(response.json, {"user_id": expected_user_id})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_add_user")
    def test_app_post_user_missing_keys(self, mock_db_add_user):
        # Define expected results
        expected_user_id = None
        expected_status_code = 400
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Execute test
        response = self.app.post(
            "/user",
            json={"user_first_name": test_user_first_name,
                  "user_email": test_user_email,
                  "user_password": test_user_password}
        )
        # Evaluate results
        mock_db_add_user.assert_not_called()
        self.assertEqual(response.json, {"user_id": expected_user_id})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_get_user")
    def test_app_get_user_success(self, mock_db_get_user):
        # Define expected results
        expected_user_id = 1
        expected_status_code = 200
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function
        mock_db_get_user.return_value = expected_user_id
        # Execute test
        response = self.app.get(
            "/user",
            json={"user_email": test_user_email,
                  "user_password": test_user_password}
        )
        # Evaluate results
        mock_db_get_user.assert_called_with(test_user_email, test_user_password)
        self.assertEqual(response.json, {"user_id": expected_user_id})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_get_user")
    def test_app_get_user_missing_keys(self, mock_db_get_user):
        # Define expected results
        expected_user_id = None
        expected_status_code = 400
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        # Execute test
        response = self.app.get(
            "/user",
            json={"user_email": test_user_email}
        )
        # Evaluate results
        mock_db_get_user.assert_not_called()
        self.assertEqual(response.json, {"user_id": expected_user_id})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_add_user_movie_top_5")
    def test_app_post_user_movie_top_5_success(self, mock_db_add_user_movie_top_5):
        # Define expected results
        expected_update_count = 5
        expected_status_code = 200
        # Prepare test data
        test_user_id = 1
        test_movie_data = {
            "movie_names": ["Shrek", "Spy", "Star Wars", "Titanic", "Top Gun"]
        }
        # Prepare mock function
        mock_db_add_user_movie_top_5.return_value = expected_update_count
        # Execute test
        response = self.app.post(
            f"/user/{test_user_id}/movie/top_5",
            json=test_movie_data
        )
        # Evaluate results
        mock_db_add_user_movie_top_5.assert_called_with(test_user_id, test_movie_data["movie_names"])
        self.assertEqual(response.json, {"update_count": expected_update_count})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_add_user_movie_top_5")
    def test_app_post_user_movie_top_5_missing_keys(self, mock_db_add_user_movie_top_5):
        # Define expected results
        expected_update_count = None
        expected_status_code = 400
        # Prepare test data
        test_user_id = 1
        test_movie_data = {}
        # Execute test
        response = self.app.post(
            f"/user/{test_user_id}/movie/top_5",
            json=test_movie_data
        )
        # Evaluate results
        mock_db_add_user_movie_top_5.assert_not_called()
        self.assertEqual(response.json, {"update_count": expected_update_count})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_get_quizzes")
    def test_app_get_quizzes_success(self, mock_db_get_quizzes):
        # Define expected results
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
        expected_status_code = 200
        # Prepare mock function
        mock_db_get_quizzes.return_value = expected_quizzes
        # Execute test
        response = self.app.get(
            "/quizzes"
        )
        # Evaluate results
        mock_db_get_quizzes.assert_called_once()
        self.assertEqual(response.json, {"quizzes": expected_quizzes})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_add_user_quiz_responses")
    def test_app_post_user_quiz_success(self, mock_db_add_user_quiz_responses):
        # Define expected results
        expected_update_count = 2
        expected_status_code = 200
        # Prepare test data
        test_user_id = 1
        test_quiz_id = 1
        test_quiz_prompt_option_id_1 = 1
        test_quiz_prompt_option_id_2 = 3
        test_quiz_responses = {"quiz_responses": [
            {"quiz_prompt_option_id": test_quiz_prompt_option_id_1},
            {"quiz_prompt_option_id": test_quiz_prompt_option_id_2}
        ]}
        test_quiz_prompt_option_ids = []
        for test_quiz_response in test_quiz_responses["quiz_responses"]:
            test_quiz_prompt_option_ids.append(str(test_quiz_response["quiz_prompt_option_id"]))
        test_quiz_prompt_option_ids_str = ",".join(test_quiz_prompt_option_ids)
        # Prepare mock function
        mock_db_add_user_quiz_responses.return_value = expected_update_count
        # Execute test
        response = self.app.post(
            f"/user/{test_user_id}/quiz/{test_quiz_id}",
            json=test_quiz_responses
        )
        # Evaluate results
        mock_db_add_user_quiz_responses.assert_called_with(test_user_id, test_quiz_id, test_quiz_prompt_option_ids_str)
        self.assertEqual(response.json, {"update_count": expected_update_count})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_add_user_quiz_responses")
    def test_app_post_user_quiz_missing_keys(self, mock_db_add_user_quiz_responses):
        # Define expected results
        expected_update_count = None
        expected_status_code = 400
        # Prepare test data
        test_user_id = 1
        test_quiz_id = 1
        test_quiz_responses = {}
        # Execute test
        response = self.app.post(
            f"/user/{test_user_id}/quiz/{test_quiz_id}",
            json=test_quiz_responses
        )
        # Evaluate results
        mock_db_add_user_quiz_responses.assert_not_called()
        self.assertEqual(response.json, {"update_count": expected_update_count})
        self.assertEqual(response.status_code, expected_status_code)

    @patch("app.db_get_movie_top_5_for_similar_users")
    @patch("app.tmdb_get_movie_for_movie_name")
    @patch("app.tmdb_get_movie_recommendations_for_movie_id")
    @patch("app.tmdb_get_unique_movies")
    @patch("app.tmdb_get_filtered_movies")
    def test_app_get_user_movie_recommendations_success(self, mock_tmdb_get_filtered_movies,
                                                        mock_tmdb_get_unique_movies,
                                                        mock_tmdb_get_movie_recommendations_for_movie_id,
                                                        mock_tmdb_get_movie_for_movie_name,
                                                        mock_db_get_movie_top_5_for_similar_users):
        # Define expected results
        expected_movies = [
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
        ]
        expected_status_code = 200
        expected_calls = [
            call('Shrek'),
            call('Spy'),
            call('Star Wars'),
            call('Titanic'),
            call('Top Gun'),
            call('Terminator')
        ]
        # Prepare test data
        test_user_id = 1
        # Prepare mock functions
        mock_db_get_movie_top_5_for_similar_users.return_value = [
            {"movie_name": "Shrek", "user_top_5": 0},
            {"movie_name": "Spy", "user_top_5": 0},
            {"movie_name": "Star Wars", "user_top_5": 1},
            {"movie_name": "Titanic", "user_top_5": 1},
            {"movie_name": "Top Gun", "user_top_5": 1},
            {"movie_name": "Terminator", "user_top_5": 0}
        ]
        mock_tmdb_get_movie_for_movie_name.return_value = {
            "movie_id": 808,
            "movie_name": "Shrek",
            "movie_overview": "It ain't easy being green ...",
            "movie_popularity": 144.817,
            "movie_release_date": "2001-05-18"
        }
        mock_tmdb_get_movie_recommendations_for_movie_id.return_value = [
            {
                "movie_id": 10192,
                "movie_name": "Shrek Forever After",
                "movie_overview": "A bored and domesticated Shrek ...",
                "movie_popularity": 119.245,
                "movie_release_date": "2010-05-16"
            }
        ]
        mock_tmdb_get_unique_movies.return_value = iter([
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
        ])
        mock_tmdb_get_filtered_movies.return_value = iter([
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
        ])
        # Execute test
        response = self.app.get(
            f"/user/{test_user_id}/movie/recommendations"
        )
        # Evaluate results
        mock_db_get_movie_top_5_for_similar_users.assert_called_with(test_user_id)
        mock_tmdb_get_movie_for_movie_name.assert_has_calls(expected_calls)
        mock_tmdb_get_movie_recommendations_for_movie_id.assert_called_with(808)
        self.assertEqual(response.json, {"movies": expected_movies})
        self.assertEqual(response.status_code, expected_status_code)


if __name__ == "__main__":
    unittest.main()
