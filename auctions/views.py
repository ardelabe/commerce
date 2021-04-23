from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bid, Comment, Watch, Category, Grouping

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def index(request):
    auctions = Auction.objects.order_by("-active", "id")
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

# @login_required
def listings(request, auction_id):
    message = None
    watch = None
    watchBool = False
    if request.method == "POST":
        if request.user.is_authenticated:
            data = request.POST
            # print(request.user.is_authenticated)
            print(data)
            # print(data["watcher_id"])
            offer = data["price"]
            bidder = User.objects.get(pk=data["watcher_id"])
            product = Auction.objects.get(pk=data["watched_id"])
            # check bid vality - REPEATED CODE HERE - NEEDS OPTIMIZATION
            auction = Auction.objects.get(pk=auction_id)
            bidOnProd = Bid.objects.filter(product=auction)
            bidOnProd = bidOnProd.aggregate(Max('offer'))
            print(offer, bidOnProd["offer__max"], auction.price)
            print(type(offer), type(bidOnProd["offer__max"]), type(auction.price))
            # print(type(float(bidOnProd["offer__max"])))
            # if offer <= bidOnProd["offer__max"] or offer < float(auction.price):
                # message = "Your offer must be greater or equal the starting price and greather than any existing current offer"
            
            if not offer:
                message = "Please enter a value"
            elif (bidOnProd["offer__max"] == None) and (float(offer) < float(auction.price)):
                message = "Your offer must be greater or equal the starting price"
                print("bop is None")
            elif (bidOnProd["offer__max"] != None) and (float(offer) <= float(bidOnProd["offer__max"])):
                message = "Your offer must be greater than the current offer"
            else:
                b = Bid(offer=offer, bidder=bidder, product=product)
                b.save()
            watch = Watch.objects.filter(watcher_id=request.user)
            for i in watch:
                if (auction_id == i.watched_id) and (i.active == True):
                    watchBool = True
        else:
            unautMess = "Please: log in to place bids"
            return render(request, "auctions/login.html", {
            "unautMess": unautMess
            })
    
    auction = Auction.objects.get(pk=auction_id)
    comments = Comment.objects.filter(subject_id=auction_id)
    watchBool = Watch.objects.filter(watched_id=auction).order_by("id").last()
    # print("WATCHBOOL IS", watchBool)
    if watchBool != None:
        watchBool = watchBool.active
    requester = request.user
    seller = User.objects.get(pk=auction.seller_id)  
    
    bidOnProd = Bid.objects.filter(product=auction).order_by("-offer").first()
    # print("bid#1", bidOnProd)
    # print("BOP IS", bidOnProd)
    # print(bidOnProd.bidder_id)


    if bidOnProd == None:
        maxBid = auction.price
        bidder = None
    else:
        maxBid = bidOnProd.offer
        # print(maxBid)
        b_id = bidOnProd.bidder_id
        bidder = User.objects.get(pk=b_id)
        # print(bidder.username)
    return render(request, "auctions/listings.html", {
        "auction": auction,
        "commentary": comments,
        "watch": watchBool,
        "maxBid": maxBid,
        "bidder": bidder, 
        "message": message,
        "seller": seller,
    })

def sell(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            print(data)
            title = data["title"]
            print(title)
            description = data["description"]
            print(description)
            price = data["price"]
            print(price)
            image = data["image"]
            # print(image)
            user = request.user
            print(user)
            print(data["category"])
            if not (title or description or price or data["category"]):
                category = Grouping.objects.all()
                print("Please fill the post fields with the required data.")
                return render(request, "auctions/sell.html", {
                    "category": category,
                    "message": "Please fill the post fields with the required data."

                })
            else:
                a = Auction(title=title, description=description, price=price, image=image, seller=user)
                a.save()
                categorized = Auction.objects.get(title=title, description=description, price=price, image=image, seller=user)
                category = Grouping.objects.get(grouping=data["category"])
                c = Category(categorized=categorized, category=category)
                print(categorized)
                c.save()
            
        # for i in Category.CATEGORY:
        #     print(Category.CATEGORY[i][1])
        # print(Category.CATEGORY)
        # print(Category.CATEGORY[0])
        # print(Category.CATEGORY[0][1])
        category = Grouping.objects.all()
        # print(category)
        return render(request, "auctions/sell.html", {
        "category": category
    })
    else:
        unautMess = "Please: log in to create listings"
        return render(request, "auctions/login.html", {
        "unautMess": unautMess
        })

def watch(request):
    unautMess = None
    products = None
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            # print(data)
            if data["action"] == "insertRow":
                # print('insertRow')
                watched_id = data["watched_id"]
                watcher_id = data["watcher_id"]
                # print(watcher_id)
                w = Watch(watched_id=watched_id, watcher_id=watcher_id, active=True)
                # print(w)
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
        # get the id of the products logged-user is watching (status active)
        watch = Watch.objects.filter(watcher_id=request.user, active=True)
        # print(watch[0].id)
        # load these products from auctions and save in whatching
        watching = []
        for product in watch:
            # print(product.id)
            watching.append(product.watched_id)
        watching = set(watching)
        # print(watching)
        products = Auction.objects.filter(pk__in=watching)
        # print(products)
    else:
        unautMess = "Please: log in to manage your watchlist"
        return render(request, "auctions/login.html", {
        "unautMess": unautMess
        })

    return render(request, "auctions/watch.html", {
        "products": products,
        "unautMess": unautMess
    })

def comment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            # print(data)
            comment = data["commentary"]
            # print(comment)
            commentator_id = request.user
            # print(commentator_id)
            subject_id = data["subject_id"]
            # print(subject_id)
            auction = Auction.objects.get(pk=subject_id)
            auction_id = auction.id
            # print(auction)
            c = Comment(comentator=commentator_id, comment=comment, subject=auction)
            # print(c)
            c.save()
    else: 
        unautMess = "Please: log in before comment in any listing"
        return render(request, "auctions/login.html", {
        "unautMess": unautMess
    })
    
    return HttpResponseRedirect(reverse("listings", kwargs={"auction_id": auction_id}))
    # return redirect(request.path)

def close(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            # print(data)
            auction_id = data["auction_id"]
            auction = Auction.objects.get(pk=auction_id)
            auction_id = auction.id
            # print(auction.active)
            auction.active = False
            auction.save()
        return HttpResponseRedirect(reverse("index"))

def category(request):
    g = Grouping.objects.all()
    rendergroup = 0

    return render(request, "auctions/category.html", {
        "g": g, # all categorized objects
        "rendergroup": rendergroup
    })

def grouping(request, distinct_id):
    message = None
    c = Category.objects.filter(category_id=distinct_id)
    # print(c[1].categorized_id)
    l = []
    for i in c:
        # print(i.categorized_id)
        a = Auction.objects.get(pk=i.categorized_id)
        l.append(a)
    print(f"l is: {l}")
    if not l:
        message = "Sorry, there isn't any listings in this category"
    

    return render(request, "auctions/category.html", {
        "l": l, # pass the list of auctions in the group
        "message": message
    })