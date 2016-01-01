import webapp2
import trueskill

from models.PlayerModel import *
from models.TournamentModel import *
from models.MatchModel import *
from models.OoRModel import *
from controllers.User import handle_user
from views.RenderTemplate import *

class GenerateRankings(webapp2.RequestHandler):
  def get(self):
    OoR = OoRModel.query().get().players
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
    # Delete All player Models
    players = PlayerModel.query()
    for player in players:
      player.key.delete()
    tournament_query = TournamentModel.query()
    tournaments = []
    for t in tournament_query:
      tournaments.append(t)
    #sort
    tournaments.sort(key = lambda x: x.timestamp)
    for tournament in tournaments:
      #self.response.out.write(tournament.name + "<br>") 
 
      matches = []
      match_query = MatchModel.query(ancestor=tournament.key)
      for m in match_query:
        matches.append(m)
      matches.sort(key = lambda x: x.timestamp)
      for match in matches:
        player1 = match.player1
        player2 = match.player2
        winner = match.winner
        if player1 in OoR or player2 in OoR:
          continue
        # Find player1 Model
        player1_query = PlayerModel.query(PlayerModel.tag == player1)
        if player1_query.get() is not None:
          player1_object = player1_query.get()
        else:
          player1_object = PlayerModel()
          player1_object.tag = player1
          player1_object.ranking = trueskill.Rating()
          player1_object.put()
        player1_object.lastActive = match.timestamp
        # Find player2 Model
        player2_query = PlayerModel.query(PlayerModel.tag == player2)
        if player2_query.get() is not None:
          player2_object = player2_query.get()
        else:
          player2_object = PlayerModel()
          player2_object.tag = player2
          player2_object.ranking = trueskill.Rating()
          player2_object.put()
        player2_object.lastActive = match.timestamp
        #Run Rankings Algo
        player1_rate = player1_object.ranking
        player2_rate = player2_object.ranking
        #self.response.out.write(player1_rate)
        #self.response.out.write('<br>')
        #self.response.out.write(player2_rate)
        #self.response.out.write('<br>')
        if winner == player1:
          new_player1, new_player2 = trueskill.rate_1vs1(player1_rate, player2_rate)
        else:
          new_player2, new_player1 = trueskill.rate_1vs1(player2_rate, player1_rate)
        #self.response.out.write(new_player1)
        #self.response.out.write('<br>')
        #self.response.out.write(new_player2)
        #self.response.out.write('<br>')
        #self.response.out.write('<br>')
        # Update player stats
        player1_object.ranking = new_player1
        player2_object.ranking = new_player2
        #Save
        player1_object.put()
        player2_object.put()
        #self.response.out.write(match.player1+" vs. "+player2)
        #self.response.out.write('<br>')
      #self.response.out.write('<hl><br><br>')
    self.redirect('/')
