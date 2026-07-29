from rest_framework import serializers
from .models import CustomUser, Publisher, Article, Newsletter


class UserSerializer(serializers.ModelSerializer):
    """Serializer for converting CustomUser instances to and from JSON."""
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for converting Publisher instances to and from JSON."""
    
    class Meta:
        model = Publisher
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for converting Article instances to and from JSON."""
    
    class Meta:
        model = Article
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for converting Newsletter instances to and from JSON."""
    
    class Meta:
        model = Newsletter
        fields = '__all__'
