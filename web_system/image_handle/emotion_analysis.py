# # emotion_analysis.py
# from snownlp import SnowNLP
#
# class EmotionAnalyzer:
#     def __init__(self):
#         # 定义情感词典
#         self.emotion_words = {
#             '喜悦': ['高兴', '开心', '愉快', '喜悦', '欢乐', '满足', '舒畅', '得意'],
#             '愤怒': ['愤怒', '生气', '恼火', '愤慨', '气愤', '不满', '怨恨', '狂怒'],
#             '悲伤': ['悲伤', '难过', '心痛', '哀伤', '沮丧', '失落', '郁闷', '痛苦'],
#             '厌恶': ['厌恶', '讨厌', '反感', '嫌弃', '憎恶', '厌烦', '恶心', '反感'],
#             '恐惧': ['恐惧', '害怕', '惊恐', '畏惧', '恐慌', '担忧', '焦虑', '忐忑'],
#             '惊讶': ['惊讶', '惊奇', '诧异', '震撼', '惊异', '意外', '惊叹', '吃惊'],
#             '中性': ['普通', '一般', '平常', '无感', '平淡', '寻常', '普通', '普通']
#         }
#
#     def analyze(self, text):
#         """分析文本的情感维度"""
#         try:
#             # 使用SnowNLP进行情感分析和分词
#             s = SnowNLP(text)
#             sentiment_score = s.sentiments  # 获取情感得分，范围为0到1
#             words = s.words  # 获取分词结果
#
#             # 初始化情感维度得分字典
#             emotion_scores = {
#                 '喜悦': 0, '愤怒': 0, '悲伤': 0,
#                 '厌恶': 0, '恐惧': 0, '惊讶': 0, '中性': 0
#             }
#
#             # 基于情感基础分设置初始倾向
#             if sentiment_score > 0.7:
#                 emotion_scores['喜悦'] += 2
#             elif sentiment_score < 0.3:
#                 emotion_scores['悲伤'] += 1
#                 emotion_scores['愤怒'] += 1
#             else:
#                 emotion_scores['中性'] += 2
#
#             # 根据情感关键词计算得分
#             for word in words:
#                 for emotion, keywords in self.emotion_words.items():
#                     if word in keywords:
#                         emotion_scores[emotion] += 1
#
#             # 确定主要情感维度
#             main_emotion = max(emotion_scores.items(), key=lambda x: x[1])
#
#             # 情感类别映射
#             if main_emotion[0] in ['喜悦', '惊讶']:
#                 sentiment = '积极'
#             elif main_emotion[0] in ['愤怒', '悲伤', '厌恶', '恐惧']:
#                 sentiment = '消极'
#             else:
#                 sentiment = '中性'
#
#             # 计算置信度 (归一化后的得分)
#             total_score = sum(emotion_scores.values())
#             confidence = int((main_emotion[1] / total_score * 100) if total_score > 0 else 50)
#
#             return main_emotion[0], sentiment, confidence
#         except Exception as e:
#             print(f"情感分析失败: {str(e)}")
#             raise


# emotion_analysis.py
# import os
# import jieba
# from collections import defaultdict
# from snownlp import SnowNLP
#
# class EmotionAnalyzer:
#     def __init__(self):
#         # 初始化情感词典
#         self.pos_words = self._load_word_list('/Users/grace/文本情感升级版/训练预测/data/positive.txt')
#         self.neg_words = self._load_word_list('/Users/grace/文本情感升级版/训练预测/data/negative.txt')
#         self.stopwords = self._load_word_list('/Users/grace/文本情感升级版/训练预测/data/hit_stopwords.txt')
#         self.emotion_words = {
#             '喜悦': ['高兴', '开心', '愉快', '喜悦', '欢乐', '满足', '舒畅', '得意'],
#             '愤怒': ['愤怒', '生气', '恼火', '愤慨', '气愤', '不满', '怨恨', '狂怒'],
#             '悲伤': ['悲伤', '难过', '心痛', '哀伤', '沮丧', '失落', '郁闷', '痛苦'],
#             '厌恶': ['厌恶', '讨厌', '反感', '嫌弃', '憎恶', '厌烦', '恶心', '反感'],
#             '恐惧': ['恐惧', '害怕', '惊恐', '畏惧', '恐慌', '担忧', '焦虑', '忐忑'],
#             '惊讶': ['惊讶', '惊奇', '诧异', '震撼', '惊异', '意外', '惊叹', '吃惊'],
#             '中性': ['普通', '一般', '平常', '无感', '平淡', '寻常', '普通', '普通']
#         }
#
#     def _load_word_list(self, filename):
#         """加载词典文件"""
#         try:
#             current_dir = os.path.dirname(os.path.abspath(__file__))
#             file_path = os.path.join(current_dir, 'resources', filename)
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 return [line.strip() for line in f.readlines()]
#         except Exception as e:
#             print(f"加载词典失败: {str(e)}")
#             return []
#
#     def _tokenize(self, text):
#         """对文本进行分词和预处理"""
#         try:
#             # 使用 jieba 分词
#             tokens = jieba.lcut(str(text))
#
#             # 过滤停用词
#             tokens = [token for token in tokens if token not in self.stopwords]
#
#             return tokens
#         except Exception as e:
#             print(f"分词失败: {str(e)}")
#             return []
#
#     def _semantic_enhancement(self, base_sentiment, words):
#         """语义增强机制，结合基础情感得分和新词权重"""
#         try:
#             # 初始权重
#             enhancement = 0.0
#             weight_factor = 0.0
#
#             # 计算正负情感词的影响
#             pos_count = sum(1 for word in words if word in self.pos_words)
#             neg_count = sum(1 for word in words if word in self.neg_words)
#
#             # 新词的影响
#             new_words_count = sum(1 for word in words if word in self.emotion_words['中性'])
#
#             # 根据情感词分布调整基础情感得分
#             if pos_count > neg_count:
#                 enhancement = 0.1 * min(pos_count - neg_count, 5) / 5
#             elif neg_count > pos_count:
#                 enhancement = -0.1 * min(neg_count - pos_count, 5) / 5
#
#             # 新词权重加成
#             if new_words_count > 0:
#                 weight_factor = 0.05 * min(new_words_count, 3) / 3
#
#             # 应用增强
#             enhanced_score = base_sentiment + enhancement
#
#             # 应用新词加成 - 向基础得分方向进一步增强
#             if base_sentiment > 0.5:  # 原本偏积极
#                 enhanced_score += weight_factor
#             elif base_sentiment < 0.5:  # 原本偏消极
#                 enhanced_score -= weight_factor
#
#             # 确保得分在 [0, 1] 范围内
#             enhanced_score = max(0.0, min(1.0, enhanced_score))
#
#             return enhanced_score
#         except Exception as e:
#             print(f"语义增强失败: {str(e)}")
#             return base_sentiment  # 失败时返回基础得分
#
#     def _analyze_emotion_dimension(self, text, words, sentiment_score):
#         """分析文本的情感维度"""
#         try:
#             # 初始化情感维度得分字典
#             emotion_scores = {
#                 '喜悦': 0, '愤怒': 0, '悲伤': 0,
#                 '厌恶': 0, '恐惧': 0, '惊讶': 0, '中性': 0
#             }
#
#             # 基于情感基础分设置初始倾向
#             if sentiment_score > 0.7:
#                 emotion_scores['喜悦'] += 2
#             elif sentiment_score < 0.3:
#                 emotion_scores['悲伤'] += 1
#                 emotion_scores['愤怒'] += 1
#             else:
#                 emotion_scores['中性'] += 2
#
#             # 根据情感关键词计算得分
#             for word in words:
#                 for emotion, keywords in self.emotion_words.items():
#                     if word in keywords:
#                         emotion_scores[emotion] += 1
#
#             # 确定主要情感维度
#             main_emotion = max(emotion_scores.items(), key=lambda x: x[1])
#
#             # 情感类别映射
#             if main_emotion[0] in ['喜悦', '惊讶']:
#                 sentiment = '积极'
#             elif main_emotion[0] in ['愤怒', '悲伤', '厌恶', '恐惧']:
#                 sentiment = '消极'
#             else:
#                 sentiment = '中性'
#
#             # 计算置信度 (归一化后的得分)
#             total_score = sum(emotion_scores.values())
#             confidence = int((main_emotion[1] / total_score * 100) if total_score > 0 else 50)
#
#             return main_emotion[0], sentiment, confidence
#         except Exception as e:
#             print(f"情感维度分析失败: {str(e)}")
#             # 基于基础情感得分提供默认结果
#             if sentiment_score > 0.6:
#                 return '喜悦', '积极', int(sentiment_score * 100)
#             elif sentiment_score < 0.4:
#                 return '悲伤', '消极', int((1 - sentiment_score) * 100)
#             else:
#                 return '中性', '中性', int(50 + abs(sentiment_score - 0.5) * 100)
#
#     def _extract_keywords(self, text, top_n=5):
#         """提取文本中的关键词"""
#         try:
#             from collections import defaultdict
#
#             # 分词
#             words = self._tokenize(text)
#             word_scores = defaultdict(float)
#
#             # 计算每个词的得分
#             for word in words:
#                 # 基础权重
#                 base_weight = 1.0
#
#                 # 情感词加权
#                 if word in self.pos_words:
#                     base_weight *= 1.5
#                 elif word in self.neg_words:
#                     base_weight *= 1.5
#
#                 # 新词加权
#                 if word in self.emotion_words['中性']:
#                     base_weight *= 2.0
#
#                 # 情感维度词加权
#                 for emotion, keywords in self.emotion_words.items():
#                     if word in keywords:
#                         base_weight *= 1.8
#                         break
#
#                 word_scores[word] += base_weight
#
#             # 过滤停用词和短词
#             for word in list(word_scores.keys()):
#                 if word in self.stopwords or len(word) < 2:
#                     del word_scores[word]
#
#             # 按权重排序返回前 N 个关键词
#             sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
#             return [word for word, _ in sorted_words[:top_n]]
#         except Exception as e:
#             print(f"提取关键词失败: {str(e)}")
#             return []
#
#
# emotion_analysis.py

import os
import jieba
from collections import defaultdict
from snownlp import SnowNLP


class EmotionAnalyzer:
    def __init__(self):
        # 初始化情感词典
        self.pos_words = self._load_word_list('/Users/grace/文本情感升级版/训练预测/data/positive.txt')
        self.neg_words = self._load_word_list('/Users/grace/文本情感升级版/训练预测/data/negative.txt')
        self.stopwords = self._load_word_list('/Users/grace/文本情感升级版/训练预测/data/hit_stopwords.txt')
        self.emotion_words = {
            '喜悦': ['高兴', '开心', '愉快', '喜悦', '欢乐', '满足', '舒畅', '得意'],
            '愤怒': ['愤怒', '生气', '恼火', '愤慨', '气愤', '不满', '怨恨', '狂怒'],
            '悲伤': ['悲伤', '难过', '心痛', '哀伤', '沮丧', '失落', '郁闷', '痛苦'],
            '厌恶': ['厌恶', '讨厌', '反感', '嫌弃', '憎恶', '厌烦', '恶心', '反感'],
            '恐惧': ['恐惧', '害怕', '惊恐', '畏惧', '恐慌', '担忧', '焦虑', '忐忑'],
            '惊讶': ['惊讶', '惊奇', '诧异', '震撼', '惊异', '意外', '惊叹', '吃惊'],
            '中性': ['普通', '一般', '平常', '无感', '平淡', '寻常', '普通', '普通']
        }

    def _load_word_list(self, filename):
        """加载词典文件"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, 'resources', filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        except Exception as e:
            print(f"加载词典失败: {str(e)}")
            return []

    def _tokenize(self, text):
        """对文本进行分词和预处理"""
        try:
            # 使用 jieba 分词
            tokens = jieba.lcut(str(text))

            # 过滤停用词
            tokens = [token for token in tokens if token not in self.stopwords]

            return tokens
        except Exception as e:
            print(f"分词失败: {str(e)}")
            return []

    def _semantic_enhancement(self, base_sentiment, words):
        """语义增强机制，结合基础情感得分和新词权重"""
        try:
            # 初始权重
            enhancement = 0.0
            weight_factor = 0.0

            # 计算正负情感词的影响
            pos_count = sum(1 for word in words if word in self.pos_words)
            neg_count = sum(1 for word in words if word in self.neg_words)

            # 新词的影响
            new_words_count = sum(1 for word in words if word in self.emotion_words['中性'])

            # 根据情感词分布调整基础情感得分
            if pos_count > neg_count:
                enhancement = 0.1 * min(pos_count - neg_count, 5) / 5
            elif neg_count > pos_count:
                enhancement = -0.1 * min(neg_count - pos_count, 5) / 5

            # 新词权重加成
            if new_words_count > 0:
                weight_factor = 0.05 * min(new_words_count, 3) / 3

            # 应用增强
            enhanced_score = base_sentiment + enhancement

            # 应用新词加成 - 向基础得分方向进一步增强
            if base_sentiment > 0.5:  # 原本偏积极
                enhanced_score += weight_factor
            elif base_sentiment < 0.5:  # 原本偏消极
                enhanced_score -= weight_factor

            # 确保得分在 [0, 1] 范围内
            enhanced_score = max(0.0, min(1.0, enhanced_score))

            return enhanced_score
        except Exception as e:
            print(f"语义增强失败: {str(e)}")
            return base_sentiment  # 失败时返回基础得分

    def _analyze_emotion_dimension(self, text, words, sentiment_score):
        """分析文本的情感维度"""
        try:
            # 初始化情感维度得分字典
            emotion_scores = {
                '喜悦': 0, '愤怒': 0, '悲伤': 0,
                '厌恶': 0, '恐惧': 0, '惊讶': 0, '中性': 0
            }

            # 基于情感基础分设置初始倾向
            if sentiment_score > 0.7:
                emotion_scores['喜悦'] += 2
            elif sentiment_score < 0.3:
                emotion_scores['悲伤'] += 1
                emotion_scores['愤怒'] += 1
            else:
                emotion_scores['中性'] += 2

            # 根据情感关键词计算得分
            for word in words:
                for emotion, keywords in self.emotion_words.items():
                    if word in keywords:
                        emotion_scores[emotion] += 1

            # 确定主要情感维度
            main_emotion = max(emotion_scores.items(), key=lambda x: x[1])

            # 情感类别映射
            if main_emotion[0] in ['喜悦', '惊讶']:
                sentiment = '积极'
            elif main_emotion[0] in ['愤怒', '悲伤', '厌恶', '恐惧']:
                sentiment = '消极'
            else:
                sentiment = '中性'

            # 计算置信度 (归一化后的得分)
            total_score = sum(emotion_scores.values())
            confidence = int((main_emotion[1] / total_score * 100) if total_score > 0 else 50)

            return main_emotion[0], sentiment, confidence
        except Exception as e:
            print(f"情感维度分析失败: {str(e)}")
            # 基于基础情感得分提供默认结果
            if sentiment_score > 0.6:
                return '喜悦', '积极', int(sentiment_score * 100)
            elif sentiment_score < 0.4:
                return '悲伤', '消极', int((1 - sentiment_score) * 100)
            else:
                return '中性', '中性', int(50 + abs(sentiment_score - 0.5) * 100)

    def analyze(self, text):
        """分析文本的情感"""
        try:
            # 使用 SnowNLP 进行情感分析和分词
            s = SnowNLP(text)
            sentiment_score = s.sentiments  # 获取情感得分，范围为 0 到 1
            words = self._tokenize(text)  # 自定义分词和预处理

            # 应用语义增强机制
            enhanced_score = self._semantic_enhancement(sentiment_score, words)

            # 进行情感维度分析
            main_emotion, sentiment, confidence = self._analyze_emotion_dimension(text, words, enhanced_score)

            return main_emotion, sentiment, confidence
        except Exception as e:
            print(f"情感分析失败: {str(e)}")
            raise