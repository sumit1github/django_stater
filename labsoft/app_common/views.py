from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.contrib.auth.models import auth
from django.conf import settings
#import requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.http import JsonResponse

from helpers import utils
from . import models

app = "app_common/"

class Login(View):
    

    def get(self, request):
        return render(request, self.template)

class Login(View):
    model=models.User
    template = app + "authentication/login.html"

    def get(self,request):
        return render(request,self.template)
    
    def post(self,request):
        data=request.POST

        # get_recaptcha = request.POST.get("g-recaptcha-response")
        # if not get_recaptcha:
        #     messages.error(request, 'Google Captcha Error')
        #     return redirect('app_common:login')

            
        user=auth.authenticate(username=data['email'], password=data['password'])

        if user is not None:
            
            auth.login(request,user) 
            if user.is_superuser == False:
                if user.org.is_active == False:
                    messages.error(request, 'Your Organization is Inactive. Please contact Admin.')
                    return redirect('app_common:login')

            if user.is_superuser == True:
                return redirect('admin_dashboard:admin_dashboard') 



        else: # for form validation error
            messages.error(request, "Login Failed")

        return redirect('app_common:login')