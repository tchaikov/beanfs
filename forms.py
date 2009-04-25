from google.appengine.ext.db import djangoforms
from models import Vendor, Item, User

class VendorForm(djangoforms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ['items']
        
class ItemForm(djangoforms.ModelForm):
    class Meta:
        model = Item
        exclude = ['thumb']

class UserForm(djangoforms.ModelForm):
    class Meta:
        model = User
