from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField

# each time you change anything in auctions/models.py, you’ll need to first 
# run python manage.py makemigrations and then python manage.py migrate to 
# migrate those changes to your database.
class User(AbstractUser):
    def __str__(self):
        return f"id: {self.id} Name: {self.first_name} {self.last_name}"

class Products(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=280)
    def __str__(self):
        return f"Product id: {self.id} - {self.title}"

# one for auction listings (listagem de leiloes)
class Auctions(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    is_active = models.BooleanField() # None by default
    product_id = models.ForeignKey(Products, on_delete=models.PROTECT, related_name="auction_product")
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Auction id: {self.id} - Owner: {self.user_id} - active: {self.is_active} - price: {self.initial_price}"

# one for bids (lances)
class Bids(models.Model):
    auction_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name="auction-bid")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"in id {self.id}, User {self.id} gave a bid of {self.bid} on the product: {self.auction_id}"

# and one for comments made on auction listings (comentarios na listagem)



# class Passenger(models.Model):
#     first = models.CharField(max_length=64)
#     last = models.CharField(max_length=64)
#     flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

#     def __str__(self):
#         return f"{self.first} {self.last}"