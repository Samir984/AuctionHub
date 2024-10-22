from django.shortcuts import render, HttpResponse
from .serializer import ItemSerializer, AuctionSerializer
from .models import Item, Auction, Bid
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# 


class ItemViewSet(ModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
