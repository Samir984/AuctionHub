from django.urls import path, include
from . import views
from rest_framework import routers, request

router = routers.DefaultRouter()
router.register("items", views.ItemViewSet, basename="items")
router.register("auctions", views.AuctionViewSet, basename="auctions")


urlpatterns = router.urls
