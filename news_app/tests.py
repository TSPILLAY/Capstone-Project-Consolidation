from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Publisher, Article, Newsletter


class NewsAppFullTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # User fixtures
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

    # --- HTML View & Routing Tests ---
    def test_registration_view_renders_and_creates_user(self):
        """Verify registration page loads and creates a new user."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_app/register.html')

        post_data = {
            'username': 'newuser',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'role': 'reader',
            'email': 'newuser@example.com'
        }
        res = self.client.post(reverse('register'), post_data)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_article_list_view_renders(self):
        """Verify public feed displays approved articles."""
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Capstone")

    def test_editor_access_to_pending_articles(self):
        """Verify only editors can access the pending review dashboard."""
        # Unauthenticated access fails / redirects
        res_anon = self.client.get(reverse('pending_articles'))
        self.assertNotEqual(res_anon.status_code, 200)

        # Editor access succeeds
        self.client.force_login(self.editor)
        res_editor = self.client.get(reverse('pending_articles'))
        self.assertEqual(res_editor.status_code, 200)

    # --- DRF API & Signal Tests ---
    def test_reader_subscribed_articles_only(self):
        """Verify reader receives subscribed content via API."""
        self.reader.subscribed_publishers.add(self.publisher)
        self.client.force_authenticate(user=self.reader)

        response = self.client.get('/api/articles/subscribed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch('requests.post')
    @patch('django.core.mail.send_mail')
    def test_editor_approval_triggers_signal(self, mock_send_mail, mock_post):
        """Verify approving an article triggers post_save signals."""
        draft_article = Article.objects.create(
            title="Draft Title", content="Draft content...", author=self.journalist, approved=False
        )
        draft_article.approved = True
        draft_article.save()

        self.assertTrue(mock_post.called)
