import logging

from django.utils import simplejson

from base import BaseRequestHandler
from models import Event
from forms import EventForm
from utils import exists_by_property

class AddPage(BaseRequestHandler):
  """ navigate in vendors, choose the item to purchase
  """
  def post(self):
      # TODO: sanity test
      group = self.request.POST['group']
      vendor = self.request.POST['vendor']
      event = Event(group = Group.get(group),
                    vendor = Vendor.get(vendor),
                    advocate = user.get_current_user())
      event.put
      if data.is_valid():
          event = data.save(commit=False)
          event.advocate = user.get_current_user()
          event.put()
          
class AddPurchase(BaseRequestHandler):
    def post(self):
        json = simplejson.loads(self.request.body)
        # create a Purchase object from its JSON presentation
        # and put it into db storage
