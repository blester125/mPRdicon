import webapp2

from google.appengine.ext import ndb

class TournamentModel(ndb.Model):
  name = ndb.StringProperty()
  url = ndb.StringProperty()
  timestamp = ndb.DateTimeProperty(auto_now_add=True)