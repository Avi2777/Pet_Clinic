# Import necessary modules from Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


# Custom User model that extends Django's AbstractUser
class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)


# UserProfile model to store additional user-related data
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    # OneToOneField links each user to a single UserProfile. 
    # on_delete=models.CASCADE means when a User is deleted, their UserProfile will also be deleted.
    # related_name='user_profile' creates a reverse relation, allowing access to the UserProfile from the User object.

    def __str__(self):
        return self.user.username  # Returns the username as the string representation of UserProfile


# Signal receiver functions that are triggered when a new User object is saved or updated.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # This function creates a UserProfile when a new User is created and saves it to the database.
    if created:
        UserProfile.objects.create(user=instance)  # Create a new UserProfile linked to the User instance
    instance.user_profile.save()  # Save the UserProfile associated with the User instance


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # This function saves the UserProfile whenever the User object is saved or updated.
    instance.user_profile.save()  # Save the UserProfile associated with the User instance
