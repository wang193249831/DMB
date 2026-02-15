from django.db import models
from django.conf import settings
from django.utils import timezone


class Comment(models.Model):
    # 关联到消息模型
    message = models.ForeignKey(
        'message_board_messages.Message',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 评论作者
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 评论内容
    content = models.TextField()
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 按创建时间倒序排列
        ordering = ['-created_at']

    def __str__(self):
        # 字符串表示，显示作者和评论的前20个字符
        return f'{self.author.username}: {self.content[:20]}...'


# 信号接收器，用于更新消息的评论计数
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Comment)
def update_message_comments_count(sender, instance, created, **kwargs):
    if created:
        # 增加消息的评论计数
        instance.message.comments_count += 1
        instance.message.save()


@receiver(post_delete, sender=Comment)
def decrease_message_comments_count(sender, instance, **kwargs):
    # 减少消息的评论计数
    instance.message.comments_count -= 1
    instance.message.save()
