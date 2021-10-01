from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import RemoteUserBackend
from django.db import IntegrityError
from django.db.models.query import EmptyQuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators import csrf
from .models import *
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from itertools import chain


def index(request):

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    likedPosts = []
    for post in Post.objects.filter(likedUsers = request.user.id):
        likedPosts.append(post.id)

    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
        "likedPosts": likedPosts
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

    if request.method == 'POST':
        if request.POST['follow'] == 'null':
            p = Post.objects.get(user=request.user, content=request.POST['old-post-content'], time=request.POST['old-post-time'])
            p.content = request.POST['new-post-content']
            p.save()
        else:
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

    likedPosts = []
    for post in Post.objects.filter(likedUsers = request.user.id):
        likedPosts.append(post.id)

    return render(request, "network/profile.html", {
        "profile": User.objects.get(id=profileid),
        "posts": Post.objects.filter(user=profileid), 
        "followers": followers,
        "following": following,
        "isSameUser": isSameUser,
        "isFollowing": isFollowing,
        "likedPosts": likedPosts
    })


@login_required
def following(request):

    following = Follower.objects.filter(following=request.user.id)
    temp = []

    for person in following:
        temp.append(Post.objects.filter(user=person.follower))

    try:
        if len(temp) > 1:
            for x in range(1, len(temp)-1):
                posts = temp[x] | temp[x+1]
        else:
            posts = temp[0]
    except IndexError:
        return HttpResponse("Not following anyone")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    likedPosts = []
    for post in Post.objects.filter(likedUsers = request.user.id):
        likedPosts.append(post.id)

    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj,
        "likedPosts": likedPosts
    })


@login_required
@csrf_exempt
def edit(request):

    # Get the data
    data = json.loads(request.body)
    postid = data.get("postid", "")
    content = data.get("content", "")

    p = Post.objects.get(id=postid)
    p.content = content
    p.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p.save()

    return JsonResponse({"message": "Post editied successfully"}, status=201)


@csrf_exempt
@login_required
def like(request):

    # Get the data
    data = json.loads(request.body)
    postid = data.get("postid", "")
    userid = data.get("userid", "")

    p = Post.objects.get(id=postid)
    p.likes += 1
    p.save()   
    p.likedUsers.add(User.objects.get(id=userid))

    return JsonResponse({"message": "Liked"}, status=201)


@csrf_exempt
@login_required
def unlike(request):

    # Get the data
    data = json.loads(request.body)
    postid = data.get("postid", "")
    userid = data.get("userid", "")

    p = Post.objects.get(id=postid)
    p.likes -= 1
    p.save()   
    p.likedUsers.remove(User.objects.get(id=userid))

    return JsonResponse({"message": "Unliked"}, status=201)