from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import TagViewSet, MessageViewSet, FavoriteViewSet, LikeViewSet

# 创建API路由器
router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'likes', LikeViewSet, basename='like')

app_name = 'message_board_messages'

urlpatterns = [
    # 常规视图路由
    path('', views.message_list, name='message_list'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('create/', views.message_create, name='message_create'),
    path('<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('<int:pk>/delete/', views.message_delete, name='message_delete'),
    path('<int:pk>/like/', views.like_message, name='like_message'),
    path('<int:pk>/favorite/', views.favorite_message, name='favorite_message'),
    path('<int:pk>/unfavorite/', views.unfavorite_message, name='unfavorite_message'),
    path('favorites/', views.favorite_list, name='favorite_list'),

    path('tag/<slug:slug>/', views.tag_messages, name='tag_messages'),
    # 通知相关路由
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('notifications/mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/delete-all/', views.delete_all_notifications, name='delete_all_notifications'),
    # API路由
    path('api/', include(router.urls)),
]