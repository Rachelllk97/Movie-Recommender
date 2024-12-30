import unittest
from unittest.mock import patch, call

import main
from menu import Menu


class TestMenu(unittest.TestCase):

    def setUp(self):
        # Prepare test options
        self.options = {
            "Option 1": main.validate_user,
            "Option 2": main.add_user
        }
        # Create test menu with test options
        self.menu = Menu("Test Menu", self.options, None, None)
        # Prepare test option parameters
        self.option_parameters = [1, 2]
        # Create test menu with test options and option parameters
        self.menu_2 = Menu("Test Menu 2", self.options, self.option_parameters, None)
        # Create test menu with test options and exit function
        self.menu_3 = Menu("Test Menu 3", self.options, None, main.exit_user_menu)

    def test_menu_initialisation(self):
        # Evaluate results of self.menu constructor
        self.assertEqual(self.menu.title, "Test Menu")
        self.assertEqual(self.menu.options, self.options)
        self.assertEqual(self.menu.option_parameters, None)
        self.assertEqual(self.menu.exit_option, len(self.options) + 1)
        self.assertEqual(self.menu.user_choice, 0)
        self.assertFalse(self.menu.exit_condition)
        self.assertFalse(self.menu.exit_function)
        # Evaluate results of self.menu_2 constructor
        self.assertEqual(self.menu_2.title, "Test Menu 2")
        self.assertEqual(self.menu_2.options, self.options)
        self.assertEqual(self.menu_2.option_parameters, self.option_parameters)
        self.assertEqual(self.menu_2.exit_option, len(self.options) + 1)
        self.assertEqual(self.menu_2.user_choice, 0)
        self.assertFalse(self.menu_2.exit_condition)
        self.assertFalse(self.menu_2.exit_function)
        # Evaluate results of self.menu_3 constructor
        self.assertEqual(self.menu_3.title, "Test Menu 3")
        self.assertEqual(self.menu_3.options, self.options)
        self.assertEqual(self.menu_3.option_parameters, None)
        self.assertEqual(self.menu_3.exit_option, len(self.options) + 1)
        self.assertEqual(self.menu_3.user_choice, 0)
        self.assertFalse(self.menu_3.exit_condition)
        self.assertTrue(self.menu_3.exit_function)

    @patch("builtins.print")
    def test_display(self, mock_print):
        # Define expected results
        expected_calls = [
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Execute test
        self.menu.display()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.validate_user")
    @patch("main.add_user")
    def test_loop_valid_choice(self, mock_add_user, mock_validate_user, mock_input, mock_print):
        # Define expected results
        expected_user_choice = 1
        expected_exit_condition = False
        expected_calls = [
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Prepare test data
        self.menu.options["Option 1"] = mock_validate_user
        self.menu.options["Option 2"] = mock_add_user
        test_input = [str(expected_user_choice)]
        # Prepare mock function
        mock_input.side_effect = test_input
        # Execute test
        self.menu.loop()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(self.menu.user_choice, expected_user_choice)
        mock_validate_user.assert_called_with()
        mock_add_user.assert_not_called()
        self.assertEqual(self.menu.exit_condition, expected_exit_condition)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.validate_user")
    @patch("main.add_user")
    def test_loop_valid_choice_with_parameters(self, mock_add_user, mock_validate_user, mock_input, mock_print):
        # Define expected results
        expected_user_choice = 1
        expected_exit_condition = False
        expected_calls = [
            call("\nTest Menu 2\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Prepare test data
        self.menu_2.options["Option 1"] = mock_validate_user
        self.menu_2.options["Option 2"] = mock_add_user
        test_input = [str(expected_user_choice)]
        # Prepare mock function
        mock_input.side_effect = test_input
        # Execute test
        self.menu_2.loop()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(self.menu_2.user_choice, expected_user_choice)
        mock_validate_user.assert_called_with(self.option_parameters[0])
        mock_add_user.assert_not_called()
        self.assertEqual(self.menu.exit_condition, expected_exit_condition)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.validate_user")
    @patch("main.add_user")
    @patch("main.exit_user_menu")
    def test_loop_valid_choice_with_exit_function(self, mock_exit_user_menu, mock_add_user, mock_validate_user,
                                                  mock_input, mock_print):
        # Define expected results
        expected_user_choice = 1
        expected_exit_condition = True
        expected_calls = [
            call("\nTest Menu 3\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Prepare test data
        self.menu_3.options["Option 1"] = mock_validate_user
        self.menu_3.options["Option 2"] = mock_add_user
        self.menu_3.exit_function = mock_exit_user_menu
        test_input = [str(expected_user_choice)]
        # Prepare mock functions
        mock_exit_user_menu.return_value = True
        mock_input.side_effect = test_input
        # Execute test
        self.menu_3.loop()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(self.menu_3.user_choice, expected_user_choice)
        mock_validate_user.assert_called_with()
        mock_add_user.assert_not_called()
        mock_exit_user_menu.assert_called_with(self.menu_3.user_choice, self.menu_3.exit_option)
        self.assertEqual(self.menu_3.exit_condition, expected_exit_condition)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.validate_user")
    @patch("main.add_user")
    def test_loop_invalid_choice(self, mock_add_user, mock_validate_user, mock_input, mock_print):
        # Define expected results
        expected_user_choice = 3
        expected_calls = [
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit"),
            call("Sorry, choice must be from the list. Please try again."),
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Prepare test data
        self.menu.options["Option 1"] = mock_validate_user
        self.menu.options["Option 2"] = mock_add_user
        test_input = ["5", str(expected_user_choice)]
        # Prepare mock function
        mock_input.side_effect = test_input
        # Execute test
        self.menu.loop()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)
        mock_validate_user.assert_not_called()
        mock_add_user.assert_not_called()
        self.assertEqual(self.menu.user_choice, expected_user_choice)

    @patch("builtins.print")
    @patch("builtins.input")
    @patch("main.validate_user")
    @patch("main.add_user")
    def test_loop_non_integer_choice(self, mock_add_user, mock_validate_user, mock_input, mock_print):
        # Define expected results
        expected_user_choice = 3
        expected_calls = [
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit"),
            call("Sorry, you must enter a numerical value. Please try again."),
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Prepare test data
        self.menu.options["Option 1"] = mock_validate_user
        self.menu.options["Option 2"] = mock_add_user
        test_input = ["A", str(expected_user_choice)]
        # Prepare mock function
        mock_input.side_effect = test_input
        # Execute test
        self.menu.loop()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)
        mock_validate_user.assert_not_called()
        mock_add_user.assert_not_called()
        self.assertEqual(self.menu.user_choice, expected_user_choice)

    @patch("builtins.print")
    @patch("builtins.input")
    def test_loop_exit(self, mock_input, mock_print):
        # Define expected results
        expected_user_choice = 3
        expected_exit_condition = True
        expected_calls = [
            call("\nTest Menu\n"),
            call("1: Option 1"),
            call("2: Option 2"),
            call("3: Exit")
        ]
        # Prepare test data
        test_input = [str(expected_user_choice)]
        # Prepare mock function
        mock_input.side_effect = test_input
        # Execute test
        self.menu.loop()
        # Evaluate results
        mock_print.assert_has_calls(expected_calls)
        self.assertEqual(self.menu.user_choice, expected_user_choice)
        self.assertEqual(self.menu.user_choice, self.menu.exit_option)
        self.assertEqual(self.menu.exit_condition, expected_exit_condition)


if __name__ == "__main__":
    unittest.main()
