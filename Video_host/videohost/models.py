from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class VideoItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)

    preview = models.ImageField(
    upload_to='previews/',
    blank=True,
    null=True,
    default='previews/default.png'
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_videos',
        blank=True,
        verbose_name='Пользователи, поставившие лайк'
    )

    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='disliked_videos',
        blank=True,
        verbose_name='Пользователи, поставившие дизлайк'
    )

    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='viewed_videos',
        blank=True,
        verbose_name='Пользователи, просмотревшие видео'
    )

    def __str__(self):
        return self.title
    
    def likes_count(self):
        return self.likes.count()

    likes_count.short_description = 'Лайков'

    def dislikes_count(self):
        return self.dislikes.count()

    dislikes_count.short_description = 'Дизлайков'
