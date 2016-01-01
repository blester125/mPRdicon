import webapp2

from google.appengine.api import users
from controllers.Config import fetchAdmin

ADMIN = fetchAdmin()

def handle_user():
  user = users.get_current_user()
  if not user:
    template_params = {
      'user': False,
      'url': users.create_login_url('/'),
      'admin': False
    }
  else:
    template_params = {
      'user': True,
      'url': users.create_logout_url('/'),
      'admin': False
    }
    if user.email() in ADMIN or user.email() == 'BLester125@gmail.com':
      template_params['admin'] = True
  return template_params
