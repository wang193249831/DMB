import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')
django.setup()

from message_board_messages.models import Category

# 创建初始分类
categories = [
    {'name': '技术', 'slug': 'technology'},
    {'name': '生活', 'slug': 'life'},
    {'name': '工作', 'slug': 'work'},
    {'name': '学习', 'slug': 'study'},
    {'name': '娱乐', 'slug': 'entertainment'},
]

for category in categories:
    try:
        Category.objects.create(**category)
        print(f"成功创建分类: {category['name']}")
    except Exception as e:
        print(f"创建分类 {category['name']} 失败: {e}")

print("初始分类创建完成！")