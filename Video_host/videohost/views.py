from django.shortcuts import render, redirect, get_object_or_404
from .forms import CraateVideo_Form
from .models import VideoItem
from django.http import JsonResponse
from .serializers import SubmetInfoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view



def main_page(request):
    if request.method == "POST":
        form = CraateVideo_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')  
    else:
        form = CraateVideo_Form()

    videos = VideoItem.objects.all()
    return render(request, "videohost/index.html", {
        "form": form,
        "list_video": videos
    })


def video_detail(request, pk):
    video = get_object_or_404(VideoItem, pk=pk)
    user = request.user
    if user.is_authenticated:
        if user not in video.views.all():
            video.views.add(user)

    return render(
        request,
        "videohost/video_detail.html", {
        "video": video
    })


@api_view(["GET","POST"])
def api_likes(request, pk):
    video = get_object_or_404(VideoItem, pk=pk)

    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return Response({"status" : False},status=403)
        
        action = request.data.get("action")

        if action == "like":
            video.dislikes.remove(user)
            if user in video.likes.all():
                video.likes.remove(user)
            else:
                video.likes.add(user)

        elif action == "dislike":
            video.likes.remove(user)
            if user in video.dislikes.all():
                video.dislikes.remove(user) 
            else:
                video.dislikes.add(user) 
    else:
        return Response(
                {"status": False, "error": "Invalid action"},
                status=400
            )


    serializer = SubmetInfoSerializer(video,context={"request": request })
    return Response(serializer.data)  
    
                           








    #         if user in video.likes.all():
    #             video.likes.remove(user)
    #             liked = False
    #         else:
    #             video.likes.add(user)
    #             liked = True
    #         video.save()
    #     else:
    #         return Response({"status": False, "error": "Anonymous"}, status=403)

    # serializer = SubmetInfoSerializer(video, context={'request': request})
    # return Response(serializer.data)
