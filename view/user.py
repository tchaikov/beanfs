import logging

from base import BaseRequestHandler
from models import Vendor
from forms import UserForm
from utils import exists_by_property


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
      if not exists_by_property(User, 'name', user.name):
        user.put()
        self.redirect('/u/%s/profile' % user.name)
      else:
        logging.debug('user %s already exists!' % user.name)
        self.generate('add_user.html',
                      {'form':data})
      

class UserProfilePage(BaseRequestHandler):
  def get(self, username):
    user = get1_by_property(User, 'name', username)
    
    if user:
      self.generate('user_profile.html',
                    {'user':user,
                     'vendors':Vendor.all()})    
    else:
      self.redirect('/oops/invalid_user')
