
import torch
from sklearn.metrics import f1_score
from transformers import BertTokenizer, BertForSequenceClassification
# 使用 Hugging Face 提供的预训练模型 ID
model_id = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_id)
model = BertForSequenceClassification.from_pretrained(model_id)
# bert_model_path = "bert-base-chinese"
#from  .conf import bert_model_path  # 假设你已经将模型路径定义在配置文件中

# 直接使用绝对路径
bert_model_path = "/Users/grace/Downloads/文本情感/web_system/utils/train_model/bert_sentiment_model"

# 检查设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载预训练的 BERT 模型和分词器
tokenizer = BertTokenizer.from_pretrained(bert_model_path)
model = BertForSequenceClassification.from_pretrained(bert_model_path)
model = model.to(device)

# 对电影评论进行情感判断
def bert_predict(string):
    # 对输入文本进行编码
    inputs = tokenizer(string, return_tensors='pt', padding=True, truncation=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}  # 确保输入张量在正确的设备上
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits).item()

    # 输出结果
    sentiment = '积极' if predicted_class == 1 else '消极'
    print(f"{string} [{sentiment}]")
    return sentiment

# 封装情感判断逻辑
def text_check(content):
    return bert_predict(content)

# 测试预测
if __name__ == "__main__":
    string = '还不错，符合需求'
    pred_result = bert_predict(string)
    print(f"预测结果: {pred_result}")

# 测试预测
if __name__ == "__main__":
    # 示例数据
    test_texts = [
        "这部电影还不错，符合我的需求",
        "这部电影太糟糕了，完全不符合我的预期",
        "这部电影一般般，没有什么特别的地方",
        "这部电影非常精彩，我非常喜欢！"
    ]
    true_labels = [1, 0, 0, 1]  # 真实标签

    # 获取预测结果
    predicted_labels = [bert_predict(text) for text in test_texts]

    # 调试输出
    print(f"真实标签: {true_labels}")
    print(f"预测标签: {predicted_labels}")

    # 计算 F1 值
    try:
        f1 = f1_score(true_labels, predicted_labels)
        print(f"F1 值: {f1:.4f}")
    except ValueError as e:
        print(f"计算 F1 值时出错: {e}")