from django.db import models
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
    slug = models.SlugField(max_length=200, unique_for_date='published_at')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='messages')
    tags = models.ManyToManyField(Tag, blank=True, related_name='messages')
    content = CKEditor5Field()
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = '消息'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def increase_views(self):
        """增加浏览量"""
        self.views += 1
        self.save(update_fields=['views'])

    def increase_likes(self):
        """增加点赞数"""
        self.likes += 1
        self.save(update_fields=['likes'])


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


class MessageComment(models.Model):
    """评论模型"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} 评论了 {self.message.title}'

    def save(self, *args, **kwargs):
        # 当评论被保存时，更新消息的评论计数
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.message.comments_count += 1
            self.message.save(update_fields=['comments_count'])

    def delete(self, *args, **kwargs):
        # 当评论被删除时，更新消息的评论计数
        self.message.comments_count -= 1
        self.message.save(update_fields=['comments_count'])
        super().delete(*args, **kwargs)
