from rest_framework import serializers
from .models import Message, Conversation, User, ConversationParticipant

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone_number",
            "profile_image",
            "role",
            "fullname",
            "is_staff",
        ]
        read_only_fields = ["user_id", "created_at", "fullname"]

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User(**validated_data)  # Remove extra field
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_fullname = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="sender"
    )

    conversation = serializers.SlugRelatedField(
        slug_field="conversation_id",
        queryset=Conversation.objects.all()
    )
    # sender_info = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "message_body",
            "conversation",
            "sender",
            "sender_id",
            "sent_at",
            "sender_fullname",
            # "sender_info",
        ]
        read_only_fields = ["sent_at", "message_id", "sender_info"]

    def get_sender_info(self, obj):
        return obj.sender.get_sender_info(obj)


class ConversationSerializer(serializers.ModelSerializer):
    # participants = serializers.SerializerMethodField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, source='participants', write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'created_at', 'participant_ids', "messages"]
        read_only_fields = ["created_at"]

    # method to use if using participants = serializers.SerialzerMethodField
    # def get_participants(self, obj):
    #     return UserSerializer(obj.participants.all(), many=True).data
    
    def create(self, validated_data):
        users = validated_data.pop("participants")
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(users)
        for user in users:
            ConversationParticipant.objects.create(user=user, conversation=conversation)
        return conversation
