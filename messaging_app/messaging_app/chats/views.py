from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, ConversationSerializer, MessageSerializer,
    ConversationCreateSerializer, MessageCreateSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def create(self, request):
        serializer = ConversationCreateSerializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        sender = request.user
        
        serializer = MessageCreateSerializer(
            data=request.data,
            context={'conversation': conversation, 'sender': sender}
        )
        
        if serializer.is_valid():
            message = serializer.save()
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        # Ensure the current user is included in participants
        participants = serializer.validated_data.get('participants', [])
        if self.request.user not in participants:
            participants.append(self.request.user)
        conversation = serializer.save()
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all()
        
        # Apply filtering
        message_filter = MessageFilter(request.GET, queryset=messages, request=request)
        filtered_messages = message_filter.qs
        
        # Apply pagination
        paginator = MessagePagination()
        page = paginator.paginate_queryset(filtered_messages, request)
        
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(filtered_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_all_as_read(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
        updated_count = messages.update(is_read=True)
        return Response({
            'status': f'{updated_count} messages marked as read',
            'updated_count': updated_count
        })

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    
    def get_queryset(self):
        # Only show messages from conversations where user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def perform_create(self, serializer):
        # Set the sender to the current user
        serializer.save(sender=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if message.sender != request.user and not message.is_read:
            message.is_read = True
            message.save()
            return Response({'status': 'Message marked as read'})
        return Response({'status': 'Message already read or sent by you'})
