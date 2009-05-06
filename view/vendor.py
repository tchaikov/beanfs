import logging

from base import BaseRequestHandler
from models import Vendor
from forms import VendorForm

class VendorListPage(BaseRequestHandler):
  def get(self):
    vendors = Vendor.all().order('hit')
    vendors = list(vendors)     # convert the iterator to a list
    logging.debug('%d vendors listed' % len(vendors))
    self.generate('list_vendor.html',
                  {'vendors':vendors,})

class VendorAddPage(BaseRequestHandler):
  def get(self):
    form = VendorForm()
    self.generate('add_vendor.html',
                  {'form':form,})

  def post(self):
    data = VendorForm(data=self.request.POST)
    vendor_name = self.request.POST.get('name')
    if data.is_valid() and not exists_by_property(Vendor, 'name', vendor_name):
      vendor = data.save(commit=False)
      vendor.put()
      self.redirect('/v/all')
    else:
      self.redirect('/v/entry')

