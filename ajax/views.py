from django.shortcuts import redirect
from django.http import JsonResponse
from signup.models import Todo, User
from utils import authutils, encutils, utils
from uuid import uuid1

def get_all_todo(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      
      if authutils.authenticated(user):
        output = {}
        todos = Todo.objects.filter(user__email=user.get("email", ""))
        for todo in todos :
          output[todo.uid] = {
            "todo": todo.todo,
            "is_done": todo.is_done
          }
        return JsonResponse(output)
  return JsonResponse({"me":"Please, don't try to exploite our website"})

def create_todo(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      if authutils.authenticated(user):
        output = {"todo":request.POST.get("todo",'').lower()}
        if output.get("todo", "") != "":
          if not Todo.objects.filter(user__email=user.get("email", ''), todo=output.get("todo","")).exists():
            todo = Todo.objects.create(user = User.objects.get(email=user.get("email", "")), todo=output.get("todo", ''), uid=uuid1().hex)
            output["created"] = True
            output["id"] = todo.uid
          else :
            output["created"] = False
            output["error"] = "ToDo already exists!"
        else :
          output["created"] = False
          output["error"] = "Empty ToDo not expected from You"
        return JsonResponse(output)
  return JsonResponse({"me":"Please, don't try to exploite our website"})

def delete_todo(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      if authutils.authenticated(user):
        output = {"uuid":request.POST.get("id",'').lower()}
        if output.get("uuid", "") != "":
          if Todo.objects.filter(user__email=user.get("email", ''), uid=output.get("uuid","")).exists():
            todo = Todo.objects.get(user__email=user.get("email", ""), uid=output.get("uuid", "")).delete()
            output["deleted"] = True
          else :
            output["error"] = "Todo never existed..."
            output["deleted"] = False
        else :
          output["error"] = "Don't try to exploite out website (-_-)"
          output["deleted"] = False
        return JsonResponse(output)
  return JsonResponse({"me":"Please, don't try to exploite our website"})

def update_todo(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      if authutils.authenticated(user):
        output = {"uuid":request.POST.get("id",'').lower(), "is_done":request.POST.get("is_done", "")}
        
        if output.get("uuid", "") != "":
          if Todo.objects.filter(user__email=user.get("email", ''), uid=output.get("uuid","")).exists():
            todo = Todo.objects.get(user__email=user.get("email", ""), uid=output.get("uuid", ""))
            todo.is_done = output.get("is_done", "false") == "true"
            todo.save()
            output["updated"] = True
          else :
            output["updated"] = False
            output["error"] = "Todo never existed!"
        else :
          output["updated"] = False
          output["error"] = "Don't try to exploite our website (-_-)"
        return JsonResponse(output)
  return JsonResponse({"me":"Please, don't try to exploite our website"})

def update_profile(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      
      if authutils.authenticated(user):
        output = {
          "name":request.POST.get("name",'').title().strip(),
          "old-password":request.POST.get("old_password", ""),
          "new-password": request.POST.get("new_password", ""),
        }
        usr = User.objects.get(email=user.get("email", ""))
        if (output["name"] != "") and (utils.is_name(output["name"])) and (output["name"] != user.get("name", "")):
          usr.name = output["name"]
          request.session.update({"name":output["name"]})
          output["name_updated"] = True
        else :
          output["name_updated"] = False
          if (output["name"] == user.get("name", "")):
            output["nameError"] = ""
          else :
            output["nameError"] = "Please enter valid name..."
        
        if (output["old-password"] != "") and (output["new-password"] != ""):
          old_password = encutils.hash_str(output["old-password"])
          if old_password == usr.password :
            if (len(output["new-password"]) > 7):
              new_password = encutils.hash_str(output["new-password"])
              usr.password = new_password
              output["password_updated"] = True
            else :
              output["password_updated"] = False
              output["passwordError"] = "Please Provide Strong Password..."
          else :
            output["password_updated"] = False
            output["passwordError"] = "Incorrect Password..."
        else :
          output["password_updated"] = False
          output["passwordError"] = ""
        usr.save()
        request.session.update({"auth_key" : encutils.hash_str(f"{usr.name}.{usr.email}.{usr.password}")})
        request.session.save()
        
        del output["old-password"], output["new-password"]
        return JsonResponse(output)
  return JsonResponse({"me": "Please, don't try to exploite our website"})


def delete_account(request):
  if not request.session.is_empty() :
    if request.session.has_key("name") and request.session.has_key("email") and request.session.has_key("auth_key"):
      user = {
        "name": request.session['name'],
        "email": request.session['email'],
        'auth_key': request.session['auth_key']
      }
      
      if authutils.authenticated(user):
        output = {"password":request.POST.get("password")}
        if(output["password"] != "") or (len(output["password"]) > 7):
          password = encutils.hash_str(output["password"])
          usr = User.objects.get(email=user.get("email",""), name=user.get("name", ""))
          if usr.password == password:
            usr.delete()
            output["deleted"] = True
          else :
            output["deleted"] = False
            output["error"] = "Incorrect password..."
        else :
          output["deleted"] = False
          output["error"] = "Please provide valid password..."
        return JsonResponse(output)
  return JsonResponse({"error":"We are under attack..."})