from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(models.User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ["email", "is_staff", "is_active", "first_name", "last_name"]
    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "created_at"]
    list_filter = ["owner"]


@admin.register(models.Auction)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["item", "seller", "starting_bid", "expired"]


@admin.register(models.Bid)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["bidder", "bid_amount", "auction"]


# Register your models here.
