from django.contrib import admin
from django.urls import path, include
from signup.views import signup
from login.views import login, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", signup),
    path("log-in/", login),
    path("logout/", logout),
    path("ajax/", include("ajax.urls")),
    path("home/", include("home.urls")),
    path("profile/", include("userprofile.urls")),
]


# static files conf

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)