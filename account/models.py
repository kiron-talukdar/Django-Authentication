from django.db import models
from  django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator #validator use to remove "space"
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=50, validators=[UnicodeUsernameValidator], unique= True)
    email=models.EmailField(max_length=50, unique=True)
    #here we don't need to define password , because we Inherite AbstructBaseUser
    is_staff= models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    date_joined= models.DateTimeField(auto_now_add=True)
    objects=UserManager()  #we creating custom model for that we need custom manager

    # we created custom model so we difine this below 2 field
    USERNAME_FIELD='username'
    REQUIRED_FIELDS= ['email',]

    class Meta:
        ordering=['-date_joined']