from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# class VideoItem(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     video_file = models.FileField(upload_to='videos/', blank=True, null=True)

#     preview = models.ImageField(
#     upload_to='previews/',
#     blank=True,
#     null=True,
#     default='previews/default.png'
#     )

#     likes = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='liked_videos',
#         blank=True,
#         verbose_name='Пользователи, поставившие лайк'
#     )

#     dislikes = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='disliked_videos',
#         blank=True,
#         verbose_name='Пользователи, поставившие дизлайк'
#     )

#     views = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='viewed_videos',
#         blank=True,
#         verbose_name='Пользователи, просмотревшие видео'
#     )

#     def __str__(self):
#         return self.title
    
#     def likes_count(self):
#         return self.likes.count()

#     likes_count.short_description = 'Лайков'

#     def dislikes_count(self):
#         return self.dislikes.count()

#     dislikes_count.short_description = 'Дизлайков'



class VideoItem(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название видео"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание видео"
    )
    video = models.FileField(
        upload_to='videos/',
        verbose_name="Видео файл"
    )
    preview = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name="Превью"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name="Автор видео"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки"
    )

    def __str__(self):
        return self.title



class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    video = models.ForeignKey(
        VideoItem,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Видео"
    )

    class Meta:
        unique_together = ('user', 'video')  

    def __str__(self):
        return f"{self.user.username} лайкнул {self.video.title}"



class Dislike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    video = models.ForeignKey(
        VideoItem,
        on_delete=models.CASCADE,
        related_name='dislikes',
        verbose_name="Видео"
    )

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} не лайкнул {self.video.title}"



class View(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    video = models.ForeignKey(
        VideoItem,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name="Видео"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата просмотра"
    )

    class Meta:
        unique_together = ('user', 'video')  

    def __str__(self):
        return f"{self.user.username} посмотрел {self.video.title}"



class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария"
    )
    video = models.ForeignKey(
        VideoItem,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Видео"
    )
    text = models.TextField(
        verbose_name="Текст комментария"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.author.username} к {self.video.title}"