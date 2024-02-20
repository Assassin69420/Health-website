from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm
from shop.models import Cart

# Create your views here.


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("/")
    return render(request, "register/register.html", {"form": form})


def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("/home")

    return render(request, "login.html", context={"form": form})
