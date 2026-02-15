from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    """消息分类模型"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '分类'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """消息标签模型"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name


class Message(models.Model):
    """消息模型"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='published_at', db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='messages', db_index=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='messages')
    content = CKEditor5Field()
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)
    views = models.PositiveIntegerField(default=0, db_index=True)
    likes = models.PositiveIntegerField(default=0, db_index=True)
    comments_count = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name_plural = '消息'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def increase_views(self):
        """增加浏览量"""
        self.views = F('views') + 1
        self.save(update_fields=['views'])
        self.refresh_from_db(fields=['views'])

    def increase_likes(self):
        """增加点赞数"""
        self.likes = F('likes') + 1
        self.save(update_fields=['likes'])
        self.refresh_from_db(fields=['likes'])


class Favorite(models.Model):
    """收藏模型，记录用户收藏的消息"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '收藏'
        ordering = ['-created_at']
        unique_together = ('user', 'message')  # 确保用户不能重复收藏同一条消息

    def __str__(self):
        return f'{self.user.username} 收藏了 {self.message.title}'


class Like(models.Model):
    """点赞模型，记录用户点赞的消息"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '点赞'
        ordering = ['-created_at']
        unique_together = ('user', 'message')  # 确保用户不能重复点赞同一条消息

    def __str__(self):
        return f'{self.user.username} 点赞了 {self.message.title}'


class Notification(models.Model):
    """通知模型，用于消息通知系统"""
    NOTIFICATION_TYPES = (
        ('like', '点赞'),
        ('comment', '评论'),
        ('favorite', '收藏'),
        ('follow', '关注'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    target = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name_plural = '通知'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.actor.username} {dict(self.NOTIFICATION_TYPES).get(self.verb)} 了 {self.target.title if self.target else "内容"}'

    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
