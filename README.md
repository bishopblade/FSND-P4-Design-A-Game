# Hangman Game API

Welcome to the Hangman API. This document details how to query the Hangman API.

## Gameplay
To create a game, first send a request to the create_user endpoint. After a user is created, you can create a game
with new_game. new_game will return a URL-safe game key, which can be used with make_move to guess letters in the
word. All words are selected randomly from a list of countries.

## Endpoints

### create_user
URL: POST `/user`
Creates a user. Requires an email and a username.

### new_game
URL: POST `/game`
Creates a new game. Requires a username, and returns a URL-safe game key.

### make_move
URL: PUT `/game/<key>`
Allows player to guess a letter in the word. Takes the URL-safe game key and a letter, and returns whether the letter
was part of the word along with all the letters guessed.

### cancel_game
URL: PUT `/game/<key>/cancel`
Cancels a game. Requires the URL-safe game key returned by new_game.

### get_game
URL: GET `/game/<key>`
Returns the current state of a game. Requires the URL-safe game key.

### get_game_history
URL: GET `/game/<key>/history`
Returns all the moves made in a game. Requires the URL-safe game key.

### get_user_rankings
URL: GET `/rankings`
Returns the leaderboard of users. Users are ranked as detailed in "Scores" below.

### get_user_games
URL: GET `/user/<user>/games`
Returns all the games for a given user. Requires a username.

### get_scores
URL: GET `/scores`
Returns all the scores.

### get_user_scores
URL: GET `/scores/user/<user>`
Returns scores for a given user. Requires a username.

### get_high_scores
URL: GET `/scores/user/<user>/high`
Returns scores for a given user sorted by number of guesses needed, ascending. Requires a username.

### get_average_attempts_remaining
URL: GET `/games/average_attempts`
Returns the average moves remaining for all games.

## Scores

Score in this implementation of Hangman is based on the number of incorrect guesses before the game ends.
A lower number of incorrect guesses is considered a better score.
In the leaderboard of players returned by get_user_rankings, players are ranked based on their number of wins
divided by their total number of incorrect guesses. This metric means that users do not gain ranks simply
by playing more games.
