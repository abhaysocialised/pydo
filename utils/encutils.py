import hashlib

def salt_string(string):
  return string.replace("", "a").replace("m", '7')

def hash_str(string):
  return hashlib.sha256(salt_string(string).encode()).hexdigest()