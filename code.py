import webapp2

from controllers.Index import *
from controllers.About import *
from controllers.History import *
from controllers.Tournaments import *
from controllers.Fetch import *
from controllers.GenerateRankings import *
from controllers.OorPlayers import *
from controllers.MergePlayers import *

app = webapp2.WSGIApplication([
  ('/', Index),
  ('/about', About),
  ('/history', History),
  ('/listTournaments', ListTournaments),
  ('/addTournaments', AddTournaments), 
  ('/deleteTournaments', DeleteTournaments),
  ('/oorPlayers', OorPlayers),
  ('/addOoR', AddOoR),
  ('/deleteOoR', DeleteOoR),
  ('/mergePlayers', MergePlayers),
  ('/generateRankings', GenerateRankings), 
  ('/fetch', Fetch)
  ])
