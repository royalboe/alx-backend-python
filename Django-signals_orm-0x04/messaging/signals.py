from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import User, Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    """
    Signal receiver function to send a notification when a new message is created.

    Args:
        sender (Model): The model class that sent the signal (Message).
        instance (Message): The actual instance of the Message model that was saved.
        created (bool): True if a new record was created.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        None
    """
    if not created:
        return None
    if created:
        print(f"New message from {instance.sender.username} to {instance.receiver.username}: {instance.content}")
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    """
    Signal receiver function to log message edits.

    Args:
        sender (Model): The model class that sent the signal (Message).
        instance (Message): The actual instance of the Message model that was saved.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        None
    """
    if instance.pk is None:
        return None
    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return None
    if instance.content != old_instance.content:
        instance.edited = True
        print(f"Message edited by {instance.sender.username}: {instance.content}")
        MessageHistory.objects.create(message=instance, content=old_instance.content, edited_by=instance.sender)
        # Display the message edit history in the user interface, allowing users to view previous versions of their messages.
        messages = MessageHistory.objects.filter(message=instance)

@receiver(post_delete, sender=User)
def delete_all_user_data(sender, instance, **kwargs):
    """
    Signal receiver function to delete all user data when a user is deleted.

    Args:
        sender (Model): The model class that sent the signal (User).
        instance (User): The actual instance of the User model that was deleted.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        None
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()