from functools import wraps
from django.shortcuts import redirect, HttpResponse
from django.contrib import messages


def super_admin_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    if request.user.is_authenticated:
      profile = request.user

      if profile.is_superuser == True :
          return function(request, *args, **kwargs)
      else:
        messages.error(request,"Only For Admin and Superuser !")
        return redirect('app_common:login')
        
    else:
      #if not login
      messages.error(request,"Login Required !")
      return redirect('app_common:login')
  return wrap

def admin_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    if request.user.is_authenticated:
      profile = request.user

      if profile.is_superuser == True or (profile.is_org_admin==True and profile.is_active == True and profile.org.is_active==True):
          return function(request, *args, **kwargs)
      else:
        messages.error(request,"Only For Admin and Superuser !")
        return redirect('app_common:login')
        
    else:
      #if not login
      messages.error(request,"Login Required !")
      return redirect('app_common:login')
  return wrap

def org_admin_only(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
    if request.user.is_authenticated:
      profile = request.user

      if profile.is_superuser == True or (profile.is_org_admin == True and profile.is_active == True and profile.org.is_active==True):

          return function(request, *args, **kwargs)
      else:
        messages.error(request,"1. Access Denied or 2. Organization is inactive !")
        return redirect('app_common:login')
        
    else:
      #if not login
      messages.error(request,"Login Required !")
      return redirect('app_common:login')
  return wrap

'''
for login only
'''
def login_required(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):

    if request.user.is_superuser or (request.user.is_authenticated and request.user.is_active==True and request.user.org.is_active == True):
      return function(request, *args, **kwargs)
    else:
      messages.error(request,"You are not login !")
      return redirect('app_common:login')
  return wrap

# '''
# for permission only
# '''

# def has_permission(permission_name):
#   def _method_wrapper(function):
#     def _arguments_wrapper(request, *args, **kwargs):
#       if permission_name not in access_list :
#         return HttpResponse('Enter An valid access name.')
#       user=request.user
#       if user.is_superuser or user.is_org_admin or permission_name in user.access:
#         return function(request, *args, **kwargs)
#       else:
#         return HttpResponse('Permission denied!!' )
#     return _arguments_wrapper
#   return _method_wrapper