from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task
from . import models
from django.utils.timezone import now
from django.conf import settings


@shared_task
def send_reset_password_email(email, code, first_name):
    subject = "Password Reset Request"
    reset_link = f"http://127.0.0.1:8000/account/reset_password/?code={code}"
    # Render the HTML content
    html_content = render_to_string(
        "password_reset_email.html",
        {"reset_link": reset_link, "first_name": first_name},
    )

    # Create the email message
    email_message = EmailMultiAlternatives(
        subject,
        "Please use an HTML-compatible email client to view this message.",
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()


@shared_task
def handel_aution_expire(auction_id):
    try:
        auction = models.Auction.objects.get(pk=auction_id, expired=False)
        auction.expired = True
        auction.save()

        print(
            f"Auction {auction.id} expired successfully.",
            auction.item,
        )

        # Check if there are any bids related to the auction using the related_name 'bid'
        if not hasattr(auction, "bid"):  # If there are any related bids
            print(f"No bids for Auction {auction.id}. Notifying seller.")
            # send mail seller and bidder , auction item is tranfer to bider
            send_mail(
                "Auction Expired - No Bids",
                f"Your auction for item {auction.item.title} has expired with no bids.",
                settings.DEFAULT_FROM_EMAIL,
                [auction.seller.email],
            )

        else:
            print(f"Notifying winner for Auction {auction.id}")
            print(auction.bid, auction.bid.bidder)
            # transer items ownership to new owner
            new_owner = auction.bid.bidder
            auction.item.owner = new_owner
            auction.item.save()

            # send mail to previous owner
            send_mail(
                "Auction Expired - Item Sold",
                f"Your auction for item {auction.item.title} has expired. It was sold to {new_owner.first_name} for {auction.bid.bid_amount}.",
                settings.DEFAULT_FROM_EMAIL,
                [auction.seller.email],
            )

            # send mail to new owner

            send_mail(
                "Auction Expired - No Bids",
                f"Congratulations! You have won the auction for item {auction.item.title} with a bid of {auction.bid.bid_amount}.",
                settings.DEFAULT_FROM_EMAIL,
                [auction.seller.email],
            )

    except models.Auction.DoesNotExist:
        print(f"Auction {auction_id} does not exist or is already expired.")
    except Exception as e:
        print(f"An error occurred while expiring auction {auction_id}: {e}")
