from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .views import (
    message_list,
    message_detail,
    message_create,
    message_edit,
    message_delete,
    like_message,
    favorite_message,
    unfavorite_message,
    favorite_list,
    category_messages,
    tag_messages
)


# 保持向后兼容性，重新导出所有视图函数
__all__ = [
    'message_list',
    'message_detail',
    'message_create',
    'message_edit',
    'message_delete',
    'like_message',
    'favorite_message',
    'unfavorite_message',
    'favorite_list',
    'category_messages',
    'tag_messages'
]


def home(request):
    """首页视图，显示最新的已发布消息"""
    from .models import Message
    latest_messages = Message.objects.filter(status='published').order_by('-published_at')[:6]
    return render(request, 'home.html', {'latest_messages': latest_messages})
