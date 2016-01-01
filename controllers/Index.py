import webapp2
import datetime
import trueskill

from models.PlayerModel import *
from views.RenderTemplate import *
from controllers.User import handle_user

from controllers.Config import *

class Index(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    # Create Example data
    '''
    member1 = PlayerModel()
    member1.tag = 'SlientSwag'
    member1.score = 2134
    member1.lastActive = datetime.datetime.now()
    
    member2 = PlayerModel()
    member2.tag = 'Abate'
    member2.score = 2054
    member2.lastActive = datetime.datetime.now()
    
    member3 = PlayerModel()
    member3.tag = 'Vudujin'
    member3.score = 2001
    member3.lastActive = datetime.datetime.now()
    
    member4 = PlayerModel()
    member4.tag = 'Taki'
    member4.score = 9001
    member4.lastActive = datetime.datetime.now() - datetime.timedelta(days=60)

    member1.put()
    member2.put()
    member3.put()
    member4.put()
    '''
    # The time period before a player goes inactive
    inactive_window = datetime.timedelta(days=40)
    cut_off = datetime.datetime.now() - inactive_window
    # Get all players that have been active since the cutoff
    players = PlayerModel.query(PlayerModel.lastActive > cut_off)
    rankings = []
    # Copy the players into a list
    for player in players:
      rankings.append(player)
    # Sort the players
    rankings.sort(key = lambda x: x.ranking.mu, reverse=True)
    #rankings.sort()
    # Zip number list with rankings list
    rankings_zip = zip(range(1, len(rankings) + 1), rankings)
    template_params['rankings'] = rankings_zip

    render_template(self, 'index.html', template_params)
