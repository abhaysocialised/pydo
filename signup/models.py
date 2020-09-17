from django.db import models

class User(models.Model):
  ID = models.AutoField(primary_key=True)
  name = models.CharField(max_length=56)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)
  verified = models.BooleanField(default=False)


class Todo(models.Model):
  ID = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  todo = models.CharField(max_length=256)
  uid = models.CharField(max_length=128, unique=True)
  is_done = models.BooleanField(default=False)