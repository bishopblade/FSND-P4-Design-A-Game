# Hangman Game API

Welcome to the Hangman API. This document details how to query the Hangman API.
In this implementation of Hangman, the word you have to guess will be randomly selected from a list of countries.
On each turn you can either guess a single character or try to guess the entire word.
See [Hangman](https://en.wikipedia.org/wiki/Hangman) on Wikipedia.

## Gameplay
To create a game, first send a request to the create_user endpoint. After a user is created, you can create a game
with new_game. new_game will return a URL-safe game key, which can be used with make_move to guess letters in the
word. All words are selected randomly from a list of countries.

## Endpoints

### create_user
Path: `/user`

Method: POST

Parameters: user_name, email

Returns: StringMessage showing result of user creation.

Creates a user.

### new_game
Path: `/game`

Method: POST

Parameters: user_name, attempts

Returns: GameForm containing information about the created game.

Creates a new game.

### make_move
Path: `/game/<key>`

Method: PUT

Parameters: guess, urlsafe_game_key

Returns: GameForm containing information about the game.

Allows player to guess a letter in the word. Returns whether the letter
was part of the word along with all the letters guessed.

### cancel_game
Path: `/game/<key>/cancel`

Method: DELETE

Parameters: urlsafe_game_key

Returns: StringMessage showing result of deleting game.

Cancels a game.

### get_game
Path: `/game/<key>`

Method: GET

Parameters: urlsafe_game_key

Returns: GameForm with information about game.

Returns the current state of a game.

### get_game_history
Path: `/game/<key>/history`

Method: GET

Parameters: urlsafe_game_key

Returns: MessageForm with JSON-encoded list of moves made in the game.

Returns all the moves made in a game.

### get_user_rankings
Path: `/rankings`

Method: GET

Returns: RankingsMessage with all users ranked.

Returns the leaderboard of users. Users are ranked as detailed in "Scores" below.

### get_user_games
Path: `/user/<user>/games`

Method: GET

Parameters: user

Returns: UserGamesForm with all the games for the requested user.

Returns all the games for a given user.

### get_scores
Path: `/scores`

Method: GET

Returns: ScoreForms with all scores.

Returns all the scores.

### get_user_scores
Path: `/scores/user/<user>`

Method: GET

Parameters: user_name, email

Returns: ScoreForms with all scores for the requested user.

Returns scores for a given user.

### get_high_scores
Path: `/scores/user/<user>/high`

Method: GET

Parameters: user_name

Returns: ScoreForms with all scores for the requested user.

Returns scores for a given user sorted by number of guesses needed, ascending.

### get_average_attempts_remaining
Path: `/games/average_attempts`

Method: GET

Returns: StringMessage with average moves remaining.

Returns the average moves remaining for all games.

## Scores

Score in this implementation of Hangman is based on the number of incorrect guesses before the game ends.
A lower number of incorrect guesses is considered a better score.
In the leaderboard of players returned by get_user_rankings, players are ranked based on their number of wins
divided by their total number of incorrect guesses. This metric means that users do not gain ranks simply
by playing more games.
