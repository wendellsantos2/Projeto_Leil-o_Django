# auctions/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AuctionItem, Bid
from .serializers import AuctionItemSerializer, BidSerializer
from django.utils import timezone

class AuctionItemViewSet(viewsets.ModelViewSet):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer

    @swagger_auto_schema(
        method='post',
        operation_description="Place a bid on an auction item",
        responses={
            status.HTTP_201_CREATED: openapi.Response('Bid placed successfully'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Invalid bid')
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Bid amount')
            },
            required=['amount']
        )
    )
    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        item = self.get_object()
        bid_amount = request.data.get('amount')
        if item.is_active() and bid_amount > item.current_price:
            bid = Bid(item=item, bidder=request.user, amount=bid_amount)
            bid.save()
            item.current_price = bid_amount
            item.save()
            return Response({'status': 'Bid placed successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'Invalid bid'}, status=status.HTTP_400_BAD_REQUEST)

class BidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
