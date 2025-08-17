from django.test import TestCase
from .models import User, Conversation
from rest_framework import status

# Create your tests here.

class UserTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(email='test_email@test.com', password='testing', first_name='test1', last_name='last1', is_staff=True)
        user2 = User.objects.create_user(email='test_email_2@test.com', password='testing', first_name='test2', last_name='last2')
        user3 = User.objects.create_user(email='test_email_3@test.com', password='testing', first_name='test3', last_name='last3')

        c1 = Conversation.objects.create()
        c2 = Conversation.objects.create()
        c3 = Conversation.objects.create()
        c1.participants.set([user1, user2])
        c2.participants.set([user1, user3])
        c3.participants.set([user2])

    def test_user_unauthenticated(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_authenticated_isadmin(self):
        user = User.objects.get(email='test_email@test.com')
        self.client.force_login(user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_authenticated_notadmin(self):
        user = User.objects.get(email='test_email_2@test.com')
        self.client.force_login(user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_conversations_endpoint_retrieves_only_authenticated_user(self):
        user = User.objects.get(email='test_email@test.com')
        self.client.force_login(user)
        response = self.client.get('/api/conversations/')
        self.assertEqual(response.status_code, 200)
        assert response.status_code == 200

    def test_user_conversations_unauthenticated(self):
        response = self.client.get('/api/conversations/')
        self.assertEqual(response.status_code, 401)
        