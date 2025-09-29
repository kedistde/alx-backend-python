import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth.models import User

class MessageFilter(filters.FilterSet):
    conversation = filters.ModelChoiceFilter(
        queryset=Conversation.objects.all(),
        field_name='conversation'
    )
    sender = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='sender'
    )
    start_date = filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='gte'
    )
    end_date = filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='lte'
    )
    is_read = filters.BooleanFilter(field_name='is_read')
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date', 'is_read']

class ConversationFilter(filters.FilterSet):
    participant = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        method='filter_by_participant'
    )
    
    class Meta:
        model = Conversation
        fields = ['participant']
    
    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(participants=value)
