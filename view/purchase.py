import logging

from base import BaseRequestHandler
from models import Purchase, Vendor
from utils import exists_by_property

class PurchasePage(BaseRequestHandler):
  """ navigate in vendors, choose the item to purchase
  """
  def get(self):
    vendors = list(Vendor.all())
    self.generate('order.html',
                  {'vendors':vendors,})
  
  def post(self):
      """
      TODO: accept a json string which presents a purchase including all stuff a models.
      """
      pass
  
