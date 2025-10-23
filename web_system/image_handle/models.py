from django.db import models


class CheckModel(models.Model):
    content = models.TextField(verbose_name='内容')
    pred_name = models.CharField(max_length=100, verbose_name='预测结果')
    check_time = models.DateTimeField(auto_now_add=True, verbose_name='检测时间')

    class Meta:
        db_table = 'db_check'
        verbose_name = '文本检测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    content = models.TextField( verbose_name='检测文本')
    sentiment = models.CharField(max_length=50, verbose_name='情感分析结果')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '文件上传检测结果'
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.content

        return f"{self.file_name} - {self.sentiment}"
# models.py
from django.db import models

class TextEmotionAnalysisResult(models.Model):
    text = models.TextField(verbose_name='原始文本')  # 原始文本
    main_emotion = models.CharField(max_length=50,verbose_name='主要情感')  # 主要情感
    sentiment = models.CharField(max_length=50,verbose_name='情感类别')  # 情感类别
    confidence = models.IntegerField(verbose_name='置信度')  # 置信度
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')  # 创建时间
    class Meta:
        verbose_name = '文本检测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.text[:50]}... - {self.sentiment}"


class FileEmotionAnalysisResult(models.Model):
    file_name = models.CharField(max_length=255,verbose_name='文件名称')  # 上传的文件名称
    text = models.TextField()  # 原始文本
    main_emotion = models.CharField(max_length=50,verbose_name='主要情感')  # 主要情感
    sentiment = models.CharField(max_length=50,verbose_name='情感类别')  # 情感类别
    confidence = models.IntegerField(verbose_name='置信度')  # 置信度
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')  # 创建时间
    class Meta:
        verbose_name = '文件批量检测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.file_name} - {self.sentiment}"