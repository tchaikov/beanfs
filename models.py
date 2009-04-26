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


class Group(db.Model):
    name = db.StringProperty(required=True)
    members = db.ListProperty(db.Key)
    leader = db.StringProperty(required=True)


class Image(db.Model):
    ext = db.StringProperty()
    thumb = db.BlobProperty(default=None)
    def name(self):
        return '.'.join([self.key(), self.thumb])
    
class Item(db.Model):
    name = db.StringProperty(required=True)
    price = db.FloatProperty(required=True)
    thumb = db.ReferenceProperty(Image)
    
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

class Transaction(db.Model):
    order = db.ReferenceProperty(Order)
    bill = db.ReferenceProperty(Bill)
    purchased = db.BooleanProperty(default=False)
    
