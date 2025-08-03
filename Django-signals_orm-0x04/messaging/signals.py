from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Message, Notification

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        print(f"New message from {instance.sender.username} to {instance.receiver.username}: {instance.content}")


