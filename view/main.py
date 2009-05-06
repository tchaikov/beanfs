from google.appengine.ext.webapp.util import login_required

from base import BaseRequestHandler

class MainPage(BaseRequestHandler):
  @login_required
  def get(self):
    self.generate('main.html')
