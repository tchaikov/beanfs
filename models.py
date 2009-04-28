#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

from google.appengine.ext import db

class User(db.Model):
    balance = db.FloatProperty(required=True, default=0.0)
    phone = db.PhoneNumberProperty(required=True)
    name = db.StringProperty(required=True)
    who = db.UserProperty(required=True)
    bills = db.ListProperty(db.Key)

class Group(db.Model):
    name = db.StringProperty(required=True)
    members = db.ListProperty(db.Key)
    leader = db.StringProperty(required=True)
    bills = db.ListProperty(db.Key)

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

class Vendor(db.Model):
    name = db.StringProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    items = db.ListProperty(db.Key)
    comment = db.TextProperty()
    hit = db.IntegerProperty(default=0)
        
    def get_items(self):
        items = Item.get(self.items)
        return items
    
class Order(db.Model):
    contact = db.ReferenceProperty(User)
    vendor = db.ReferenceProperty(Vendor)
    purchases = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)


class Bill(db.Model):
    payer = db.ReferenceProperty(User)
    items = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)

    
class GroupBill(db.Model):
    payer = db.ReferenceProperty(User)
    user_bills = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)

    
class UserBill(db.Model):
    """
    `user` who owns this bill
    
    `items` may have duplicated items, which means that item is payed
    several times.

    `group_bill` the group bill this user bill belongs to.
    """
    user  = db.ReferenceProperty(User)
    items = db.ListProperty(db.Key)
    group_bill = db.ReferenceProperty(GroupBill)
    
class Transaction(db.Model):
    order = db.ReferenceProperty(Order)
    bill = db.ReferenceProperty(Bill)
    purchased = db.BooleanProperty(default=False)
    
