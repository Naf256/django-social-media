import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow


@csrf_exempt
def edit(request, id):
    if request.method == 'GET':
        return HttpResponse('should be a put request')

    data = json.loads(request.body)
    content = data.get("content", "")

    post = Post.objects.get(pk=id)
    post.content = content
    post.save()
    return HttpResponse('successful')


@csrf_exempt
def follow(request, id):
    profile = User.objects.get(pk=id)

    profile_owner = Follow.objects.get(user=profile)
    user = Follow.objects.get(user=request.user)

    is_following = Follow.objects.filter(user=profile, followers=request.user)

    if is_following:
        profile_owner.followers.remove(request.user)
        profile_owner.save()
        user.following.remove(profile)
        user.save()
        return HttpResponse('unfollowing the profile')

    profile_owner.followers.add(request.user)
    profile_owner.save()
    user.following.add(profile)
    user.save()
    return HttpResponse('following the profile')


@csrf_exempt
def profile(request, id, page_num=1):
    user = User.objects.get(pk=id)

    follow = Follow.objects.get(user=user)

    following = follow.following.all().count()
    followers = follow.followers.all().count()

    posts = Post.objects.filter(creator=user)
    liked_posts = Post.objects.filter(likes=user, creator=user)

    already_follow = Follow.objects.filter(user=request.user, following=user)

    show_follow = 1

    if already_follow:
        show_follow = 0

    p = Paginator(posts, 10)
    posts = p.page(page_num)

    return render(request, "network/profile.html", {
        "following": following,
        "followers": followers,
        "posts": posts.object_list,
        "liked_posts": liked_posts,
        "owner": user,
        "show_follow": show_follow,
        "page_range": p.page_range,
        "previous_page_number": posts.previous_page_number() if posts.has_previous() else 0,
        "next_page_number": posts.next_page_number() if posts.has_next() else 0,
        "previous": posts.has_previous(),
        "next": posts.has_next(),
    })


@csrf_exempt
def following(request, page_num=1):
    user = request.user
    follow = Follow.objects.get(user=user)

    followings = follow.following.all()

    liked_posts = []

    posts = Post.objects.none()

    for u in followings:
        posts = posts | Post.objects.filter(creator=u)

    liked = Post.objects.filter(likes=request.user)

    for post in posts:
        if post in liked:
            liked_posts.append(post)

    p = Paginator(posts, 10)
    posts = p.page(page_num)

    return render(request, "network/following.html", {
        "posts": posts.object_list,
        "liked_posts": liked_posts,
        "page_range": p.page_range,
        "previous_page_number": posts.previous_page_number() if posts.has_previous() else 0,
        "next_page_number": posts.next_page_number() if posts.has_next() else 0,
        "previous": posts.has_previous(),
        "next": posts.has_next(),
    })


@csrf_exempt
def like(request, id):
    post = Post.objects.get(pk=id)

    if post.likes.filter(username=request.user.username).exists():
        post.like = post.like - 1
        post.likes.remove(request.user)
        post.save()
    else:
        post.like = post.like + 1
        post.likes.add(request.user)
        post.save()

    return HttpResponse('successfully liked/unliked the post')


def index(request, page_num=1):
    if request.user.is_authenticated:
        objects = Post.objects.all()
        p = Paginator(objects, 10)
        posts = p.page(page_num)
        liked_posts = Post.objects.filter(likes=request.user)

        return render(request, "network/index.html", {
            "posts": posts.object_list,
            "liked_posts": liked_posts,
            "page_range": p.page_range,
            "previous_page_number": posts.previous_page_number() if posts.has_previous() else 0,
            "next_page_number": posts.next_page_number() if posts.has_next() else 0,
            "previous": posts.has_previous(),
            "next": posts.has_next(),
        })
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def post(request):
    content = request.POST["content"]

    post = Post(content=content, creator=request.user)
    post.save()

    return HttpResponseRedirect(reverse("index"))


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
