from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Product, Auction, Bid


def index(request):
    return render(request, "auctions/index.html")

# renders a login form when a user tries to GET the page
# When a user submits the form using the POST request method, the user is authenticated, logged in, and redirected to the index page
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

# displays a registration form to the user, and creates a new user when the form is submitted
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

def create(request):
    if request.method == "POST":

        # IMPORTANT: requires development of authentication check
        
        # presents the dict on screen
        # print(request.POST)

        # saves the dict in a variable
        data_post = request.POST

        # actions based in posting data of product
        if "title" in data_post:
            print("***Product insertion***")
            # print(f"Decription:", data_post["description"])
            # title = str(data_post["title"])
            # description = str(data_post["description"])
            # print(title, description)

            # THIS IS WHAT DJANGO CALLS "DIRECT ASSINGMENT" - IT IS FORBIDDEN IN MANYTOMANY FIELDS
            # the logic below this part of code follows the notations about 
            # "modifying db via py"
            newproduct = Product()
            newproduct.title = data_post["title"]
            newproduct.description = data_post["description"]
            # print(newproduct.title)
            # print(newproduct.description)
            # print(f"Newproduct is", newproduct)
            newproduct.save()

        #actions based in posting data of auction
        # for is posting product.id
        if "product" in data_post:
            print("***Auction insertion***")

            # this chunk of code works with user-info
            # user = request.user.is_authenticated # saves True or False
            # print(user) 
            owner = request.user
            # print(user)
            # print(user.id)
            # print(user.first_name)
            # getting user id to add to Auctions
            # owner = owner.id
            # print(User.objects.get(pk=user_id))
            # user_id = User.objects.get(pk=user.id)
            print(f"USER:", owner)

            # setting is_active to true, because it's just created
            # maybe put this on default?
            active = True
            print(F"ACTIVE", active)


            # figuring out what is the product_id selected
            # print(request.POST)
            # print(data_post["product"])
            # product_id = data_post["product"]
            # print(Product.objects.get(pk=product_id))
            anounced = Product.objects.get(pk=data_post["product"])
            print(f"PRODUCT:", anounced)


            # getting the price set
            # print(data_post["price"])
            price = data_post["price"]
            print(f"PRICE:", price)

            a = Auction(owner=owner, active=active, anounced=anounced, price=price)
            print(a)
            print(a.anounced)
            a.save()
            






           

    # BELOW THIS POINT WE ARE DEALING WITH GET

    # here I could use .get(<param>) to get one result
    # I could use .filter(<param>) to obtain a dict with multiple values or, as I did
    # use.all() to fetch all product in db
    data = Product.objects.all() 

    # this prints the dictionary returned by Product.objects.all()
    # print(f"sending this:", data) 
    
    # iterates over data and prints the data inside dict (looks like the string representation from def __str__)
    # for item in data: 
    #     print(item)
    
    # this access the contents of product
    # prodex = Product.objects.get(pk=1)
    # print(prodex.title)
    # print(prodex.description)

    return render(request, "auctions/create.html", {
        "product": data
    })