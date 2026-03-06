
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import VideoItem, Like, Dislike, View, Comment, Category
from django.db.models import Count,Q

def main_page(request):
    query = request.GET.get('q')
    if query:
        videos = VideoItem.objects.filter(title__icontains=query, approved=True)
    else:
        videos = VideoItem.objects.filter(approved=True)

    popular_videos = videos.annotate(views_count_db=Count('view')).order_by('-views_count_db')[:10]
    new_videos = videos.order_by('-created_at')[:10]

    categories = Category.objects.all().order_by('position')
    category_videos = []
    for cat in categories:
        cat_videos = cat.videos.filter(approved=True)
        if query:
            cat_videos = cat_videos.filter(title__icontains=query)
        cat_videos = cat_videos.order_by('-created_at')[:10]
        category_videos.append({
            'name': cat.name,
            'videos': cat_videos
        })

    context = {
        'popular_videos': popular_videos,
        'new_videos': new_videos,
        'category_videos': category_videos,
    }
    return render(request, 'videohost/index.html', context)


def video_detail(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)

    
    user_reaction = None
    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user, video=video).exists():
            user_reaction = 'like'
        elif Dislike.objects.filter(user=request.user, video=video).exists():
            user_reaction = 'dislike'

    
    list_video = VideoItem.objects.exclude(id=video.id).filter(approved=True).order_by('-created_at')

    context = {
        'video': video,
        'user_reaction': user_reaction,
        'list_video': list_video,
    }
    return render(request, 'videohost/video_detail.html', context)


@login_required
@csrf_exempt
def api_reaction(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)
    data = json.loads(request.body)
    action = data.get("action")

    if action == "like":
        Like.objects.get_or_create(user=request.user, video=video)
        Dislike.objects.filter(user=request.user, video=video).delete()
    elif action == "dislike":
        Dislike.objects.get_or_create(user=request.user, video=video)
        Like.objects.filter(user=request.user, video=video).delete()

    return JsonResponse({
        "count_likes": video.like_set.count(),
        "count_dislikes": video.dislike_set.count(),
        "count_views": video.view_set.count(),
    })

@csrf_exempt
def api_views(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)
    session = request.session.session_key or request.session.create()

    if request.user.is_authenticated:
        View.objects.get_or_create(user=request.user, video=video)
    else:
        View.objects.get_or_create(session=session, video=video)

    return JsonResponse({"views": video.view_set.count()})


@login_required
@csrf_exempt
def api_comments(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)
    data = json.loads(request.body)
    text = data.get("text")
    if text:
        comment = Comment.objects.create(author=request.user, video=video, text=text)
        return JsonResponse({"author": comment.author.username, "text": comment.text})
    return JsonResponse({"error": "Нет текста"}, status=400)


@login_required
def upload_video(request):
    from .forms import CreateVideo_Form  
    if request.method == 'POST':
        form = CreateVideo_Form(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = CreateVideo_Form()
    return render(request, 'videohost/upload_video.html', {'form': form})


def user_channel(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    videos = VideoItem.objects.filter(author=user, approved=True).order_by('-created_at')
    return render(request, 'videohost/user_channel.html', {'channel_user': user, 'videos': videos})