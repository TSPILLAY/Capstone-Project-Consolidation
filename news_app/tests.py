from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Publisher, Article


class NewsAPITests(TestCase):
    """Unit test suite verifying news API endpoints and signal notifications."""

    def setUp(self):
        """Set up initial database fixtures and API client for testing."""
        self.client = APIClient()
        
        self.reader = CustomUser.objects.create_user(username='reader1', password='password123', role='reader')
        self.journalist = CustomUser.objects.create_user(username='writer1', password='password123', role='journalist')
        self.editor = CustomUser.objects.create_user(username='editor1', password='password123', role='editor')
        
        self.publisher = Publisher.objects.create(name="Tech Times")
        self.article = Article.objects.create(
            title="Django Capstone",
            content="Testing suite details...",
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

    def test_reader_subscribed_articles_only(self):
        """Verify that subscribed readers only receive articles from subscribed publishers."""
        self.reader.subscribed_publishers.add(self.publisher)
        self.client.force_authenticate(user=self.reader)

        response = self.client.get('/api/articles/subscribed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch('requests.post')
    @patch('django.core.mail.send_mail')
    def test_editor_approval_triggers_signal(self, mock_send_mail, mock_post):
        """Verify that approving an article triggers post_save signals and HTTP webhooks."""
        draft_article = Article.objects.create(
            title="Draft Title", content="Draft content...", author=self.journalist, approved=False
        )

        # Approve article to trigger signals
        draft_article.approved = True
        draft_article.save()

        # Assert mock HTTP post was dispatched by signal listener
        self.assertTrue(mock_post.called)
