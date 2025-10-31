import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import subprocess
import json
import time, re

# === Ollama CLI 標註函數 ===
def run_ollama_command(command, user_input):
    """透過 subprocess 執行 ollama run 並回傳 stdout"""
    full_command = f'echo "{user_input}" | {command}'
    start_time = time.time()
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    end_time = time.time()
    response_time = end_time - start_time
    return stdout.decode('utf-8').strip(), response_time

def download_model(model_name):
    """檢查並下載模型"""
    print(f"Checking if the model '{model_name}' is already downloaded...")
    download_command = f"ollama pull {model_name}"
    process = subprocess.Popen(download_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print(f"Model '{model_name}' has been successfully downloaded.")
    else:
        print(f"Failed to download the model '{model_name}'. Error: {stderr.decode('utf-8')}")
        exit(1)

def extract_json_from_text(text, default_value=3):
    """
    從文字中抓取第一個 JSON 物件，解析為字典
    text: 模型回傳的文字
    default_value: 若抓不到或解析失敗，填入預設值
    """
    try:
        # 抓出第一個 { ... } 的部分
        match = re.findall(r'"(\w+_level)":\s*([1-5])', text)
        json_match = {k:int(v) for k,v in match}
        print(f"Extracted JSON: {json_match}")
        if len(json_match) == 4:
            return json_match
    except Exception as e:
        print(f"⚠️ JSON解析失敗: {e} | 原始文字: {text[:100]}...")
    
    # 失敗就回傳 None，讓呼叫端知道需要重試
    return None

def run_ollama_with_retry(command, prompt, max_retries=3, retry_delay=1):
    """
    帶有重試機制的 Ollama 執行函數
    command: ollama 命令
    prompt: 輸入提示
    max_retries: 最大重試次數
    retry_delay: 重試間隔（秒）
    """
    for attempt in range(max_retries):
        response, rt = run_ollama_command(command, prompt)
        labels = extract_json_from_text(response)
        print(f"Used time:{rt}")
        if labels is not None:
            return labels, rt, response
        else:
            print(f"⚠️ 第 {attempt + 1} 次嘗試失敗，{f'{retry_delay}秒後重試...' if attempt < max_retries - 1 else '已達最大重試次數'}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    # 所有重試都失敗，回傳預設值
    print("❌ 所有重試失敗，使用預設值")
    default_labels = {
        'stress_level': 3,
        'happiness_level': 3,
        'humor_level': 3,
        'encouragement_level': 3
    }
    return default_labels, 0, ""

# === 主程式 ===
if __name__ == "__main__":
    model_name = "gemma3:4b"

    # 下載模型
    download_model(model_name)
    command = f"ollama run {model_name}"

    # === 讀入雞湯資料 ===
    df = pd.read_csv("data/chicken_soup.csv")
    for col in ['stress_level', 'happiness_level', 'humor_level', 'encouragement_level', 'vector']:
        if col not in df.columns:
            df[col] = None

    # === 初始化 SentenceTransformer 模型 ===
    st_model = SentenceTransformer('all-MiniLM-L6-v2')

    # === 對每條雞湯標註心理指標 & 計算向量 ===
    for idx, row in df.iterrows():
        text = row['text']

        prompt = f"請將下面雞湯標註心理指標（1~5）：- stress_level: 壓力感（1~5） - happiness_level: 開心程度（1~5） - humor_level: 幽默程度（1~5） - encouragement_level: 鼓勵需求（1~5） - 雞湯內容：{text} - 請只回傳 JSON 格式，例如：{{stress_level:?, happiness_level:?, humor_level:?, encouragement_level:?}}"

        # 使用帶有重試機制的函數
        labels, rt, response = run_ollama_with_retry(command, prompt)
        
        df.at[idx, 'stress_level'] = labels['stress_level']
        df.at[idx, 'happiness_level'] = labels['happiness_level']
        df.at[idx, 'humor_level'] = labels['humor_level']
        df.at[idx, 'encouragement_level'] = labels['encouragement_level']

        # 計算文本向量
        df.at[idx, 'vector'] = st_model.encode(text, convert_to_tensor=True)

        if (idx+1) % 20 == 0:
            print(f"✅ 已處理 {idx+1} 條雞湯，耗時 {rt:.2f}s")

    # === 儲存資料庫 ===
    torch.save(df['vector'].tolist(), "data/chicken_soup_vectors.pt")
    df.to_csv("data/chicken_soup_with_features.csv", index=False, encoding="utf-8-sig")
    print("✅ 雞湯資料庫建立完成，包含心理指標與向量")