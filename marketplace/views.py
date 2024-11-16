from django.shortcuts import render, redirect
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
from .models import Item, Auction, Bid
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
from .tasks import send_reset_password_email
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # Adjust if using a custom user model


class CustomLoginView(APIView):
    def post(self, request):
        # Extract email and password from the request
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.is_active:
            return Response(
                {"detail": "This account is inactive."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Generate tokens using SimpleJWT
        refresh = RefreshToken.for_user(user)

        # Return tokens in the response
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        # Perform the password change logic
        user = self.request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        print("i am called second2")

        return Response(
            {"detail": "Password has been changed successfully"},
            status=response.status_code,
        )


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


from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponse
from .forms import ResetPasswordForm

User = get_user_model()  # Always use this to refer to your custom user model


class ResetPasswordTemplateView(views.APIView):
    template_name = "reset_password.html"

    def get(self, request):
        code = request.query_params.get("code")  # Accessing code from query parameters
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
            cache.delete(f"code:{code}")
            messages.success(request, "Your password has been reset successfully.")
            return redirect("login")  # Replace with your login URL

        return render(request, self.template_name, {"form": form})


# -------------------------------------------------------------


class ItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Item.objects.select_related("owner").all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["owner"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        return {"request": self.request}

    serializer_class = ItemSerializer


class AuctionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Auction.objects.prefetch_related("item", "bid").filter(expired=False)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return AuctionUpdateSerializer

        return AuctionSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class BidViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
