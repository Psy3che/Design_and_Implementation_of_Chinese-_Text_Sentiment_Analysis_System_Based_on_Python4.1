# -*- coding: utf-8 -*-
# FileName  : conf.py
import os
from pathlib import Path

# 本文件位置
my_path = Path(__file__).resolve()

# 模型文件位置
svm_model_path = os.path.join(my_path.parent, 'train_model', 'svm_model.pkl')
w2v_model_path = os.path.join(my_path.parent, 'train_model', 'w2v_model.pkl')
bert_model_path=os.path.join(my_path.parent, 'train_model', '/Users/grace/Downloads/文本情感升级版/web_system/utils/train_model/bert_setiment_model')
