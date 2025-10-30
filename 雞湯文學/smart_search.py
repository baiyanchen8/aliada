import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# === 初始化模型 ===
print("🚀 載入模型中，請稍候...")
model = SentenceTransformer('all-MiniLM-L6-v2')

try:
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased")
except Exception as e:
    print("⚠️ 中文情緒分析模型載入失敗，使用英文預設模型。")
    sentiment_analyzer = pipeline("sentiment-analysis")

# === 載入雞湯資料與向量 ===
df = pd.read_csv("data/chicken_soup.csv")
vectors = torch.load("data/chicken_soup_vectors.pt")
df['vector'] = vectors

print("✅ 資料與模型已載入完成！\n")

# === 功能選單 ===
print("==== 🐣 智慧雞湯推薦系統 ====")
print("1️⃣ 問卷模式：我自己選要聽雞湯或毒雞湯")
print("2️⃣ 自動模式：AI 幫我判斷心情，自動推薦雞湯\n")

mode = input("請選擇模式（輸入 1 或 2）：").strip()

# === 使用者心情輸入 ===
user_mood = input("\n請描述你現在的心情：")

# === 模式 1：問卷模式 ===
if mode == "1":
    user_prefer = input("你想聽【雞湯】還是【毒雞湯】？(輸入 positive 或 negative)：").strip().lower()
    if user_prefer not in ["positive", "negative"]:
        print("⚠️ 輸入錯誤，預設為 positive（正向雞湯）")
        user_prefer = "positive"
    prefer = user_prefer

# === 模式 2：自動判斷情緒 ===
elif mode == "2":
    sentiment = sentiment_analyzer(user_mood)[0]
    label = sentiment['label']
    score = sentiment['score']

    print(f"\n🧠 模型判斷你的情緒為：{label}（信心值 {score:.2f}）")

    # 若為負面 → 推正向雞湯；若為正面 → 推毒雞湯
    if "NEG" in label.upper():
        prefer = "positive"
    elif "POS" in label.upper():
        prefer = "negative"
    else:
        prefer = "positive"

    print(f"📘 系統決定為你推薦：{prefer} 雞湯\n")

else:
    print("⚠️ 未選擇有效模式，預設為問卷模式（正向雞湯）")
    prefer = "positive"

# === 心情轉向量 ===
mood_vector = model.encode(user_mood, convert_to_tensor=True)

# === 過濾雞湯類別 ===
filtered_df = df[df['label'] == prefer].copy()

# === 計算相似度 ===
filtered_df['similarity'] = filtered_df['vector'].apply(
    lambda x: util.cos_sim(x, mood_vector).item()
)

# === 取前5名 ===
top_chicken_soups = filtered_df.sort_values(by='similarity', ascending=False).head(5)

# === 輸出結果 ===
print("===== 🍵 為你推薦的雞湯 =====")
for i, row in top_chicken_soups.iterrows():
    print(f"\n[{row['label']}] 相似度: {row['similarity']:.3f}")
    print(f"👉 {row['text']}")

print("\n✨ 推薦完成！祝你心情更好 💖")
