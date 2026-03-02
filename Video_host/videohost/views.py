from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import VideoItem, Like, Dislike, View, Comment
from Registration.models import MyUser
from .forms import CreateVideo_Form
from .serializers import SubmetInfoSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, Prefetch , Q

def main_page(request):
    query = request.GET.get("q")   

    videos = (
        VideoItem.objects
        .select_related("author")
        .annotate(
            views_count=Count("views")
        )
    )

    
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    videos = videos.order_by("-created_at")

    return render(request, "videohost/index.html", {
        "list_video": videos,
        "query": query
    })

@login_required
def upload_video(request):
    if request.method == "POST":
        form = CreateVideo_Form(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user  
            video.save()

            return redirect('main')
    else:
        form = CreateVideo_Form()

    return render(request, "videohost/upload_video.html", {"form": form})


def video_detail(request, pk):
   
    video = get_object_or_404(
        VideoItem.objects.select_related("author").prefetch_related("comments__author"),
        pk=pk
    )

    
    video.likes_count = video.likes.count()
    video.dislikes_count = video.dislikes.count()
    video.views_count = video.views.count()

    
    list_video = VideoItem.objects.annotate(
        views_count=Count("views", distinct=True)  
    ).order_by("-created_at")

    
    user_reaction = None
    if request.user.is_authenticated:
        if video.likes.filter(user=request.user).exists():
            user_reaction = "like"
        elif video.dislikes.filter(user=request.user).exists():
            user_reaction = "dislike"

    return render(request, "videohost/video_detail.html", {
        "video": video,
        "list_video": list_video,
        "user_reaction": user_reaction
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_reaction(request, pk):
    video = get_object_or_404(VideoItem, pk=pk)
    user = request.user
    action = request.data.get("action")

    if action not in ["like", "dislike"]:
        return Response({"status": False, "error": "Invalid action"}, status=400)

    
    from django.db import transaction
    with transaction.atomic():
        if action == "like":
            Dislike.objects.filter(user=user, video=video).delete()
            like, created = Like.objects.get_or_create(user=user, video=video)
            if not created:
                like.delete()
        else:
            Like.objects.filter(user=user, video=video).delete()
            dislike, created = Dislike.objects.get_or_create(user=user, video=video)
            if not created:
                dislike.delete()

    count_likes = Like.objects.filter(video=video).count()
    count_dislikes = Dislike.objects.filter(video=video).count()
    count_views = View.objects.filter(video=video).count()

    return Response({
        "count_likes": count_likes,
        "count_dislikes": count_dislikes,
        "count_views": count_views
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_comments(request, pk):
    
    video = get_object_or_404(VideoItem, pk=pk)
    text = request.data.get("text")
    

    if not text:
        return Response({"status": False, "error": "Empty comment"}, status=400)

    comment = Comment.objects.create(author=request.user, video=video, text=text)

    return Response({
        "status": True,
        "author": comment.author.username,
        "text": comment.text,
        "created_at": comment.created_at.strftime("%d %b %Y %H:%M")
    })


@api_view(["POST"])
def api_views(request, pk):
    video = get_object_or_404(VideoItem, pk=pk)
    percent = request.data.get("watched_percent")

    if percent is None or float(percent) < 35:
        views_count = View.objects.filter(video=video).count()
        return Response({"views": views_count})

    if request.user.is_authenticated:
       
        View.objects.get_or_create(video=video, user=request.user, session=None)
    else:
        
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        View.objects.get_or_create(video=video, user=None, session=session_key)

    views_count = View.objects.filter(video=video).count()
    return Response({"views": views_count})


def user_channel(request, username):
    user = get_object_or_404(MyUser, username=username)

    videos = (
        VideoItem.objects
        .filter(author=user)
        .annotate(
            views_count=Count("views"),
            likes_count=Count("likes"),
        )
        .order_by("-created_at")
    )

    return render(request, "videohost/channel.html", {
        "channel_user": user,
        "videos": videos
    })









                           







