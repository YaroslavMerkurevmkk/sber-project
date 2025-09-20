from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'front/index.html', {"title": "Chats"})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("chat")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("chat")
    else:
        form = RegisterForm()
    return render(request, "front/register.html", {"title": "Register", "form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("chat")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("chat")
    else:
        form = LoginForm()
    return render(request, "front/login.html", {"title": "Login", "form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
