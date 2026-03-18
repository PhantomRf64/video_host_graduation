from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import Registration_Form, Login_Form  
from django.conf import settings
from videohost.models import View
from videohost.models import VideoItem, Category
from .models import MyUser
from .forms import OTPForm

def welcome(request):
    if request.user.is_authenticated:
        return redirect("wellcome") 
    categories = Category.objects.prefetch_related('videos').all()

    
    popular_videos = VideoItem.objects.order_by('-view')[:5]

    return render(request, "registration/index.html", {
        'category_videos': categories,   
        'popular_videos': popular_videos,
    })





def register(request):
    if request.user.is_authenticated:
        return redirect("main")

    if request.method == "POST":
        form = Registration_Form(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            
            session_key = request.session.session_key
            if session_key:
                View.objects.filter(session=session_key, user=None).update(user=user, session=None)

            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect("main")
        else:
            messages.error(request, "Ошибка регистрации. Проверьте данные.")
    else:
        form = Registration_Form()

    return render(request, "Registration/registr.html", {"form": form, "isLogin": False})





def sign_in(request):
    if request.user.is_authenticated:
        return redirect("main")  

    if request.method == "POST":
        form = Login_Form(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            
            request.session["pre_2fa_user"] = user.id

            
            return redirect("two_factor_auth")
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = Login_Form()

    return render(request, "Registration/registr.html", {"form": form, "isLogin": True})



def sign_out(request):
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect('wellcome')

def two_factor_auth(request):
    if not request.session.get("pre_2fa_user"):
        return redirect("login")

    user_id = request.session["pre_2fa_user"]
    user = MyUser.objects.get(id=user_id)

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            if user.verify_otp(otp):
                user.otp_code = None
                user.otp_created_at = None
                user.save()

   
                login(request, user)
                del request.session["pre_2fa_user"]
                return redirect("main")
            else:
                messages.error(request, "Неверный или просроченный код")
    else:
        form = OTPForm()

        
        if not user.otp_created_at or \
           timezone.now() > user.otp_created_at + timedelta(minutes=5):

            otp = user.generate_otp()
            print(f"OTP для теста: {otp}")

    return render(request, "registration/otp.html", {"form": form})
