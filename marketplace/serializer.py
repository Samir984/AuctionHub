from rest_framework import serializers
from . import models


class RegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # This will call the create_user method in your custom manager
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
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

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
