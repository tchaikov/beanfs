import logging

from google.appengine.api import users
from models import User, MutualBalance
from utils import get1_by_property

class Percentage:
    def __init__(self, percent):
        assert 0 <= percent <= 100
        self.percent = percent*100.
        self.comp_percent = 100. - self.percent

class Balance:
    def __init__(self, amount, name, max_amount = 0):
        self.amount = amount
        self.name = name
        if max_amount:
            self.max_amount = max_amount
        else:
            self.max_amount = amount
        
    @staticmethod
    def create_from_mutual_balance(mutual_balance, user):
        if user.user_id() == mutual_balance.from_user.user_id():
            amount = mutual_balance.amount
            name = mutual_balance.to_user.nickname()
        elif user.user_id() == mutual_balance.to_user.user_id():
            amount = -mutual_balance.amount
            name = mutual_balance.from_user.nickname()
        else:
            assert "%s not belongs to (%s, %s)" % \
                   (user.nickname(),
                    mutual_balance.from_user.nickname(),
                    mutual_balance.to_user.nickname())
        return Balance(amount, name)

    def normalize(self, max_amount):
        self.max_amount = max_amount
            
    @property
    def lend(self):
        if self.amount >= 0 and self.max_amount != 0:
            return Percentage(self.amount/self.max_amount)
        else:
            return Percentage(0.0)

    @property
    def own(self):
        if self.amount < 0 and self.max_amount != 0:
            return Percentage(-self.amount/self.max_amount)
        else:
            return Percentage(0.0)
        
class UserBalance:
    def __init__(self, user = users.get_current_user()):
        self.user = user
                
    def get_balances(self):
        user = get1_by_property(User, 'who', self.user)
        bs = [Balance.create_from_mutual_balance(b, self.user) \
              for b in user.get_balances()]
        if not bs:
            return bs, 0, 0
        amount_list = [b.amount for b in bs]
        max_amount = max(abs(a) for a in amount_list)
        total_amount = sum(amount_list)
        for b in bs:
            b.normalize(max_amount)
        return bs, total_amount, max_amount

    def pay_for(self, other, amount):
        """adjust the balance of self and other

        other: an users.User
        """
        me = self.user
        balance = MutualBalance.get_balance(me, other)
        if balance.from_user == me:
            balance.amount += amount
        else:
            balance.amount -= amount
        balance.put()
        
            
