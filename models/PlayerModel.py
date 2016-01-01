import webapp2

from google.appengine.ext import ndb

class PlayerModel(ndb.Model):
  tag = ndb.StringProperty()
  score = ndb.IntegerProperty()
  ranking = ndb.PickleProperty()
  lastActive = ndb.DateTimeProperty()

  def __cmp__(self, other):
    if isinstance(other, PlayerModel):
      if self.ranking.mu == other.ranking.mu:
        return self.ranking.sigma - other.ranking.sigma
      else:
        return self.ranking.mu - other.ranking.mu
    return NotImplemented