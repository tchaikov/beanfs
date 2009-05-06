from base import BaseRequestHandler
from models import Photo

class ImagePage(BaseRequestHandler):
  def get(self, type, id):
    photo = Photo.get_by_id(int(id))
    if photo:
      self.response.headers.add_header('Expires', 'Thu, 01 Dec 2014 16:00')
      self.response.headers['Cache-Control'] = 'public, max-age=366000'
      #self.response.headers['Content-type'] = self.get_content_type(photo.name)
      # TODO: tell image type by looking at its name or read the image file header
      self.response.headers['Content-type'] = 'image/png'
      if type == 'image':
        self.response.out.write(photo.image)
      elif type == "thumb":
        self.response.out.write(photo.thumb)
      else:
        self.error(500)
    else:
      self.error(404)
