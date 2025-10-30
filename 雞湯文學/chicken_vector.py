import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# 載入模型
model = SentenceTransformer('all-MiniLM-L6-v2')
from transformers import pipeline

from transformers import pipeline

from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="uer/xlm-roberta-large-finetuned-jd-binary-chinese"
)


df = pd.read_csv("data/chicken_soup.csv")

# 定義每個心理指標候選分數
stress_labels = ["1","2","3","4","5"]          # 低到高壓力
happiness_labels = ["1","2","3","4","5"]      # 不開心→非常開心
humor_labels = ["1","2","3","4","5"]          # 認真→幽默
encourage_labels = ["1","2","3","4","5"]      # 不需要→非常需要鼓勵

# 用 zero-shot 自動標註心理指標
def predict_level(text, candidate_labels):
    result = classifier(text, candidate_labels)
    # 選分數最高的 label
    return int(result['labels'][0])

df['stress_level'] = df['text'].apply(lambda x: predict_level(x, stress_labels))
df['happiness_level'] = df['text'].apply(lambda x: predict_level(x, happiness_labels))
df['humor_level'] = df['text'].apply(lambda x: predict_level(x, humor_labels))
df['encouragement_level'] = df['text'].apply(lambda x: predict_level(x, encourage_labels))

# 計算語意向量
df['vector'] = df['text'].apply(lambda x: model.encode(x, convert_to_tensor=True))

# 儲存
torch.save(df['vector'].tolist(), "data/chicken_soup_vectors.pt")
df.to_csv("data/chicken_soup_with_features_auto.csv", index=False, encoding="utf-8-sig")

print("✅ 雞湯向量資料庫建立完成，心理指標自動標註")
