from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class Role(models.TextChoices):
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)




class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    # password_hash = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['first_name'], name='firstname_idx'),
        ]

    @property
    def id(self):
        return self.user_id
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_host(self):
        return self.role == self.Role.HOST
    
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_sender_info(self, obj):
        return {
            "user_id": obj.sender.user_id,
            "email": obj.sender.email,
            "first_name": obj.sender.first_name,
            "last_name": obj.sender.last_name,
            "phone_number": obj.sender.phone_number if obj.sender.phone_number else None,
            "profile_image": obj.sender.profile_image.url if obj.sender.profile_image else None
        }

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name or str(self.email).split('@')[0]
    
    def __str__(self):
        return self.email


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def id(self):
        return self.conversation_id
    
    def __str__(self):
        return f"Conversation {self.conversation_id}"
    def last_10_messages(self):
        return self.messages.objects.order_by('-sent_at')[:10]
    # .values('message_id', 'message_body', 'sent_at', 'sender__user_id', 'sender__first_name', 'sender__last_name', 'sender__profile_image', 'sender__email', 'sender__phone_number')


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="participant_links")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participants_through")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    is_muted = models.BooleanField(default=False)
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['conversation', 'user'], name='unique_participant')
    ]

    def __str__(self):
        return f"{self.user} in {self.conversation}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sent_at = models.DateTimeField(auto_now_add=True)
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def id(self):
        return self.message_id
    class Meta:
        ordering = ["sent_at"]

    def __str__(self):
        return f"Message {self.id} from {self.sender} in {self.conversation}"
