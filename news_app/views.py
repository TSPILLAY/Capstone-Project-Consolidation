from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Q

from .models import Article, CustomUser, Publisher, Newsletter
from .serializers import ArticleSerializer, UserSerializer, PublisherSerializer, NewsletterSerializer


def is_editor(user):
    """
    Check if the user is authenticated and holds the 'editor' role.
    
    Args:
        user (CustomUser): The user object to evaluate.
        
    Returns:
        bool: True if the user is authenticated and is an editor, False otherwise.
    """
    return user.is_authenticated and user.role == 'editor'


@user_passes_test(is_editor)
def pending_articles_list(request):
    """
    Render a list of unapproved articles for editor review.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: Rendered HTML page containing pending articles.
    """
    articles = Article.objects.filter(approved=False)
    return render(request, 'news_app/approve_articles.html', {'articles': articles})


@user_passes_test(is_editor)
def approve_article_action(request, article_id):
    """
    Approve an article and trigger the article approval signal.
    
    Args:
        request (HttpRequest): The HTTP request object.
        article_id (int): Primary key of the Article to approve.
        
    Returns:
        HttpResponseRedirect: Redirects to the pending articles list.
    """
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()  # Triggers post_save signal
    return redirect('pending_articles')


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing approved articles.
    """
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """
        Retrieve approved articles.
        
        Returns:
            QuerySet: Filtered queryset containing only approved articles.
        """
        return Article.objects.filter(approved=True)

    def get_permissions(self):
        """
        Determine permissions based on the request action.
        
        Returns:
            list: List of permission instances required for the action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['get'])
    def subscribed(self, request):
        """
        Custom API action returning approved articles from publishers and 
        journalists subscribed to by the authenticated reader.
        
        Args:
            request (Request): REST framework request object.
            
        Returns:
            Response: JSON response containing serialized subscribed articles or error details.
        """
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
        if getattr(request.user, 'role', None) != 'reader':
            return Response(
                {"detail": "Only readers can access subscribed articles."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        fav_publishers = request.user.subscribed_publishers.all()
        fav_journalists = request.user.subscribed_journalists.all()

        articles = Article.objects.filter(approved=True).filter(
            Q(publisher__in=fav_publishers) | Q(author__in=fav_journalists)
        ).distinct()

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def api_approved_log(request):
    """
    Webhook endpoint receiving article approval notifications from post_save signals.
    
    Args:
        request (Request): REST framework request object containing payload data.
        
    Returns:
        Response: Success confirmation message.
    """
    return Response({"status": "Article approval logged successfully"}, status=status.HTTP_200_OK)
