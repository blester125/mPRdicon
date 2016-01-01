import webapp2

from google.appengine.ext import ndb

class OoRModel(ndb.Model):
  players = ndb.StringProperty(repeated=True)