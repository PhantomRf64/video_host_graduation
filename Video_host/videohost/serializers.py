from rest_framework import serializers
from .models import VideoItem



class SubmetInfoSerializer(serializers.ModelSerializer):
    count_likes = serializers.SerializerMethodField()
    count_dislikes = serializers.SerializerMethodField()
    count_views = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()  

    class Meta:
        model = VideoItem
        fields = ['id', 'title', 'count_likes', 'count_dislikes', 'count_views', 'status']

    def get_count_likes(self, obj):
        return obj.likes.count()

    def get_count_dislikes(self, obj):
        return obj.dislikes.count()

    def get_count_views(self, obj):
        return obj.views.count()

    def get_status(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user in obj.likes.all()