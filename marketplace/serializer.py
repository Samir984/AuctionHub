from rest_framework import serializers
from . import models


class RegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        user = models.User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = models.User
        fields = ["id", "first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"detail": "Old password is not correct."}
            )
        return value


# ######################################################


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["id", "title", "description", "created_at", "owner"]


class AuctionSerializer(serializers.ModelSerializer):
    current_bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Item.objects.all(), write_only=True
    )

    def validate_item_id(self, value):
        request = self.context["request"]
        if request.method == "POST":
            if models.Auction.objects.filter(item_id=value).exists():
                raise serializers.ValidationError(
                    "An auction for this item already exists."
                )
        return value

    def create(self, validated_data):
        item = validated_data.pop("item_id")
        request = self.context.get("request")

        validated_data["item"] = item
        validated_data["seller"] = request.user

        print(request.user, "\n\n\n")
        validated_data["seller"] = request.user  #
        return super().create(validated_data)

    class Meta:
        model = models.Auction
        fields = [
            "id",
            "item_id",
            "item",
            "seller",
            "starting_bid",
            "current_bid",
            "created_at",
            "ends_at",
        ]
        extra_kwargs = {"seller": {"read_only": True}}


class AuctionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Auction
        fields = [
            "id",
            "starting_bid",
            "ends_at",
        ]


class BidSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context["request"].user
        auction_id = self.context["auction_id"]

        current_bid = models.Bid.objects.filter(auction_id=auction_id).first()

        if current_bid is not None:
            if current_bid.bid_amount >= validated_data["bid_amount"]:
                raise serializers.ValidationError(
                    {"detail": "Bid amount must be higher than the current bid."}
                )
            else:
                current_bid.delete()

        return models.Bid.objects.create(
            auction_id=auction_id, bidder=user, **validated_data
        )

    class Meta:
        model = models.Bid
        fields = ["id", "auction", "bid_amount", "bidder", "created_at"]
        extra_kwargs = {"auction": {"read_only": True}, "bidder": {"read_only": True}}
