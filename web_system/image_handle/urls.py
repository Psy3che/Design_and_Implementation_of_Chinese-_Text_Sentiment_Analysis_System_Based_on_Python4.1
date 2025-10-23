from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # 确保正确导入了views

app_name = 'image_handle'

urlpatterns = [
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


    # path('', include('web_system.urls')),  # 确保只包含一次
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)