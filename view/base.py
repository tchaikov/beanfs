import os
import Cookie

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

import config

class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def get(self, *params):
      self.error(403)
      
  def generate(self, template_name, template_values={}):
    values = {
        'request': self.request,
        'user': users.get_current_user(),
        'login_url': users.create_login_url(self.request.uri),
        'logout_url': users.create_logout_url('http://%s/' % (
            self.request.host,)),
        'debug': self.request.get('deb'),}
    values.update(template_values)
    root_dir = config.APP_ROOT_DIR
    path = os.path.join(root_dir, 'templates', template_name)
    self.response.out.write(template.render(path, values, debug=config.DEBUG))

  def get_cookie(self, name):
    cookies = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
    if name in cookies:
      return cookies[name].value
    else:
      return None


class ErrorPage(BaseRequestHandler):
  pass
