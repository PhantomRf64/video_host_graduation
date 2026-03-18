
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import VideoItem, Like, Dislike, View, Comment, Category,Tag
from django.db.models import Count,Q
from .Services.recommendations import get_recommendations,get_popular_videos
from django.utils.text import slugify
from django.contrib import messages
from .forms import CreateVideo_Form

def main_page(request):
    query = request.GET.get('q')
    if query:
       videos = VideoItem.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        , approved=True).distinct()
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
    user = request.user

    
    if request.method == "POST":
        if request.user != video.author:
            return HttpResponseForbidden()

        tags_str = request.POST.get('tags', '')
        tags_list = [t.strip() for t in tags_str.split(',') if t.strip()]

        for tag_name in tags_list:
            tag, _ = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            video.tags.add(tag)

    
    user_reaction = None
    if request.user.is_authenticated:
        if Like.objects.filter(user=request.user, video=video).exists():
            user_reaction = 'like'
        elif Dislike.objects.filter(user=request.user, video=video).exists():
            user_reaction = 'dislike'

    recommendations_video = get_recommendations(user, video, limit=10)
    popular_videos = get_popular_videos(limit=5)

    history_videos = []
    if user.is_authenticated:
        history_videos = VideoItem.objects.filter(view__user=user).exclude(id=video.id).distinct().order_by('-view__created_at')[:3]

    
    if not recommendations_video:
        recommendations_video = popular_videos

    context = {
        'video': video,
        'user_reaction': user_reaction,
        'recommendations_video': recommendations_video,
        'popular_videos': popular_videos,
        'history_videos': history_videos,
        'current_video': video,  
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

            tags_str = form.cleaned_data['tags']
            tags_list = [t.strip() for t in tags_str.split(',') if t.strip()]

            for tag_name in tags_list:
                tag, _ = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': tag_name.lower()}
                )
                video.tags.add(tag)
            return redirect('video_detail', video_id=video.id)
    else:
        form = CreateVideo_Form()
    return render(request, 'videohost/upload_video.html', {'form': form})


def user_channel(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    tab = request.GET.get('tab', 'my_channel')
    videos = VideoItem.objects.none()

    if tab == 'my_channel':
        videos = VideoItem.objects.filter(author=user, approved=True).order_by('-created_at')
    elif tab == 'history' and request.user == user:
        videos = VideoItem.objects.filter(view__user=user).distinct().order_by('-view__created_at')
    elif tab == 'moderation' and request.user.is_moderator:
        videos = VideoItem.objects.filter(approved=False).order_by('-created_at')
    else:
        tab = 'my_channel'
        videos = VideoItem.objects.filter(author=user, approved=True).order_by('-created_at')

    context = {
        'channel_user': user,
        'videos': videos,
        'active_tab': tab
    }
    return render(request, 'videohost/user_channel.html', context)


@login_required
def edit_video(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)

    if request.user != video.author and not request.user.is_staff:
        return HttpResponseForbidden("Вы не можете редактировать это видео.")

    if request.method == "POST":
        form = CreateVideo_Form(request.POST, request.FILES, instance=video)
        if form.is_valid():
            video = form.save()
            tags_str = form.cleaned_data.get('tags', '')
            video.tags.clear()
            for tag_name in [t.strip() for t in tags_str.split(',') if t.strip()]:
                tag, _ = Tag.objects.get_or_create(name=tag_name, defaults={'slug': slugify(tag_name)})
                video.tags.add(tag)
            messages.success(request, "Видео успешно обновлено!")
            return redirect('video_detail', video_id=video.id)
    else:
        initial_tags = ', '.join(video.tags.values_list('name', flat=True))
        form = CreateVideo_Form(instance=video, initial={'tags': initial_tags})

    return render(request, 'videohost/edit_video.html', {'form': form, 'video': video})


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)

    if request.user != video.author and not request.user.is_staff:
        return HttpResponseForbidden("Вы не можете удалить это видео.")

    if request.method == "POST":
        video.delete()
        messages.success(request, "Видео успешно удалено!")
        return redirect('user_channel', username=request.user.username)

    return render(request, 'videohost/confirm_delete.html', {'video': video})

@login_required
def approve_video(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)
    if not request.user.is_moderator:
        return HttpResponseForbidden("Только модератор может одобрять видео.")
    if request.method == "POST":
        video.approved = True
        video.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def reject_video(request, video_id):
    video = get_object_or_404(VideoItem, id=video_id)
    if not request.user.is_moderator:
        return HttpResponseForbidden("Только модератор может отклонять видео.")
    if request.method == "POST":
        video.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))