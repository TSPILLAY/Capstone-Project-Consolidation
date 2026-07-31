from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')

urlpatterns = [
    # Entry Point & Main Feed
    path('', views.register_view, name='register'),
    path('feed/', views.article_list_view, name='article_list'),
    
    # Journalist Workflows
    path('articles/create/', views.create_article_view, name='create_article'),
    
    # Editor Dashboard Workflows
    path('pending/', views.pending_articles_list, name='pending_articles'),
    path('approve/<int:article_id>/', views.approve_article_action, name='approve_article'),
    
    # Newsletter Workflows
    path('newsletters/', views.newsletter_list_view, name='newsletter_list'),
    path('newsletters/create/', views.create_newsletter_view, name='create_newsletter'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/approved-log/', views.api_approved_log, name='api_approved_log'),
]
