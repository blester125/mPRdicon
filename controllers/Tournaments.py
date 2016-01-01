import webapp2
import datetime
from dateutil import parser

from models.TournamentModel import *
from models.MatchModel import *
from controllers.User import handle_user
from controllers.Config import fetchChallonge
from views.RenderTemplate import *

from challonge import *

CHALLONGE_USERNAME, CHALLONGE_API = fetchChallonge()

class ListTournaments(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    # Create Example Data
    '''
    tourn1 = TournamentModel()
    tourn1.name = "MoaL 85 Melee Singles"
    tourn1.url = "http://moal.challonge.com/MoaL85MeleeSingles"
    tourn1.timestamp = datetime.datetime.now()
    tourn2 = TournamentModel()
    tourn2.name = "MoaL 84 Melee Singles"
    tourn2.url = "http://moal.challonge.com/MoaL84MeleeSingles"
    tourn2.timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
    tournaments = [tourn1, tourn2]
    template_params['tournaments'] = tournaments
    tourn1.put()
    tourn2.put()
    # Fetch from data store 
    '''
    tournament_list = []
    tournaments =  TournamentModel.query()
    for tournament in tournaments:
      tournament_list.append(tournament)
    tournament_list.sort(key = lambda x: x.timestamp, reverse=True)
    template_params['tournaments'] = tournament_list
    
    render_template(self, 'listTournaments.html', template_params)


class AddTournaments(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    render_template(self, 'addTournaments.html', template_params)

  def post(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    tournament_url = self.request.get("url")
    # Check for input
    if tournament_url == "":
      self.redirect("/addTournaments")
      return
    dup_check = TournamentModel.query(TournamentModel.url==convert_url(tournament_url))
    if dup_check.get() is not None:
      render_template(self, 'error_dup_league.html', template_params)
      return
    api.set_credentials(CHALLONGE_USERNAME, CHALLONGE_API)
    #Handle tournament not found error
    tournament = tournaments.show(tournament_url)
    tournament_object = TournamentModel()
    tournament_object.name = tournament['name']
    tournament_object.url = convert_url(tournament_url)
    timestamp = parser.parse(tournament['created-at'][:-6])
    tournament_object.timestamp = timestamp
    tournament_object.put()

    # Extract the matches
    # Move participant seach to preindex'd list rather than 3 challonge requests
    match_list = matches.index(tournament['id'])
    participant_list = participants.index(tournament['id'])
    self.response.out.write(participant_list)
    for match in match_list:
      match_object = MatchModel(parent=tournament_object.key)
      # Find names via challonge
      #match_object.player1 = participants.show(tournament['id'], match['player1-id'])['name']
      #match_object.player2 = participants.show(tournament['id'], match['player2-id'])['name']
      # Find names via list
      for p in participant_list:
        if p['id'] == match['player1-id']:
          match_object.player1 = p['name']
        if p['id'] == match['player2-id']:
          match_object.player2 = p['name']
      if match['scores-csv'] != "":
        parts = match['scores-csv'].split('-')
        match_object.player1Score = int(parts[0])
        match_object.player2Score = int(parts[1])
      winner = participants.show(tournament['id'], match['winner-id'])
      match_object.winner = winner['name'] 
      match_object.label = match['identifier']
      timestamp = parser.parse(match['started-at'][:-6])
      match_object.timestamp = timestamp
      match_object.put()
      
    self.redirect("/listTournaments")

class DeleteTournaments(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    tournament_list = TournamentModel.query()
    tournament_array = []
    for tournament in tournament_list:
      tournament_array.append(tournament)
    tournament_array.sort(key = lambda x: x.timestamp, reverse=True)
    template_params['tournaments'] = tournament_array
    render_template(self, 'deleteTournaments.html', template_params)

  def post(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    tournament_url = self.request.get("tournament_to_delete")
    tournament = TournamentModel.query(TournamentModel.url==tournament_url)
    match_list = MatchModel.query(ancestor=tournament.get().key)
    for match in match_list:
      match.key.delete()
    tournament.get().key.delete()
    self.redirect('/listTournaments')

'''
  Transform a url in the form of subdomain-url or url to the 
  actual challonge url, ie, http://subdomain.challonge.com/url
'''
def convert_url(tournament_url):
  subdomain = ""
  parts = tournament_url.split("-")
  if len(parts) > 1:
    subdomain = parts[0]
    subdomain = subdomain + "."
    tournament_url = parts[1]
  return "http://{}challonge.com/{}".format(subdomain, tournament_url)
