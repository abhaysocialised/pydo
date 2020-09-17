from django.urls import path
from . import views


urlpatterns = (
  path("", views.update_profile),
  path("delete-profile/", views.delete_profile),
)