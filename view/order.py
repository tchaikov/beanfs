from django.utils import simplejson

from base import BaseRequestHandler
from models import User, Vendor, Group, Event, Order
from control.balance import UserBalance

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
  def get(self, id):
      order = Order.get_by_id(id)
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
    """collect new purchase of event whose key is `event_key'
    """
    event = Event.get(event_key)
    if not event:
      self.error(404)
    self.generate('put_order.html',
                  {'vendor':event.vendor,
                   'purchases':event.purchases})
    
  def post(self, event_id):
    """save the new order into db

    all items in the event have been confirmed by the contact person.. we need:
    - close the current event
    - create a new order
    """
    event = Event.get_by_id(event_id)
    if not event:
      self.error(404)
      return
    event.is_open = False
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
    event.put()
    
class OrderPayPage(BaseRequestHandler):
  """the payer will see this page
  """
  def get(self, order_id):
    order = Order.get_by_id(long(order_id))
    if order is None:
      self.error(404)
      return
    purchases = order.get_purchases()
    self.generate('pay.html',
                  {'order':order,
                   'purchases':purchases})

  def post(self, order_id):
    order = Order.get_by_id(long(order_id))
    if order is None:
      self.error(404)
      return
    # TODO: `purchaese' should be the received json object
    purchases = order.get_purchases()
    balance = UserBalance()
    for p in purchases:
      balance.pay_for(p.customer, p.item.price)
    self.redirect('/u/mine/profile')
