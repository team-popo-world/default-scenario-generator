import re
from datetime import datetime
import os
import json

def extract_json(text):
    # 코드블록(```json ... ```) 제거
    text = text.strip()
    codeblock_pattern = r"```(?:json)?(.*?)```"
    match = re.search(codeblock_pattern, text, re.DOTALL)
    if match:
        json_text = match.group(1).strip()
    else:
        json_text = text
    # 가장 먼저 나오는 [ 또는 {부터 끝까지 추출
    start = min([json_text.find(c) if json_text.find(c) != -1 else 99999 for c in ['[', '{']])
    if start != 99999:
        json_text = json_text[start:]
    return json_text

def load_prompt(theme, prompt_type):
    base_path = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_path, "templates", theme, f"{prompt_type}_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def save_json_to_dir(data, dir_path="unknown_json_files", base_filename="unknown_json"):
    # __file__ 기준 절대경로 사용
    base_path = os.path.dirname(os.path.abspath(__file__))
    abs_dir_path = os.path.join(base_path, dir_path)
    os.makedirs(abs_dir_path, exist_ok=True)
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(abs_dir_path, f"{base_filename}_{now_str}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[저장됨] {file_path}")
    return file_path

def get_latest_json_file(base_filename, dir_path="news_json_files"):
    base_path = os.path.dirname(os.path.abspath(__file__))
    abs_dir_path = os.path.join(base_path, dir_path)
    # 해당 디렉토리 내에서 base_filename으로 시작하는 .json 파일 리스트업
    files = [f for f in os.listdir(abs_dir_path) if f.startswith(base_filename) and f.endswith(".json")]
    if not files:
        raise FileNotFoundError("해당 디렉토리에 news_json 파일이 없습니다.")
    files.sort()
    latest_file = files[-1]
    latest_news_json_path = os.path.join(abs_dir_path, latest_file)
    with open(latest_news_json_path, encoding="utf-8") as f:
        news_json = json.load(f)
    return news_json
