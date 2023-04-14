from django.db import models
import io
from PIL import Image
import os
import uuid
from django.core.files import File
from django.core.files.base import ContentFile

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import MyAccountManager

 
def document_path(self, filename):
    basefilename, file_extension= os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return 'media/files/{basename}{randomstring}{ext}'.format(basename= basefilename, randomstring= str(myuuid), ext= file_extension)

def generate_random_string():
    random_uuid = uuid.uuid4()
    random_string = random_uuid.hex
    return random_string

def user_logo_path(self, filename):
    basefilename, file_extension= os.path.splitext(filename)
    myuuid = uuid.uuid4()
    return 'user/logo/{basename}{randomstring}{ext}'.format(basename= basefilename, randomstring= str(myuuid), ext= file_extension)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE=(
        ('cc','Collection Center'),
        ('user','user')
    )
    
    password = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True,unique=True)

    token= models.TextField(null=True, blank=True)

    contact = models.CharField(max_length= 10, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # billing details
    billing_name = models.TextField(null=True,blank=True)
    billing_email = models.EmailField(null=True,blank=True)
    billing_contact = models.CharField(max_length=10, null=True, blank=True)
    billing_address = models.TextField(null=True,blank=True)
    logo = models.ImageField(upload_to=user_logo_path, null=True, blank=True)


    USERNAME_FIELD = "email"	
    REQUIRED_FIELDS = ["password"]

    objects = MyAccountManager()


    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name if full_name else self.email

    @property
    def full_name(self):
        return self.get_full_name()
    
    @property
    def full_contact_number(self):
        if self.contact_number:
            contact_number = '+91' + self.contact_number
        else:
            contact_number='no contact present'

        return contact_number
    
    def get_token(self, *args, **kwargs):
        token= generate_random_string()
        self.token= token
        super().save(*args, **kwargs)
        return token

    def __str__(self):
        return self.email