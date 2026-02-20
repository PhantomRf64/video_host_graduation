from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import Registration_Form, Login_Form  # формы должны быть корректны
from django.conf import settings


def welcome(request):
    if request.user.is_authenticated:
        return redirect("wellcome") 
    return render(request, "Registration/index.html")



def register(request):
    if request.user.is_authenticated:
        print (12)
        return redirect("main")

    if request.method == "POST":
        form = Registration_Form(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"]) 
            user.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            print (1)
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
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Вы вошли как {user.username}")
                next_url = request.GET.get("next")
                return redirect(next_url if next_url else "main")
            else:
                messages.error(request, "Неверный логин или пароль")
    else:
        form = Login_Form()

    return render(request, "Registration/registr.html", {"form": form, "isLogin": True})



def sign_out(request):
    logout(request)
    messages.success(request, "Вы вышли из системы")
    return redirect('wellcome')
