from django.urls import path, include
from . import views
from rest_framework import routers, request

router = routers.DefaultRouter()
router.register("items", views.ItemViewSet, basename="items")
router.register("auctions", views.AuctionViewSet, basename="auctions")


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("me/", views.MyDetailView.as_view(), name="my_detail"),
    path("change_password/", views.ChangePasswordView.as_view(), name="change_password"),
]
urlpatterns += router.urls
