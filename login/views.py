from django.shortcuts import render, redirect
from signup.models import User
from utils import utils, encutils


def login(request):
  if not request.session.is_empty():
    return redirect("/home")
  if request.method == "POST":
    user = {"usr": request.POST}
    if utils.is_email(user["usr"].get("email", '')):
      password = encutils.hash_str(user["usr"].get("password", ''))
      usr = User.objects.filter(email=user["usr"].get("email", ''), password=password)
      if usr.exists() :
        request.session["name"] = usr[0].name
        request.session["email"] = usr[0].email
        request.session["auth_key"] = encutils.hash_str(f"{usr[0].name}.{usr[0].email}.{password}")
        
        return redirect("/home")
      else :
        user["Error"] = "Email-id and password don't match"
    else :
      user["emailError"] = "Please enter valid email-id"
    return render(request, "login.html", user)
  return render(request, "login.html")


def logout(request):
  request.session.flush()
  return redirect("/log-in")