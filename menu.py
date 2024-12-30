# Define class to display configurable menu
class Menu:
    # Define constructor method to initialise menu
    def __init__(self, title, options, option_parameters=None, exit_function=None):
        # Set attributes to input parameters
        self.title = title
        self.options = options
        # Set attributes to optional input parameters
        self.option_parameters = option_parameters
        self.exit_function = exit_function
        # Set exit_option to 1 more than number of options
        self.exit_option = len(self.options) + 1
        # Initialise user_choice and exit_condition
        self.user_choice = 0
        self.exit_condition = False

    # Define method to display menu title and options
    def display(self, index=0):
        # Display menu title in first loop iteration
        if index == 0:
            print("\n" + self.title + "\n")
        # Display numbered option with key from options dictionary as option title if not exit option
        if index < len(self.options):
            print(f"{index + 1}: {list(self.options.keys())[index]}")
        # Display exit option if all other options processed and exit loop
        if index == len(self.options):
            print(f"{self.exit_option}: Exit")
            pass
        else:
            # Recursively call display method, incrementing option to display
            return self.display(index + 1)

    # Define method to display menu and process user choice
    def loop(self):
        self.display()
        # Try to process user choice
        try:
            # Prompt user to choose option
            self.user_choice = int(input("\nPlease choose an option: ").strip())
            # Test if option outside valid range
            if self.user_choice < 1 or self.user_choice > self.exit_option:
                # Display error message and restart loop
                print("Sorry, choice must be from the list. Please try again.")
                return self.loop()
            else:
                # Test if user selected non-exit option
                if self.user_choice < self.exit_option:
                    # Transform menu options into list to extract function for option chosen by user
                    option_function = list(self.options.values())[self.user_choice - 1]
                    # Test if option function can be called
                    if callable(option_function):
                        # Test if menu has option parameters
                        if self.option_parameters:
                            # Test if sufficient option parameters for user choice
                            if len(self.option_parameters) >= self.user_choice:
                                # Call option function with option parameter corresponding to user choice
                                option_function(self.option_parameters[self.user_choice - 1])
                            else:
                                option_function()
                        else:
                            option_function()
                    else:
                        # Set exit condition to True as trying to call uncallable function
                        self.exit_condition = True
                    # Test if menu has callable exit function
                    if callable(self.exit_function):
                        # Set exit condition to return value of exit function called with user_choice and exit_option
                        self.exit_condition = self.exit_function(self.user_choice, self.exit_option)
                        # Test if exit condition True
                        if self.exit_condition:
                            # Exit loop
                            pass
                        else:
                            # Restart loop
                            return self.loop()
                    else:
                        # Exit loop if exit function not callable
                        pass
                else:
                    # Set exit condition to True and exit loop as user selected exit option
                    self.exit_condition = True
                    pass
        # Handle value type error by prompting user to re-enter option number, and restart loop
        except ValueError:
            print("Sorry, you must enter a numerical value. Please try again.")
            return self.loop()
