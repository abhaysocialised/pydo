from django.urls import path
from . import views


urlpatterns = (
  path("create-todo/", views.create_todo),
  path("get-todos/", views.get_all_todo),
  path("delete-todo/", views.delete_todo),
  path("update-todo/", views.update_todo),
  path("update-profile/", views.update_profile),
  path("delete-account/", views.delete_account),
)