#!/usr/bin/env python
"""数据库初始化脚本
用于创建PostgreSQL数据库并设置必要的权限
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 数据库连接参数
DB_CONFIG = {
    'user': 'WYZ',
    'password': '193249831',
    'host': 'localhost',
    'port': '5432'
}

# 要创建的数据库名称
DB_NAME = 'message_board'


def create_database():
    """创建数据库并设置权限"""
    try:
        # 首先连接到默认的postgres数据库
        conn = psycopg2.connect(
            dbname='postgres',
            **DB_CONFIG
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        print(f"正在检查数据库 '{DB_NAME}' 是否存在...")
        # 检查数据库是否已经存在
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            # 创建数据库
            print(f"创建数据库 '{DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"数据库 '{DB_NAME}' 已创建成功")
        else:
            print(f"数据库 '{DB_NAME}' 已存在")
        
        # 授予权限
        print(f"为用户 '{DB_CONFIG['user']}' 授予权限...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_CONFIG['user']}")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        # 连接到新创建的数据库以设置schema权限
        print(f"连接到数据库 '{DB_NAME}' 设置schema权限...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            **DB_CONFIG
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 授予public schema的权限
        cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO CURRENT_USER")
        print("已授予public schema的所有权限")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        raise


if __name__ == '__main__':
    print("开始数据库初始化...")
    create_database()