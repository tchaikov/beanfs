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

from models import Vendor, User
from forms import VendorForm, ItemForm, UserForm

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
    self.generate('main.html')

class VendorListPage(BaseRequestHandler):
  def get(self):
    vendors = Vendor.all().order('hit')
    vendors = list(vendors)     # convert the iterator to a list
    logging.debug('%d vendors listed' % len(vendors))
    self.generate('list_vendor.html',
                  {'vendors':vendors,})

class VendorAddPage(BaseRequestHandler):
  def get(self):
    form = VendorForm()
    self.generate('add_vendor.html',
                  {'form':form,})

  def post(self):
    data = VendorForm(data=self.request.POST)
    vendor_name = self.request.POST.get('name')
    if data.is_valid() and Vendor.get_by_name(vendor_name) is None:
      vendor = data.save(commit=False)
      vendor.put()
      self.redirect('/list_vendor')
    else:
      self.redirect('/add_vendor')

class ItemListPage(BaseRequestHandler):
  def get(self, vendor_name):
    vendor = Vendor.get_by_name(vendor_name)
    if vendor is None:
      logging.debug('vendor %s not found ' % vendor_name)
      self.redirect('/v/entry?vendor=%s' % vendor_name )
      return
    items = list(vendor.get_items())
    logging.debug('%d items listed' % len(items))
    self.generate('list_item.html',
                  {'items':items,})

class ItemAddPage(BaseRequestHandler):
  def get(self, vendor_name):
    form = ItemForm()
    self.generate('add_item.html',
                  {'form':form,})

  def post(self, vendor_name):
    # TODO: need to append this item to the vendor which offers it
    #       upload thumb
    data = ItemForm(data=self.request.POST)
    if data.is_valid():
      item = data.save(commit=False)
      vendor = Vendor.get_by_name(vendor_name)
      vendor.items.append(item.put())
      self.redirect('/v/%s/item/list' %  vendor_name)
    else:
      self.redirect('/v/%s/item/entry' % vendor_name)

class OrderListPage(BaseRequestHandler):
  pass

class OrderAddPage(BaseRequestHandler):
  pass

class OrderPayPage(BaseRequestHandler):
  pass


class UserProfilePage(BaseRequestHandler):
  def get(self, username):
    user_list = list(User.all().filter('name =', username))
    assert len(user_list) <= 1

    if len(user_list) == 0:
      self.redirect('/oops/invalid_user')
    else:
      user = user_list[0]
      self.generate('user_profile.html',
                    {'user':user})    
    

class UserAddPage(BaseRequestHandler):
  def get(self):
    form = UserForm()
    self.generate('add_user.html',
                  {'form':form})

  def post(self):
    data = UserForm(data=self.request.POST)

    if not data.is_valid():
      self.redirect('/u/register')
    else:
      user = data.save(commit=False)

      # TODO: to avoid convert to list
      if list(User.all().filter('name =', user.name)) == []:
        user.put()
        self.redirect('/u/%s/profile' % user.name)
      else:
        self.generate('add_user.html',
                      {'form':data})
      


class ErrorPage(BaseRequestHandler):
  pass


application = webapp.WSGIApplication([
  (r'/', MainPage),
  (r'/u/(?P<username>.*)/profile', UserProfilePage),
  (r'/u/register', UserAddPage),        # TODO: need a complete impl of registration
  (r'/v/all', VendorListPage),          # will be replaced with the main page
  (r'/v/entry', VendorAddPage),
  (r'/v/(?P<vendor>.*)/item/list', ItemListPage),
  (r'/v/(?P<vendor>.*)/item/entry', ItemAddPage),
  (r'/o/(?P<txn>.*)/list', OrderListPage),
  (r'/o/(?P<txn>.*)/entry', OrderAddPage),
  (r'/o/(?P<txn>.*)/pay', OrderPayPage),
  (r'/oops/(?P<error>.*)', ErrorPage),
  ], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
