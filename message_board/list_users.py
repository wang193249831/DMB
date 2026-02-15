#!/usr/bin/env python
"""
查看Django项目中所有用户数据和超级用户信息的脚本
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')

# 导入Django模块
import django
django.setup()

# 导入用户模型
from django.contrib.auth.models import User
from accounts.models import Profile


def list_all_users():
    """列出所有用户数据和超级用户信息"""
    print("\n=== Django项目用户信息 ===\n")
    
    # 获取所有用户
    all_users = User.objects.all()
    
    if not all_users:
        print("没有找到任何用户")
        return
    
    print(f"总用户数: {all_users.count()}\n")
    
    # 查找超级用户
    superusers = User.objects.filter(is_superuser=True)
    print(f"超级用户数: {superusers.count()}")
    
    if superusers:
        print("超级用户列表:")
        for user in superusers:
            print(f"- 用户名: {user.username}", end="")
            print(f", 邮箱: {user.email}", end="")
            print(f", 创建时间: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("没有找到超级用户")
    
    print("\n=== 所有用户详细信息 ===\n")
    
    # 遍历所有用户并显示详细信息
    for user in all_users:
        print(f"用户名: {user.username}")
        print(f"  - 邮箱: {user.email}")
        print(f"  - 全名: {user.first_name} {user.last_name}")
        print(f"  - 是否激活: {'是' if user.is_active else '否'}")
        print(f"  - 是否超级用户: {'是' if user.is_superuser else '否'}")
        print(f"  - 是否工作人员: {'是' if user.is_staff else '否'}")
        print(f"  - 创建时间: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  - 最后登录: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '从未登录'}")
        
        # 尝试获取用户的扩展资料
        try:
            profile = user.profile
            print(f"  - 个人简介: {profile.bio if profile.bio else '无'}")
            print(f"  - 网站: {profile.website if profile.website else '无'}")
            print(f"  - 头像: {'有' if profile.avatar else '无'}")
        except Profile.DoesNotExist:
            print("  - 没有扩展资料")
        
        print("------------------------")


if __name__ == '__main__':
    print("正在获取用户信息...")
    list_all_users()