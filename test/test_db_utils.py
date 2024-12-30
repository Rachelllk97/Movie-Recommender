import unittest
from unittest.mock import patch, MagicMock

from db_config import HOST, USER, PASSWORD
from db_utils import (db_connect, db_add_user, db_get_user, db_add_user_movie_top_5, map_quiz_prompt_option_rows,
                      db_get_quizzes, db_add_user_quiz_responses, map_movie_rows, db_get_movie_top_5_for_similar_users,
                      DbConnectionError)


class TestDbUtils(unittest.TestCase):
    @patch("db_utils.mysql.connector.connect")
    def test_db_connect(self, mock_db_connect):
        # Define expected results
        expected_host = HOST
        expected_user = USER
        expected_password = PASSWORD
        expected_database = "user_movie_vibes"
        # Prepare mock function
        mock_db_connection = MagicMock()
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        db_connection = db_connect()
        # Evaluate results
        mock_db_connect.assert_called_once_with(
            host=expected_host, user=expected_user, password=expected_password, database=expected_database
        )
        self.assertEqual(db_connection, mock_db_connection)

    @patch("db_utils.db_connect")
    def test_db_add_user(self, mock_db_connect):
        # Define expected result
        expected_user_id = 1
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_last_name = "Stubbs"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.callproc.return_value = (test_user_first_name, test_user_last_name, test_user_email,
                                             test_user_password, expected_user_id)
        mock_db_connection.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        user_id = db_add_user(test_user_first_name, test_user_last_name, test_user_email, test_user_password)
        # Evaluate results
        mock_cursor.callproc.assert_called_once_with(
            "sp_add_user",
            (test_user_first_name, test_user_last_name, test_user_email, test_user_password, (None, "SIGNED"))
        )
        self.assertEqual(user_id, expected_user_id)

    @patch("db_utils.db_connect")
    def test_db_get_user(self, mock_db_connect):
        # Define expected result
        expected_user_id = 1
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [expected_user_id]
        mock_db_connection.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        user_id = db_get_user(test_user_email, test_user_password)
        # Evaluate results
        mock_cursor.execute.assert_called_once_with(
            """
            SELECT
                user_id
            FROM
                users
            WHERE
                user_email = %s
                AND BINARY user_password = %s
            """,
            (test_user_email, test_user_password)
        )
        self.assertEqual(user_id, expected_user_id)

    @patch("db_utils.db_connect")
    def test_db_add_user_movie_top_5(self, mock_db_connect):
        # Define expected result
        expected_update_count = 5
        # Prepare test data
        test_user_id = 1
        test_movie_names = "Shrek, Spy, Star Wars, Titanic, Top Gun"
        # Prepare mock function and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.callproc.return_value = (test_user_id, test_movie_names, expected_update_count)
        mock_db_connection.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        update_count = db_add_user_movie_top_5(test_user_id, test_movie_names)
        # Evaluate results
        mock_cursor.callproc.assert_called_once_with(
            "sp_add_user_movie_top_5",
            (test_user_id, test_movie_names, (None, "SIGNED"))
        )
        self.assertEqual(update_count, expected_update_count)

    def test_map_quiz_prompt_option_rows(self):
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
        test_quiz_prompt_option_rows = [
            (1, 1, "Quiz Prompt 1", 1, "Quiz Prompt Option 1"),
            (1, 1, "Quiz Prompt 1", 2, "Quiz Prompt Option 2"),
            (1, 2, "Quiz Prompt 2", 3, "Quiz Prompt Option 3"),
            (2, 3, "Quiz Prompt 3", 4, "Quiz Prompt Option 4")
        ]
        # Execute test
        quizzes = map_quiz_prompt_option_rows(test_quiz_prompt_option_rows)
        # Evaluate results
        self.assertEqual(quizzes, expected_quizzes)

    @patch("db_utils.db_connect")
    def test_db_get_quizzes(self, mock_db_connect):
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
        test_quiz_prompt_option_rows = [
            (1, 1, "Quiz Prompt 1", 1, "Quiz Prompt Option 1"),
            (1, 1, "Quiz Prompt 1", 2, "Quiz Prompt Option 2"),
            (1, 2, "Quiz Prompt 2", 3, "Quiz Prompt Option 3"),
            (2, 3, "Quiz Prompt 3", 4, "Quiz Prompt Option 4")
        ]
        # Prepare mock function and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = test_quiz_prompt_option_rows
        mock_db_connection.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        quizzes = db_get_quizzes()
        # Evaluate results
        self.assertEqual(quizzes, expected_quizzes)

    @patch("db_utils.db_connect")
    def test_db_add_user_quiz_responses(self, mock_db_connect):
        # Define expected result
        expected_update_count = 2
        # Prepare test data
        test_user_id = 1
        test_quiz_id = 1
        test_quiz_responses_str = "1, 3"
        # Prepare mock function and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.callproc.return_value = (test_user_id, test_quiz_id, test_quiz_responses_str, expected_update_count)
        mock_db_connection.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        update_count = db_add_user_quiz_responses(test_user_id, test_quiz_id, test_quiz_responses_str)
        # Evaluate results
        mock_cursor.callproc.assert_called_once_with(
            "sp_add_user_quiz_responses",
            (test_user_id, test_quiz_id, test_quiz_responses_str, (None, "SIGNED"))
        )
        self.assertEqual(update_count, expected_update_count)

    def test_map_movie_rows(self):
        # Define expected result
        expected_movies = [
            {"movie_name": "Shrek", "user_top_5": 1},
            {"movie_name": "Spy", "user_top_5": 1},
            {"movie_name": "Star Wars", "user_top_5": 1},
            {"movie_name": "Titanic", "user_top_5": 1},
            {"movie_name": "Top Gun", "user_top_5": 1},
            {"movie_name": "Terminator", "user_top_5": 0}
        ]
        # Prepare test data
        test_movie_rows = [
            ("Shrek", 1),
            ("Spy", 1),
            ("Star Wars", 1),
            ("Titanic", 1),
            ("Top Gun", 1),
            ("Terminator", 0)
        ]
        # Execute test
        movies = map_movie_rows(test_movie_rows)
        # Evaluate results
        self.assertEqual(movies, expected_movies)

    @patch("db_utils.db_connect")
    def test_db_get_movie_top_5_for_similar_users(self, mock_db_connect):
        # Define expected result
        expected_movies = [
            {"movie_name": "Shrek", "user_top_5": 1},
            {"movie_name": "Spy", "user_top_5": 1},
            {"movie_name": "Star Wars", "user_top_5": 1},
            {"movie_name": "Titanic", "user_top_5": 1},
            {"movie_name": "Top Gun", "user_top_5": 1},
            {"movie_name": "Terminator", "user_top_5": 0}
        ]
        # Prepare test data
        test_movie_rows = [
            ("Shrek", 1),
            ("Spy", 1),
            ("Star Wars", 1),
            ("Titanic", 1),
            ("Top Gun", 1),
            ("Terminator", 0)
        ]
        # Prepare mock function and cursor
        mock_db_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = test_movie_rows
        mock_db_connection.cursor.return_value = mock_cursor
        mock_db_connect.return_value = mock_db_connection
        # Execute test
        movies = db_get_movie_top_5_for_similar_users(1)
        # Evaluate results
        self.assertEqual(movies, expected_movies)


class TestDbConnectionError(unittest.TestCase):
    def test_db_connection_error(self):
        with self.assertRaises(DbConnectionError):
            raise DbConnectionError("Failed to connect")


if __name__ == "__main__":
    unittest.main()
