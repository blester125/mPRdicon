import webapp2

from models.MatchModel import *
from controllers.User import handle_user
from views.RenderTemplate import *

class History(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    render_template(self, 'history.html', template_params)

  def post(self):
    template_params = handle_user()
    player1 = self.request.get("player1")
    player2 = self.request.get("player2")
    if player1 == "" and player2 == "":
      history = MatchModel.query()
    elif player2 == "":
      history = MatchModel.query(ndb.OR(MatchModel.player1 == player1, 
                                        MatchModel.player2 == player1))
    elif player1 == "":
      history = MatchModel.query(ndb.OR(MatchModel.player1 == player2,
                                        MatchModel.player2 == player1))
    else:
      history = MatchModel.query(ndb.OR(ndb.AND(MatchModel.player1 == player1,
                                                MatchModel.player2 == player2),
                                        ndb.AND(MatchModel.player1 == player2,
                                                MatchModel.player2 == player1)
                                        )
                                )
    matches = []
    for i in history:
      match = Result()
      score = str(i.player1Score) + " - " + str(i.player2Score)
      match.player1 = i.player1
      match.player2 = i.player2
      match.winner = i.winner
      if i.winner == i.player1:
        self.p1winner = "True"
      match.score = score
      match.tournament = i.key.parent().get().name 
      match.tournament_url = i.key.parent().get().url
      matches.append(match)
    template_params['rankings'] = matches
    render_template(self, 'history.html', template_params)


class Result():
  def __init__(self):
    self.player1 = ""
    self.player2 = ""
    self.p1winner = ""
    self.score = ""
    self.tournament = ""
    self.tournament_url = ""
