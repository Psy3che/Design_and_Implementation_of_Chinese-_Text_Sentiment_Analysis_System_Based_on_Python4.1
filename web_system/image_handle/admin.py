#
# from .models import CheckModel
# from web_system.settings import admin_title
# from openpyxl import Workbook
# from django.http import HttpResponse
# from django.contrib import admin
# from .models import AnalysisResult  # 确保导入路径正确
#
# @admin.register(AnalysisResult)
# class AnalysisResultAdmin(admin.ModelAdmin):
#
#     list_display = ('file_name', 'content', 'sentiment', 'created_at')
#     search_fields = ('file_name', 'content', 'sentiment')
#
# # 导出Excel Mixin
# class ExportExcelMixin(object):
#     def export_as_excel(self, request, queryset):
#         meta = self.model._meta
#         field_names = [field.name for field in meta.fields]
#
#         # 创建 HTTP 响应
#         response = HttpResponse(content_type='application/msexcel')
#         response['Content-Disposition'] = f'attachment; filename={meta.verbose_name}_export.xlsx'
#
#         # 创建 Excel 工作簿
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Exported Data"
#
#         # 写入表头
#         ws.append(field_names)
#
#         # 写入数据行
#         for obj in queryset:
#             row_data = []
#             for field in field_names:
#                 # 获取字段值
#                 value = getattr(obj, field)
#                 row_data.append(str(value) if value is not None else "")
#             ws.append(row_data)
#
#         # 保存到响应
#         wb.save(response)
#         return response
#
#     export_as_excel.short_description = '导出Excel'
#
#
# # 自定义 Admin 类
# class ExportAdmin(admin.ModelAdmin, ExportExcelMixin):
#     actions = ['export_as_excel']
#
#     def get_list_display(self, request):
#         return [field.name for field in self.model._meta.fields]
#
#
# class CheckAdmin(ExportAdmin):
#     list_display = ('id', 'content', 'pred_name', 'check_time')
#     list_filter = ('pred_name',)
#     search_fields = ('content',)
#
#
# admin.site.register(CheckModel, CheckAdmin)
# admin.site.site_header = admin_title
#
#
#
#
# from django.contrib import admin
# from .models import TextEmotionAnalysisResult, FileEmotionAnalysisResult
#
# @admin.register(TextEmotionAnalysisResult)
# class TextEmotionAnalysisResultAdmin(admin.ModelAdmin):
#     list_display = ('text', 'main_emotion', 'sentiment', 'confidence', 'created_at')
#     search_fields = ('text', 'main_emotion', 'sentiment')
#     list_filter = ('sentiment', 'created_at')
#
#
# @admin.register(FileEmotionAnalysisResult)
# class FileEmotionAnalysisResultAdmin(admin.ModelAdmin):
#     list_display = ('file_name', 'text', 'main_emotion', 'sentiment', 'confidence', 'created_at')
#     search_fields = ('file_name', 'text', 'main_emotion', 'sentiment')
#     list_filter = ('sentiment', 'created_at')
#
from django.contrib import admin
from .models import TextEmotionAnalysisResult, FileEmotionAnalysisResult
from openpyxl import Workbook
from django.http import HttpResponse

# 导出Excel Mixin
class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        # 创建 HTTP 响应
        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name}_export.xlsx'

        # 创建 Excel 工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = "Exported Data"

        # 写入表头
        ws.append(field_names)

        # 写入数据行
        for obj in queryset:
            row_data = []
            for field in field_names:
                # 获取字段值
                value = getattr(obj, field)
                row_data.append(str(value) if value is not None else "")
            ws.append(row_data)

        # 保存到响应
        wb.save(response)
        return response

    export_as_excel.short_description = '导出Excel'


# 自定义 Admin 类
class ExportAdmin(admin.ModelAdmin, ExportExcelMixin):
    actions = ['export_as_excel']

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]


@admin.register(TextEmotionAnalysisResult)
class TextEmotionAnalysisResultAdmin(ExportAdmin):
    list_display = ('text', 'main_emotion', 'sentiment', 'confidence', 'created_at')
    search_fields = ('text', 'main_emotion', 'sentiment')
    list_filter = ('sentiment', 'created_at')


@admin.register(FileEmotionAnalysisResult)
class FileEmotionAnalysisResultAdmin(ExportAdmin):
    list_display = ('file_name', 'text', 'main_emotion', 'sentiment', 'confidence', 'created_at')
    search_fields = ('file_name', 'text', 'main_emotion', 'sentiment')
    list_filter = ('sentiment', 'created_at')