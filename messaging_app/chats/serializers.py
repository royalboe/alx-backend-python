from rest_framework import serializers
from .models import Message, Conversation, User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "profile_image",
        ]
        read_only_fields = ["user_id"]

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # Remove extra field
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            profile_image=validated_data.get("profile_image", None),
        )
        return user

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        return data


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='participants'
    )
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'participant_ids']
        read_only_fields = ["created_at"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="sender"
    )
    conversation = serializers.SlugRelatedField(
        slug_field="conversation_id",
        queryset=Conversation.objects.all()
    )
    sender_info = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "message_body",
            "conversation",
            "sender",
            "sender_id",
            "sent_at",
        ]
        read_only_fields = ["sent_at"]

    def get_sender_info(self, obj):
        return f"{obj.sender.get_full_name()}"


