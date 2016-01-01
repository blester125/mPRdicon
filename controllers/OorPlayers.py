import webapp2

from models.OoRModel import * 
from controllers.User import handle_user
from views.RenderTemplate import *

class OorPlayers(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    OoR = OoRModel.query().get()
    if OoR == None:
      template_params['players'] = []
    else:
      template_params['players'] = OoR.players
    render_template(self, 'oor.html', template_params)

class AddOoR(webapp2.RequestHandler):
  def post(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    newPlayer = self.request.get("newPlayer")
    OoR_object = OoRModel.query().get()
    if OoR_object == None:
      OoR_object = OoRModel()
    OoR_list = OoR_object.players
    if OoR_list.count(newPlayer) == 0:
      OoR_list.append(newPlayer)
    OoR_object.players = OoR_list
    OoR_object.put()
    self.redirect('/')


class DeleteOoR(webapp2.RequestHandler):
  def post(self):
    template_params = handle_user()
    if not 'admin' in template_params:
      self.redirect('/')
      return
    todelete = self.request.get("deletePlayer")
    OoR_object = OoRModel.query().get()
    OoR_list = OoR_object.players
    if OoR_list.count != 0:
      OoR_list.remove(todelete)
    OoR_object.players = OoR_list
    OoR_object.put()
    self.redirect('/')