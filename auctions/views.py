from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment, Watch


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

# renders a login form when a user tries to GET the page
# When a user submits the form using the POST request method, the user is authenticated,
# logged in, and redirected to the index page
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

# logs the user out and redirects them to the index page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# displays a registration form to the user, and creates a new user when the form is 
# submitted
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

# Adding the @login_required decorator on top of any view will ensure that only a user 
# who is logged in can access that view.

def listings(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    # print(auction_id)
    comments = Comment.objects.filter(subject_id=auction_id)
    watch = Watch.objects.filter(watcher_id=request.user)
    watchBool = False
    # print(watch)
    for i in watch:
        # print(i)
        # print(i.watched_id)
        if (auction_id == i.watched_id) and (i.active == True):
            watchBool = True
    # print(watchBool) 
    return render(request, "auctions/listings.html", {
        "auction": auction,
        "commentary": comments,
        "watch": watchBool,
    })

def sell(request):
    if request.method == "POST":
        data = request.POST
        # print(data)
        title = data["title"]
        # print(title)
        description = data["description"]
        price = data["price"]
        image = data["image"]
        print(image)
        user = request.user
        # print(seller)
        a = Auction(title=title, description=description, price=price, image=image, seller=user)
        # print(a)
        a.save()
    return render(request, "auctions/sell.html")

def watch(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        if data["action"] == "insertRow":
            print('insertRow')
            watched_id = data["watched_id"]
            watcher_id = data["watcher_id"]
            print(watcher_id)
            w = Watch(watched_id=watched_id, watcher_id=watcher_id, active=True)
            print(w)
            w.save()
        elif data["action"] == "inactiveRow":
            # print('inactiveRow')
            watch = Watch.objects.filter(watcher_id=request.user)
            # print(watch)
            for i in watch:
                # print("THE ID IS", i.id)
                # print(i.watcher_id)
                # print(i.watched_id)
                if int(i.watcher_id) == int(data["watcher_id"]) and int(i.watched_id) == int(data["watched_id"]):
                    # print("they match")
                    # print(i.active)
                    inac = Watch.objects.get(pk=i.id)
                    inac.active = False
                    inac.save()
            # print("what is coming from POST is:", data["watcher_id"], "and", data["watched_id"])
    
    
    return render(request, "auctions/watch.html", {
    })

def comment(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        comment = data["commentary"]
        print(comment)
        commentator_id = request.user
        print(commentator_id)
        subject_id = data["subject_id"]
        print(subject_id)
        auction = Auction.objects.get(pk=subject_id)
        print(auction)
        c = Comment(comentator=commentator_id, comment=comment, subject=auction)
        print(c)
        c.save()
        
        return HttpResponseRedirect(reverse("index"))