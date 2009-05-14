from google.appengine.ext.db import djangoforms
from models import Vendor, Item, User, Group, Event

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
        exclude = ['who', 'groups']


class GroupForm(djangoforms.ModelForm):
    class Meta:
        model = Group

class EventForm(djangoforms.ModelForm):
    class Meta:
        model = Event
        exclude = ['advocate', 'is_open']
    
