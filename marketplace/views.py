from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.contrib import messages
from .forms import ResetPasswordForm
from django.shortcuts import render, HttpResponse
from .serializer import (
    ItemSerializer,
    AuctionSerializer,
    AuctionUpdateSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    BidSerializer,
    ForgotPasswordSerializer,
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Item, Auction, Bid, User
from rest_framework.viewsets import ModelViewSet
from rest_framework import views
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)
import time
from django.core.cache import cache
import random
from .task import send_reset_password_email


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


class ForgotPasswordView(views.APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = random.randint(100000, 999999)
        print(email, code, "\n\n\n")
        first_name = serializer.context["first_name"]
        cache.set(f"code:{code}", email, timeout=300)
        print("sending mail")
        send_reset_password_email.delay(email, code, first_name)
        print("mail send")
        return Response(
            {"detail": "Checkout email to reset the password"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(views.APIView):
    template_name = "reset_password.html"

    def get(self, request):
        code = request.query_params.get("code")  # Accessing code from query parameters
        print("\n\n\n\n code", code)
        if not code:
            return HttpResponse({"detail": "invalid reset link"}, status=400)

        # Fetch email associated with this code from Redis
        email = cache.get(f"code:{code}")

        if not email:
            return HttpResponse(
                {"detail": "The reset link is invalid or has expired."}, status=400
            )

        form = ResetPasswordForm()
        return render(request, self.template_name, {"form": form, "code": code})

    def post(self, request):
        code = request.query_params.get("code")  # Accessing code from query parameters

        if not code:
            return HttpResponse("Invalid password reset link.", status=400)

        email = cache.get(f"code:{code}")

        if not email:
            return HttpResponse("The reset link is invalid or has expired.", status=400)

        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["new_password"]
            user = User.objects.get(email=email)
            user.set_password(password)  # Use set_password to hash the password
            user.save()

            # Invalidate the used code
            cache.delete(f"otp:{code}")
            messages.success(request, "Your password has been reset successfully.")
            return redirect("login")  # Replace with your login URL

        return render(request, self.template_name, {"form": form})


# -------------------------------------------------------------


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


class Test(views.APIView):
    def get(self, request):
        # email = "sasuki984@gmail.com"
        # cache.
        # data = cache.get(email)

        return Response(f"d")
