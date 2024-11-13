# auctions/urls.py
from django.urls import path, include
from .views import AuctionItemViewSet, BidViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', AuctionItemViewSet)
router.register(r'bids', BidViewSet)

urlpatterns = router.urls
