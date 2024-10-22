from rest_framework import serializers
from . import models


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["id", "title", "description", "created_at", "owner"]


class AuctionSerializer(serializers.ModelSerializer):
    current_bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = models.Auction
        fields = [
            "id",
            "item",
            "seller",
            "starting_bid",
            "current_bid",
            "created_at",
            "ends_at",
        ]
