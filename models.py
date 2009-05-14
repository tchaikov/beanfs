#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

from google.appengine.api import users
from google.appengine.ext import db
from itertools import chain
from utils import get1_by_property


from utils import get1_by_property

class User(db.Model):
    balance = db.FloatProperty(required=True, default=0.0)
    #phone = db.PhoneNumberProperty(required=True)
    name = db.StringProperty(required=True)
    who = db.UserProperty()
    groups = db.ListProperty(db.Key)

    def get_groups(self):
        return Group.get(self.groups)
    
    @staticmethod
    def user(name):
        """Get google user by name"""
        return get1_by_property(User, 'name', name).who
    
    @staticmethod
    def get_current_user():
        user = get1_by_property(User, 'who', users.get_current_user())
        return user
    
    @staticmethod
    def get_groups_of_current_user():
        user = User.get_current_user()
        if user:
            return user.get_groups()
        else:
            return []
    
class Group(db.Model):
    name = db.StringProperty(required=True)
    members = db.ListProperty(db.Key)
    leader = db.UserProperty()
    def get_members(self):
        return User.get(self.members)

    def get_open_events(self):
        return db.Query(Event).filter('group = ', self).filter('is_open = ', True)
    
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

class Vendor(db.Model):
    name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    items = db.ListProperty(db.Key)
    comment = db.TextProperty()
    hit = db.IntegerProperty(default=0)
        
    def get_items(self):
        items = Item.get(self.items)
        return items

class Event(db.Model):
    vendor = db.ReferenceProperty(Vendor)
    advocate = db.UserProperty()
    group = db.ReferenceProperty(Group)
    is_open = db.BooleanProperty(default=True)
    
    @property
    def purchases(self):
        return db.Query(Purchase).filter('event = ', self)
        

class Purchase(db.Model):
    customer = db.UserProperty(required=True)
    item = db.ReferenceProperty(Item)
    fallbacks = db.ListProperty(db.Key)
    status = db.StringProperty(default='new', choices=('new', 'collected', 'payed'))
    event = db.ReferenceProperty(Event)
    
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
            

class Order(db.Model):
    contact = db.UserProperty(required=True)
    vendor = db.ReferenceProperty(Vendor)
    purchases = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)
    
    def get_purchases(self):
        ps = Purchase.get(self.purchases)
        return ps
    
class Bill(db.Model):
    payer = db.UserProperty(required=True)
    items = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)

class Transaction(db.Model):
    order = db.ReferenceProperty(Order)
    bill = db.ReferenceProperty(Bill)
    purchased = db.BooleanProperty(default=False)
    
