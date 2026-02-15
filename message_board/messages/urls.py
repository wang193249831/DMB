from django.urls import path
from . import views

app_name = 'message_board_messages'

urlpatterns = [
    path('', views.message_list, name='message_list'),
    path('<int:pk>/', views.message_detail, name='message_detail'),
    path('create/', views.message_create, name='message_create'),
    path('<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('<int:pk>/delete/', views.message_delete, name='message_delete'),
    path('<int:pk>/like/', views.like_message, name='like_message'),
    path('category/<slug:slug>/', views.category_messages, name='category_messages'),
    path('tag/<slug:slug>/', views.tag_messages, name='tag_messages'),
]