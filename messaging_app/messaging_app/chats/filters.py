import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class MessageFilter(filters.FilterSet):
    conversation = filters.ModelChoiceFilter(
        queryset=Conversation.objects.all(),
        field_name='conversation',
        method='filter_conversation'
    )
    
    sender = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='sender'
    )
    
    start_date = filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='gte',
        method='filter_start_date'
    )
    
    end_date = filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='lte',
        method='filter_end_date'
    )
    
    is_read = filters.BooleanFilter(field_name='is_read')
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date', 'is_read']
    
    def filter_conversation(self, queryset, name, value):
        """
        Filter messages by conversation, ensuring user is a participant
        """
        request = self.request
        if request and request.user.is_authenticated:
            # Ensure user is a participant in the conversation
            if value.participants.filter(id=request.user.id).exists():
                return queryset.filter(conversation=value)
        return queryset.none()
    
    def filter_start_date(self, queryset, name, value):
        """
        Filter messages from start date
        """
        if value:
            return queryset.filter(timestamp__gte=value)
        return queryset
    
    def filter_end_date(self, queryset, name, value):
        """
        Filter messages until end date
        """
        if value:
            return queryset.filter(timestamp__lte=value)
        return queryset
