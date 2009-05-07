import simplejson

from base import BaseRequestHandler
from models import Vendor, Group

class PurchaseListPage(BaseRequestHandler):
  """list all orders of current user
  """
  def get(self, status):
    Purchase.get_current_user_purchase(status=status)
    self.generate('user_bill_list.html',
                  {'user_bills':user.bills})

class OrderListPage(BaseRequestHandler):
  """
  Show all purchases in an order.
  """
  def get(self, key):
      order = Order().get(key)
      if order is None:
          self.error(404)
      purchases = order.get_purchases()
      self.generate('purchase_in_order.html',
                    {'order':order,
                     'purchases':purchases})
      
class OrderAddPage(BaseRequestHandler):
  """collect all purchases in an event, and call the vendor.
  """
  def get(self, event_key):
    """collect all new purchases in a group indicated by `group_key`
    TODO: maybe we need send a JSON repsentation to the client?
    """
    event = Event.get(event_key)
    if not event:
      self.error(404)
    self.generate('put_order.html',
                  {'vendor':event.vendor,
                   'purchases':event.purchases})
    
  def post(self, event_key):
    """save the new order into db
    """
    event = Event.get(event_key)
    if not event:
      self.error(404)

    json = self.request.get('json')
    json = simplejson.loads(json)
    purchases = []
    for p in json['purchases']:
      purchase = Purchase.get(p['key'])
      purchase.item = Item.get(p['item'])
      purchase.status = 'collected'
      purchases.append(purchase.put())
    order = Order(contact=users.get_current_user(),
                  vendor=event.vendor,
                  purchases=purchases)
    order.put()

class OrderPayPage(BaseRequestHandler):
  pass

class PurchasePage(BaseRequestHandler):

  """
  Show all user bills for one user.
  """
  def get(self, purchase_key):
      pass

  def post(self):
    pass


