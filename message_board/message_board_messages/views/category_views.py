from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from ..models import Message, Category, Tag


@cache_page(60 * 15)  # 缓存15分钟
def category_messages(request, slug):
    """按分类查看消息"""
    category = get_object_or_404(Category, slug=slug)
    # 使用select_related优化查询
    messages_list = Message.objects.filter(category=category, status='published').select_related('author', 'category').order_by('-published_at')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    messages = paginator.get_page(page)  # 自动处理无效页码
    return render(request, 'messages/message_list.html', {
        'messages': messages,
        'category': category
    })


@cache_page(60 * 15)  # 缓存15分钟
def tag_messages(request, slug):
    """按标签查看消息"""
    tag = get_object_or_404(Tag, slug=slug)
    # 使用select_related和prefetch_related优化查询
    messages_list = Message.objects.filter(tags=tag, status='published').select_related('author', 'category').order_by('-published_at')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    messages = paginator.get_page(page)  # 自动处理无效页码
    return render(request, 'messages/message_list.html', {
        'messages': messages,
        'tag': tag
    })
