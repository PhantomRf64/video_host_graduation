from django.contrib import admin
from .models import VideoItem, Category, Like, Dislike, View, Comment

@admin.register(VideoItem)
class VideoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'approved', 'created_at', 'likes_count', 'dislikes_count', 'views_count')
    list_filter = ('approved', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('likes_count', 'dislikes_count', 'views_count')
    actions = ['approve_videos']

    def approve_videos(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} видео(ей) одобрено модератором.")
    approve_videos.short_description = "Одобрить выбранные видео"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    ordering = ('position',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video')

@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video')

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'session', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'video', 'text', 'created_at')