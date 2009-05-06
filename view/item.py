import logging

from google.appengine.api import images

from base import BaseRequestHandler
from utils import get1_by_property
from models import Vendor
from forms import ItemForm


class ItemListPage(BaseRequestHandler):
  
  def get(self, vendor_name):
    vendor = get1_by_property(Vendor, 'name', vendor_name)
    if vendor is None:
      logging.debug('vendor %s not found ' % vendor_name)
      self.redirect('/v/entry?vendor=%s' % vendor_name )
      return
    items = list(vendor.get_items())
    logging.debug('%d items listed' % len(items))
    self.generate('list_item.html',
                  {'items':items,})

class ItemAddPage(BaseRequestHandler):
  def get(self, vendor_name):
    form = ItemForm()
    self.generate('add_item.html',
                  {'form':form,})

  def post(self, vendor_name):
    # TODO: should be editing existing item if the name of item is identical with existing one
    #       upload thumb
    #       resize thumb using google.appengine.api.images
    data = ItemForm(data=self.request.POST)
    if data.is_valid():
      item = data.save(commit=False)
      item.photo = self.get_photo()
      vendor = get1_by_property(Vendor, 'name', vendor_name)
      vendor.items.append(item.put())
      vendor.put()
      self.redirect('/v/%s/item/list' %  vendor_name)
    else:
      self.redirect('/v/%s/item/entry' % vendor_name)

  def get_photo(self):
    if "photo" not in self.request.POST:
      logging.debug('no image uploaded for new item!')
      return None
    try:
      img = self.request.POST.get("photo")
      img_name = img.filename
      img_data = img.file.read()
      img = images.Image(img_data)

      img.im_feeling_lucky()
      img.resize(640,480)
      png_data = img.execute_transforms(images.PNG)

      img.resize(200,140)
      thumb = img.execute_transforms(images.PNG)

      photo = Photo(name=img_name,
                    image=png_data,
                    thumb=thumb)
      return photo.put()
    except images.BadImageError:
      self.error(400)                                                                     
      self.response.out.write(                                                            
          'Sorry, we had a problem processing the image provided.')
    except images.NotImageError:
      self.error(400)
      self.response.out.write(
          'Sorry, we don\'t recognize that image format.'
          'We can process JPEG, GIF, PNG, BMP, TIFF, and ICO files.')
    except images.LargeImageError:
      self.error(400)
      self.response.out.write(
          'Sorry, the image provided was too large for us to process.')
