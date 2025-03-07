from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    context = models.JSONField(default=dict)  # Stores additional context (if needed)
    last_updated = models.DateTimeField(auto_now=True)
    history = models.JSONField(default=list)  # Stores conversation history as a list of messages

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"Conversation with {username} on {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"

class ChatMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", null=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
