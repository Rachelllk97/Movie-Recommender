import mysql.connector

from db_config import HOST, USER, PASSWORD


# Create custom exception to handle database connection errors
class DbConnectionError(Exception):
    pass


# Define function to connect to user_movie_vibes database, using credentials from config
def db_connect():
    db_connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database="user_movie_vibes"
    )
    return db_connection


# Define function to add new user
def db_add_user(user_first_name, user_last_name, user_email, user_password):
    # Initialise user_id to return
    user_id = None
    db_connection = None
    # Try to set user_id to output value of sp_add_user stored procedure
    try:
        db_connection = db_connect()
        cursor = db_connection.cursor()
        # Set parameters for sp_add_user stored procedure: 4 input, 1 output (integer)
        args = (user_first_name, user_last_name, user_email, user_password, (user_id, "SIGNED"))
        # Execute stored procedure, capturing updated parameters in result_args
        result_args = cursor.callproc("sp_add_user", args)
        # Set user_id to value of output parameter
        user_id = result_args[4]
        cursor.close()
    # Raise exception in event of DB error
    except Exception:
        raise DbConnectionError("Failed to write to database.")
    # Close DB connection if exists
    finally:
        if db_connection:
            db_connection.close()
    # Return user_id of new user added or None if failed to add
    return user_id


# Define function to get existing user
def db_get_user(user_email, user_password):
    # Initialise user_id to return
    user_id = None
    db_connection = None
    # Try to set user_id to output value of SELECT query on users table
    try:
        db_connection = db_connect()
        cursor = db_connection.cursor()
        # Prepare query to retrieve user_id for supplied email and password
        query = """
            SELECT
                user_id
            FROM
                users
            WHERE
                user_email = %s
                AND BINARY user_password = %s
            """
        # Execute query with supplied email and password
        cursor.execute(query, (user_email, user_password))
        # Set user_id to first column of output row if one exists
        user = cursor.fetchone()
        if user:
            user_id = user[0]
        cursor.close()
    # Raise exception in event of DB error
    except Exception:
        raise DbConnectionError("Failed to read from database.")
    # Close DB connection if exists
    finally:
        if db_connection:
            db_connection.close()
    # Return user_id of existing user or None if user row not found
    return user_id


# Define function to add user's top 5 movies
def db_add_user_movie_top_5(user_id, movie_top_5):
    # Initialise update_count to return
    update_count = None
    db_connection = None
    # Try to set update_count to output value of sp_add_user_movie_top_5 stored procedure
    try:
        db_connection = db_connect()
        cursor = db_connection.cursor()
        # Set parameters for sp_add_user_movie_top_5 stored procedure: 2 input, 1 output (integer)
        args = (user_id, movie_top_5, (update_count, "SIGNED"))
        # Execute stored procedure, capturing updated parameters in result_args
        result_args = cursor.callproc("sp_add_user_movie_top_5", args)
        # Set update_count to value of output parameter
        update_count = result_args[2]
        cursor.close()
    # Raise exception in event of DB error
    except Exception:
        raise DbConnectionError("Failed to write to database.")
    # Close DB connection if exists
    finally:
        if db_connection:
            db_connection.close()
    # Return update_count of rows added or None if failed to add
    return update_count


# Define helper function to map quiz_prompt_option_rows into nested list of quiz dictionary items
def map_quiz_prompt_option_rows(quiz_prompt_option_rows):
    # Initialise variables for building nested list of quiz dictionary items to return
    quizzes = []
    quiz_prompts = []
    quiz_prompt_options = []
    # Initialise tracking variables
    quiz_id = None
    quiz_prompt_id = None
    # Iterate over quiz_prompt_option_rows
    for quiz_prompt_option_row in quiz_prompt_option_rows:
        # quiz_prompt_option_row comprises:
        # quiz_prompt_option_row[0] holds quiz_id
        # quiz_prompt_option_row[1] holds quiz_prompt_id
        # quiz_prompt_option_row[2] holds quiz_prompt_text
        # quiz_prompt_option_row[3] holds quiz_prompt_option_id
        # quiz_prompt_option_row[4] holds quiz_prompt_option_text

        # If tracking variable indicates processing new quiz
        if quiz_prompt_option_row[0] != quiz_id:
            # Update quiz tracking variable
            quiz_id = quiz_prompt_option_row[0]
            # (Re)initialise quiz prompts to empty list
            quiz_prompts = []
            # Create new quiz dictionary item
            quiz = {"quiz_id": quiz_prompt_option_row[0],
                    "quiz_prompts": quiz_prompts}
            # Append quiz dictionary item to list of quizzes to be returned
            quizzes.append(quiz)
        # If tracking variable indicates processing new quiz_prompt
        if quiz_prompt_option_row[1] != quiz_prompt_id:
            # Update quiz prompt tracking variable
            quiz_prompt_id = quiz_prompt_option_row[1]
            # (Re)initialise quiz prompt options to empty list
            quiz_prompt_options = []
            # Create new quiz prompt dictionary item
            quiz_prompt = {"quiz_prompt_id": quiz_prompt_option_row[1],
                           "quiz_prompt_text": quiz_prompt_option_row[2],
                           "quiz_prompt_options": quiz_prompt_options}
            # Append quiz prompt dictionary item to list of quiz prompts in parent quiz
            quiz_prompts.append(quiz_prompt)
        # For every quiz_prompt_option_row, create new quiz prompt option dictionary item
        quiz_prompt_option = {"quiz_prompt_option_id": quiz_prompt_option_row[3],
                              "quiz_prompt_option_text": quiz_prompt_option_row[4]}
        # Append quiz prompt option dictionary item to list of quiz prompt options in parent quiz prompt
        quiz_prompt_options.append(quiz_prompt_option)
    # Return nested list of quiz dictionary items or empty list if no rows supplied
    return quizzes


# Define function to get quizzes
def db_get_quizzes():
    # Initialise list of quizzes to return
    quizzes = []
    db_connection = None
    # Try to set quizzes to transformed output value of SELECT query on vw_quiz_prompt_options view
    try:
        db_connection = db_connect()
        cursor = db_connection.cursor()
        # Prepare and execute query to retrieve quiz details
        query = """
            SELECT
                quiz_id,
                quiz_prompt_id,
                quiz_prompt_text,
                quiz_prompt_option_id,
                quiz_prompt_option_text
            FROM
                vw_quiz_prompt_options
        """
        cursor.execute(query)
        # Set quizzes to output of mapping all rows returned
        quiz_prompt_option_rows = cursor.fetchall()
        quizzes = map_quiz_prompt_option_rows(quiz_prompt_option_rows)
        cursor.close()
    # Raise exception in event of DB error
    except Exception:
        raise DbConnectionError("Failed to read from database.")
    # Close DB connection if exists
    finally:
        if db_connection:
            db_connection.close()
    # Return nested list of quiz dictionary items or empty list if query failed
    return quizzes


# Define function to add user's quiz responses
def db_add_user_quiz_responses(user_id, quiz_id, quiz_responses):
    # Initialise update_count to return
    update_count = None
    db_connection = None
    # Try to set update_count to output value of sp_add_user_quiz_responses stored procedure
    try:
        db_connection = db_connect()
        cursor = db_connection.cursor()
        # Set parameters for sp_add_user_quiz_responses stored procedure: 3 input, 1 output (integer)
        args = (user_id, quiz_id, quiz_responses, (update_count, "SIGNED"))
        # Execute stored procedure, capturing updated parameters in result_args
        result_args = cursor.callproc("sp_add_user_quiz_responses", args)
        # Set update_count to value of output parameter
        update_count = result_args[3]
        cursor.close()
    # Raise exception in event of DB error
    except Exception:
        raise DbConnectionError("Failed to write to database.")
    # Close DB connection if exists
    finally:
        if db_connection:
            db_connection.close()
    # Return update_count of rows added or None if failed to add
    return update_count


# Define helper function to map movie_rows into list of movie dictionary items
def map_movie_rows(movie_rows):
    # Initialise variable for building list of movie dictionary items to return
    movies = []
    # Iterate over movie_rows
    for movie_row in movie_rows:
        # movie_row comprises:
        # movie_row[0] holds movie_name
        # movie_row[1] holds user_top_5

        # Create movie dictionary item
        movie_item = {
            "movie_name": movie_row[0],
            "user_top_5": movie_row[1]
        }
        # Append movie dictionary item to list of movies
        movies.append(movie_item)
    # Return list of movie dictionary items or empty list if no rows supplied
    return movies


# Define function to get top 5 movies for similar users
def db_get_movie_top_5_for_similar_users(user_id):
    # Initialise list of movies to return
    movies = []
    db_connection = None
    # Try to set movies to transformed output value of SELECT query on vw_user_similar_vibe_movies view
    try:
        db_connection = db_connect()
        cursor = db_connection.cursor()
        # Prepare query to retrieve movie details for supplied user_id
        query = """
            SELECT
                movie_name,
                user_top_5_count
            FROM
                vw_user_similar_vibe_movies
            WHERE
                user_id = %s
        """
        # Execute query with supplied user_id
        cursor.execute(query, (user_id,))
        # Set movies to output of mapping all rows returned
        movie_rows = cursor.fetchall()
        movies = map_movie_rows(movie_rows)
        cursor.close()
    # Raise exception in event of DB error
    except Exception:
        raise DbConnectionError("Failed to read from database.")
    # Close DB connection if exists
    finally:
        if db_connection:
            db_connection.close()
    # Return list of movie dictionary items or empty list if query failed
    return movies
