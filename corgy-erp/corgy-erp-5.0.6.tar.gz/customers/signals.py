from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer
from .models import Organization
from .models import Individual
#
# @receiver(post_save, sender=Organization)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()