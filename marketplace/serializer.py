from rest_framework import serializers
from django.shortcuts import get_object_or_404
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


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        user = models.User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError("Email doesn't exist")
        self.context["first_name"] = user.first_name
        return email


# ######################################################


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["id", "title", "description", "created_at", "owner"]


class BidSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context["request"].user
        auction_id = self.context["auction_id"]
        new_bid = validated_data["bid_amount"]

        previous_bid = models.Bid.objects.filter(auction_id=auction_id).first()
        auction = get_object_or_404(models.Auction, pk=auction_id)

        if previous_bid is None:
            # # when bid amount of bidder is greater or  equal to price
            print("previous_bid is none\n\n")
            if auction.price <= validated_data["bid_amount"]:
                print("auction price less or = to bid_amount \n\n")

                item_to_transfer = auction.item
                item_to_transfer.owner = user
                item_to_transfer.save()
                auction.expired = True
                auction.save()

        elif previous_bid is not None:
            #  reject the current bid
            print("previous vide is present\n\n")
            if previous_bid.bid_amount >= new_bid:
                print("previous bid amount in greater then new bid\n")
                raise serializers.ValidationError(
                    {"detail": "Bid amount must be higher than the current bid.\n"}
                )
                # delete prevous bid
            elif previous_bid.bid_amount <= new_bid and new_bid < auction.price:
                print("in between about \n\n")
                previous_bid.delete()

            else:
                print("new bid is highter then price")
                # delete previous bid
                previous_bid.delete()
                # transfer item to new owner from previous owner
                item_to_transfer = auction.item
                item_to_transfer.owner = user
                item_to_transfer.save()
                # delete current auction
                auction.expired = True
                auction.save()

        return models.Bid.objects.create(
            auction_id=auction_id, bidder=user, **validated_data
        )

    class Meta:
        model = models.Bid
        fields = ["id", "auction", "bid_amount", "bidder", "created_at"]
        extra_kwargs = {"auction": {"read_only": True}, "bidder": {"read_only": True}}


class AuctionSerializer(serializers.ModelSerializer):
    current_bid = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    bid = BidSerializer(read_only=True)
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
            "price",
            "bid",
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
            "price",
            "ends_at",
        ]
