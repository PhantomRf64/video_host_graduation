from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0, help_text="Порядок отображения категорий")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20,unique=True,db_index=True)
    slug = models.SlugField(max_length=20,unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "tag"
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class VideoItem(models.Model):
    title = models.CharField(max_length=200,db_index=True)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='videos/')
    preview = models.ImageField(upload_to='previews/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False, verbose_name="Одобрено модератором")
    tags = models.ManyToManyField(Tag,blank=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

   
    @property
    def likes_count(self):
        return self.like_set.count()

    @property
    def dislikes_count(self):
        return self.dislike_set.count()

    @property
    def views_count(self):
        return self.view_set.count()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    video = models.ForeignKey(VideoItem, on_delete=models.CASCADE, verbose_name="Видео")

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} лайкнул {self.video.title}"


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    video = models.ForeignKey(VideoItem, on_delete=models.CASCADE, verbose_name="Видео")

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} не лайкнул {self.video.title}"


class View(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    video = models.ForeignKey(VideoItem, on_delete=models.CASCADE, verbose_name="Видео")
    session = models.CharField(max_length=40, null=True, blank=True, verbose_name="Сессия анонимного пользователя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата просмотра")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video', 'user'], condition=models.Q(user__isnull=False), name='unique_view_user'),
            models.UniqueConstraint(fields=['video', 'session'], condition=models.Q(user__isnull=True), name='unique_view_session'),
        ]

    def __str__(self):
        return f"{self.user or self.session} посмотрел {self.video.title}"


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор комментария")
    video = models.ForeignKey(VideoItem, on_delete=models.CASCADE, related_name='comments', verbose_name="Видео")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.author.username} к {self.video.title}"