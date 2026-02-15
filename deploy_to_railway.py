#!/usr/bin/env python3
"""
自动化部署Django项目到Railway平台
"""
import os
import subprocess
import sys
import json


def run_command(command, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True
        )
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            return False
        print(f"成功: {result.stdout}")
        return True
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False


def update_settings():
    """更新settings.py文件，添加环境变量支持"""
    settings_path = "message_board/message_board/settings.py"
    if not os.path.exists(settings_path):
        print(f"错误: {settings_path} 文件不存在")
        return False

    # 读取现有设置
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 更新数据库配置
    if "DATABASES" in content:
        # 保留现有数据库配置，添加环境变量支持
        if "import dj_database_url" not in content:
            # 在文件顶部添加导入
            content = "import dj_database_url\n" + content

        # 替换数据库配置
        if "'default':" in content:
            # 替换数据库配置
            old_db_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'message_board',
        'USER': 'postgre',
        'PASSWORD': '193249831',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}'''
            new_db_config = '''# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}'''
            content = content.replace(old_db_config, new_db_config)

    # 更新LANGUAGE_CODE和TIME_ZONE
    content = content.replace("LANGUAGE_CODE = 'zh-hans'", "LANGUAGE_CODE = 'zh-hans'")
    content = content.replace("TIME_ZONE = 'Asia/Shanghai'", "TIME_ZONE = 'Asia/Shanghai'")

    # 更新ALLOWED_HOSTS
    if "ALLOWED_HOSTS = []" in content:
        content = content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']")

    # 更新SECRET_KEY
    if "SECRET_KEY = 'django-insecure-#t7qg5$%&amp;*()_+qwertyuiopasdfghjklzxcvbnm'" in content:
        content = content.replace(
            "SECRET_KEY = 'django-insecure-#t7qg5$%&amp;*()_+qwertyuiopasdfghjklzxcvbnm'",
            "SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-#t7qg5$%&amp;*()_+qwertyuiopasdfghjklzxcvbnm')"
        )

    # 添加os导入
    if "import os" not in content:
        content = "import os\n" + content

    # 写入更新后的设置
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"更新 {settings_path} 成功")
    return True


def update_requirements():
    """更新requirements.txt文件，确保包含所有必要的依赖"""
    requirements_path = "requirements.txt"
    if not os.path.exists(requirements_path):
        print(f"错误: {requirements_path} 文件不存在")
        return False

    # 读取现有依赖
    with open(requirements_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 添加缺失的依赖
    dependencies = [
        "gunicorn>=20.1.0,<21.0.0",  # WSGI服务器
        "dj-database-url>=2.1.0,<3.0.0",  # 数据库URL解析
        "psycopg2-binary>=2.9.9,<3.0.0",  # PostgreSQL适配器
    ]

    for dep in dependencies:
        dep_name = dep.split('>')[0].strip()
        if dep_name not in content:
            content += f"\n{dep}"

    # 写入更新后的依赖
    with open(requirements_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"更新 {requirements_path} 成功")
    return True


def main():
    """主函数"""
    print("=== 开始部署Django项目到Railway ===")
    print()

    # 更新settings.py
    print("1. 更新settings.py文件")
    if not update_settings():
        print("更新settings.py失败")
        return 1

    # 更新requirements.txt
    print("2. 更新requirements.txt文件")
    if not update_requirements():
        print("更新requirements.txt失败")
        return 1

    # 添加所有文件到Git
    print("3. 添加所有文件到Git")
    if not run_command("git add ."):
        print("添加文件到Git失败")
        return 1

    # 提交更改
    print("4. 提交更改")
    if not run_command('git commit -m "部署到Railway: 更新配置"'):
        print("提交更改失败")
        return 1

    # 推送更改到GitHub
    print("5. 推送更改到GitHub")
    if not run_command("git push origin master"):
        print("推送更改到GitHub失败")
        return 1

    # 提示用户在Railway上部署
    print()
    print("=== 在Railway上完成部署 ===")
    print()
    print("请按照以下步骤在Railway上完成部署:")
    print()
    print("1. 登录Railway")
    print("   - 访问 https://railway.app/")
    print("   - 登录您的账户")
    print()
    print("2. 创建新项目")
    print("   - 点击 'New Project'")
    print("   - 选择 'Deploy from GitHub repo'")
    print("   - 选择您的仓库: wang193249831/DMB")
    print("   - 点击 'Deploy'")
    print()
    print("3. 配置环境变量")
    print("   - 在项目页面，点击 'Variables'")
    print("   - 添加以下环境变量:")
    print("     - SECRET_KEY: 生成一个安全的密钥")
    print("     - DEBUG: false")
    print("     - PYTHON_VERSION: 3.11")
    print()
    print("4. 配置数据库")
    print("   - Railway会自动创建PostgreSQL数据库")
    print("   - 数据库连接字符串会自动设置为DATABASE_URL环境变量")
    print()
    print("5. 等待部署完成")
    print("   - Railway会自动执行构建和部署步骤")
    print("   - 部署完成后，您会获得一个URL")
    print()
    print("6. 访问部署后的应用")
    print("   - 通过Railway提供的URL访问您的Django应用")
    print()
    print("=== 部署完成！===")

    return 0


if __name__ == "__main__":
    sys.exit(main())
