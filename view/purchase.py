import logging

from google.appengine.api import users
from django.utils import simplejson

from base import BaseRequestHandler
from models import Purchase, Vendor, Event, Order
from utils import exists_by_property, get1_by_property


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
    TODO: accept multiple json objects which present purchases.
    """
    event_id = long(id)
    response = {}
    try:
      jsons = simplejson.loads(self.request.body)
      purchases = [Purchase.create_from_json(event_id, json) for json in jsons]
      for purchase in purchases:
        purchase.put()
      response = {'status': 'success',
                  'redirect': '/e/%d/list' % event_id,
                  'n_purchase':len(purchases)}
    except Exception, e:
      response = {'status': str(e), 'n_purchase':0}
    simplejson.dump(response, self.response.out)

class EventList(BaseRequestHandler):
  def get(self, event_id):
    event = Event.get_by_id(long(event_id))
    if event is None:
      # TODO: should bring user to a "event not found, do you want to init an event?"
      self.error(404)
      return
    self.generate('list_purchase.html',
                  {'event':event,
                   'purchases':event.purchases})


class EventClose(BaseRequestHandler):
  def get(self, event_id):
    event = Event.get_by_id(long(event_id))
    if event is None:
      self.error(404)
      return
    # TODO: allow user to edit the purchase items
    self.generate('close_event.html',
                  {'event':event,
                   'purchases':event.purchases})

  def get_purchase_from_json(self, event):
    # TODO: should accept a json object represents
    #       all confirmed items
    return event.purchases
  
  def post(self, event_id):
    event = Event.get_by_id(long(event_id))
    if event is None:
      self.error(404)
      return
    logging.debug("event close: %r" % self.request.body)
    # TODO: merge with order.OrderAddPage.post
    event.is_open = False

    purchases = self.get_purchase_from_json(event)
    for purchase in purchases:
      purchase.status = 'collected'
      purchase.put()
    order = Order(contact = users.get_current_user(),
                  vendor = event.vendor,
                  purchases = [p.key() for p in purchases])
    order.put()
    event.order = order
    event.put()
    self.redirect('/u/mine/profile')
