from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    def __str__(self):
        return self.name
    

class Auction(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="auction")
    auction_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 
    

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return f"Auction for {self.item.name}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at =models.DateTimeField(default=timezone.now) 

    class Meta:
        ordering = ['-bid_amount']

    def __str__(self):
        return f"Bid by {self.bidder.username} on {self.auction.item.name}"
