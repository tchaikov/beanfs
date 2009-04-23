#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

import cgi
import Cookie
import logging
import datetime
import os
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

from models import Vendor
from forms import VendorForm

_DEBUG = True

class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    values = {
        'request': self.request,
        'user': users.get_current_user(),
        'login_url': users.create_login_url(self.request.uri),
        'logout_url': users.create_logout_url('http://%s/' % (
            self.request.host,)),
        'debug': self.request.get('deb'),}
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    logging.debug('rendering: %s' % path)
    self.response.out.write(template.render(path, values, debug=_DEBUG))

  def get_cookie(self, name):
    cookies = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
    if name in cookies:
      return cookies[name].value
    else:
      return None
      
class MainPage(BaseRequestHandler):
  @login_required
  def get(self):
    self.redirect('/list_vendor')

class VendorListPage(BaseRequestHandler):
  def get(self):
    vendor_list = Vendor.all().order('hit')
    vendor_list = list(vendor_list)     # XXX, not sure what this is for
    self.generate('list_vendor.html',
                  {'vendor_list':vendor_list,})

class AddVendorPage(BaseRequestHandler):
  def get(self):
    form = VendorForm()
    self.generate('add_vendor.html',
                  {'form':form,})

  def post(self):
    data = VendorForm(data=self.request.POST)
    if data.is_valid():
      vendor = data.save(commit=False)
      vendor.put()
      self.redirect('/items')
    else:
      self.redirect('/add_vendor')


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/add_vendor', AddVendorPage),
  ('/list_vendor', VendorListPage)], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
