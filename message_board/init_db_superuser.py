#!/usr/bin/env python
"""修改版数据库初始化脚本
使用postgres超级用户创建数据库和用户
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# PostgreSQL超级用户连接参数
SUPERUSER_CONFIG = {
    'user': 'postgres',  # PostgreSQL超级用户
    'password': '',      # 超级用户密码，如果设置了的话
    'host': 'localhost',
    'port': '5432'
}

# 要创建的数据库和用户信息
DB_NAME = 'message_board'
DB_USER = 'WYZ'
DB_PASSWORD = '193249831'


def create_database_and_user():
    """使用postgres超级用户创建数据库和用户"""
    try:
        print("开始数据库初始化...")
        
        # 连接到默认的postgres数据库
        print("连接到PostgreSQL服务器...")
        conn = psycopg2.connect(
            dbname='postgres',
            **SUPERUSER_CONFIG
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # 检查用户是否存在
        print(f"检查用户 '{DB_USER}' 是否存在...")
        cursor.execute("SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = %s", (DB_USER,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            # 创建用户
            print(f"创建用户 '{DB_USER}'...")
            cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD %s", (DB_PASSWORD,))
            print(f"用户 '{DB_USER}' 已创建成功")
        else:
            print(f"用户 '{DB_USER}' 已存在")
        
        # 检查数据库是否存在
        print(f"检查数据库 '{DB_NAME}' 是否存在...")
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        db_exists = cursor.fetchone()
        
        if not db_exists:
            # 创建数据库
            print(f"创建数据库 '{DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}")
            print(f"数据库 '{DB_NAME}' 已创建成功")
        else:
            # 更新数据库所有者
            print(f"更新数据库 '{DB_NAME}' 的所有者为 '{DB_USER}'...")
            cursor.execute(f"ALTER DATABASE {DB_NAME} OWNER TO {DB_USER}")
        
        # 授予权限
        print(f"为用户 '{DB_USER}' 授予权限...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("数据库初始化完成！")
        
    except psycopg2.OperationalError as e:
        print(f"连接PostgreSQL服务器失败: {e}")
        print("可能原因:")
        print("1. PostgreSQL服务未启动")
        print("2. 超级用户密码不正确")
        print("3. 连接参数有误")
        raise
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        raise


if __name__ == '__main__':
    create_database_and_user()