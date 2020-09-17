import re

def is_name(name):
  return len(name) > 1

def is_email(email):
  return re.match("([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)", email) != None

def is_strong_password(password):
  return len(password) > 7