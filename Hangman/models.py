"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import csv
import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

WORDS_LIST = []
with open('countries.csv') as countries:
    reader = csv.reader(countries)
    for row in reader:
        WORDS_LIST.append(row[1])

def getRanking(self):
    scores = Score.query(Score.user == self.key)
    guesses = sum(score.guesses for score in scores)
    wins = sum(score.won for score in scores)

    if guesses > 0:
        return float(wins) / guesses
    else:
        return float(wins)

class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    ranking_points = ndb.ComputedProperty(getRanking)

    def to_form(self):
        return RankingMessage(user_name=self.name, ranking_points=self.ranking_points) 

class Game(ndb.Model):
    """Game object"""
    target = ndb.StringProperty(required=True)
    guessed_letters = ndb.IntegerProperty(repeated=True)
    attempts_allowed = ndb.IntegerProperty(required=True)
    attempts_remaining = ndb.IntegerProperty(required=True, default=5)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    history = ndb.TextProperty(required=True, default='[]')

    @classmethod
    def new_game(cls, user, attempts):
        """Creates and returns a new game"""
        game = Game(user=user,
                    target=random.choice(WORDS_LIST).upper(),
                    guessed_letters=[],
                    attempts_allowed=attempts,
                    attempts_remaining=attempts,
                    game_over=False)
        game.put()
        return game

    def word_progress(self):
        progress = ''
        for i, c in enumerate(self.target):
            if i in self.guessed_letters:
                progress += c
            else:
                progress += '_'
        return progress

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)

class UserGamesForm(messages.Message):
    """Form to store list of games"""
    games = messages.StringField(1, repeated=True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    attempts = messages.IntegerField(4, default=5)

class MessageForm(messages.Message):
    """Used to send a single message"""
    message = messages.StringField(1, required=True)

class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)

class RankingMessage(messages.Message):
    """Represents information for an individual player in rankings"""
    user_name = messages.StringField(1, required=True)
    ranking_points = messages.FloatField(2, required=True)

class RankingsMessage(messages.Message):
    """Message for player rankings"""
    rankings = messages.MessageField(RankingMessage, 1, repeated=True)

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
