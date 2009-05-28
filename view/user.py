import logging

from google.appengine.api import users
from google.appengine.ext import db
from django.utils import simplejson

from base import BaseRequestHandler
from control import balance
from models import Vendor, User, Group, Event
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
        for group in self.request.POST.getall('group'):
          user.join(Group.get(group))
        self.redirect('/u/%s/profile' % user.name)
      else:
        logging.debug('user %s already exists!' % user.name)
        self.generate('add_user.html',
                      {'form':data,
                       'groups':Group.all()})
      

class UserProfilePage(BaseRequestHandler):
  def get_balances(self, user):
    user_balance = balance.UserBalance(user)
    balances, total_amount, max_amount = user_balance.get_balances()
    total = balance.Balance(amount=total_amount, name="Total", max_amount=max_amount)
    balances.append(total)
    return balances
  
  def get(self, username):
    if username == 'mine':
      user = User.get_current_user()
    else:
      user = get1_by_property(User, 'name', username)
    
    if user:
      balances = self.get_balances(user)
      self.generate('user_profile.html',
                    {'user':user,
                     'balances':balances,
                     'groups':Group.all(),
                     'vendors':Vendor.all()})    
    else:
      self.redirect('/oops/invalid_user')

  def post(self, username):
    # TODO
    pass

class CheckAvailability(BaseRequestHandler):
  def get(self):
    username = self.request.get("username")
    is_validate = not exists_by_property(User, 'name', username)
    content = simplejson.dumps({'is_available':is_validate})
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(content)
    self.response.out.write("\n")

