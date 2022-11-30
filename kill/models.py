from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from kill.managers import UserManager


class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    username = None
    email = models.EmailField("email address", blank=False, null=False, unique=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)
    instance.profile.save()
