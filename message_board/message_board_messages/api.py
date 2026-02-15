from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message, Category, Tag, Favorite, Like
from .serializers import MessageSerializer, CategorySerializer, TagSerializer, FavoriteSerializer, LikeSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """分类API视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """标签API视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """消息API视图集"""
    queryset = Message.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    serializer_class = MessageSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """收藏API视图集"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """获取当前用户的收藏"""
        return Favorite.objects.filter(user=self.request.user).select_related('message', 'message__author', 'message__category')
    
    def perform_create(self, serializer):
        """创建收藏时设置用户"""
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    """点赞API视图集"""
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """获取当前用户的点赞"""
        return Like.objects.filter(user=self.request.user).select_related('message', 'message__author', 'message__category')
    
    def perform_create(self, serializer):
        """创建点赞时设置用户"""
        serializer.save(user=self.request.user)
