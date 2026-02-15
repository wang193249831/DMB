from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Comment
from message_board_messages.models import Message, Notification


@login_required
def add_comment(request, message_id):
    # 获取消息对象
    message = get_object_or_404(Message, id=message_id)

    if request.method == 'POST':
        # 获取评论内容
        content = request.POST.get('content')

        if not content or content.strip() == '':
            # 内容为空，返回错误
            return HttpResponseBadRequest('评论内容不能为空')

        # 创建评论
        comment = Comment.objects.create(
            message=message,
            author=request.user,
            content=content
        )
        
        # 创建通知（如果评论者不是消息作者）
        if request.user != message.author:
            Notification.objects.create(
                recipient=message.author,
                actor=request.user,
                verb='comment',
                target=message,
                content=f'{request.user.username} 评论了您的消息 "{message.title}"'
            )

    # 重定向到消息详情页
    return redirect('message_board_messages:message_detail', pk=message_id)
