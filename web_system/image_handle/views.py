import os

import torch

# from torch.onnx._internal.fx._pass import AnalysisResult
from transformers import BertForSequenceClassification, BertTokenizer
from .models import TextEmotionAnalysisResult, FileEmotionAnalysisResult

from utils.model_check import text_check
from web_system.settings import admin_title, index_info

import jieba.analyse

from django.http import FileResponse

import os
import uuid
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import jieba.analyse
import pandas as pd
from .forms import AnalysisForm  # 确保这里的导入路径正确


def index(request):
    context = {
        'title': admin_title,
        'index_info': index_info
    }

    def some_view(request):
        form = AnalysisForm(request.POST or None)
    return render(request, 'index.html', context=context)


def check(request):
    return render(request, 'check.html')

from django.http import JsonResponse

def check_content(request):
    if request.method == 'POST':
        input_content = request.POST.get('input_content')
        file_input = request.POST.get('file_input')
        # 处理逻辑
        return JsonResponse({'code': 200, 'data': {'pred_name': 'example'}})
    else:
        return JsonResponse({'code': 400, 'message': 'Invalid request method'})


def download_result(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = FileResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        return HttpResponse("File not found", status=404)
def text_analysis(request):
    # 修改词云保存路径
    output_dir = os.path.join(settings.MEDIA_ROOT, 'analysis_results')
    os.makedirs(output_dir, exist_ok=True)

    # 生成唯一文件名
    import uuid
    unique_id = uuid.uuid4().hex[:8]

    # 词云图路径
    wordcloud_filename = f'wordcloud_{unique_id}.png'
    output_path = os.path.join(output_dir, wordcloud_filename)

    # 柱状图路径
    bar_chart_filename = f'barchart_{unique_id}.png'
    bar_chart_path = os.path.join(output_dir, bar_chart_filename)
    if request.method == 'POST':
        # 检查是否上传了文件
        if 'text_file' not in request.FILES:
            return HttpResponse("请上传文件")

        uploaded_file = request.FILES['text_file']

        # 读取文件内容
        try:
            lyric = uploaded_file.read().decode('utf-8')
            if not lyric.strip():
                return HttpResponse("文件内容为空，请上传包含文本的文件")
            print("文件内容:", lyric)  # 打印文件内容，检查是否正确读取
        except UnicodeDecodeError:
            try:
                lyric = uploaded_file.read().decode('gbk')
                if not lyric.strip():
                    return HttpResponse("文件内容为空，请上传包含文本的文件")
                print("文件内容:", lyric)  # 打印文件内容，检查是否正确读取
            except UnicodeDecodeError:
                return HttpResponse("文件编码错误，请确保文件是UTF-8或GBK编码")

        # 提取关键词，调整参数
        result = jieba.analyse.textrank(
            lyric,
            topK=20,
            withWeight=True,
            allowPOS=('n', 'vn', 'v', 'ns', 'nr', 'nt', 'nz')
        )
        keywords = {item[0]: item[1] for item in result}
        keywords = {item[0]: item[1] for item in result}
        print("关键词:", keywords)  # 打印关键词，检查是否提取到

        # 检查关键词是否为空
        if not keywords:
            return HttpResponse("无法提取关键词，请检查文件内容")


        # 生成词云图
        background_image_path = '/Users/grace/文本情感升级版/web_system/image_handle/background.png'  # 修改为你的背景图片路径
        mask_image = None
        if os.path.exists(background_image_path):
            mask_image = np.array(Image.open(background_image_path))

        font_path = '/Users/grace/文本情感升级版/web_system/image_handle/Songti.ttc'  # 修改为你的中文字体文件路径
        if not os.path.exists(font_path):
            return HttpResponse("字体文件不存在，请检查字体路径")

        wc = WordCloud(
            font_path=font_path,
            background_color='white',
            max_words=50,
            mask=mask_image
        )

        wc.generate_from_frequencies(keywords)


        # 保存词云
        wordcloud_filename = f'wordcloud_{unique_id}.png'
        output_path = os.path.join(output_dir, wordcloud_filename)

        wc.to_file(output_path)


        # 绘制柱状图
        X = list(keywords.keys())
        Y = list(keywords.values())
        num = len(X)

        plt.figure(figsize=(28, 10))
        plt.bar(range(num), Y, tick_label=X, width=0.5)
        plt.xticks(rotation=50, fontproperties=FontProperties(fname=font_path), fontsize=20)
        plt.yticks(fontsize=20)
        plt.title("Words Frequency Chart", fontproperties=FontProperties(fname=font_path), fontsize=30)
        plt.tight_layout()

        # 保存柱状图
        bar_chart_filename = f'barchart_{unique_id}.png'
        bar_chart_path = os.path.join(output_dir, bar_chart_filename)
        plt.savefig(bar_chart_path, bbox_inches='tight')  # 防止标签被截断
        plt.close()



        # 将结果传递给前端
        return render(request, 'result.html', {
            'wordcloud_url': wordcloud_filename,
            'bar_chart_url': bar_chart_filename

        })
    print("词云图生成成功:", output_path)
    print("柱状图生成成功:", bar_chart_path)
    return render(request, 'upload.html')


from django.http import JsonResponse

# #上传表格文件
# def upload_file(request):
#     # 临时验证视图
#     if request.method == 'POST':
#         return JsonResponse({'status': 'success', 'message': '路由验证成功'})
#     return JsonResponse({'status': 'error', 'message': '仅支持 POST 请求'}, status=405)
#
#
# # 加载自定义 BERT 模型和分词器
# model_path = '/Users/grace/文本情感升级版/训练预测/bert_sentiment_model'
# tokenizer = BertTokenizer.from_pretrained(model_path)
# model = BertForSequenceClassification.from_pretrained(model_path)
#
# # 将模型设置为评估模式
# model.eval()
#
# 表格文件情感分析方法定义
# def analyze_sentiment(texts):
#     results = []
#     for text in texts:
#         # 分词
#         inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt", max_length=512)
#
#         # 模型推理
#         with torch.no_grad():
#             outputs = model(**inputs)
#
#         # 获取预测结果
#         logits = outputs.logits
#         predicted_class = torch.argmax(logits, dim=1).item()
#
#         # 假设模型输出是二分类，0为负面情感，1为正面情感
#         sentiment = "积极" if predicted_class == 1 else "消极"
#         results.append({
#             '检测文本': text,
#             '情感分类': sentiment,
#         })
#     return results

from django.http import JsonResponse

from django.http import JsonResponse

def file_analysis(request):
    if request.method == 'POST':
        # 处理文件上传的逻辑
        # 假设生成了一个下载链接 download_url
        download_url = "https://example.com/download/file.txt"
        return JsonResponse({'code': 200, 'data': {'download_url': download_url}})
    else:
        return JsonResponse({'code': 400, 'message': 'Invalid request method'})
from django.shortcuts import render
from .emotion_analysis import EmotionAnalyzer

# # 初始化情感分析器
# emotion_analyzer = EmotionAnalyzer()
#
# def emotion_analysis_view(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#
#         try:
#             if not text:
#                 return render(request, 'error.html', {'message': '请输入文本进行分析。'})
#
#             # 进行情感分析
#             main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
#
#             # 将结果传递到前端
#             return render(request, 'emotion_analysis_result.html', {
#                 'text': text,
#                 'main_emotion': main_emotion,
#                 'sentiment': sentiment,
#                 'confidence': confidence
#             })
#         except Exception as e:
#             # 记录错误信息
#             print(f"情感分析失败: {str(e)}")
#             # 返回错误页面或提示信息
#             return render(request, 'error.html', {'message': '情感分析失败，请重试。'})
#     return render(request, 'emotion_analysis_form.html')
# views.py
from django.shortcuts import render
# from .emotion_analysis import EmotionAnalyzer
#
# # 初始化情感分析器
# emotion_analyzer = EmotionAnalyzer()
#
# def emotion_analysis_view(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#
#         try:
#             if not text:
#                 return render(request, 'error.html', {'message': '请输入文本进行分析。'})
#
#             # 进行情感分析
#             main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
#
#             # 将结果传递到前端
#             return render(request, 'emotion_analysis_result.html', {
#                 'text': text,
#                 'main_emotion': main_emotion,
#                 'sentiment': sentiment,
#                 'confidence': confidence
#             })
#         except Exception as e:
#             # 记录错误信息
#             print(f"情感分析失败: {str(e)}")
#             # 返回错误页面或提示信息
#             return render(request, 'error.html', {'message': '情感分析失败，请重试。'})
#     return render(request, 'emotion_analysis_form.html')

#
# # views.py
# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from .emotion_analysis import EmotionAnalyzer
# import pandas as pd
# from django.core.files.storage import default_storage
# from django.conf import settings
# import os
# from wsgiref.util import FileWrapper
# import mimetypes
#
# # 初始化情感分析器
# emotion_analyzer = EmotionAnalyzer()
#
# def emotion_analysis_view(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#
#         try:
#             if not text:
#                 return JsonResponse({'error': '请输入文本进行分析。'}, status=400)
#
#             # 进行情感分析
#             main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
#
#             # 返回结果
#             return JsonResponse({
#                 'main_emotion': main_emotion,
#                 'sentiment': sentiment,
#                 'confidence': confidence
#             })
#         except Exception as e:
#             # 记录错误信息
#             print(f"情感分析失败: {str(e)}")
#             return JsonResponse({'error': '情感分析失败，请重试。'}, status=500)
#
#     return render(request, 'emotion_analysis_form.html')
#
#
# def batch_emotion_analysis_view(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         try:
#             file = request.FILES['file']
#             file_path = os.path.join(settings.MEDIA_ROOT, file.name)
#             with default_storage.open(file_path, 'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#
#             # 使用 pandas 读取文件
#             if file.name.endswith('.csv'):
#                 df = pd.read_csv(file_path, encoding='utf-8')
#             elif file.name.endswith(('.xlsx', '.xls')):
#                 df = pd.read_excel(file_path)
#             else:
#                 return JsonResponse({'error': '不支持的文件格式，请使用CSV或Excel文件'}, status=400)
#
#             # 自动识别文本列
#             text_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['text', '文本', '内容', 'comment'])]
#
#             if not text_columns:
#                 text_column = df.columns[0]
#             else:
#                 text_column = text_columns[0]
#
#             # 初始化结果列
#             df['sentiment'] = None  # 情感倾向
#             df['emotion'] = None    # 情感维度
#             df['confidence'] = None # 置信度
#
#             # 分析每行文本
#             for idx, row in df.iterrows():
#                 text = str(row[text_column])
#                 try:
#                     main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
#                     df.at[idx, 'sentiment'] = sentiment
#                     df.at[idx, 'emotion'] = main_emotion
#                     df.at[idx, 'confidence'] = confidence
#                 except Exception as e:
#                     print(f"分析失败: {str(e)}")
#                     df.at[idx, 'sentiment'] = '分析失败'
#                     df.at[idx, 'emotion'] = '分析失败'
#                     df.at[idx, 'confidence'] = 0
#
#             # 生成输出文件名
#             output_file_name = f"results_{file.name}"
#             output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)
#
#             # 保存结果
#             if output_file_name.endswith('csv'):
#                 df.to_csv(output_file_path, encoding='utf-8', index=False)
#             else:
#                 df.to_excel(output_file_path, index=False)
#
#             # 返回下载链接
#             download_url = f"{settings.MEDIA_URL}{output_file_name}"
#             return JsonResponse({'download_url': download_url})
#
#         except Exception as e:
#             print(f"批量分析失败: {str(e)}")
#             return JsonResponse({'error': '文件上传失败，请重试。'}, status=500)
#
#     return JsonResponse({'error': '无效的请求'}, status=400)
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .emotion_analysis import EmotionAnalyzer
import pandas as pd
from django.core.files.storage import default_storage
from django.conf import settings
import os
from wsgiref.util import FileWrapper
import mimetypes

# # 初始化情感分析器
# emotion_analyzer = EmotionAnalyzer()
#
# def emotion_analysis_view(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#
#         try:
#             if not text:
#                 return JsonResponse({'error': '请输入文本进行分析。'}, status=400)
#
#             # 进行情感分析
#             main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
#
#             # 返回结果
#             return JsonResponse({
#                 'main_emotion': main_emotion,
#                 'sentiment': sentiment,
#                 'confidence': confidence
#             })
#         except Exception as e:
#             # 记录错误信息
#             print(f"情感分析失败: {str(e)}")
#             return JsonResponse({'error': '情感分析失败，请重试。'}, status=500)
#
#     return render(request, 'emotion_analysis_form.html')
#
#
# import os
# import uuid
# import pandas as pd
# from django.conf import settings
# from django.http import JsonResponse, FileResponse, HttpResponse
# from django.shortcuts import render
#
# # 上传文件视图
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         if file:
#             try:
#                 # 保存上传的文件
#                 filename = f"{uuid.uuid4()}{os.path.splitext(file.name)[1]}"
#                 file_path = os.path.join(settings.MEDIA_ROOT, filename)
#                 with open(file_path, 'wb+') as destination:
#                     for chunk in file.chunks():
#                         destination.write(chunk)
#
#                 return JsonResponse({
#                     'code': 200,
#                     'message': 'File uploaded successfully',
#                     'file_path': filename
#                 })
#             except Exception as e:
#                 return JsonResponse({'code': 500, 'message': str(e)})
#         else:
#             return JsonResponse({'code': 400, 'message': 'No file provided'})
#     else:
#         return JsonResponse({'code': 400, 'message': 'Invalid method'})
#
# # 下载文件视图
# def download_file(request, file_name):
#     file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as f:
#             response = FileResponse(f, content_type='application/octet-stream')
#             response['Content-Disposition'] = f'attachment; filename={file_name}'
#             return response
#     else:
#         return HttpResponse("File not found", status=404)
#
# # 主页视图
# def index(request):
#     return render(request, 'index.html')
#
# # 检查视图
# def check(request):
#     return render(request, 'check.html')
#
#
# def batch_emotion_analysis_view(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         try:
#             file = request.FILES['file']
#             file_path = os.path.join(settings.MEDIA_ROOT, file.name)
#             with default_storage.open(file_path, 'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#
#             # 使用 pandas 读取文件
#             if file.name.endswith('.csv'):
#                 df = pd.read_csv(file_path, encoding='utf-8')
#             elif file.name.endswith(('.xlsx', '.xls')):
#                 df = pd.read_excel(file_path)
#             else:
#                 return JsonResponse({'error': '不支持的文件格式，请使用CSV或Excel文件'}, status=400)
#
#             # 自动识别文本列
#             text_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['text', '文本', '内容', 'comment'])]
#
#             if not text_columns:
#                 text_column = df.columns[0]
#             else:
#                 text_column = text_columns[0]
#
#             # 初始化结果列
#             df['sentiment'] = None  # 情感倾向
#             df['emotion'] = None    # 情感维度
#             df['confidence'] = None # 置信度
#
#             # 分析每行文本
#             for idx, row in df.iterrows():
#                 text = str(row[text_column])
#                 try:
#                     main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
#                     df.at[idx, 'sentiment'] = sentiment
#                     df.at[idx, 'emotion'] = main_emotion
#                     df.at[idx, 'confidence'] = confidence
#                 except Exception as e:
#                     print(f"分析失败: {str(e)}")
#                     df.at[idx, 'sentiment'] = '分析失败'
#                     df.at[idx, 'emotion'] = '分析失败'
#                     df.at[idx, 'confidence'] = 0
#
#             # 生成输出文件名
#             output_file_name = f"results_{file.name}"
#             output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)
#
#             # 保存结果
#             if output_file_name.endswith('xslx'):
#                 df.to_csv(output_file_path, encoding='utf-8', index=False)
#             else:
#                 df.to_excel(output_file_path, index=False)
#
#             # 返回下载链接
#             download_url = f"{settings.MEDIA_URL}{output_file_name}"
#             return JsonResponse({'download_url': download_url})
#
#         except Exception as e:
#             print(f"批量分析失败: {str(e)}")
#             return JsonResponse({'error': '文件上传失败，请重试。'}, status=500)
#
#     return JsonResponse({'error': '无效的请求'}, status=400)
#
# # views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import os
# from django.conf import settings
#
# @csrf_exempt  # 如果您不使用Django的CSRF保护，可以临时禁用它进行测试
# def upload_file_analysis(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         if file:
#             try:
#                 # 保存上传的文件
#                 filename = f"{uuid.uuid4()}{os.path.splitext(file.name)[1]}"
#                 file_path = os.path.join(settings.MEDIA_ROOT, filename)
#                 with open(file_path, 'wb+') as destination:
#                     for chunk in file.chunks():
#                         destination.write(chunk)
#
#                 return JsonResponse({
#                     'code': 200,
#                     'message': 'File uploaded successfully',
#                     'file_path': filename
#                 })
#             except Exception as e:
#                 return JsonResponse({'code': 500, 'message': str(e)})
#         else:
#             return JsonResponse({'code': 400, 'message': 'No file provided'})
#     else:
#         return JsonResponse({'code': 400, 'message': 'Invalid method'})
#
# from django.http import JsonResponse
#
# def check_content(request):
#     if request.method == 'POST':
#         input_content = request.POST.get('input_content')
#         file_input = request.POST.get('file_input')
#         # 处理逻辑
#         return JsonResponse({'code': 200, 'data': {'pred_name': 'example'}})
#     else:
#         return JsonResponse({'code': 400, 'message': 'Invalid request method'})


from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .emotion_analysis import EmotionAnalyzer

emotion_analyzer = EmotionAnalyzer()

@csrf_exempt
def emotion_analysis_view(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')

        try:
            if not text:
                return JsonResponse({'error': '请输入文本进行分析。'}, status=400)

            # 进行情感分析
            main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
            # 保存到数据库
            TextEmotionAnalysisResult.objects.create(
                text=text,
                main_emotion=main_emotion,
                sentiment=sentiment,
                confidence=confidence
            )
            # 返回结果
            return JsonResponse({
                'main_emotion': main_emotion,
                'sentiment': sentiment,
                'confidence': confidence
            })

        except Exception as e:
            # 记录错误信息
            print(f"情感分析失败: {str(e)}")
            return JsonResponse({'error': '情感分析失败，请重试。'}, status=500)


    return render(request, 'emotion_analysis_form.html')

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.conf import settings


@csrf_exempt
def batch_emotion_analysis_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # 使用 pandas 读取文件
            if file.name.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return JsonResponse({'code': 400, 'message': '不支持的文件格式，请使用CSV或Excel文件'}, status=400)

            # 检查文件内容是否为空
            if df.empty:
                return JsonResponse({'code': 400, 'message': '文件内容为空'})

            # 检查文件中是否有 'content' 列
            if 'content' not in df.columns:
                return JsonResponse({'code': 400, 'message': "'content' 列未找到在文件中"})

            # 初始化结果列
            df['main_emotion'] = None  # 主要情感
            df['sentiment'] = None    # 情感类别
            df['confidence'] = None   # 置信度

            # 分析每行文本
            for idx, row in df.iterrows():
                text = str(row['content'])
                try:
                    main_emotion, sentiment, confidence = emotion_analyzer.analyze(text)
                    df.at[idx, 'main_emotion'] = main_emotion
                    df.at[idx, 'sentiment'] = sentiment
                    df.at[idx, 'confidence'] = confidence
                    # 保存到数据库
                    FileEmotionAnalysisResult.objects.create(
                        file_name=file.name,
                        text=text,
                        main_emotion=main_emotion,
                        sentiment=sentiment,
                        confidence=confidence
                    )
                except Exception as e:
                    print(f"分析失败: {str(e)}")
                    df.at[idx, 'main_emotion'] = '分析失败'
                    df.at[idx, 'sentiment'] = '分析失败'
                    df.at[idx, 'confidence'] = 0

            # 生成输出文件名
            output_file_name = f"results_{file.name}"
            output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)

            # 保存结果
            if output_file_name.endswith('.csv'):
                df.to_csv(output_file_path, encoding='utf-8', index=False)
            else:
                df.to_excel(output_file_path, index=False)

            # 返回下载链接
            download_url = f"{settings.MEDIA_URL}{output_file_name}"
            return JsonResponse({'code': 200, 'data': {'download_url': download_url}})

        except Exception as e:
            print(f"批量分析失败: {str(e)}")
            return JsonResponse({'code': 500, 'message': '文件处理失败，请重试。'}, status=500)

    return JsonResponse({'code': 400, 'message': '无效的请求'}, status=400)


from django.http import FileResponse
import os

def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = FileResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)
