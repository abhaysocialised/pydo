from django.shortcuts import render, redirect
from .models import User
from utils import utils, encutils

def signup(request):
  if not request.session.is_empty():
    return redirect("/home")
  if request.method == "POST":
    user = {'usr':request.POST}
    temp = []
    if utils.is_name(user["usr"].get("name", '')) :
      temp.append(True)
    else :
      temp.append(False)
      user["nameError"] = "Please enter Your Legal name and your name should not be greater than 50 Characters."
  
    if utils.is_email(user["usr"].get("email", '')) :
      if User.objects.filter(email=user["usr"].get("email", "")).exists() :
        temp.append(False)
        user["emailError"] = f"{user['usr'].get('email', '')} is already taken."
      else :
        temp.append(True)
    else :
      temp.append(False)
      user["emailError"] = "Please enter valid Email-id."
    
    if utils.is_strong_password(user["usr"].get("password", '')) :
      temp.append(True)
    else :
      temp.append(False)
      user["passwordError"] = "Please create a password greater than or equal to 8."
    
    if all(temp):
      password = encutils.hash_str(user["usr"].get("password"))
      User.objects.create(name=user["usr"].get("name"), email=user["usr"].get("email"), password=password)
      request.session["name"] = user["usr"].get("name", "")
      request.session["email"] = user["usr"].get("email", "")
      request.session["auth_key"] = encutils.hash_str(f"{user['usr']['name']}.{user['usr']['email']}.{password}")
      
      return redirect("/home")
    return render(request, "signup.html", user)
    
  return render(request, "signup.html")