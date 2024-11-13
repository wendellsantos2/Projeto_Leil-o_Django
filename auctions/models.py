# auctions/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AuctionItem(models.Model):
    TYPE_CHOICES = [
        ('vehicle', 'Vehicle'),
        ('real_estate', 'Real Estate'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    end_time = models.DateTimeField()
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image_url = models.URLField(blank=True, null=True)

    def is_active(self):
        return timezone.now() < self.end_time

class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, related_name="bids", on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bidder} - {self.amount}'
