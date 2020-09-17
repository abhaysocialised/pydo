from signup.models import User
from . import utils, encutils

def authenticated(user):
  if utils.is_name(user.get("name")) and utils.is_email(user.get("email")):
    usr = User.objects.filter(name=user.get("name"), email=user.get("email"))
    if usr.exists():
      auth_key = encutils.hash_str(f"{usr[0].name}.{usr[0].email}.{usr[0].password}")
      if auth_key == user.get("auth_key", ""):
        user["auth_key"] = ""
        return True
  return False