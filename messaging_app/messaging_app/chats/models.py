from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        participant_names = [user.username for user in self.participants.all()]
        return f"Conversation: {', '.join(participant_names)}"
    
    def clean(self):
        if self.participants.count() < 2:
            raise ValidationError("A conversation must have at least 2 participants.")
    
    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    
    def clean(self):
        if self.sender not in self.conversation.participants.all():
            raise ValidationError("Sender must be a participant in the conversation.")
    
    class Meta:
        ordering = ['timestamp']
