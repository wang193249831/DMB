# Django消息发布平台 - Docker容器化部署指南

## 前提条件
- 已安装Docker和Docker Compose

## 快速启动

1. **克隆代码库**
   ```bash
   git clone <repository-url>
   cd message_board
   ```

2. **构建并启动容器**
   ```bash
   docker-compose up --build
   ```

3. **创建数据库迁移**
   在新的终端中运行:
   ```bash
   docker-compose exec web python message_board/manage.py makemigrations
   docker-compose exec web python message_board/manage.py migrate
   ```

4. **创建超级用户**
   ```bash
   docker-compose exec web python message_board/manage.py createsuperuser
   ```

5. **访问应用**
   打开浏览器，访问 http://localhost:8000

## 容器化配置说明

### Dockerfile
- 使用Python 3.10-slim-bullseye作为基础镜像
- 安装必要的系统依赖和Python依赖
- 复制项目文件并收集静态文件
- 暴露8000端口并设置默认运行命令

### docker-compose.yml
- 定义了两个服务: web(应用)和db(PostgreSQL数据库)
- 配置了数据卷以持久化存储数据库数据、静态文件和媒体文件
- 设置了环境变量文件和端口映射

### .env文件
- 存储Django配置和数据库连接信息
- 包含SECRET_KEY、DEBUG模式、允许的主机和数据库连接字符串

### .dockerignore
- 指定构建镜像时应忽略的文件和目录
- 包括Python缓存文件、数据库文件、媒体文件和日志文件等

## 常见问题

### 1. 如何停止容器?
```bash
docker-compose down
```

### 2. 如何查看应用日志?
```bash
docker-compose logs -f web
```

### 3. 如何重新构建镜像?
```bash
docker-compose build
```

### 4. 如何在生产环境中运行?
- 修改.env文件中的DEBUG=False
- 配置ALLOWED_HOSTS为你的域名
- 考虑使用Nginx作为反向代理
- 使用Gunicorn或uWSGI代替Django开发服务器

## 注意事项
- 本配置适用于开发环境，生产环境需要额外的安全配置
- 定期备份数据库数据卷以防止数据丢失
- 确保在生产环境中使用强密码和安全的SECRET_KEY