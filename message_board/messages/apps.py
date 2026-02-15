from django.apps import AppConfig


class MessagesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messages'
    verbose_name = '消息管理'
