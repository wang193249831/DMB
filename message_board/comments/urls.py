from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # 添加评论
    path('message/<int:message_id>/add/', views.add_comment, name='add_comment'),
]