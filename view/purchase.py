import logging

from django.utils import simplejson

from base import BaseRequestHandler
from models import Purchase, Vendor, Event
from utils import exists_by_property

class PurchasePage(BaseRequestHandler):
  """ navigate in vendors, choose the item to purchase
  """
  def get(self, event_id):
    event = Event.get_by_id(long(event_id))
    if event is None:
      # TODO: should bring user to a "event not found, do you want to init an event?"
      self.error(404)
      return
    vendors = list(Vendor.all())
    self.generate('order.html',
                  {'vendors':vendors,
                   'event':event,
                   'default_vendor':vendors.index(event.vendor)})
  
  def post(self, id):
    """
    TODO: accept a json string which presents a purchase including all stuff a models.
    """
    event = Event.get_by_id(long(id))
    if not event:
      self.error(404)
    logging.debug("posting to event: %s %s" % (event.vendor.name, event.advocate.nickname()))
    
