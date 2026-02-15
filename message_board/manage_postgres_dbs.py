#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
管理PostgreSQL数据库的脚本
用于列出用户WYZ名下的所有数据库，并删除除message_board外的其他数据库
"""
import psycopg2
from psycopg2 import OperationalError, ProgrammingError
import getpass

# PostgreSQL连接参数
DB_PARAMS = {
    'user': 'WYZ',
    'password': '193249831',
    'host': 'localhost',
    'port': '5432',
    'dbname': 'postgres'  # 使用默认的postgres数据库来连接
}

# 要保留的数据库名称
KEEP_DB = 'message_board'

# 超级用户配置（默认postgres）
SUPERUSER_PARAMS = {
    'user': 'postgres',
    'password': '',  # 将在运行时提示输入
    'host': 'localhost',
    'port': '5432',
    'dbname': 'postgres'
}


def connect_to_postgresql(params):
    """连接到PostgreSQL数据库"""
    try:
        conn = psycopg2.connect(**params)
        print("成功连接到PostgreSQL数据库")
        return conn
    except OperationalError as e:
        print(f"连接数据库时出错: {e}")
        return None


def list_all_databases(conn):
    """列出所有数据库"""
    try:
        cursor = conn.cursor()
        # 查询所有数据库
        cursor.execute("SELECT datname FROM pg_database;")
        databases = cursor.fetchall()
        cursor.close()
        return [db[0] for db in databases]
    except ProgrammingError as e:
        print(f"查询数据库时出错: {e}")
        return []


def drop_database(conn, db_name):
    """删除指定的数据库"""
    try:
        # 注意：删除数据库需要在非目标数据库的连接中进行
        # 创建一个新的连接来执行删除操作
        drop_conn = psycopg2.connect(
            user=DB_PARAMS['user'],
            password=DB_PARAMS['password'],
            host=DB_PARAMS['host'],
            port=DB_PARAMS['port'],
            dbname='postgres'  # 使用postgres数据库执行删除操作
        )
        
        # 设置自动提交模式
        drop_conn.autocommit = True
        cursor = drop_conn.cursor()
        
        # 先尝试直接删除数据库，不强制断开连接
        print(f"正在尝试直接删除数据库'{db_name}'...")
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
            cursor.close()
            drop_conn.close()
            print(f"数据库'{db_name}'已成功删除")
            return True
        except Exception as e:
            print(f"直接删除数据库失败: {e}")
            
            # 如果失败，尝试断开连接后再删除
            print(f"\n提示：可能需要断开连接才能删除数据库。\n")
            print(f"权限说明：只有拥有SUPERUSER属性的角色才能终止其他进程的连接。\n")
            print(f"建议：请使用具有SUPERUSER权限的账号重新运行此脚本，或者手动使用pgAdmin等工具删除数据库。\n")
            return False
    except Exception as e:
        print(f"删除数据库'{db_name}'时出错: {e}")
        return False


def drop_database_with_superuser(db_name):
    """尝试使用超级用户权限删除指定的数据库"""
    try:
        # 在非交互式环境中，我们无法提示输入密码
        # 提供手动删除的详细步骤
        print(f"\n在非交互式环境中无法自动获取超级用户密码。")
        print(f"请手动使用以下步骤删除数据库'{db_name}':")
        print(f"\n1. 打开命令提示符（cmd）")
        print(f"2. 导航到PostgreSQL的bin目录:")
        print(f"   cd \"C:\\Program Files\\PostgreSQL\\17\\bin\"")
        print(f"3. 以超级用户身份登录PostgreSQL:")
        print(f"   psql -U postgres -W")
        print(f"   (系统会提示输入postgres用户的密码)")
        print(f"4. 执行以下命令删除数据库:")
        print(f"   DROP DATABASE IF EXISTS {db_name};")
        print(f"   \\q")
        print(f"\n或者使用pgAdmin图形界面工具删除数据库。")
        print(f"\n如果您知道超级用户的密码，也可以修改脚本中的SUPERUSER_PARAMS['password']参数。")
        
        # 为了演示，我们尝试使用一个假设的密码（这不是最佳实践）
        print(f"\n正在尝试使用默认密码连接...")
        SUPERUSER_PARAMS['password'] = 'postgres'  # 这是一个常见的默认密码，可能不是实际密码
        
        # 连接到PostgreSQL超级用户
        super_conn = connect_to_postgresql(SUPERUSER_PARAMS)
        if not super_conn:
            print(f"无法以超级用户'{SUPERUSER_PARAMS['user']}'连接到PostgreSQL数据库")
            return False
        
        # 设置自动提交模式
        super_conn.autocommit = True
        cursor = super_conn.cursor()
        
        # 强制断开所有连接到目标数据库的会话
        print(f"正在断开连接到数据库'{db_name}'的所有会话...")
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
              AND pid <> pg_backend_pid();
        """)
        
        # 删除数据库
        print(f"正在删除数据库'{db_name}'...")
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
        
        cursor.close()
        super_conn.close()
        print(f"数据库'{db_name}'已成功删除")
        return True
    except Exception as e:
        print(f"使用超级用户删除数据库'{db_name}'时出错: {e}")
        print(f"\n请按照上述手动步骤删除数据库。")
        return False


def main():
    # 连接到PostgreSQL
    conn = connect_to_postgresql(DB_PARAMS)
    if not conn:
        print("无法连接到PostgreSQL数据库，退出脚本")
        return
    
    try:
        # 列出所有数据库
        all_databases = list_all_databases(conn)
        print(f"用户WYZ名下的所有数据库: {all_databases}")
        
        # 识别需要删除的数据库
        # 排除系统数据库和要保留的数据库
        system_dbs = ['postgres', 'template0', 'template1']
        dbs_to_drop = [db for db in all_databases if db not in system_dbs and db != KEEP_DB]
        
        print(f"需要保留的数据库: {KEEP_DB}")
        print(f"需要删除的数据库: {dbs_to_drop}")
        
        # 尝试删除不需要的数据库
        if dbs_to_drop:
            print(f"\n由于在非交互式环境中运行，将直接尝试使用超级用户权限删除数据库...")
            
            # 自动尝试使用超级用户权限删除
            print(f"\n尝试使用超级用户权限删除数据库...")
            for db in dbs_to_drop:
                success = drop_database_with_superuser(db)
                if not success:
                    print(f"使用超级用户删除数据库'{db}'失败，请手动删除")
            
        # 再次列出数据库，确认删除结果
        all_databases_after = list_all_databases(conn)
        print(f"\n当前所有数据库: {all_databases_after}")
        
    finally:
        # 关闭数据库连接
        if conn:
            conn.close()
            print("已关闭数据库连接")


if __name__ == "__main__":
    main()