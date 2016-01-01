import webapp2

from google.appengine.ext import ndb

class MatchModel(ndb.Model):
  player1 = ndb.StringProperty()
  player2 = ndb.StringProperty()
  player1Score = ndb.IntegerProperty(default=0)
  player2Score = ndb.IntegerProperty(default=0)
  winner = ndb.StringProperty()
  label = ndb.StringProperty()
  timestamp = ndb.DateTimeProperty()