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
  """collect all purchases put by user's group members, and call the vendor.
  """
  def collect_purchases(self, group_key):
    """collect all new purchases in a group indicated by `group_key`
    """
    group = Group.get(group_key)
    assert group is not None, "the user should belong to an existing group"
    #members = User.get
    
  def get(self):
    pass


class OrderPage(BaseRequestHandler):
  """
  show a page for user to choose which item to order.
  """
  def get(self):
    self.generate('order_for_item.html')

  
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


