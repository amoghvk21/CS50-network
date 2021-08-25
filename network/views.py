from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from datetime import datetime


def index(request):
    if request.method == "POST":
        p = Post(user=request.user, content=request.POST["new-post-form-content"], time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), likes=0)
        p.save()

    return render(request, "network/index.html", {
        "posts": Post.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, profileid):

    if request.method == "POST":
        if request.POST["button"] == "follow":
            f = Follower(follower=User.objects.get(id=profileid), following=User.objects.get(id=request.user.id))
            f.save()
        else:
            Follower.objects.get(follower=profileid, following=request.user.id).delete()

    followers_ = Follower.objects.filter(follower=profileid)
    following_ = Follower.objects.filter(following=profileid)
    followers = 0
    following = 0

    for _ in followers_:
        followers += 1

    for _ in following_:
        following += 1

    if request.user.id == profileid:
        isSameUser = True
    else:
        isSameUser = False

    try:
        Follower.objects.get(follower=profileid, following=request.user.id)
        isFollowing = True
    except:
        isFollowing = False

    return render(request, "network/profile.html", {
        "profile": User.objects.get(id=profileid),
        "posts": Post.objects.filter(user=profileid), 
        "followers": followers,
        "following": following,
        "isSameUser": isSameUser,
        "isFollowing": isFollowing
    })