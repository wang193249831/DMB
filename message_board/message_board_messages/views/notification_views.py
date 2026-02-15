from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from ..models import Notification


@login_required
def notification_list(request):
    """用户通知列表"""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    notification_page = paginator.get_page(page)
    
    # 标记所有通知为已读
    unread_notifications = notifications.filter(is_read=False)
    for notification in unread_notifications:
        notification.mark_as_read()
    
    context = {
        'notification_page': notification_page,
        'unread_count': 0,  # 已标记为已读，所以为0
    }
    return render(request, 'message_board_messages/notification_list.html', context)


@login_required
def notification_detail(request, notification_id):
    """通知详情"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    
    # 标记为已读
    if not notification.is_read:
        notification.mark_as_read()
    
    context = {
        'notification': notification,
    }
    return render(request, 'message_board_messages/notification_detail.html', context)


@login_required
def mark_all_as_read(request):
    """标记所有通知为已读"""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')


@login_required
def delete_notification(request, notification_id):
    """删除通知"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return redirect('notification_list')


@login_required
def delete_all_notifications(request):
    """删除所有通知"""
    Notification.objects.filter(recipient=request.user).delete()
    return redirect('notification_list')


def get_unread_notification_count(user):
    """获取用户未读通知数量"""
    if user.is_authenticated:
        return Notification.objects.filter(recipient=user, is_read=False).count()
    return 0
