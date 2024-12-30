import unittest
from unittest.mock import patch, call

import main
from main import (display_welcome_banner, get_valid_input, add_user, validate_user, exit_user_menu,
                  add_user_movie_top_5, add_user_quiz_response, take_quiz, get_user_movie_recommendations)


class TestMain(unittest.TestCase):

    @patch("builtins.print")
    def test_display_welcome_banner(self, mock_print):
        # Define expected results
        expected_calls = [
            call("=" * 48),
            call(" " * 10 + "Welcome to Movie Recommender" + " " * 10),
            call("=" * 48)
        ]
        # Execute test
        display_welcome_banner()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_get_valid_input_email(self, mock_input, mock_print):
        # Define expected result
        expected_valid_input = "sophie.stubbs@nomail.com"
        # Prepare test data
        test_prompt = "Please enter your email address: "
        test_valid_regex_format = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        test_error_message = "Sorry, invalid email address. Please try again."
        # Prepare mock function
        mock_input.side_effect = ["sls@com", expected_valid_input]
        # Execute test
        valid_input = get_valid_input(test_prompt, test_valid_regex_format, test_error_message)
        # Evaluate results
        mock_input.assert_any_call(test_prompt)
        mock_print.assert_any_call(test_error_message)
        self.assertEqual(valid_input, expected_valid_input)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_get_valid_input_password(self, mock_input, mock_print):
        # Define expected result
        expected_valid_input = "TestPassword1!"
        # Prepare test data
        test_prompt = "Please enter your password: "
        test_valid_regex_format = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        test_error_message = "Sorry, invalid password. Please try again."
        # Prepare mock function
        mock_input.side_effect = ["2Short!", expected_valid_input]
        # Execute test
        valid_input = get_valid_input(test_prompt, test_valid_regex_format, test_error_message)
        # Evaluate results
        mock_input.assert_any_call(test_prompt)
        mock_print.assert_any_call(test_error_message)
        self.assertEqual(valid_input, expected_valid_input)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.api_add_user")
    def test_add_user_success(self, mock_api_add_user, mock_input, mock_print):
        # Define expected results
        expected_user_id = 1
        expected_calls = [
            call("Account created successfully!")
        ]
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_last_name = "Stubbs"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function
        mock_input.side_effect = [test_user_first_name, test_user_last_name, test_user_email, test_user_password]
        mock_api_add_user.return_value = expected_user_id
        # Execute test
        add_user()
        # Evaluate results
        mock_api_add_user.assert_called_with(test_user_first_name, test_user_last_name, test_user_email,
                                             test_user_password)
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(main.user_id, expected_user_id)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.api_add_user")
    def test_add_user_failure(self, mock_api_add_user, mock_input, mock_print):
        # Define expected results
        expected_user_id = None
        expected_calls = [
            call("Failed to create account. Please try again.")
        ]
        # Prepare test data
        test_user_first_name = "Sophie"
        test_user_last_name = "Stubbs"
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function
        mock_input.side_effect = [test_user_first_name, test_user_last_name, test_user_email, test_user_password]
        mock_api_add_user.return_value = expected_user_id
        # Execute test
        add_user()
        # Evaluate results
        mock_api_add_user.assert_called_with(test_user_first_name, test_user_last_name, test_user_email,
                                             test_user_password)
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(main.user_id, expected_user_id)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.api_get_user")
    def test_validate_user_success(self, mock_api_get_user, mock_input, mock_print):
        # Define expected results
        expected_user_id = 1
        expected_calls = [
            call("Welcome to your account!")
        ]
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword1!"
        # Prepare mock function
        mock_input.side_effect = [test_user_email, test_user_password]
        mock_api_get_user.return_value = expected_user_id
        # Execute test
        validate_user()
        # Evaluate results
        mock_api_get_user.assert_called_with(test_user_email, test_user_password)
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(main.user_id, expected_user_id)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.api_get_user")
    def test_validate_user_failure(self, mock_api_get_user, mock_input, mock_print):
        # Define expected results
        expected_user_id = None
        expected_calls = [
            call("Account details not recognised. Please try again, or select '2' to create a new account.")
        ]
        # Prepare test data
        test_user_email = "sophie.stubbs@nomail.com"
        test_user_password = "TestPassword2!"
        # Prepare mock function
        mock_input.side_effect = [test_user_email, test_user_password]
        mock_api_get_user.return_value = expected_user_id
        # Execute test
        validate_user()
        # Evaluate results
        mock_api_get_user.assert_called_with(test_user_email, test_user_password)
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(main.user_id, expected_user_id)

    def test_exit_user_menu_with_user_id(self):
        # Define expected result
        expected_result = True
        # Prepare test data
        test_user_id = 1
        test_user_choice = 1
        test_exit_option = 3
        main.user_id = test_user_id
        # Execute test
        result = exit_user_menu(test_user_choice, test_exit_option)
        # Evaluate results
        self.assertEqual(result, expected_result)

    def test_exit_user_menu_without_user_id(self):
        # Define expected result
        expected_result = False
        # Prepare test data
        test_user_id = None
        test_user_choice = 1
        test_exit_option = 3
        main.user_id = test_user_id
        # Execute test
        result = exit_user_menu(test_user_choice, test_exit_option)
        # Evaluate results
        self.assertEqual(result, expected_result)

    def test_exit_user_menu_with_user_choice_equals_exit_option(self):
        # Define expected result
        expected_result = True
        # Prepare test data
        test_user_id = None
        test_user_choice = 3
        test_exit_option = 3
        main.user_id = test_user_id
        # Execute test
        result = exit_user_menu(test_user_choice, test_exit_option)
        # Evaluate results
        self.assertEqual(result, expected_result)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.api_add_user_movie_top_5")
    def test_add_user_movie_top_5_success(self, mock_api_add_user_movie_top_5, mock_input, mock_print):
        # Define expected result
        expected_calls = [
            call("Top 5 movies recorded successfully.")
        ]
        # Prepare test data
        test_user_id = 1
        test_movie_names = "Shrek, Spy, Star Wars, Titanic, Top Gun"
        test_update_count = 5
        main.user_id = test_user_id
        # Prepare mock function
        mock_input.side_effect = [test_movie_names]
        mock_api_add_user_movie_top_5.return_value = test_update_count
        # Execute test
        add_user_movie_top_5()
        # Evaluate results
        mock_api_add_user_movie_top_5.assert_called_with(test_user_id, test_movie_names)
        mock_print.assert_has_calls(expected_calls)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.api_add_user_movie_top_5")
    def test_add_user_movie_top_5_failure(self, mock_api_add_user_movie_top_5, mock_input, mock_print):
        # Define expected result
        expected_calls = [
            call("Sorry, unable to add top 5 movies. Please try again.")
        ]
        # Prepare test data
        test_user_id = 1
        test_movie_names = "Shrek, Spy, Star Wars, Titanic, Top Gun"
        test_update_count = None
        main.user_id = test_user_id
        # Prepare mock function
        mock_input.side_effect = [test_movie_names]
        mock_api_add_user_movie_top_5.return_value = test_update_count
        # Execute test
        add_user_movie_top_5()
        # Evaluate results
        mock_api_add_user_movie_top_5.assert_called_with(test_user_id, test_movie_names)
        mock_print.assert_has_calls(expected_calls)

    def test_add_user_quiz_response(self):
        # Define expected result
        expected_user_quiz_responses = [2]
        # Prepare test data
        test_user_quiz_responses = []
        test_user_quiz_response = expected_user_quiz_responses[0]
        main.user_quiz_responses = test_user_quiz_responses
        # Execute test
        add_user_quiz_response(test_user_quiz_response)
        # Evaluate results
        self.assertIn(test_user_quiz_response, main.user_quiz_responses)
        self.assertEqual(main.user_quiz_responses, expected_user_quiz_responses)

    @patch("builtins.print")
    @patch("main.api_get_quizzes")
    @patch("builtins.input")
    @patch("main.api_add_user_quiz_responses")
    def test_take_quiz_success(self, mock_api_add_user_quiz_responses, mock_input, mock_api_get_quizzes, mock_print):
        # Define expected result
        expected_calls = [
            call("\nQuiz Prompt 1\n"),
            call("1: Quiz Prompt Option 1"),
            call("2: Quiz Prompt Option 2"),
            call("3: Exit"),
            call("\nQuiz Prompt 2\n"),
            call("1: Quiz Prompt Option 3"),
            call("2: Exit"),
            call("Quiz responses recorded successfully.")
        ]
        # Prepare test data
        test_user_id = 1
        test_quizzes = [
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
            }
        ]
        test_quiz_id = test_quizzes[0]["quiz_id"]
        test_user_quiz_responses = []
        main.user_id = test_user_id
        main.user_quiz_responses = test_user_quiz_responses
        test_user_input = ["2", "1"]
        test_update_count = 2
        # Prepare mock functions
        mock_api_get_quizzes.return_value = test_quizzes
        mock_input.side_effect = test_user_input
        mock_api_add_user_quiz_responses.return_value = test_update_count
        # Execute test
        take_quiz()
        # Evaluate results
        mock_api_get_quizzes.assert_called_once()
        mock_print.assert_has_calls(expected_calls)
        mock_api_add_user_quiz_responses.assert_called_with(test_user_id, test_quiz_id, main.user_quiz_responses)

    @patch("builtins.print")
    @patch("main.api_get_quizzes")
    @patch("builtins.input")
    @patch("main.api_add_user_quiz_responses")
    def test_take_quiz_failure(self, mock_api_add_user_quiz_responses, mock_input, mock_api_get_quizzes, mock_print):
        # Define expected result
        expected_calls = [
            call("\nQuiz Prompt 1\n"),
            call("1: Quiz Prompt Option 1"),
            call("2: Quiz Prompt Option 2"),
            call("3: Exit"),
            call("\nQuiz Prompt 2\n"),
            call("1: Quiz Prompt Option 3"),
            call("2: Exit"),
            call("Sorry, unable to record quiz responses. Please try again.")
        ]
        # Prepare test data
        test_user_id = 1
        test_quizzes = [
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
            }
        ]
        test_quiz_id = test_quizzes[0]["quiz_id"]
        test_user_quiz_responses = []
        main.user_id = test_user_id
        main.user_quiz_responses = test_user_quiz_responses
        test_user_input = ["2", "1"]
        test_update_count = None
        # Prepare mock functions
        mock_api_get_quizzes.return_value = test_quizzes
        mock_input.side_effect = test_user_input
        mock_api_add_user_quiz_responses.return_value = test_update_count
        # Execute test
        take_quiz()
        # Evaluate results
        mock_api_get_quizzes.assert_called_once()
        mock_print.assert_has_calls(expected_calls)
        mock_api_add_user_quiz_responses.assert_called_with(test_user_id, test_quiz_id, main.user_quiz_responses)

    @patch("builtins.print")
    @patch("main.api_get_user_movie_recommendations")
    def test_get_user_movie_recommendations_success(self, mock_api_get_user_movie_recommendations, mock_print):
        # Define expected result
        expected_calls = [
            call("1. Shrek (2001)"),
            call("It ain't easy being green ...\n"),
            call("2. Spy (2015)"),
            call("A desk-bound CIA analyst ...\n")
        ]
        # Prepare test data
        test_user_id = 1
        main.user_id = test_user_id
        test_movies = [
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
        # Prepare mock function
        mock_api_get_user_movie_recommendations.return_value = test_movies
        # Execute test
        get_user_movie_recommendations()
        # Evaluate results
        mock_api_get_user_movie_recommendations.assert_called_with(test_user_id)
        mock_print.assert_has_calls(expected_calls)

    @patch("builtins.print")
    @patch("main.api_get_user_movie_recommendations")
    def test_get_user_movie_recommendations_failure(self, mock_api_get_user_movie_recommendations, mock_print):
        # Define expected result
        expected_calls = [
            call("Sorry, unable to get movie recommendations.")
        ]
        # Prepare test data
        test_user_id = 1
        main.user_id = test_user_id
        test_movies = []
        # Prepare mock function
        mock_api_get_user_movie_recommendations.return_value = test_movies
        # Execute test
        get_user_movie_recommendations()
        # Evaluate results
        mock_api_get_user_movie_recommendations.assert_called_with(test_user_id)
        mock_print.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()
