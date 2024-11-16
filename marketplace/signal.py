from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auction
from .schedulars import schedule_auction_expiry


@receiver(post_save, sender=Auction)
def create_expiry_sechedular_for_auction(sender, instance, created, **kwargs):
    print(
        sender,
        instance,
        created,
        instance.id,
        instance.ends_at,
        " signal call\n\n\n\n\n",
    )
    if created:
        schedule_auction_expiry(instance.id, instance.ends_at)
