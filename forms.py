from google.appengine.ext.db import djangoforms
from models import Vendor, Item, User, Group
from google.appengine.ext import db


class VendorForm(djangoforms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ['items']
        
class ItemForm(djangoforms.ModelForm):
    class Meta:
        model = Item
        exclude = ['photo']

class UserForm(djangoforms.ModelForm):
    class Meta:
        model = User
        exclude = ['bills']


class GroupForm(djangoforms.ModelForm):
    class Meta:
        model = Group
