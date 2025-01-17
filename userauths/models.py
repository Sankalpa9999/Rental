from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30,unique=True)
   
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.username