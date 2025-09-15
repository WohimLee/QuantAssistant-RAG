# Sigmoid vs Softmax 在多标签分类中的应用

## 1. 数学特性区别

```python
# Sigmoid函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Softmax函数
def softmax(x):
    exp_x = np.exp(x - np.max(x))  # 减去最大值防止溢出
    return exp_x / np.sum(exp_x)
```

## 2. 主要区别

### Sigmoid
- 输出范围：[0,1]
- 每个类别的概率是独立的
- 所有类别的概率之和可以大于1
- 适合多标签分类

### Softmax
- 输出范围：[0,1]
- 所有类别的概率之和等于1
- 类别之间相互竞争
- 适合多分类问题

## 3. 具体例子

```python
# 假设有三个类别，输入logits为[2.0, 1.0, 0.1]

# Sigmoid输出
sigmoid_output = [0.88, 0.73, 0.52]
# 特点：每个类别独立，总和>1

# Softmax输出
softmax_output = [0.47, 0.31, 0.22]
# 特点：所有类别概率和为1
```

## 4. 在意图识别中的应用

```python
# 示例：用户问题"如何查询股票历史数据并进行回测？"

# 使用Sigmoid
intent_probs = {
    "数据查询": 0.9,    # 很可能涉及
    "回测相关": 0.8,    # 很可能涉及
    "交易操作": 0.2,    # 不太可能涉及
    "因子相关": 0.1     # 不太可能涉及
}
# 总和 = 2.0 > 1，这是合理的，因为问题确实涉及多个意图

# 使用Softmax
intent_probs = {
    "数据查询": 0.4,    # 被其他类别"稀释"
    "回测相关": 0.3,    # 被其他类别"稀释"
    "交易操作": 0.2,    # 被强制分配概率
    "因子相关": 0.1     # 被强制分配概率
}
# 总和 = 1.0，这不太合理，因为问题确实主要涉及前两个意图
```

## 5. 为什么选择Sigmoid

### a. 独立性
```python
# 每个类别的预测是独立的
class MultiLabelClassifier(nn.Module):
    def __init__(self, input_size, num_labels):
        super().__init__()
        self.classifier = nn.Linear(input_size, num_labels)
        
    def forward(self, x):
        logits = self.classifier(x)
        return torch.sigmoid(logits)  # 每个类别独立预测
```

### b. 阈值设置
```python
def predict_with_threshold(probs, threshold=0.5):
    # 可以灵活设置每个类别的阈值
    return (probs > threshold).int()
```

### c. 损失函数
```python
# 使用二元交叉熵损失
criterion = nn.BCEWithLogitsLoss()
# 直接使用logits，内部会应用sigmoid
```

## 6. 实际应用建议

```python
class IntentClassifier(nn.Module):
    def __init__(self, model_name, num_labels):
        super().__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Linear(768, num_labels)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask)
        logits = self.classifier(outputs.pooler_output)
        return torch.sigmoid(logits)

def predict_intents(model, text, tokenizer, threshold=0.5):
    inputs = tokenizer(text, return_tensors='pt')
    probs = model(**inputs)
    
    # 可以设置不同类别的不同阈值
    thresholds = {
        "数据查询": 0.5,
        "回测相关": 0.6,
        "交易操作": 0.7,
        "因子相关": 0.7
    }
    
    predictions = {}
    for i, label in enumerate(labels):
        predictions[label] = (probs[0][i] > thresholds[label]).item()
    
    return predictions
```

## 7. 注意事项

- 需要为每个类别设置合适的阈值
- 可能需要类别特定的阈值
- 评估指标要使用适合多标签的指标
- 数据标注需要更细致

## 8. 总结

### Sigmoid适合多标签分类，因为：
- 保持类别独立性
- 允许一个样本属于多个类别
- 概率值更合理
- 便于设置阈值

### Softmax适合多分类，因为：
- 强制类别互斥
- 概率和为1
- 适合单标签预测

在量化API文档意图识别任务中，使用Sigmoid是更合适的选择，因为它能更好地处理一个问题可能涉及多个意图的情况。 