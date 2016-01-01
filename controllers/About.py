import webapp2

from controllers.User import handle_user
from views.RenderTemplate import *

class About(webapp2.RequestHandler):
  def get(self):
    template_params = handle_user()
    render_template(self, 'about.html', template_params)