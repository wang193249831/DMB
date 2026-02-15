"""
URL configuration for message_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from message_board_messages.views import message_list

# Debug Toolbar URL配置
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
else:
    urlpatterns = []

urlpatterns += [
    path('admin/', admin.site.urls),
    # 首页
    path('', message_list, name='home'),
    # accounts应用
    path('accounts/', include('accounts.urls')),
    # messages应用
    path('messages/', include('message_board_messages.urls')),
    # django_ckeditor_5应用
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # 处理@vite/client请求，避免404错误
    path('@vite/client', lambda request: HttpResponse('')),
    # comments应用
    path('comments/', include('comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
