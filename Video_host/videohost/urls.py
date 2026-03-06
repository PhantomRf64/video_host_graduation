from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from videohost import views as videohost_views

urlpatterns = [
    
    

    
    path('', videohost_views.main_page, name='main'),

    
    path('upload/', videohost_views.upload_video, name='upload_video'),

    
    path('video/<int:video_id>/', videohost_views.video_detail, name='video_detail'),

    
    path('api/video/<int:video_id>/reaction/', videohost_views.api_reaction, name='api_reaction'),
    path('api/video/<int:video_id>/views/', videohost_views.api_views, name='api_views'),
    path('api/video/<int:video_id>/comments/', videohost_views.api_comments, name='api_comments'),

    
    path('channel/<str:username>/', videohost_views.user_channel, name='user_channel'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)