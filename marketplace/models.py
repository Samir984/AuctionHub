from django.db import models
from django.contrib.auth.models import  AbstractUser, BaseUserManager


# Custom User Manager
class UserManager(BaseUserManager):
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

    objects = UserManager()  # Specify the custom manager

    def __str__(self):
        return self.email  # Return email for object representation
