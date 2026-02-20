from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VideoItem, Like, Dislike, View, Comment
from .forms import CreateVideo_Form
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import SubmetInfoSerializer
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import render, redirect, get_object_or_404
from .models import VideoItem
from .forms import CreateVideo_Form  
from django.contrib.auth.decorators import login_required

def main_page(request):
    videos = VideoItem.objects.all().order_by('-created_at')
    return render(request, "videohost/index.html", {"list_video": videos})

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
    video = get_object_or_404(VideoItem, pk=pk)
    user = request.user

    if user.is_authenticated:
        View.objects.get_or_create(user=user, video=video)

    
    list_video = VideoItem.objects.all().order_by('-created_at')

    return render(request, "videohost/video_detail.html", {
        "video": video,
        "list_video": list_video
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_reaction(request, pk):
    
    
    video = get_object_or_404(VideoItem, pk=pk)
    user = request.user
    action = request.data.get("action")

    if action == "like":
        
        Dislike.objects.filter(user=user, video=video).delete()
        
        like, created = Like.objects.get_or_create(user=user, video=video)
        if not created:
            like.delete()

    elif action == "dislike":
        
        
        Like.objects.filter(user=user, video=video).delete()
        
        dislike, created = Dislike.objects.get_or_create(user=user, video=video)
        if not created:
            dislike.delete()
    else:
        return Response({"status": False, "error": "Invalid action"}, status=400)
    
    video.refresh_from_db()

    serializer = SubmetInfoSerializer(video, context={"request": request})
    return Response(serializer.data)


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
@permission_classes([IsAuthenticated])
def api_views(request, pk):
    
    video = get_object_or_404(VideoItem, pk=pk)

    
    percent = request.data.get("watched_percent")
    if percent is None:
        return Response({"error": "percent required"}, status=400)

    
    if float(percent) >= 35:
        View.objects.get_or_create(user=request.user, video=video)

    
    return Response({"views": video.views.count()})










                           







