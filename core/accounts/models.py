from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)

class UserManger(BaseUserManager):
    """ user manager class"""

    def create_user(self,email,password=None,**kwargs):
        user=self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """custom user model"""
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManger()

    USERNAME_FIELD='email'