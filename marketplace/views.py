from django.shortcuts import render, HttpResponse
from .serializer import (
    ItemSerializer,
    AuctionSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)
from .models import Item, Auction, Bid, User
from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        user = self.request.user
        print(serializer.validated_data)
        user.set_password(serializer.validated_data["new_password"])
        user.save()


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
