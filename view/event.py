import logging

from django.utils import simplejson
from google.appengine.api import users

from base import BaseRequestHandler
from models import Event, Group, Vendor
from forms import EventForm
from utils import exists_by_property

class AddPage(BaseRequestHandler):
  """ navigate in vendors, choose the item to purchase
  """
  def post(self):
      # TODO: sanity test
      group = self.request.get('group')
      vendor = self.request.get('vendor')
      event = Event(group = Group.get_by_id(long(group)),
                    vendor = Vendor.get_by_id(long(vendor)),
                    advocate = users.get_current_user())
      
      event.put()
      self.redirect('/u/mine/profile')
      
class AddPurchase(BaseRequestHandler):
    def post(self):
        json = simplejson.loads(self.request.body)
        # create a Purchase object from its JSON presentation
        # and put it into db storage
