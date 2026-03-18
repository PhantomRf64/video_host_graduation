from videohost.models import VideoItem, Like, Dislike, View, Comment, Category
from django.db.models import Count,Q






def get_similar_by_category(video):

    similar_videos = (
        VideoItem.objects
        .select_related("category")
        .prefetch_related("tags")
        .annotate(
            num_views=Count('view'),
            num_likes=Count('like')
        )
        .filter(
            Q(title__icontains=video.title) |
            Q(description__icontains=video.title) |
            Q(category=video.category) |
            Q(tags__in=video.tags.all())
        )
        .exclude(id=video.id)
        .distinct()
        .order_by('-num_views', '-num_likes')[:5]
    )

    return similar_videos
   
    
def get_popular_videos(limit=10):
    return (
        VideoItem.objects
        .select_related("category")
        .prefetch_related("tags")
        .filter(approved=True)
        .annotate(
            num_views=Count('view'),
            num_likes=Count('like')
        )
        .order_by('-num_views', '-num_likes')[:limit]
    )
    
def get_user_recommendations(user, limit=10):
    
    if not user.is_authenticated:
        
        return get_popular_videos(limit)

    
    viewed_videos_ids = (
        View.objects
        .filter(user=user)
        .values_list('video', flat=True)
        .distinct()
    )

    
    categories_ids = (
        VideoItem.objects
        .filter(id__in=viewed_videos_ids)
        .values_list('category', flat=True)
        .distinct()
    )

    
    recommended_videos = (
        VideoItem.objects
        .filter(category__in=categories_ids, approved=True)
        .exclude(id__in=viewed_videos_ids)
        .annotate(num_views=Count('view'), num_likes=Count('like'))  
        .order_by('-num_views', '-num_likes')[:limit]
    )

    return recommended_videos


def get_recommendations(user,video,limit=10):
    
    semerial = get_similar_by_category(video)
    popular = get_popular_videos(5)
    recommend_video = get_user_recommendations(user,limit=5)

    list_video = list(semerial)+list(popular)+list(recommend_video)

    unique = {}
    
    for video in list_video:
            unique[video.id] = video

    return(list(unique.values()))[:limit]
        
        

