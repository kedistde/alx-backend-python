from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
    
    def test_notification_created_on_new_message(self):
        """Test that notification is created when new message is sent"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Check if notification was created
        notification_count = Notification.objects.filter(
            user=self.user2,
            message=message
        ).count()
        
        self.assertEqual(notification_count, 1)
    
    def test_message_edit_logging(self):
        """Test that message edits are logged"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        
        # Edit the message
        message.content = "Edited content"
        message.save()
        
        # Check if edit was logged
        history_count = MessageHistory.objects.filter(message=message).count()
        self.assertEqual(history_count, 1)
        self.assertEqual(MessageHistory.objects.first().old_content, "Original content")
    
    def test_user_data_cleanup(self):
        """Test that user data is cleaned up on deletion"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        
        # Delete user and check if related data is cleaned up
        user1_id = self.user1.id
        self.user1.delete()
        
        # Check if messages sent by user are deleted
        sent_messages_count = Message.objects.filter(sender_id=user1_id).count()
        self.assertEqual(sent_messages_count, 0)

class ManagerTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        
        # Create read and unread messages
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 1",
            read=False
        )
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Unread message 2", 
            read=False
        )
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Read message",
            read=True
        )
    
    def test_unread_messages_manager(self):
        """Test custom unread messages manager"""
        unread_count = Message.unread_messages.unread_count_for_user(self.user2)
        self.assertEqual(unread_count, 2)
        
        unread_messages = Message.unread_messages.for_user(self.user2)
        self.assertEqual(unread_messages.count(), 2)
        
        for message in unread_messages:
            self.assertFalse(message.read)

class ThreadedConversationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'password')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'password')
        
        # Create a threaded conversation
        self.parent_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Parent message"
        )
        
        self.reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content="Reply 1",
            parent_message=self.parent_message
        )
        
        self.reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Reply 2", 
            parent_message=self.reply1
        )
    
    def test_thread_retrieval(self):
        """Test recursive thread retrieval"""
        thread = self.parent_message.get_thread()
        self.assertEqual(len(thread), 2)
        self.assertIn(self.reply1, thread)
        self.assertIn(self.reply2, thread)
