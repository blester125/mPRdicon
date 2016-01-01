import webapp2
import json

from models.PlayerModel import *

class Fetch(webapp2.RequestHandler):
  def get(self):
    query = PlayerModel.query()
    rankings_list = []
    for player in query:
      rankings_list.append(player)
    rankings_list.sort(key = lambda x: x.ranking.mu, reverse=True)
    rankings = {}
    rankings['size'] = len(rankings_list)
    rankings['players'] = []
    for player in rankings_list:
      rankings['players'].append(player.tag)
    self.response.out.write(json.dumps(rankings))
