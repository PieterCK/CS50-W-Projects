from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import POSTS,COMMENT_SECTION,User , FOLLOWERS
from django.forms import modelform_factory, Textarea
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

def index(request):

    # Perliminary data
    user = request.user
    post_form = modelform_factory(POSTS, fields=("content",), widgets={"content":Textarea}, labels={"content":""})
    all_post = POSTS.objects.all()
    paginate_post = Paginator(all_post, 5)
    
    CONTEXT={
        "posts": all_post,
        "post_form": post_form,
        "user_inf": None
    }
    if user.is_authenticated:
        user_inf = User.objects.get(id=user.id)
        CONTEXT["user_inf"] = user_inf

## DELETE request handler
    if request.method == "DELETE":
        interacted_post = POSTS.objects.get(id = request.body)
        interacted_post.delete()
        return JsonResponse({"action":"deleted"})
        
## PUT request handler
    if request.method == "PUT":
        interacted_post = POSTS.objects.get(id = request.body)
        likers_list = interacted_post.like.all()

        # Redirect to login page if not signed in
        if not user.is_authenticated:

            return JsonResponse({"action":"login"})

        # Modify model & update button
        if user_inf in likers_list:
            interacted_post.like.remove(user_inf)
            like_status = "unlike"
        else:
            interacted_post.like.add(user_inf)
            like_status = "like"
        interacted_post.save()
        return JsonResponse({"action":like_status})

## GET request handler
    if request.method == "GET":
        return render(request, "network/index.html", CONTEXT)



## POST request handler
    f = post_form(request.POST)

    # Form error handler
    if not f.is_valid():
        CONTEXT["new_post"]: f
        return render(request, "network/index.html", CONTEXT)

    # Save to data base & refresh
    new_post = f.save(commit=False)
    new_post.user = User.objects.get(id=user.id)
    new_post.save()
    f.save_m2m()
    print(new_post)
    return HttpResponseRedirect(reverse('index'))

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
