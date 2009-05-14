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
        exclude = ['balance', 'who', 'phone', 'groups']


class GroupForm(djangoforms.ModelForm):
    class Meta:
        model = Group


class EventForm(djangoforms.ModelForm):
    group = djangoforms.forms.CharField( \
        widget = djangoforms.forms.Select(choices=User.get_groups_of_current_user()))
    vendor = djangoforms.forms.CharField( \
        widget = djangoforms.forms.Select(choices=Vendor.all()))
    class Meta:
        model = Event
        exclude = ['advocate', 'is_open']
    
