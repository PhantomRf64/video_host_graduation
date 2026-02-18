from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)



























