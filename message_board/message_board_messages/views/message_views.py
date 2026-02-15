from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from ..models import Message, Category, Tag
from ..forms import MessageForm


@cache_page(60 * 15)  # 缓存15分钟
def message_list(request):
    """消息列表视图"""
    # 获取所有已发布的消息，使用select_related优化查询
    messages_list = Message.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')
    # 分页，每页显示10条，使用get_page()方法简化分页代码
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    messages = paginator.get_page(page)  # 自动处理无效页码
    return render(request, 'messages/message_list.html', {'messages': messages})


def message_detail(request, pk):
    """消息详情视图"""
    # 使用select_related优化查询，减少数据库查询次数
    message = get_object_or_404(Message.objects.select_related('author', 'category'), pk=pk, status='published')
    # 增加浏览量
    message.increase_views()
    # 获取相关消息，使用select_related优化查询
    related_messages = Message.objects.filter(
        category=message.category, status='published'
    ).select_related('author', 'category').exclude(pk=pk).order_by('-published_at')[:3]
    # 获取当前消息的评论，使用select_related优化查询
    from comments.models import Comment
    comments = Comment.objects.filter(message=message).select_related('author').order_by('-created_at')
    return render(request, 'messages/message_detail.html', {
        'message': message,
        'related_messages': related_messages,
        'comments': comments
    })


@login_required
def message_create(request):
    """创建消息视图"""
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            if message.status == 'published':
                message.published_at = timezone.now()
            message.save()
            form.save_m2m()  # 保存多对多关系（标签）
            messages.success(request, '消息已创建成功！')
            return redirect('message_board_messages:message_detail', pk=message.pk)
    else:
        form = MessageForm()
    return render(request, 'messages/message_form.html', {'form': form})


@login_required
def message_edit(request, pk):
    """编辑消息视图"""
    message = get_object_or_404(Message, pk=pk, author=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            message = form.save(commit=False)
            if message.status == 'published' and not message.published_at:
                message.published_at = timezone.now()
            elif message.status == 'draft':
                message.published_at = None
            message.save()
            form.save_m2m()  # 保存多对多关系（标签）
            messages.success(request, '消息已更新成功！')
            return redirect('message_board_messages:message_detail', pk=message.pk)
    else:
        form = MessageForm(instance=message)
    return render(request, 'messages/message_form.html', {'form': form, 'message': message})


@login_required
def message_delete(request, pk):
    """删除消息视图"""
    message = get_object_or_404(Message, pk=pk, author=request.user)
    if request.method == 'POST':
        message.delete()
        messages.success(request, '消息已删除成功！')
        return redirect('message_board_messages:message_list')
    # 如果是GET请求，重定向到消息详情页
    return redirect('message_board_messages:message_detail', pk=pk)
