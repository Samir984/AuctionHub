from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Item)
admin.site.register(models.Auction)
admin.site.register(models.Bid)


# Register your models here.
