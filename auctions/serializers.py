# auctions/serializers.py
from rest_framework import serializers
from .models import AuctionItem, Bid

class AuctionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = ['id', 'title', 'description', 'starting_price', 'current_price', 'end_time', 'item_type', 'image_url', 'is_active']

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'item', 'bidder', 'amount', 'timestamp']
