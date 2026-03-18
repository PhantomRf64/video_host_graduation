from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    is_moderator = models.BooleanField(
        default=False,
        verbose_name="Модератор",
        help_text="Отметьте, если пользователь может проверять и одобрять видео."
    )
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def generate_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code

    def verify_otp(self, code, validity_minutes=5):
        if not self.otp_code or not self.otp_created_at:
            return False
        expired = timezone.now() > self.otp_created_at + timezone.timedelta(minutes=validity_minutes)
        if expired:
            return False
        return self.otp_code == code

    def __str__(self):
        return self.username



























