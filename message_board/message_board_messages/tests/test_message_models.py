import pytest
from django.contrib.auth.models import User
from ..models import Message, Category, Tag, Favorite, Like


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


class TestMessageModel:
    """测试消息模型"""
    
    def test_message_creation(self, message):
        """测试消息创建"""
        assert message.title == '测试消息标题'
        assert message.slug == 'test-message'
        assert message.status == 'published'
        assert message.views == 0
        assert message.likes == 0
        assert message.comments_count == 0
    
    def test_increase_views(self, message):
        """测试增加浏览量"""
        initial_views = message.views
        message.increase_views()
        assert message.views == initial_views + 1
    
    def test_increase_likes(self, message):
        """测试增加点赞数"""
        initial_likes = message.likes
        message.increase_likes()
        assert message.likes == initial_likes + 1


class TestCategoryModel:
    """测试分类模型"""
    
    def test_category_creation(self, category):
        """测试分类创建"""
        assert category.name == '测试分类'
        assert category.slug == 'test-category'


class TestTagModel:
    """测试标签模型"""
    
    def test_tag_creation(self, tag):
        """测试标签创建"""
        assert tag.name == '测试标签'
        assert tag.slug == 'test-tag'


class TestFavoriteModel:
    """测试收藏模型"""
    
    def test_favorite_creation(self, user, message):
        """测试收藏创建"""
        favorite = Favorite.objects.create(
            user=user,
            message=message
        )
        assert favorite.user == user
        assert favorite.message == message
    
    def test_favorite_uniqueness(self, user, message):
        """测试收藏唯一性"""
        # 创建第一个收藏
        Favorite.objects.create(
            user=user,
            message=message
        )
        # 尝试创建相同的收藏，应该会失败
        with pytest.raises(Exception):
            Favorite.objects.create(
                user=user,
                message=message
            )


class TestLikeModel:
    """测试点赞模型"""
    
    def test_like_creation(self, user, message):
        """测试点赞创建"""
        like = Like.objects.create(
            user=user,
            message=message
        )
        assert like.user == user
        assert like.message == message
    
    def test_like_uniqueness(self, user, message):
        """测试点赞唯一性"""
        # 创建第一个点赞
        Like.objects.create(
            user=user,
            message=message
        )
        # 尝试创建相同的点赞，应该会失败
        with pytest.raises(Exception):
            Like.objects.create(
                user=user,
                message=message
            )
