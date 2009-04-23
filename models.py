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

class Item(db.Model):
    price = db.FloatProperty(required=True)
    name = db.StringProperty(required=True)

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
    


    
