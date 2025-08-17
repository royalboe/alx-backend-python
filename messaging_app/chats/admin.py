from django.contrib import admin
from .models import User, Message, Conversation, ConversationParticipant

class MessageInline(admin.TabularInline):
    model = Message
    # extra = 0

class ConversationParticipantInline(admin.TabularInline):
    model = ConversationParticipant

class ConversationAdmin(admin.ModelAdmin):
    inlines = [MessageInline, ConversationParticipantInline]


admin.site.register(User)
admin.site.register(Message)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationParticipant)

# Register your models here.

