from models import Group, User
from base import BaseRequestHandler
from utils import get1_by_property

class GroupAddPage(BaseRequestHandler):
  """
  Add a group.
  """

  # TODO: Can we just use leader's name as group name? And group name
  # is not the primary key.
  
  # FIXME: we should use djangoforms like approaches, but it seems
  # that GAE's djangoforms does not support ListProperty well.
  def _populate(self):
    leader = User.user(self.request.POST['leader'])
    group = Group(name=self.request.POST['name'],
                  leader=leader)

    return group
    
  def get(self):
    self.generate('add_group.html')

  def post(self):
    group = self._populate()
    group.put()
    self.redirect('/g/%s/profile' % group.name)
      
class GroupListPage(BaseRequestHandler):
  """
  List all groups.
  """
  def get(self):
    self.generate("list_group.html",
                  {"groups":list(Group.all())})
    
class GroupProfilePage(BaseRequestHandler):
  """
  Show a group's information.
  """
  def get(self, group_name):
    group = get1_by_property(Group, 'name', group_name)

    self.generate('group_profile.html',
                  {'group':group})

  def post(self, group_name):
    group = get1_by_property(Group, 'name', group_name)
    user_name = self.request.POST.get('member')

    user = get1_by_property(User, 'name', user_name)

    if not user:
      self.redirect('/oops/invalid_user')
    else:
      user.join(group)
      group.put()
      self.redirect('/g/%s/profile' % group.name)
    
