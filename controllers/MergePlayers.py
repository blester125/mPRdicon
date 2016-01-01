import webapp2

from models.PlayerModel import *
from models.MatchModel import *
from controllers.User import handle_user
from views.RenderTemplate import *

class MergePlayers(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    players = []
    player_query = PlayerModel.query()
    for p in player_query:
      players.append(p)
    template_params['players'] = players
    render_template(self, 'mergePlayers.html', template_params)

  def post(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    newTag = self.request.get("newTag")
    oldTag = self.request.get("oldTag")
    if newTag == "" or oldTag == "":
      self.redirect('/')
      return
    # Replace p1 newtags with old tag
    matches = MatchModel.query(MatchModel.player1 == newTag)
    for match in matches:
      match.player1 = oldTag
      match.put()
    # Replace p2 noewtags with oldtags
    matches = MatchModel.query(MatchModel.player2 == newTag)
    for match in matches:
      match.player2 = oldTag
      match.put()
    self.redirect('/generateRankings')
