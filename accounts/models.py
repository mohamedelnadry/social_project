from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField( max_length=50)
    email = models.CharField(max_length=254,unique=True)
    password = models.CharField(max_length=255)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class UserToken(models.Model):
    user = models.OneToOneField(User,related_name="token_user", on_delete=models.CASCADE)

    token = models.CharField(max_length=255)