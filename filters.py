from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def vendors_items_uri(vendor_name):
    return '/v/%s/item/list' % vendor_name

register.filter(vendors_items_uri)
