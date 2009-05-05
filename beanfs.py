#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

import cgi
import Cookie
import logging
import datetime
import os
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users, images
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

from models import Vendor, Item, User, Group, Photo, GroupBill, UserBill
from forms import VendorForm, ItemForm, UserForm
from utils import exists_by_property, get1_by_property

_DEBUG = True

class BaseRequestHandler(webapp.RequestHandler):
  """Supplies a common template generation function.

  When you call generate(), we augment the template variables supplied with
  the current user in the 'user' variable and the current webapp request
  in the 'request' variable.
  """
  def generate(self, template_name, template_values={}):
    values = {
        'request': self.request,
        'user': users.get_current_user(),
        'login_url': users.create_login_url(self.request.uri),
        'logout_url': users.create_logout_url('http://%s/' % (
            self.request.host,)),
        'debug': self.request.get('deb'),}
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

  def get_cookie(self, name):
    cookies = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
    if name in cookies:
      return cookies[name].value
    else:
      return None
      
class MainPage(BaseRequestHandler):
  @login_required
  def get(self):
    self.generate('main.html')

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

class ItemListPage(BaseRequestHandler):
  
  def get(self, vendor_name):
    vendor = get1_by_property(Vendor, 'name', vendor_name)
    if vendor is None:
      logging.debug('vendor %s not found ' % vendor_name)
      self.redirect('/v/entry?vendor=%s' % vendor_name )
      return
    items = list(vendor.get_items())
    logging.debug('%d items listed' % len(items))
    self.generate('list_item.html',
                  {'items':items,})

class ItemAddPage(BaseRequestHandler):
  def get(self, vendor_name):
    form = ItemForm()
    self.generate('add_item.html',
                  {'form':form,})

  def post(self, vendor_name):
    # TODO: should be editing existing item if the name of item is identical with existing one
    #       upload thumb
    #       resize thumb using google.appengine.api.images
    data = ItemForm(data=self.request.POST)
    if data.is_valid():
      item = data.save(commit=False)
      item.photo = self.get_photo()
      vendor = get1_by_property(Vendor, 'name', vendor_name)
      vendor.items.append(item.put())
      vendor.put()
      self.redirect('/v/%s/item/list' %  vendor_name)
    else:
      self.redirect('/v/%s/item/entry' % vendor_name)

  def get_photo(self):
    if "photo" not in self.request.POST:
      logging.debug('no image uploaded for new item!')
      return None
    try:
      img = self.request.POST.get("photo")
      img_name = img.filename
      img_data = img.file.read()
      img = images.Image(img_data)

      img.im_feeling_lucky()
      img.resize(640,480)
      png_data = img.execute_transforms(images.PNG)

      img.resize(200,140)
      thumb = img.execute_transforms(images.PNG)

      photo = Photo(name=img_name,
                    image=png_data,
                    thumb=thumb)
      return photo.put()
    except images.BadImageError:
      self.error(400)                                                                     
      self.response.out.write(                                                            
          'Sorry, we had a problem processing the image provided.')
    except images.NotImageError:
      self.error(400)
      self.response.out.write(
          'Sorry, we don\'t recognize that image format.'
          'We can process JPEG, GIF, PNG, BMP, TIFF, and ICO files.')
    except images.LargeImageError:
      self.error(400)
      self.response.out.write(
          'Sorry, the image provided was too large for us to process.')

class OrderListPage(BaseRequestHandler):
  """list all orders by a given criteria (e.g. vendor, time, user)
  """
  pass

class OrderAddPage(BaseRequestHandler):
  """collect all purchases put by user's group members, and call the vendor.
  """
  pass

class OrderPayPage(BaseRequestHandler):
  pass


class GroupBillListPage(BaseRequestHandler):
  """
  Show all group bills for one group.
  """
  def get(self, group_name):
    group = get1_by_property(Group, 'name', group_name)

    
    self.generate('group_bill_list.html',
                  {'group_bills':group.bills})
        

class GroupBillPage(BaseRequestHandler):
  """
  Show one group bill for the group
  """
  def get(self, bill_key):
    group_bill = GroupBill().get(bill_key)
    user_bills = [UserBill().get(key) for key in group_bill.user_bills]
    
    logging.info('group_bill.user_bills: %s' % group_bill.user_bills)
    self.generate('group_bill.html',
                  {'group_bill':group_bill,
                   'user_bills':user_bills})

    
class UserBillListPage(BaseRequestHandler):
  """
  Show all user bills for one user.
  """
  def get(self, user_name):
    user = get1_by_property(User, 'name', user_name)
    self.generate('user_bill_list.html',
                  {'user_bills':user.bills})


class UserBillPage(BaseRequestHandler):
  """
  Show one user bill for the user
  """
  def get(self, bill_key):
    bill = UserBill().get(bill_key)
    self.generate('user_bill.html',
                  {'user_bill':bill})


class GroupBillAddPage(BaseRequestHandler):
  """
  for testing
  """
  def get(self):
    self.generate('add_group_bill.html')

  def post(self):
    logging.info('GroupBillAddPage::post() is called\n')

    group_name = self.request.POST.get('name')
    group = get1_by_property(Group, 'name', group_name)

    logging.info('Group Name is %s' % group_name)
    
    if not group.bills or group.bills == []:
      group_bill = GroupBill(payer = get1_by_property(User, 'name', self.request.POST.get('payer')))
      group_bill.put()
      
      usera = get1_by_property(User, 'name', 'yami')
      user_billa = UserBill(user  = usera,
                            items = [get1_by_property(Item, 'name', 'xiaochao').key()],
                            group_bill = group_bill)
      user_billa.put()
      usera.bills.append(user_billa.key())

      userb = get1_by_property(User,'name', 'hua')
      user_billb = UserBill(user = userb,
                            items = [get1_by_property(Item, 'name', 'xiaochao').key()],
                            group_bill = group_bill)
      user_billb.put()
      userb.bills.append(user_billb.key())

      usera.put()
      userb.put()


      group_bill.user_bills.append(user_billa.key())
      group_bill.user_bills.append(user_billb.key())
      group_bill.put()
      
      group.bills.append(group_bill)
      
    self.redirect('/g/bill/%s' % group_bill.key())
      
class UserProfilePage(BaseRequestHandler):
  def get(self, user_name):
    user = get1_by_property(User, 'name', user_name)
    
    if user:
      self.generate('user_profile.html',
                    {'user':user})    
    else:
      self.redirect('/oops/invalid_user')


class UserAddPage(BaseRequestHandler):
  def get(self):
    form = UserForm()
    self.generate('add_user.html',
                  {'form':form})

  def post(self):
    data = UserForm(data=self.request.POST)

    if not data.is_valid():
      self.redirect('/u/register')
    else:
      user = data.save(commit=False)

      # TODO: to avoid convert to list
      if not exists_by_property(User, 'name', user.name):
        user.put()
        self.redirect('/u/%s/profile' % user.name)
      else:
        logging.debug('user %s already exists!' % user.name)
        self.generate('add_user.html',
                      {'form':data})
      
class GroupAddPage(BaseRequestHandler):
  """
  Add a group.
  """

  # TODO: Can we just use leader's name as group name? And group name
  # is not the primary key.
  
  # FIXME: we should use djangoforms like approaches, but it seems
  # that GAE's djangoforms does not support ListProperty well.
  def _populate(self):
    group = Group(name=self.request.POST['name'],
                  leader=self.request.POST['leader'])

    return group
    
  def get(self):
    self.generate('add_group.html')

  def post(self):
    group = self._populate()
    group.put()
    self.redirect('/g/%s/profile' % group.name)
      

class GroupListPage(BaseRequestHandler):
  """
  List all groups.
  """
  def get(self):
    self.generate("list_group.html",
                  {"groups":list(Group.all())})


class GroupProfilePage(BaseRequestHandler):
  """
  Show a group's information.
  """
  def get(self, group_name):
    group = get1_by_property(Group, 'name', group_name)

    self.generate('group_profile.html',
                  {'group':group})

  def post(self, group_name):
    group = get1_by_property(Group, 'name', group_name)
    user_name = self.request.POST.get('member')

    user = get1_by_property(User, 'name', user_name)

    if not user:
      self.redirect('/oops/invalid_user')
    else:
      group.members.append(user.key())
      group.put()
      self.redirect('/g/%s/profile' % group.name)
    


class ErrorPage(BaseRequestHandler):
  pass

class PurchasePage(BaseRequestHandler):
  """ navigate in vendors, choose the item to purchase
  """
  def get(self):
    vendors = list(Vendor.all())
    self.generate('order.html',
                  {'vendors':vendors,})

  def post(self):
    pass

class ImagePage(BaseRequestHandler):
  def get(self, type, id):
    photo = Photo.get_by_id(int(id))
    if photo:
      self.response.headers.add_header('Expires', 'Thu, 01 Dec 2014 16:00')
      self.response.headers['Cache-Control'] = 'public, max-age=366000'
      #self.response.headers['Content-type'] = self.get_content_type(photo.name)
      # TODO: tell image type by looking at its name or read the image file header
      self.response.headers['Content-type'] = 'image/png'
      if type == 'image':
        self.response.out.write(photo.image)
      elif type == "thumb":
        self.response.out.write(photo.thumb)
      else:
        self.error(500)
    else:
      self.error(404)
        
webapp.template.register_template_library('filters')
application = webapp.WSGIApplication([
  (r'/', MainPage),
  (r'/u/(?P<username>.*)/profile', UserProfilePage),
  (r'/u/register', UserAddPage),        # TODO: need a complete impl of registration
  (r'/v/all', VendorListPage),          # will be replaced with the main page
  (r'/v/entry', VendorAddPage),
  (r'/v/(?P<vendor>.*)/item/list', ItemListPage),
  (r'/v/(?P<vendor>.*)/item/entry', ItemAddPage),
  (r'/o/(?P<txn>.*)/list', OrderListPage),
  (r'/o/(?P<txn>.*)/entry', OrderAddPage),
  (r'/o/(?P<txn>.*)/pay', OrderPayPage),
  (r'/g/(?P<group>.*)/profile', GroupProfilePage),
  (r'/g/add_group', GroupAddPage),
  (r'/g/list_group', GroupListPage),
  (r'/g/add_group_bill', GroupBillAddPage),
  (r'/g/bill/(.*)', GroupBillPage),
  (r'/g/(.*)/bill', GroupBillListPage),
  (r'/oops/(?P<error>.*)', ErrorPage),
  (r'/purchase', PurchasePage),
  (r'/(image)/(\d+)', ImagePage),
  (r'/(thumb)/(\d+)', ImagePage),
  ], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
