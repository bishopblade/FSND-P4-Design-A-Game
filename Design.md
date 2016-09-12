# Design

## What additional properties did you add to your models and why?
I added the ranking_points computed property to the User model. This allowed me to sort users in the rankings based on
their calculated amount of ranking points (wins divided by guesses.)

On the Game model, I added the guessed_letters and history properties. The guessed_letters stores the indices of the
letters in the word that the user has successfully guessed. The history property stores all the moves made as JSON.

## What were some of the trade-offs or struggles you faced when implementing the new game logic?
The main problem I had when implementing the new game logic was getting used to using the Message class with all the API
endpoints. Although I had used the Google App Engine before, I had never used its Endpoints API. It took a while to get
used to using containers for all the requests and responses, but once I got used to them then the rest wasn't too hard.
