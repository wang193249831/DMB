from rest_framework import serializers
from .models import Message, Tag, Favorite, Like
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']





class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'title', 'slug', 'author', 'tags', 'content',
            'image', 'status', 'views', 'likes', 'comments_count',
            'created_at', 'updated_at', 'published_at'
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'message', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    """点赞序列化器"""
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'message', 'created_at']
