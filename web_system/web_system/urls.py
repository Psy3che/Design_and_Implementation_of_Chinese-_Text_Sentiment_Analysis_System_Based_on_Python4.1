"""web_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.urls import path

from image_handle import views

urlpatterns = [
    path('', include('image_handle.urls', namespace='image_handle')),
                  path('', views.index, name='index'),
                  path('admin/', admin.site.urls),
                  path('check/', views.check, name='check'),
                  path('check_content/', views.check_content, name='check_content'),
                  path('text-analysis/', views.text_analysis, name='text_analysis'),
                  path('download/<path:file_path>', views.download_result),
                  path('upload-file-analysis/', views.file_analysis, name='upload_file_analysis'),
                  # path('upload/', views.upload_file, name='upload-file'),  # 保留核心功能路由
                  path('emotion-analysis/', views.emotion_analysis_view, name='emotion_analysis'),
                  path('batch-emotion-analysis/', views.batch_emotion_analysis_view, name='batch_emotion_analysis'),
                  path('check_content/', views.check_content, name='check_content'),
                  path('upload-file-analysis/', views.file_analysis, name='upload_file_analysis'),
                  path('download-file/<str:file_name>/', views.download_file, name='download_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

