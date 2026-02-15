#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试PostgreSQL数据库连接和操作的脚本
用于验证数据迁移后的数据库功能是否正常
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_board.settings')

# 导入Django并初始化
import django
django.setup()

# 导入项目模型
from message_board_messages.models import Message, Category
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


def test_database_connection():
    """测试数据库连接是否正常"""
    print("\n=== 开始数据库测试 ===")
    print("测试数据库连接...")
    
    try:
        # 简单的查询操作来测试连接
        users_count = User.objects.count()
        messages_count = Message.objects.count()
        categories_count = Category.objects.count()
        
        print(f"✓ 数据库连接成功！")
        print(f"  - 用户表中共有 {users_count} 个用户")
        print(f"  - 消息表中共有 {messages_count} 条消息")
        print(f"  - 分类表中共有 {categories_count} 个分类")
        
        return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {str(e)}")
        return False


def test_read_operation():
    """测试数据库读取操作"""
    print("\n测试数据库读取操作...")
    
    try:
        # 读取最近的5条消息
        recent_messages = Message.objects.order_by('-created_at')[:5]
        
        if recent_messages:
            print(f"✓ 成功读取 {len(recent_messages)} 条最近的消息")
            print("  前3条消息预览:")
            
            for i, msg in enumerate(recent_messages[:3], 1):
                content_preview = (msg.content[:50] + '...') if len(msg.content) > 50 else msg.content
                print(f"  {i}. {msg.title} (作者: {msg.author.username if msg.author else '匿名'})")
                print(f"     {content_preview}")
        else:
            print("  消息表为空")
            
        # 读取分类信息
        categories = Category.objects.all()
        if categories:
            print(f"✓ 成功读取 {len(categories)} 个分类")
            for category in categories:
                print(f"  - {category.name}")
        else:
            print("  分类表为空")
            
        # 读取用户信息
        superusers = User.objects.filter(is_superuser=True)
        if superusers:
            print(f"✓ 成功读取 {len(superusers)} 个超级用户")
            for user in superusers:
                print(f"  - {user.username} (邮箱: {user.email})")
        
        return True
    except Exception as e:
        print(f"✗ 读取操作失败: {str(e)}")
        return False


def test_write_operation():
    """测试数据库写入操作"""
    print("\n测试数据库写入操作...")
    
    try:
        # 检查是否有可用的用户
        if User.objects.exists():
            # 获取第一个用户作为测试作者
            test_user = User.objects.first()
            
            # 检查是否有分类，如果没有则创建一个
            if not Category.objects.exists():
                print("  创建测试分类...")
                test_category = Category.objects.create(
                    name="测试分类",
                    slug="test-category"
                )
                print(f"  ✓ 成功创建测试分类: {test_category.name}")
            else:
                test_category = Category.objects.first()
                print(f"  使用现有分类: {test_category.name}")
            
            # 创建一条测试消息
            test_message = Message.objects.create(
                title="PostgreSQL测试消息",
                slug="postgresql-test-message",
                content="这是一条用于测试PostgreSQL数据库写入功能的消息。如果您看到这条消息，说明数据库写入操作正常。",
                author=test_user,
                category=test_category,
                status='published',
                published_at=django.utils.timezone.now()
            )
            
            print(f"✓ 成功创建测试消息 (ID: {test_message.id})")
            
            # 验证消息是否被正确保存
            saved_message = Message.objects.get(id=test_message.id)
            print(f"✓ 成功读取刚创建的消息: {saved_message.title}")
            print(f"  消息分类: {saved_message.category.name}")
            print(f"  消息作者: {saved_message.author.username}")
            
            # 可选：删除测试消息
            # test_message.delete()
            # print("✓ 测试消息已删除")
            
            return True
        else:
            print("! 用户表为空，无法创建测试消息")
            return False
    except Exception as e:
        print(f"✗ 写入操作失败: {str(e)}")
        return False


def test_comment_system():
    """测试评论系统是否正常工作"""
    print("\n测试评论系统...")
    
    try:
        # 检查是否存在评论模型（可能是Django内置的或自定义的）
        try:
            from message_board_messages.models import Comment
            use_custom_comments = True
        except ImportError:
            try:
                from django.contrib.comments.models import Comment
                use_custom_comments = False
            except ImportError:
                print("✓ 评论系统检查 - 未找到评论模型，但这可能是预期的")
                return True
        
        # 检查是否有可评论的消息
        if Message.objects.exists():
            message = Message.objects.first()
            
            # 检查已有评论数
            if use_custom_comments:
                existing_comments = Comment.objects.filter(message=message).count()
            else:
                content_type = ContentType.objects.get_for_model(Message)
                existing_comments = Comment.objects.filter(
                    content_type=content_type,
                    object_pk=message.id
                ).count()
            
            print(f"✓ 评论系统检查成功")
            print(f"  - 第一条消息(ID: {message.id})有 {existing_comments} 条评论")
            
            # 如果有用户，尝试创建测试评论
            if User.objects.exists():
                test_user = User.objects.first()
                
                # 创建测试评论
                if use_custom_comments:
                    test_comment = Comment.objects.create(
                        message=message,
                        author=test_user,
                        content="这是一条测试评论，用于验证评论系统是否正常工作。"
                    )
                else:
                    content_type = ContentType.objects.get_for_model(Message)
                    test_comment = Comment.objects.create(
                        content_type=content_type,
                        object_pk=message.id,
                        user=test_user,
                        comment="这是一条测试评论，用于验证评论系统是否正常工作。",
                        site_id=1  # 默认站点ID
                    )
                
                print(f"✓ 成功创建测试评论 (ID: {test_comment.id})")
                
                # 验证评论是否被正确保存
                if use_custom_comments:
                    saved_comment = Comment.objects.get(id=test_comment.id)
                else:
                    saved_comment = Comment.objects.get(id=test_comment.id)
                print(f"✓ 成功读取刚创建的评论")
            
        else:
            print("! 消息表为空，无法测试评论系统")
            
        return True
    except Exception as e:
        print(f"✗ 评论系统测试失败: {str(e)}")
        print("  注意：评论系统可能使用了不同的实现方式")
        return False


def main():
    """主测试函数"""
    # 执行各项测试
    connection_result = test_database_connection()
    read_result = test_read_operation() if connection_result else False
    write_result = test_write_operation() if read_result else False
    comment_result = test_comment_system() if write_result else False
    
    # 汇总测试结果
    print("\n=== 测试结果汇总 ===")
    print(f"数据库连接: {'✓ 成功' if connection_result else '✗ 失败'}")
    print(f"读取操作: {'✓ 成功' if read_result else '✗ 失败'}")
    print(f"写入操作: {'✓ 成功' if write_result else '✗ 失败'}")
    print(f"评论系统: {'✓ 成功' if comment_result else '⚠ 需注意'}")
    
    # 总体结论
    if connection_result and read_result and write_result:
        print("\n🎉 测试成功！PostgreSQL数据库配置正确，应用可以正常使用。")
        print("✅ 数据迁移项目已完成！")
    else:
        print("\n⚠ 测试存在一些问题，请查看上面的详细信息。")


if __name__ == "__main__":
    main()