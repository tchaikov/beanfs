#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

from google.appengine.ext import db
from itertools import chain
from utils import find


class User(db.Model):
    balance = db.FloatProperty(required=True, default=0.0)
    phone = db.PhoneNumberProperty(required=True)
    name = db.StringProperty(required=True)
    who = db.UserProperty(required=True)
    group = db.ListProperty(db.Key)

class Group(db.Model):
    name = db.StringProperty(required=True)
    members = db.ListProperty(db.Key)
    leader = db.StringProperty(required=True)
    def get_members(self):
        return User.get(self.members)

class Photo(db.Model):
    image = db.BlobProperty(default=None)
    thumb = db.BlobProperty(default=None)
    name = db.StringProperty()
    def name(self):
        return '.'.join([self.key(), self.ext])
    
class Item(db.Model):
    name = db.StringProperty(required=True)
    price = db.FloatProperty(required=True)
    photo = db.ReferenceProperty(Photo)
    
class Purchase(db.Model):
    customer = db.ReferenceProperty(User)
    item = db.ReferenceProperty(Item)
    fallbacks = db.ListProperty(db.Key)
    status = db.StringProperty(default='new', choices=('new', 'collected', 'payed'))

    @staticmethod
    def get_purchase_of_user(user, status='new'):
        query = db.Query(Purchase).filter('customer = ', user)
        if status != 'all':
            query = query.filter('status = ', status)
        return list(query)

    @staticmethod
    def get_current_user_purchase(status='new'):
        return Purchase.get_purchase_of_user(users.get_current_user(), status)
    
    @staticmethod
    def get_new_in_group(group):
        return chain(Purchase.get_purchase_of_user(m) \
                     for m in group.get_members())
            
class Vendor(db.Model):
    name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    items = db.ListProperty(db.Key)
    comment = db.TextProperty()
    hit = db.IntegerProperty(default=0)
        
    def get_items(self):
        items = Item.get(self.items)
        return items

    def get_item(self, name):
        item_key = find(lambda item_key: Item.get(item_key).name == name,
                        self.items)
        
        if item_key:
            return Item.get(item_key)

            
class Order(db.Model):
    contact = db.ReferenceProperty(User)
    vendor = db.ReferenceProperty(Vendor)
    purchases = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)
    
    def get_purchases(self):
        ps = Purchase.get(self.purchases)
        return ps
    
class Bill(db.Model):
    payer = db.ReferenceProperty(User)
    items = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)

class Transaction(db.Model):
    order = db.ReferenceProperty(Order)
    bill = db.ReferenceProperty(Bill)
    purchased = db.BooleanProperty(default=False)
    
