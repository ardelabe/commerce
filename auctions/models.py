from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import DateTimeField


# each time you change anything in auctions/models.py, you’ll need to first 
# run python manage.py makemigrations and then python manage.py migrate to 
# migrate those changes to your database.
class User(AbstractUser):
    
    def __str__(self):
        return f"id: {self.id} Name: {self.first_name} {self.last_name}"

class Product(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=280)
    
    def __str__(self):
        return f"Product id: {self.id} - {self.title} - {self.description}"

# one for auction listings (listagem de leiloes)
class Auction(models.Model):
    user_id = models.ManyToManyField(User, blank=True, related_name="owner")
    is_active = models.BooleanField() # None by default
    product = models.ManyToManyField(Product, blank=True, related_name="auction_product")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Auction id: {self.id} - Owner: {self.user_id} - active: {self.is_active}"

# one for bids (lances)
class Bid(models.Model):
    user_id = models.ManyToManyField(User, blank=True, related_name="bidder")
    auction = models.ForeignKey(User, on_delete=models.PROTECT, related_name="auction_bid")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"in id {self.id}, User {self.id} gave a bid of {self.bid} on the product: {self.auction_id}"

# and one for comments made on auction listings (comentarios na listagem)
