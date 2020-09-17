from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
  list_display = ("ID", "name", "email", "verified")
admin.site.register(models.User, UserAdmin)


class TodoAdmin(admin.ModelAdmin):
  list_display = ("ID", "user", "todo", "uid", "is_done")
admin.site.register(models.Todo, TodoAdmin)