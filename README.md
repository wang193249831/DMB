# Django消息发布平台

## 项目概述
这是一个基于Django框架开发的消息发布平台，允许用户创建、编辑、发布和管理各类消息内容。该平台支持用户认证、消息分类、评论互动、标签管理等功能，并提供了响应式设计，确保在不同设备上都能获得良好的用户体验。

## 功能特点
- **用户认证系统**：注册、登录、登出、密码重置、个人资料管理
- **消息管理**：创建、编辑、删除、发布消息，支持富文本编辑器
- **分类与标签**：消息分类管理，支持多标签标注
- **互动功能**：评论、点赞、收藏消息
  - 评论系统：用户可以在消息详情页添加评论，评论会实时显示
  - 点赞功能：登录用户可以对消息进行点赞，系统会记录点赞数
  - 收藏功能：登录用户可以收藏感兴趣的消息
- **搜索功能**：按标题、内容、标签等搜索消息
- **权限控制**：基于角色的访问控制(RBAC)
- **响应式设计**：适配手机、平板和桌面设备
- **后台管理**：Django Admin定制版，方便内容管理
- **SEO优化**：支持自定义meta标签，优化搜索引擎排名
- **数据统计**：消息阅读量、点赞数等数据统计

## 技术栈
- **后端**：Python 3.9+, Django 4.2+
- **数据库**：SQLite (开发), PostgreSQL (生产)
- **前端**：HTML5, CSS3, JavaScript, Bootstrap 5
- **富文本编辑器**：CKEditor/TinyMCE
- **认证**：Django内置认证系统
- **搜索**：Django Haystack + Elasticsearch
- **部署**：Docker, Nginx, Gunicorn

## 安装指南

###  prerequisites
- Python 3.9+
- pip
- virtualenv (推荐)
- PostgreSQL (生产环境)

### 本地开发环境设置
1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/django-message-board.git
   cd django-message-board
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   # Windows激活
   venv\Scripts\activate
   # macOS/Linux激活
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   创建`.env`文件，添加以下内容：
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=message_board
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

7. **运行开发服务器**
   ```bash
   python manage.py runserver
   ```
   访问 http://localhost:8000/ 查看网站，访问 http://localhost:8000/admin/ 进入后台管理。

## 使用说明

### 用户功能
- **注册/登录**：在首页点击"注册"或"登录"按钮
- **创建消息**：登录后，点击导航栏的"发布消息"按钮
- **编辑消息**：在消息详情页点击"编辑"按钮
- **评论消息**：在消息详情页下方评论区输入评论内容，点击提交
- **点赞消息**：登录后，在消息详情页点击"点赞"按钮
- **收藏消息**：登录后，在消息详情页点击"收藏"按钮
- **管理个人资料**：点击右上角用户名，选择"个人资料"
- **查看收藏**：点击导航栏的"我的收藏"查看已收藏的消息

### 管理员功能
- **后台管理**：登录超级用户后，访问 http://localhost:8000/admin/
- **管理用户**：在后台管理中选择"用户"进行管理
- **管理消息**：在后台管理中选择"消息"进行管理
- **管理分类**：在后台管理中选择"分类"进行管理

## 最近更新
- 修复了点赞功能，添加了登录验证和成功提示
- 实现了完整的评论系统，包括添加评论和显示评论列表
- 优化了消息详情页，删除了重复的评论区域
- 修复了views.py文件中的代码重复和缩进错误

## 部署步骤

### 使用Docker部署
1. **构建Docker镜像**
   ```bash
   docker-compose build
   ```

2. **运行Docker容器**
   ```bash
   docker-compose up -d
   ```

3. **数据库迁移(容器内)**
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

4. **创建超级用户(容器内)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### 传统部署
1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置生产环境**
   修改`settings.py`文件：
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'message_board',
           'USER': 'postgres',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **收集静态文件**
   ```bash
   python manage.py collectstatic
   ```

4. **配置Nginx**
   创建Nginx配置文件：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /path/to/static/;
       }

       location /media/ {
           alias /path/to/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **使用Gunicorn运行应用**
   ```bash
   gunicorn --bind 127.0.0.1:8000 message_board.wsgi:application
   ```

## 项目结构
```
message_board/
├── message_board/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── messages/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── comments/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
├── media/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

## 贡献指南
1. Fork 本项目
2. 创建特性分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -am 'Add some feature'`
4. 推送到分支: `git push origin feature/new-feature`
5. 提交Pull Request

## 许可证
本项目采用MIT许可证 - 详情请见LICENSE文件