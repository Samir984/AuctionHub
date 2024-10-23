from django.contrib import admin
from . import models


@admin.register(models.User)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
    ]
    search_fields = ["email"]
    list_per_page = 10
    list_filter = ["email", "first_name", "last_name"]


admin.site.register(models.Item)
admin.site.register(models.Auction)
admin.site.register(models.Bid)


# Register your models here.
