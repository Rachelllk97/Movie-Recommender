-- Create database to hold details of users, their top 5 movies, quizzes and quiz responses
CREATE DATABASE user_movie_vibes;
USE user_movie_vibes;

-- Create table to store details of users
CREATE TABLE users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	user_first_name VARCHAR(50),
	user_last_name VARCHAR(50),
	user_email VARCHAR(100) UNIQUE NOT NULL,
	user_password VARCHAR(50) NOT NULL
);

-- Create table to store details of users' top 5 movies
CREATE TABLE user_movie_top_5 (
	user_movie_top_5_id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	movie_name VARCHAR(200) NOT NULL,
	CONSTRAINT fk_user_movie_top_5_user_id FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create table to store details of quizzes
CREATE TABLE quizzes (
	quiz_id INT AUTO_INCREMENT PRIMARY KEY,
	quiz_name VARCHAR(50)
);

-- Create table to store details of prompts for quizzes
CREATE TABLE quiz_prompts (
	quiz_prompt_id INT AUTO_INCREMENT PRIMARY KEY,
	quiz_id INT NOT NULL,
	quiz_prompt_text VARCHAR(200) NOT NULL,
	quiz_prompt_order INT, -- Order to display quiz prompts for quiz 
	CONSTRAINT fk_quiz_prompts_quiz_id FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
);

-- Create table to store details of options for quiz prompts
CREATE TABLE quiz_prompt_options (
	quiz_prompt_option_id INT AUTO_INCREMENT PRIMARY KEY,
	quiz_prompt_id INT NOT NULL,
	quiz_prompt_option_text VARCHAR(200) NOT NULL,
	quiz_prompt_option_vibe VARCHAR(1), -- Vibe associated with quiz prompt option
	quiz_prompt_option_order INT, -- Order to display quiz prompt options for quiz prompt
	CONSTRAINT fk_quiz_prompt_options_quiz_prompt_id FOREIGN KEY (quiz_prompt_id) REFERENCES quiz_prompts(quiz_prompt_id)
);

-- Create table to store details of vibes extrapolated from users' quiz responses
CREATE TABLE quiz_response_vibes (
	vibe_id INT AUTO_INCREMENT PRIMARY KEY,
	quiz_id INT NOT NULL,
	vibe_name VARCHAR(50),
	quiz_prompt_option_vibe_mode VARCHAR(1), -- Dominant quiz prompt option vibe
	CONSTRAINT fk_quiz_response_vibes_quiz_id FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
);

-- Create table to store users' quiz responses
CREATE TABLE user_quiz_responses (
	user_quiz_response_id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	quiz_id INT NOT NULL,
	quiz_prompt_option_id INT NOT NULL,
	CONSTRAINT fk_user_quiz_responses_user_id FOREIGN KEY (user_id) REFERENCES users(user_id),
	CONSTRAINT fk_user_quiz_responses_quiz_id FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id),
	CONSTRAINT fk_user_quiz_responses_quiz_prompt_option_id FOREIGN KEY (quiz_prompt_option_id) REFERENCES quiz_prompt_options(quiz_prompt_option_id)
);

-- Create view to join all quiz, quiz prompt and quiz prompt option details
CREATE OR REPLACE VIEW vw_quiz_prompt_options AS
SELECT
	qp.quiz_id AS quiz_id,
	qp.quiz_prompt_id AS quiz_prompt_id,
	qp.quiz_prompt_text AS quiz_prompt_text,
	qpo.quiz_prompt_option_id AS quiz_prompt_option_id,
	qpo.quiz_prompt_option_text AS quiz_prompt_option_text
FROM
	quiz_prompts qp
INNER JOIN
	quiz_prompt_options qpo
	ON qpo.quiz_prompt_id = qp.quiz_prompt_id
ORDER BY
	qp.quiz_id,
	qp.quiz_prompt_order,
	qpo.quiz_prompt_option_order;

-- Create view to extrapolate users' vibes
CREATE OR REPLACE VIEW vw_user_vibes AS
SELECT
	qpov.user_id AS user_id,
	qrv.vibe_id AS vibe_id,
	qrv.vibe_name AS vibe_name
FROM (
	-- Select row 1 as dominant vibe for each user for each quiz
	SELECT 
		user_id,
		quiz_id,
		quiz_prompt_option_vibe
	FROM (
		-- Sort vibe counts for each user for each quiz in descending order and allocate row number
		SELECT
			user_id,
			quiz_id,
			quiz_prompt_option_vibe,
			ROW_NUMBER() OVER(PARTITION BY user_id, quiz_id ORDER BY vibe_count DESC) AS rn
		FROM (
			-- Calculate number of responses for each vibe for each user for each quiz
			SELECT
				uqr.user_id,
				uqr.quiz_id,
				qpo.quiz_prompt_option_vibe,
				COUNT(*) AS vibe_count
			FROM
				user_quiz_responses uqr
			INNER JOIN
				quiz_prompt_options qpo
				ON qpo.quiz_prompt_option_id = uqr.quiz_prompt_option_id
			GROUP BY
				uqr.user_id,
				uqr.quiz_id,
				qpo.quiz_prompt_option_vibe
		) t1
	) t2
	WHERE
		rn = 1
) qpov
-- Join dominant vibe for each user for each quiz to quiz_response_vibes to get vibe details
INNER JOIN
	quiz_response_vibes qrv
	ON qrv.quiz_id = qpov.quiz_id
	AND qrv.quiz_prompt_option_vibe_mode = qpov.quiz_prompt_option_vibe;

-- Create view to get top 5 movies for user and users with same vibe
CREATE OR REPLACE VIEW vw_user_similar_vibe_movies AS
SELECT 
	vuv1.user_id AS user_id,
	umt5.movie_name AS movie_name,
	-- Determine if movie in user's top 5
	MAX(CASE WHEN vuv1.user_id = umt5.user_id THEN 1 ELSE 0 END) AS user_top_5_count,
	-- Calculate number of other users with movie in their top 5
	COUNT(DISTINCT CASE WHEN vuv1.user_id <> umt5.user_id THEN vuv2.user_id END) AS others_top_5_count
FROM
	vw_user_vibes vuv1
-- Inner join to vw_user_vibes again to select other users with same vibe
INNER JOIN
	vw_user_vibes vuv2
	ON vuv2.vibe_id = vuv1.vibe_id
	AND vuv2.user_id <> vuv1.user_id
-- Inner join to user_movie_top_5 to get top 5 movies for user and users with same vibe
INNER JOIN
	user_movie_top_5 umt5
	ON umt5.user_id = vuv1.user_id
	OR umt5.user_id = vuv2.user_id
GROUP BY
	vuv1.user_id,
	umt5.movie_name
ORDER BY
	vuv1.user_id,
	umt5.movie_name;

DELIMITER //
-- Create stored procedure to add user with supplied details and set output parameter to user_id of row added
CREATE PROCEDURE sp_add_user (
	IN in_first_name VARCHAR(50),
	IN in_last_name VARCHAR(50),
	IN in_email VARCHAR(100),
	IN in_password VARCHAR(50),
	OUT out_user_id INT
)
BEGIN
	-- Declare handler for SQL Exception to roll back changes and set output user_id to NULL
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK;
		SET out_user_id = NULL;
	END;
	-- Start transaction block to add user, set output user_id to id of row added and commit change
	START TRANSACTION;
		INSERT INTO
			users (user_first_name, user_last_name, user_email, user_password)
		VALUES
			(in_first_name, in_last_name, in_email, in_password);
		SET out_user_id = LAST_INSERT_ID();
	COMMIT;
END //

DELIMITER //
-- Create stored procedure to add user's top 5 movies and set output parameter to number of movies added
CREATE PROCEDURE sp_add_user_movie_top_5 (
	IN in_user_id INT,
	IN in_movie_names VARCHAR(1000),
	OUT out_movies_added INT
)
BEGIN
	-- Declare tracking variables
	DECLARE number_of_movies_to_add INT;
	DECLARE movie_name_to_add VARCHAR(200);
	-- Declare handler for SQL Exception to roll back changes and set output number of movies added to 0
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK;
		SET out_movies_added = 0;
	END;
	-- Initialise number of movies added
	SET out_movies_added = 0;
	-- Calculate number of movies in comma-separated list supplied
	SET number_of_movies_to_add = CHAR_LENGTH(in_movie_names) - CHAR_LENGTH(REPLACE(in_movie_names,',','')) + 1;
	-- Start transaction block to remove any previous top 5 movies for user, add supplied movie names, set output parameter and commit change
	START TRANSACTION;
	-- Delete any previous top 5 movies for user
	DELETE FROM
		user_movie_top_5
	WHERE
		user_id = in_user_id;
	-- Process list of movie names in loop
	WHILE in_movie_names <> '' DO
		-- Extract movie name up to next comma or end of string
		SET movie_name_to_add = TRIM(SUBSTRING_INDEX(in_movie_names, ',', 1));
		-- Add movie to user's top 5
		INSERT INTO
			user_movie_top_5 (user_id, movie_name)
		VALUES
			(in_user_id, movie_name_to_add);
		-- Increment number of movies added
		SELECT ROW_COUNT() + out_movies_added INTO out_movies_added;
		-- Check whether commas remaining in list of movie names to process
		IF LOCATE(',', in_movie_names) > 0 THEN
			-- Remove up to and including first comma from list of movie names to process, as that movie already processed
			SET in_movie_names = SUBSTRING(in_movie_names, LOCATE(',', in_movie_names) + 1);
		ELSE
			-- Set list of movie names to empty string, as all movies processed
			SET in_movie_names = '';
		END IF;
	END WHILE;
	-- Commit changes if expected number of movies added, otherwise roll back and set output number of movies added to 0
	IF out_movies_added = number_of_movies_to_add THEN
		COMMIT;
	ELSE
		ROLLBACK;
		SET out_movies_added = 0;
	END IF;
END //

DELIMITER //
-- Create stored procedure to add user's quiz responses and set output parameter to number of responses added
CREATE PROCEDURE sp_add_user_quiz_responses (
	IN in_user_id INT,
	IN in_quiz_id INT,
	IN in_quiz_responses VARCHAR(200),
	OUT out_responses_added INT
)
BEGIN
	-- Declare tracking variable
	DECLARE number_of_responses_to_add INT;
	-- Declare variable to hold dynamic SQL statement
	DECLARE sql_statement VARCHAR(1000);
	-- Declare handler for SQL Exception to roll back changes and set output number of responses added to 0
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK;
		SET out_responses_added = 0;
	END;
	-- Initialise number of responses added
	SET out_responses_added = 0;
	-- Calculate number of responses in comma-separated list supplied
	SET number_of_responses_to_add = CHAR_LENGTH(in_quiz_responses) - CHAR_LENGTH(REPLACE(in_quiz_responses,',','')) + 1;
	-- Start transaction block to remove any previous quiz responses for user, add supplied responses, set output parameter and commit change
	START TRANSACTION;
		-- Delete any previous quiz responses for user
		DELETE FROM
			user_quiz_responses
		WHERE
			user_id = in_user_id
			AND quiz_id = in_quiz_id;
		-- Prepare SQL to add quiz responses for user by inserting quiz prompt options that match responses supplied
		SET @sql_statement = CONCAT(
			'INSERT INTO
				user_quiz_responses (user_id, quiz_id, quiz_prompt_option_id) '
			'SELECT ',
				in_user_id,',',
				in_quiz_id,','
				'quiz_prompt_option_id '
			'FROM
				quiz_prompt_options '
			'WHERE
				quiz_prompt_option_id IN (', in_quiz_responses,');'
		);
		-- Prepare and execute dynamic SQL statement
		PREPARE statement FROM @sql_statement;
		EXECUTE statement;
		-- Set output parameter to number of responses added
		SELECT ROW_COUNT() INTO out_responses_added;
		-- Deallocate resources used for dynamic SQL statement
		DEALLOCATE PREPARE statement;
		-- Commit changes if expected number of responses added, otherwise roll back and set output number of responses added to 0
		IF out_responses_added = number_of_responses_to_add THEN
			COMMIT;
		ELSE
			ROLLBACK;
			SET out_responses_added = 0;
		END IF;
END //

DELIMITER ;


-- Add sample users
CALL sp_add_user('Sophie', 'Stubbs', 'sophie.stubbs@nomail.com', 'TestPassword1!', @user1);
CALL sp_add_user('Mark', 'Stubbs', 'mark.stubbs@nomail.com', 'TestPassword2!', @user2);
CALL sp_add_user('Amanda', 'Stubbs', 'amanda.stubbs@nomail.com', 'TestPassword3!', @user3);
CALL sp_add_user('Nuala', 'Hussey', 'nuala.hussey@nomail.com', 'TestPassword4!', @user4);
CALL sp_add_user('Ardelyn', 'Quiambao', 'ardelyn@nomail.com', 'Hellopassword1?', @user5);
CALL sp_add_user('Zoe', 'Walker', 'zoewalker@nomail.com', 'TestPassword7!', @user6);
CALL sp_add_user('Leif', 'Bryant', 'leif.bryant@nomail.com', 'TestPassword7!', @user7);
CALL sp_add_user('Steve', 'Boyle', 'steven.boyle@nomail.com', 'TestPassword7!', @user8);
CALL sp_add_user('Jo', 'Spicer', 'jo.spicer@nomail.com', 'TestPassword7!', @user9);
CALL sp_add_user('Tracey', 'Pelling', 'trace.p@nomail.com', 'Password123!', @user10);
CALL sp_add_user('Emma', 'Pritchard', 'emmalikedinosaurs@nomail.com', 'Password123!', @user11);
CALL sp_add_user('Luca', 'Mansfield', 'luca.mansfield@nomail.com', 'Password123!', @user12);
CALL sp_add_user('Kelly', 'McMahon', 'kellymcmahon@nomail.com', 'Password123!', @user13);
CALL sp_add_user('Kay', 'Merricks', 'kaymerricks@nomail.com', 'Hellopassword1?', @user14);
CALL sp_add_user('Meg', 'McCallister', 'meg@nomail.com', 'Password456?', @user15);
CALL sp_add_user('Maddie', 'McVeigh', 'maddie@nomail.com', 'Password123!', @user16);
CALL sp_add_user('Rachel', 'Kelly', 'rachel.kelly@nomail.com', 'Password1997!', @user17);

-- Add sample users' top 5 movies
CALL sp_add_user_movie_top_5(@user1, 'Hot Fuzz, Spy, Princess Bride, True Lies, Love Actually', @update_count);
CALL sp_add_user_movie_top_5(@user2, 'Hot Fuzz, Blade Runner (1982), Monty Python and the Holy Grail, True Lies, Galaxy Quest', @update_count);
CALL sp_add_user_movie_top_5(@user3, 'Hot Fuzz, The Sound of Music, My Fair Lady, Lethal Weapon, Love Actually', @update_count);
CALL sp_add_user_movie_top_5(@user4, 'Shiva Baby, Palm Springs, Sweeney Todd, Black Swan, Sightseers', @update_count);
CALL sp_add_user_movie_top_5(@user5, 'Past Lives, Get Out, White Chicks, Your Name, Avengers: Endgame', @update_count);
CALL sp_add_user_movie_top_5(@user6, 'Pride and Prejudice (2005), The Rock, Princess Bride, Dune (2021), Train to Busan', @update_count);
CALL sp_add_user_movie_top_5(@user7, 'Treasure Planet, Mad Max: Fury Road, Howl\'s Moving Castle, Coraline, The Mummy', @update_count);
CALL sp_add_user_movie_top_5(@user8, 'The Night of the Hunter, 8 1/2 (1963), Hour of the Wolf (1968), Local Hero (1983), Parasite (2019)', @update_count);
CALL sp_add_user_movie_top_5(@user9, 'Shawshank Redemption, Thelma and Louise, The Devil Wears Prada, Occasional Coarse Language, The Proposal', @update_count);
CALL sp_add_user_movie_top_5(@user10, 'Fight Club, Heathers, Young Guns, Young Guns 2, Pump Up The Volume', @update_count);
CALL sp_add_user_movie_top_5(@user11, 'Where The Wild Things Are, You\'ve Got Mail, Bridget Jones\' Diary, Gone Girl, Rugrats Go Wild', @update_count);
CALL sp_add_user_movie_top_5(@user12, 'RRR, In Bruges, Vampire Hunter D: Bloodlust, Dark Crystal, The Guest', @update_count);
CALL sp_add_user_movie_top_5(@user13, 'Dirty Dancing, Pretty Woman, Withnail and I, Step Brothers, Wedding Crashers', @update_count);
CALL sp_add_user_movie_top_5(@user14, 'Shawshank Redemption, Braveheart, When Harry Met Sally, The Notebook, Me Before You', @update_count);
CALL sp_add_user_movie_top_5(@user15, 'Man On Fire, Age of Adaline, Crazy Stupid Love, Finding Nemo, Matilda', @update_count);
CALL sp_add_user_movie_top_5(@user16, 'Fight Club, Interstellar, Alien, Muppet Treasure Island, Terminator 2', @update_count);
CALL sp_add_user_movie_top_5(@user17, 'About Time, The Notebook, Ocean\'s Eleven, Grown Ups, Crazy Stupid Love', @update_count);

-- Set up sample quiz with prompts, options and vibes
INSERT INTO
	quizzes (quiz_name)
VALUES
	('Movie Vibe Quiz');

INSERT INTO
	quiz_prompts (quiz_id, quiz_prompt_text, quiz_prompt_order)
VALUES
	(1, 'Your partner moves across the world...what do you do?', 1),
	(1, 'Your team at work swap out the sugar for salt and it ruins your coffee...how do you react?', 2),
	(1, 'You\'re on holiday with your family and your cousin suggests you all go skydiving...how do you feel?', 3),
	(1, 'You\'re home alone, the internet\'s down and the only DVD in the house is a horror movie...do you watch it?', 4),
	(1, 'The couple next door are having a shouting match in the garden...what do you do?', 5);

INSERT INTO
	quiz_prompt_options (quiz_prompt_id, quiz_prompt_option_text, quiz_prompt_option_vibe, quiz_prompt_option_order)
VALUES
	(1, 'Move with them! They\'re the love of your life and you\'re always up for an adventure!', 'A', 1),
	(1, 'You\'ll do long distance and see how it goes. You could never move away from home!', 'B', 2),
	(1, 'Call it quits. You\'ve got your own plans and you\'re not changing them for anyone!', 'C', 3),
	(2, 'Pretend to laugh, then cry to your work best friend. You don\'t find that kind of thing funny.', 'A', 1),
	(2, 'Laugh and plot your revenge! You love a good prank!', 'B', 2),
	(2, 'Take it on the chin and get on with your work!', 'C', 3),
	(3, 'Nervous! You love adventure but skydiving may be a step too far!', 'A', 1),
	(3, 'Totally terrified! You point-blank refuse.', 'B', 2),
	(3, 'Buzzing! You\'re an adrenaline junky!', 'C', 3),
	(4, 'You\'ll give it a go...with the lights on and the doors locked!', 'A', 1),
	(4, 'Not a chance! You\'ll curl up with a good book instead!', 'B', 2),
	(4, 'Absolutely! With the lights off!', 'C', 3),
	(5, 'Go round and help them resolve it! True love always prevails!', 'A', 1),
	(5, 'Go back inside and pretend you heard nothing!', 'B', 2),
	(5, 'Call the police, just for the drama!', 'C', 3);

INSERT INTO
	quiz_response_vibes (quiz_id, vibe_name, quiz_prompt_option_vibe_mode)
VALUES
	(1, 'Hopeless romantic', 'A'),
	(1, 'Comedy-loving homebody', 'B'),
	(1, 'Independent thrill-seeker', 'C');

-- Add sample users' quiz responses
CALL sp_add_user_quiz_responses(@user1, 1, '1,4,7,11,14', @update_count);
CALL sp_add_user_quiz_responses(@user2, 1, '1,5,9,10,13', @update_count);
CALL sp_add_user_quiz_responses(@user3, 1, '1,6,8,11,14', @update_count);
CALL sp_add_user_quiz_responses(@user4, 1, '3,5,7,11,13', @update_count);
CALL sp_add_user_quiz_responses(@user5, 1, '3,4,9,11,14', @update_count);
CALL sp_add_user_quiz_responses(@user6, 1, '1,4,8,11,14', @update_count);
CALL sp_add_user_quiz_responses(@user7, 1, '2,4,8,12,14', @update_count);
CALL sp_add_user_quiz_responses(@user8, 1, '1,6,9,12,14', @update_count);
CALL sp_add_user_quiz_responses(@user9, 1, '1,4,7,10,13', @update_count);
CALL sp_add_user_quiz_responses(@user10, 1, '3,4,8,12,14', @update_count);
CALL sp_add_user_quiz_responses(@user11, 1, '3,6,7,11,14', @update_count);
CALL sp_add_user_quiz_responses(@user12, 1, '1,4,9,12,15', @update_count);
CALL sp_add_user_quiz_responses(@user13, 1, '1,5,7,10,13', @update_count);
CALL sp_add_user_quiz_responses(@user14, 1, '3,5,7,10,14', @update_count);
CALL sp_add_user_quiz_responses(@user15, 1, '1,5,8,11,14', @update_count);
CALL sp_add_user_quiz_responses(@user16, 1, '2,4,9,12,13', @update_count);
CALL sp_add_user_quiz_responses(@user17, 1, '1,5,9,10,14', @update_count);