from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from . import forms, models

def welcome(request): 
    if request.method == "POST":
        logout(request)
    elif request.user.is_authenticated:
        return redirect("main")
    return render(request, "Registration/index.html")

def register(request):
    if request.method == "POST":
        f = forms.Registration_Form(data=request.POST)
        if f.is_valid():
            user = f.save()
            login(request, user)
            return redirect("main")
            
    form = forms.Registration_Form()
    return render(request, "Registration/registr.html", {"form" : form , "isLogin":False})
    

def sign_in(request):
    if request.method == "POST":
        f = forms.Login_Form(data=request.POST)
        if f.is_valid():
            username = f.cleaned_data["username"]
            password = f.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main")

    form = forms.Login_Form()
    return render(request, "Registration/registr.html", {"form":form, "isLogin":True})

