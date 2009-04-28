from google.appengine.ext import webapp
from models import User
register = webapp.template.create_template_register()

def vendors_items_uri(vendor_name):
    return '/v/%s/item/list' % vendor_name


def user_key2name(user_key):
    return User.get(user_key).name


register.filter(vendors_items_uri)
register.filter(user_key2name)
