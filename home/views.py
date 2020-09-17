from django.shortcuts import render, redirect
from utils import authutils

def home(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      if authutils.authenticated(user):
        return render(request, "home.html", user)
  return redirect("/logout")