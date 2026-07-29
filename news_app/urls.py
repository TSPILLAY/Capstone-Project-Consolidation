from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router for REST API viewsets
router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')

urlpatterns = [
    # Map root URL to your pending articles list (or another valid view)
    path('', views.pending_articles_list, name='home'),
    
    # HTML views
    path('pending/', views.pending_articles_list, name='pending_articles'),
    path('approve/<int:article_id>/', views.approve_article_action, name='approve_article'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/approved-log/', views.api_approved_log, name='api_approved_log'),
]