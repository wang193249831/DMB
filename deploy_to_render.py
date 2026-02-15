#!/usr/bin/env python3
"""
自动化部署Django项目到Render平台
"""
import os
import subprocess
import sys


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


def main():
    """主函数"""
    print("=== 开始部署Django项目到Render ===")
    print()

    # 检查Git是否初始化
    if not os.path.exists(".git"):
        print("1. 初始化Git仓库")
        if not run_command("git init"):
            print("初始化Git仓库失败")
            return 1
    else:
        print("1. Git仓库已初始化")

    # 检查.gitignore文件
    if not os.path.exists(".gitignore"):
        print("2. 创建.gitignore文件")
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class

# Django
*.log
local_settings.py

# Database
*.sqlite3

# Media files
media/

# Static files
staticfiles/

# IDE
.vscode/
.idea/

# Environment
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml
"""
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print(".gitignore文件创建成功")
    else:
        print("2. .gitignore文件已存在")

    # 添加所有文件到Git
    print("3. 添加所有文件到Git")
    if not run_command("git add ."):
        print("添加文件到Git失败")
        return 1

    # 提交更改
    print("4. 提交更改")
    if not run_command('git commit -m "部署到Render: 准备项目"'):
        print("提交更改失败")
        return 1

    # 提示用户创建GitHub仓库并推送代码
    print()
    print("=== 下一步操作 ===")
    print("请按照以下步骤在GitHub和Render上完成部署:")
    print()
    print("1. 登录GitHub，创建一个新的仓库")
    print("2. 复制仓库的SSH或HTTPS地址")
    print("3. 在终端中运行:")
    print("   git remote add origin <仓库地址>")
    print("   git push -u origin master")
    print()
    print("4. 登录Render (https://render.com/)")
    print("5. 点击 'New' -> 'From Git Repository'")
    print("6. 连接你的GitHub账户")
    print("7. 选择你的Django项目仓库")
    print("8. Render会自动检测render.yaml文件")
    print("9. 确认配置无误后，点击 'Create' 开始部署")
    print()
    print("=== 部署完成后 ===")
    print("部署完成后，Render会提供一个URL（如 'django-message-board.onrender.com'）")
    print("通过这个URL访问你的Django应用")
    print()
    print("=== 部署注意事项 ===")
    print("1. 首次部署可能需要5-10分钟")
    print("2. Render免费计划有运行时间限制（每月750小时）")
    print("3. 数据库有大小限制（1GB）")
    print("4. 确保ALLOWED_HOSTS环境变量包含Render分配的域名")

    return 0


if __name__ == "__main__":
    sys.exit(main())
