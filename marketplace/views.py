from django.shortcuts import render, HttpResponse
from .serializer import (
    ItemSerializer,
    AuctionSerializer,
    AuctionUpdateSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    BidSerializer,
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Item, Auction, Bid, User
from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)
import time


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.userme


class ChangePasswordView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        user = self.request.user
        print(serializer.validated_data)
        user.set_password(serializer.validated_data["new_password"])
        user.save()


class ItemViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Item.objects.select_related("owner").all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    pagination_class = PageNumberPagination

    serializer_class = ItemSerializer


class AuctionViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Auction.objects.prefetch_related("item", "bid").filter(expired=False)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return AuctionUpdateSerializer

        return AuctionSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class BidViewSet(ModelViewSet):
    http_method_names = ["post", "get"]

    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs["auction_pk"])

    def get_serializer_context(self):
        return {"request": self.request, "auction_id": self.kwargs["auction_pk"]}


count = 0


class Test(views.APIView):
    def get(self, request):
        global count
        count += 1
        time.sleep(3)
        return Response(f"hello {count}")
