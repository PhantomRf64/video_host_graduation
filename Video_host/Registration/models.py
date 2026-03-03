from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_moderator = models.BooleanField(
        default=False,
        verbose_name="Модератор",
        help_text="Отметьте, если пользователь может проверять и одобрять видео."
    )

    def __str__(self):
        return self.username



























