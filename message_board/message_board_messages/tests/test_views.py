import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Message, Category, Tag


@pytest.fixture
def client():
    """创建测试客户端"""
    return Client()


@pytest.fixture
def user():
    """创建测试用户"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword'
    )


@pytest.fixture
def category():
    """创建测试分类"""
    return Category.objects.create(
        name='测试分类',
        slug='test-category'
    )


@pytest.fixture
def tag():
    """创建测试标签"""
    return Tag.objects.create(
        name='测试标签',
        slug='test-tag'
    )


@pytest.fixture
def message(user, category, tag):
    """创建测试消息"""
    message = Message.objects.create(
        title='测试消息标题',
        slug='test-message',
        author=user,
        category=category,
        content='测试消息内容',
        status='published'
    )
    message.tags.add(tag)
    return message


class TestMessageViews:
    """测试消息视图"""
    
    def test_home_view(self, client):
        """测试首页视图"""
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200
        assert 'latest_messages' in response.context
    
    def test_message_list_view(self, client, message):
        """测试消息列表视图"""
        url = reverse('message_board_messages:message_list')
        response = client.get(url)
        assert response.status_code == 200
        assert 'messages' in response.context
    
    def test_message_detail_view(self, client, message):
        """测试消息详情视图"""
        url = reverse('message_board_messages:message_detail', args=[message.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'message' in response.context
        assert 'related_messages' in response.context
        assert 'comments' in response.context
    
    def test_message_create_view_not_logged_in(self, client):
        """测试未登录用户访问创建消息视图"""
        url = reverse('message_board_messages:message_create')
        response = client.get(url)
        # 未登录用户应该被重定向到登录页面
        assert response.status_code == 302
        assert 'login' in response.url
    
    def test_message_create_view_logged_in(self, client, user, category):
        """测试登录用户访问创建消息视图"""
        client.login(username='testuser', password='testpassword')
        url = reverse('message_board_messages:message_create')
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_category_messages_view(self, client, category, message):
        """测试按分类查看消息视图"""
        url = reverse('message_board_messages:category_messages', args=[category.slug])
        response = client.get(url)
        assert response.status_code == 200
        assert 'messages' in response.context
        assert 'category' in response.context
    
    def test_tag_messages_view(self, client, tag, message):
        """测试按标签查看消息视图"""
        url = reverse('message_board_messages:tag_messages', args=[tag.slug])
        response = client.get(url)
        assert response.status_code == 200
        assert 'messages' in response.context
        assert 'tag' in response.context


class TestUserViews:
    """测试用户相关视图"""
    
    def test_like_message_view_not_logged_in(self, client, message):
        """测试未登录用户访问点赞视图"""
        url = reverse('message_board_messages:like_message', args=[message.pk])
        response = client.post(url)
        # 未登录用户应该返回405错误
        assert response.status_code == 405
    
    def test_like_message_view_logged_in(self, client, user, message):
        """测试登录用户访问点赞视图"""
        client.login(username='testuser', password='testpassword')
        url = reverse('message_board_messages:like_message', args=[message.pk])
        response = client.post(url, format='json')
        assert response.status_code == 200
        assert response.json()['liked'] == True
    
    def test_favorite_message_view_not_logged_in(self, client, message):
        """测试未登录用户访问收藏视图"""
        url = reverse('message_board_messages:favorite_message', args=[message.pk])
        response = client.get(url)
        # 未登录用户应该被重定向到登录页面
        assert response.status_code == 302
        assert 'login' in response.url
    
    def test_favorite_message_view_logged_in(self, client, user, message):
        """测试登录用户访问收藏视图"""
        client.login(username='testuser', password='testpassword')
        url = reverse('message_board_messages:favorite_message', args=[message.pk])
        response = client.get(url)
        # 登录用户应该被重定向到消息详情页面
        assert response.status_code == 302
        assert 'message_detail' in response.url
    
    def test_favorite_list_view_not_logged_in(self, client):
        """测试未登录用户访问收藏列表视图"""
        url = reverse('message_board_messages:favorite_list')
        response = client.get(url)
        # 未登录用户应该被重定向到登录页面
        assert response.status_code == 302
        assert 'login' in response.url
    
    def test_favorite_list_view_logged_in(self, client, user):
        """测试登录用户访问收藏列表视图"""
        client.login(username='testuser', password='testpassword')
        url = reverse('message_board_messages:favorite_list')
        response = client.get(url)
        assert response.status_code == 200
        assert 'messages' in response.context
