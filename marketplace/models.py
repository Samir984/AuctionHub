from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


# Custom User Manager
class CustomerUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractUser):
    username = None  # Removing username field
    email = models.EmailField(unique=True)  # Setting email as unique

    USERNAME_FIELD = "email"  # Set email to be used as the unique identifier
    REQUIRED_FIELDS = []  # Removes username from required fields

    objects = CustomerUserManager()  # Specify the custom manager

    def __str__(self):
        return self.get_full_name()  # Return email for object representation


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    highest_bidder = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="highest_bidder",
        null=True,
        blank=True,
    )

    def is_active(self):
        return self.ends_at > timezone.now()

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction_item = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="bids"
    )
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.first_name} - {self.bid_amount}"
