from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Message, Category, Tag
from .forms import MessageForm


def home(request):
    """首页视图，显示最新的已发布消息"""
    latest_messages = Message.objects.filter(status='published').order_by('-published_at')[:6]
    return render(request, 'home.html', {'latest_messages': latest_messages})


def message_list(request):
    """消息列表视图"""
    # 获取所有已发布的消息
    messages_list = Message.objects.filter(status='published').order_by('-published_at')
    # 分页，每页显示10条
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，显示第一页
        messages = paginator.page(1)
    except EmptyPage:
        # 如果page超出范围，显示最后一页
        messages = paginator.page(paginator.num_pages)
    return render(request, 'messages/message_list.html', {'messages': messages})


def message_detail(request, pk):
    """消息详情视图"""
    message = get_object_or_404(Message, pk=pk, status='published')
    # 增加浏览量
    message.increase_views()
    # 获取相关消息
    related_messages = Message.objects.filter(
        category=message.category, status='published'
    ).exclude(pk=pk).order_by('-published_at')[:3]
    return render(request, 'messages/message_detail.html', {
        'message': message,
        'related_messages': related_messages
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
            return redirect('message_detail', pk=message.pk)
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
            return redirect('message_detail', pk=message.pk)
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
        return redirect('message_list')
    return render(request, 'messages/message_confirm_delete.html', {'message': message})


def like_message(request, pk):
    """点赞消息视图"""
    message = get_object_or_404(Message, pk=pk, status='published')
    message.increase_likes()
    return redirect('message_detail', pk=pk)


def category_messages(request, slug):
    """按分类查看消息"""
    category = get_object_or_404(Category, slug=slug)
    messages_list = Message.objects.filter(category=category, status='published').order_by('-published_at')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return render(request, 'messages/message_list.html', {
        'messages': messages,
        'category': category
    })


def tag_messages(request, slug):
    """按标签查看消息"""
    tag = get_object_or_404(Tag, slug=slug)
    messages_list = Message.objects.filter(tags=tag, status='published').order_by('-published_at')
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return render(request, 'messages/message_list.html', {
        'messages': messages,
        'tag': tag
    })
