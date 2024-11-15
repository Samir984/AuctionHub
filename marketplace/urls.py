from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("items", views.ItemViewSet, basename="items")
router.register("auctions", views.AuctionViewSet, basename="auctions")

# Corrected Nested Router Setup
auction_router = routers.NestedDefaultRouter(router, "auctions", lookup="auction")
auction_router.register("bid", views.BidViewSet, basename="auction-bid")

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("me/", views.MyDetailView.as_view(), name="my_detail"),
    path("test/", views.Test.as_view(), name="test"),
    path(
        "forgot_password/",
        views.ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
]

# Include router URLs
urlpatterns += router.urls + auction_router.urls
