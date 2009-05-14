import logging

from google.appengine.api import users
from google.appengine.ext import db

from base import BaseRequestHandler
from models import Vendor, User, Group
from forms import UserForm
from utils import exists_by_property, get1_by_property


class UserAddPage(BaseRequestHandler):
  def get(self):
    form = UserForm()
    self.generate('add_user.html',
                  {'form':form,
                   'groups':Group.all()})
    
  def post(self):
    data = UserForm(data=self.request.POST)

    logging.info(self.request.POST)
    
    if not data.is_valid():
      self.redirect('/u/register')
    else:
      user = data.save(commit=False)

      if not exists_by_property(User, 'name', user.name):
        user.who = users.get_current_user()
        user.put()
        self.redirect('/u/%s/profile' % user.name)
      else:
        logging.debug('user %s already exists!' % user.name)
        self.generate('add_user.html',
                      {'form':data})
      

class UserProfilePage(BaseRequestHandler):
  def get(self, username):
    if username == 'mine':
      user = User.get_current_user()
    else:
      user = get1_by_property(User, 'name', username)
    
    if user:
      self.generate('user_profile.html',
                    {'user':user,
                     'vendors':Vendor.all()})    
    else:
      self.redirect('/oops/invalid_user')

  def post(self, username):
    # TODO: display check boxes presenting different groups,
    #       allowing user to join multiple groups
    pass
