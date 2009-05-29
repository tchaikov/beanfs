#!/usr/bin/env python
#
# Copyright 2009 Kov Chai <tchaikov@gmail.com>
#

from itertools import chain
import logging
from google.appengine.api import users
from google.appengine.ext import db
from itertools import chain
from utils import get1_by_property


from utils import get1_by_property

class MutualBalance(db.Model):
    from_user = db.UserProperty(required=True)
    to_user = db.UserProperty(required=True)
    amount = db.FloatProperty(required=True, default=0.0)

    @staticmethod
    def get_balance(from_user, to_user):
        if from_user.user_id() > to_user.user_id():
            from_user, to_user = to_user, from_user
        balance = MutualBalance.gql("WHERE from_user = :from_user AND to_user = :to_user",
                                    from_user=from_user, to_user=to_user)
        if balance:
            return balance
        else:
            return MutualBalance(from_user=from_user, to_user=to_user, amount=0.0)

   
class User(db.Model):
    balance = db.FloatProperty(required=True, default=0.0)
    #phone = db.PhoneNumberProperty(required=True)
    name = db.StringProperty(required=True)
    who = db.UserProperty()
    
    @property
    def groups(self):
        return Group.gql("WHERE members = :me", me = self.key())

    def join(self, group):
        if group is None:
            return
        group.members.append(self.key())

    def get_balances(self):
        """ get all non-zero mutual balances 
        """
        user = self.who
        non_zero_balances = db.Query(MutualBalance).filter('amount > ', 0)
        my_balances = chain(non_zero_balances.filter('from_user = ', user),
                        non_zero_balances.filter('to_user = ', user))
        return my_balances
 
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
            return user.groups
        else:
            return []
    
class Group(db.Model):
    name = db.StringProperty(required=True)
    members = db.ListProperty(db.Key)
    leader = db.UserProperty()

    def __contains__(self, user):
        if user is not None:
            return user.key() in self.members
        return False
    
    def get_members(self):
        return User.get(self.members)

    def get_all_events(self):
        return db.Query(Event).filter('group = ', self)
    
    def get_open_events(self):
        return self.get_all_event().filter('is_open = ', True)
    
    def has_current_user(self):
        current_user = User.get_current_user()
        return current_user in self

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

    def __eq__(self, other):
        return self.name == other.name and \
               self.phone == other.phone
    
    def get_items(self):
        items = Item.get(self.items)
        return items
    
class Order(db.Model):
    contact = db.UserProperty(required=True)
    vendor = db.ReferenceProperty(Vendor)
    purchases = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)
    
    def get_purchases(self):
        ps = Purchase.get(self.purchases)
        return ps

class Event(db.Model):
    vendor = db.ReferenceProperty(Vendor)
    advocate = db.UserProperty()
    group = db.ReferenceProperty(Group)
    is_open = db.BooleanProperty(default=True)
    order = db.ReferenceProperty(Order)
    
    class NotExists(Exception):
        def __init__(self, id):
            self.id = id
        
        def __str__(self):
            return "unknown event %d" % self.id

    @property
    def purchases(self):
        return db.Query(Purchase).filter('event = ', self)
        
class Purchase(db.Model):
    customer = db.UserProperty(required=True)
    item = db.ReferenceProperty(Item, required=True)
    fallbacks = db.ListProperty(db.Key)
    notes = db.TextProperty()
    status = db.StringProperty(default='new', choices=('new', 'collected', 'payed', 'canceled'))
    event = db.ReferenceProperty(Event)

    class NotExists(Exception):
        def __init__(self, id = -1, name = 'unknown'):
            self.name = name
            self.id = id
        
        def __str__(self):
            return "unknown item %s:%d" % (self.name, self.id)

    @staticmethod
    def create_from_json(event_id, json):
        """convert a json object to an instance of models.Purchase
        """
        def get_item(name):
            item = get1_by_property(Item, 'name', name)
            if item is None:
                raise Purchase.NotExists(name=name)
            else:
                return item
        event = Event.get_by_id(event_id)
        logging.debug("create_from_json(event): %s %s: %r" % \
                      (event.vendor.name, event.advocate.nickname(), json))
    
        item = get_item(json['item'])
        fallbacks = [get_item(name).key().id() for name in json['fallbacks']]
        return Purchase(customer = users.get_current_user(),
                        item = item,
                        event = event)
        
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
            
    
class Bill(db.Model):
    payer = db.UserProperty(required=True)
    items = db.ListProperty(db.Key)
    time = db.DateTimeProperty(required=True, auto_now_add=True)

class Transaction(db.Model):
    order = db.ReferenceProperty(Order)
    bill = db.ReferenceProperty(Bill)
    purchased = db.BooleanProperty(default=False)
    
