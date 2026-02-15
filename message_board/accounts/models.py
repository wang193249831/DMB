from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # 与User模型一对一关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 头像
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)
    # 网站
    website = models.URLField(blank=True)
    # 注册时间（自动生成）
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新时间（自动更新）
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}的个人资料'


# 信号接收器：当User对象被创建时，自动创建对应的Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收器：当User对象被保存时，自动保存对应的Profile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
