#!/usr/bin/env python3
"""
检查数据库中的已发布消息
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')
django.setup()

# 导入Message模型
from message_board_messages.models import Message

# 打印所有消息
print("=== 所有消息 ===")
all_messages = Message.objects.all()
print(f"总消息数: {all_messages.count()}")

for msg in all_messages:
    print(f"ID: {msg.id}")
    print(f"标题: {msg.title}")
    print(f"状态: {msg.status}")
    print(f"创建时间: {msg.created_at}")
    print(f"发布时间: {msg.published_at}")
    print(f"作者: {msg.author.username}")
    print("---")

# 打印已发布的消息
print("\n=== 已发布的消息 ===")
published_messages = Message.objects.filter(status='published')
print(f"已发布消息数: {published_messages.count()}")

for msg in published_messages:
    print(f"ID: {msg.id}")
    print(f"标题: {msg.title}")
    print(f"状态: {msg.status}")
    print(f"创建时间: {msg.created_at}")
    print(f"发布时间: {msg.published_at}")
    print(f"作者: {msg.author.username}")
    print("---")
