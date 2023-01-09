from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .utils import listing_form, auto_bidding_form
from .models import User, AUCTION_LISTINGS, CATALOG, BIDS
from django.forms import modelform_factory

def index(request):
    active_listings = AUCTION_LISTINGS.objects.all()
    return render(request, "auctions/index.html", {"listings": active_listings})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    categories = CATALOG.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, specified_category):
    category_id = CATALOG.objects.get(category=specified_category)
    category = AUCTION_LISTINGS.objects.filter(category=category_id.id)
    return render(request, "auctions/category.html", {"category": category})


def listing(request, list_id):
    
    # General Info
    listing = AUCTION_LISTINGS.objects.get(id=list_id)
    user = request.user

    # Recognize listing owner
    owner = User.objects.get(id = user.id)
    seller = owner.selling.values_list("id", flat=True)
    viewer_status= None
    if int(list_id) in seller:
        viewer_status = user.id
    ### TO DO: install edit listing button for owner of listing
    
    # Bidding Infos
    bidders_info = listing.past_bids.all()
    top_bid = 0
    if bidders_info:
        top_bid = max(bidders_info.values_list("amount", flat=True))

    # Watchlist mechanism
    watchlist = False
    if user.id:
        watchlist = user.watched.filter(id=listing.id)
    form_value = "Watchlist"
    if watchlist:
        form_value = "[V] Watchlist"

    # Page Context
    CONTEXT = {
        "listing": listing,
        "form_value": form_value,
        "form": auto_bidding_form(top_bid, list_id),
        "bidders_info": bidders_info,
        "error_msg": None,
        "info_msg": None,
        "viewer_status": viewer_status
    }

    # GET Request handler
    if request.method == "GET":
        return render(request, "auctions/listing.html", CONTEXT)

    # POST Request handler
    bid_form = auto_bidding_form(top_bid, list_id)
    form = bid_form(request.POST)
    if not form.is_valid():
        CONTEXT["form"] = form
        return render(request, "auctions/listing.html", CONTEXT)
    new_bid = form.cleaned_data["bid"]

    # Process new bid
    if new_bid <= top_bid:
        CONTEXT["error_msg"] = "Invalid Bid Amount, Please Try Again."
        return render(request, "auctions/listing.html", CONTEXT)
    NEW_BID = BIDS(
        bidder=User.objects.get(id=user.id),
        amount=new_bid,
        bid_item=listing
    )
    NEW_BID.save()
    return HttpResponseRedirect("listing/"+str(listing.id))


@login_required(login_url='login')
def watchlist(request):
    user = request.user
    if request.method == "GET":
        watchlist = user.watched.all()
        return render(request, "auctions/watchlist.html", {"watchlist": watchlist})
    listing_id = request.POST["listing"]
    if request.POST["status"] == "Watchlist":
        user.watched.add(listing_id)
    else:
        remove = user.watched.get(id=listing_id)
        user.watched.remove(remove)
    return HttpResponseRedirect("listing/"+str(listing_id))


@login_required(login_url='login')
def create_listing(request):
    user = request.user
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {"form": listing_form})
    form = listing_form(request.POST)
    if not form.is_valid():
        return render(request, "auctions/create_listing.html", {"form": form})
    new_listing = form.save(commit=False)
    new_listing.owner = User.objects.get(id=user.id)
    new_listing.save()
    form.save_m2m()
    NEW_LISTING = AUCTION_LISTINGS.objects.get(
        title=form.cleaned_data["title"])
    return HttpResponseRedirect("listing/"+str(NEW_LISTING.id))

@login_required(login_url='login')
def edit_listing(request, list_id):
    user = request.user

    # Redirect if not owner of listing
    owner = User.objects.get(id = user.id)
    seller = owner.selling.values_list("id", flat=True)
    if int(list_id) not in seller:
        return HttpResponseRedirect("listing/"+list_id)
    
    # Populate editing form
    listing_info = AUCTION_LISTINGS.objects.get(id = list_id)
    class editing_form (listing_form):
        class Meta(listing_form.Meta):
            exclude=('status', 'watchlist', 'owner','current_price',)
    edit_form = editing_form(instance= listing_info)
    
    # Page contexts
    CONTEXT={
        "form": edit_form,
        "info_msg": list_id,
        "error_msg": None
    }

    ## GET request
    if request.method == "GET":
        return render(request, "auctions/edit_listing.html",CONTEXT)
    
    ## POST request
    form = editing_form(request.POST, instance=listing_info)
    if not form.is_valid():
        CONTEXT["error_msg"] = form
        return render(request, "auctions/edit_listing.html",CONTEXT)
    new_edits = form.save(commit=False)
    new_edits.save()
    form.save_m2m()
    return HttpResponseRedirect(reverse('index'))