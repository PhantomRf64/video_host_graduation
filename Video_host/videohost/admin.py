

from django.contrib import admin
from .models import VideoItem


@admin.register(VideoItem)
class VideoItemAdmin(admin.ModelAdmin):
    exclude = ('likes', 'dislikes', 'views')