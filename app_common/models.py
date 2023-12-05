from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from .manager import MyAccountManager
from helpers import utils


class TempUser(models.Model):
    # if the user sign up but not complted the verification
    # after user verification the data of this table will go to User Table

    email = models.EmailField(null=True,blank=True,unique=True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(null=True,blank=True,unique=True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    wallet = models.FloatField(default=0.0)

    # we are storing some extra data in the meta data field
    meta_data = models.JSONField(default= dict)

    USERNAME_FIELD = "email"	
    REQUIRED_FIELDS = ["password"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    

class Wallet_Trasnsaction_History(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    user_pk = models.CharField(null = True, blank= True, max_length= 255)
    history = models.JSONField(default= dict)

    def save(self, *args, **kwargs):
        if not self.user_pk:
            self.user_pk = self.user.id
        super().save(*args, **kwargs)
