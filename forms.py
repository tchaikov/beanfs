from google.appengine.ext.db import djangoforms
from models import Vendor

class VendorForm(djangoforms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ['items']
        
