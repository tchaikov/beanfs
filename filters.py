from google.appengine.ext import webapp
from models import User, Item
register = webapp.template.create_template_register()

def vendors_items_uri(vendor_name):
    return '/v/%s/item/list' % vendor_name


def user_key2name(user_key):
    return User.get(user_key).name


def item_key2name(item_key):
    return Item.get(item_key).name


register.filter(vendors_items_uri)
register.filter(user_key2name)
register.filter(item_key2name)
