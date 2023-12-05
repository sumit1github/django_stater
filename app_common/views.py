from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.models import auth
from django.conf import settings
#import requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.http import JsonResponse


from . import forms
from helpers import utils
from . import models

app = "app_common/"


class Register(View):
    model = models.User
    template = app + "authentication/register.html"
    form_class = forms.RegisterForm

    def get(self,request):
        initial_data = {'invitation_code':request.GET.get('ref_id', None)}
        context = {
            'form': self.form_class(initial= initial_data)
        }

        return render(request, self.template, context)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account is created successfully')
            return redirect('app_common:register')
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

            return redirect('app_common:register')


class Login(View):
    model=models.User
    template = app + "authentication/login.html"
    form_class = forms.LoginForm

    def get(self,request):
        context = {
            "form": self.form_class
        }
        return render(request, self.template, context)
    
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
    
class Home(View):
    template = app + 'index.html'

    def get(self, request):
        
        return render(
            request,
            self.template
        )