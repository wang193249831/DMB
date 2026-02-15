from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from ..models import Message, Favorite, Like, Notification


@login_required
def like_message(request, pk):
    """点赞消息视图"""
    # 确保只接受POST请求
    if request.method != 'POST':
        return JsonResponse({
            'liked': False,
            'likes_count': 0,
            'error': '只支持POST请求。'
        }, status=405)
        
    message = get_object_or_404(Message, pk=pk, status='published')
    
    # 检查用户是否已经点赞
    if Like.objects.filter(user=request.user, message=message).exists():
        # 用户已经点赞，返回错误信息
        return JsonResponse({
            'liked': False,
            'likes_count': message.likes,
            'error': '您已经点赞过这条消息了。'
        })
    
    # 创建点赞记录
    Like.objects.create(user=request.user, message=message)
    
    # 增加点赞数
    message.increase_likes()
    
    # 创建通知（如果点赞者不是消息作者）
    if request.user != message.author:
        Notification.objects.create(
            recipient=message.author,
            actor=request.user,
            verb='like',
            target=message,
            content=f'{request.user.username} 点赞了您的消息 "{message.title}"'
        )
    
    # 返回JSON响应
    return JsonResponse({
        'liked': True,
        'likes_count': message.likes
    })


@login_required
def favorite_message(request, pk):
    """收藏消息视图"""
    message = get_object_or_404(Message, pk=pk, status='published')
    # 检查是否已经收藏
    if not Favorite.objects.filter(user=request.user, message=message).exists():
        # 创建收藏记录
        Favorite.objects.create(user=request.user, message=message)
        messages.success(request, '消息已收藏成功！')
        
        # 创建通知（如果收藏者不是消息作者）
        if request.user != message.author:
            Notification.objects.create(
                recipient=message.author,
                actor=request.user,
                verb='favorite',
                target=message,
                content=f'{request.user.username} 收藏了您的消息 "{message.title}"'
            )
    else:
        messages.info(request, '您已经收藏过这条消息了。')
    return redirect('message_board_messages:message_detail', pk=pk)


@login_required
def unfavorite_message(request, pk):
    """取消收藏消息视图"""
    message = get_object_or_404(Message, pk=pk, status='published')
    # 检查是否存在收藏记录
    favorite = Favorite.objects.filter(user=request.user, message=message).first()
    if favorite:
        # 删除收藏记录
        favorite.delete()
        messages.success(request, '已取消收藏消息！')
    else:
        messages.info(request, '您尚未收藏这条消息。')
    return redirect('message_board_messages:message_detail', pk=pk)


@login_required
def favorite_list(request):
    """查看用户收藏的消息列表"""
    # 使用select_related优化查询，减少数据库查询次数
    favorites = Favorite.objects.filter(user=request.user).select_related('message__author', 'message__category').order_by('-created_at')
    # 获取收藏的消息，过滤已发布的消息
    messages_list = [favorite.message for favorite in favorites if favorite.message.status == 'published']
    # 分页，每页显示10条，使用get_page()方法简化分页代码
    from django.core.paginator import Paginator
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    messages = paginator.get_page(page)  # 自动处理无效页码
    return render(request, 'messages/message_list.html', {
        'messages': messages,
        'title': '我的收藏'
    })
