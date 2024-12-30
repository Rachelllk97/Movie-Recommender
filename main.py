import re

from api_utils import (api_add_user, api_get_user, api_add_user_movie_top_5, api_get_quizzes,
                       api_add_user_quiz_responses, api_get_user_movie_recommendations)
from menu import Menu


# Initialise global variables
user_id = None
user_quiz_responses = []


# Define function to display welcome banner
def display_welcome_banner():
    print("=" * 48)
    print(" " * 10 + "Welcome to Movie Recommender" + " " * 10)
    print("=" * 48)


# Define helper function to obtain data from user in specified format
def get_valid_input(prompt, valid_regex_format, error_message):
    # Initialise input to return
    valid_input = None
    # Loop until valid input obtained
    while valid_input is None:
        # Prompt user to provide input
        user_input = input(prompt).strip()
        # Test if user input matches specified regular expression
        if re.match(valid_regex_format, user_input):
            # Set valid input as user input to terminate loop
            valid_input = user_input
        else:
            # Print specified error message and continue loop
            print(error_message)
    # Return validated input
    return valid_input


# Define function to add user
def add_user():
    # Set scope of user_id to populate
    global user_id
    # Prompt user to supply details
    user_first_name = input("Please enter your first name: ").strip()
    user_last_name = input("Please enter your last name: ").strip()
    user_email = get_valid_input("Please enter a valid email address: ",
                                 r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                                 "Sorry, invalid email address. Please try again.")
    user_password = get_valid_input("Please enter a strong password: ",
                                    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
                                    "Sorry, invalid password. Please try again."
                                    "Password must be at least 8 characters, including 1 uppercase, 1 lowercase, "
                                    "1 digit and 1 special character.")
    # Set user_id to return value of api_add_user called with user details
    user_id = api_add_user(user_first_name, user_last_name, user_email, user_password)
    # Test if user_id returned and display message accordingly
    if user_id:
        print("Account created successfully!")
    else:
        print("Failed to create account. Please try again.")


# Define function to validate user
def validate_user():
    # Set scope of user_id to populate
    global user_id
    # Prompt user to supply details
    user_email = input("Please enter your email address: ").strip()
    user_password = input("Please enter your password: ").strip()
    # Set user_id to return value of api_get_user called with user details
    user_id = api_get_user(user_email, user_password)
    # Test if user_id returned and display message accordingly
    if user_id:
        print("Welcome to your account!")
    else:
        print("Account details not recognised. Please try again, or select '2' to create a new account.")


# Define function to evaluate whether to exit User Menu
def exit_user_menu(user_choice, exit_option):
    # Test for populated global user_id or exit option chosen
    if user_id or user_choice == exit_option:
        return True
    else:
        return False


# Define function to add user's top 5 movies
def add_user_movie_top_5():
    # Prompt user to supply comma-separated list of movie names
    movie_names = get_valid_input("Please enter a comma-separated list of your top 5 movies. ",
                                  r"(.*)\,(.*)",
                                  "Movie names must be separated by commas. Please try again.")
    # Set update_count to return value of api_add_user_movie_top_5 called with user_id and movie_names
    update_count = api_add_user_movie_top_5(user_id, movie_names)
    # Test if 5 movies added and display message accordingly
    if update_count == 5:
        print("Top 5 movies recorded successfully.")
    else:
        print("Sorry, unable to add top 5 movies. Please try again.")


# Define helper function to add user's quiz response to global list
def add_user_quiz_response(menu_option_parameter):
    global user_quiz_responses
    user_quiz_responses.append(menu_option_parameter)


# Define function to display quiz and record user's responses
def take_quiz():
    # Set scope of user_quiz_responses to populate
    global user_quiz_responses
    # Set quizzes to return value of api_get_quizzes
    quizzes = api_get_quizzes()
    # Iterate over nested list of quizzes
    for quiz in quizzes:
        # Extract list of quiz prompts
        quiz_prompts = quiz["quiz_prompts"]
        # Iterate over nested list of quiz prompts
        for quiz_prompt in quiz_prompts:
            # Initialise menu options and parameters to build quiz menu
            menu_options = {}
            menu_option_parameters = []
            # Iterate over list of quiz prompt options
            for quiz_prompt_option in quiz_prompt["quiz_prompt_options"]:
                # Add entry to menu_options dictionary with key of "quiz_prompt_option_text" and value of
                # add_user_quiz_response function
                menu_options[quiz_prompt_option["quiz_prompt_option_text"]] = add_user_quiz_response
                # Append quiz_prompt_option_id to menu_option_parameters list so add_user_quiz_response function
                # called with appropriate quiz_prompt_option_id parameter
                menu_option_parameters.append(quiz_prompt_option["quiz_prompt_option_id"])
            # Create instance of Menu class with title as quiz prompt text and options and option parameters built
            # from processing current quiz prompt
            menu = Menu(
                title=quiz_prompt["quiz_prompt_text"],
                options=menu_options,
                option_parameters=menu_option_parameters,
                exit_function=None
            )
            # Display menu for current quiz prompt
            menu.loop()
            # Break out of quiz processing loop if user chooses to exit
            if menu.user_choice == menu.exit_option:
                break
        # Test if user response for every quiz prompt
        if len(user_quiz_responses) == len(quiz_prompts):
            # Set update count to return value of api_add_user_quiz_responses called with user_id, current quiz_id
            # and user's quiz responses
            update_count = api_add_user_quiz_responses(user_id, quiz["quiz_id"], user_quiz_responses)
            # Test if update_count matches number of quiz prompts and display message accordingly
            if update_count == len(quiz_prompts):
                print("Quiz responses recorded successfully.")
            else:
                print("Sorry, unable to record quiz responses. Please try again.")


# Define function to get user's movie recommendations
def get_user_movie_recommendations():
    # Set movies to return value of api_get_user_movie_recommendations called with global user_id
    movies = api_get_user_movie_recommendations(user_id)
    # Test if movies returned
    if movies:
        # Initialise tracking variable
        index = 1
        # Iterate over movies
        for movie in movies:
            # If processing first item, display title
            if index == 1:
                print("\nYour Top 25 Movie Recommendations:\n")
            # Extract and display movie name, year and overview
            movie_name = movie["movie_name"]
            release_year = movie["movie_release_date"][:4]
            movie_overview = movie.get("movie_overview", "No overview available.")
            print(f"{index}. {movie_name} ({release_year})")
            print(f"{movie_overview}\n")
            # Increment tracking variable
            index += 1
    else:
        print("Sorry, unable to get movie recommendations.")


# Define main function to run application
def run():
    display_welcome_banner()
    # Set up and call User Menu
    user_menu_options = {
        "Existing User Login": validate_user,
        "New User Registration": add_user
    }
    user_menu = Menu("User Menu", user_menu_options, None, exit_user_menu)
    user_menu.loop()
    # If user has not selected Exit from User Menu, set up and call Main Menu
    if user_menu.user_choice != user_menu.exit_option:
        main_menu_options = {
            "Add your top 5 movies": add_user_movie_top_5,
            "Take a quiz": take_quiz,
            "Get movie recommendations": get_user_movie_recommendations
        }
        main_menu = Menu("Main Menu", main_menu_options, None, None)
        # Loop Main Menu until user selects Exit
        while not main_menu.exit_condition:
            main_menu.loop()
    print("\nThank you for using Movie Recommender!")


if __name__ == "__main__":
    run()
