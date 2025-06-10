import google.generativeai as genai
import json
from util import extract_json
from config import GEMINI_API_KEY, GEMINI_MODEL, PIG_NEWS_PROMPT_PATH, DEFAULT_TEMPERATURE
from datetime import datetime
import os

def load_prompt(prompt_path):
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_news_scenario(
    user_input,
    api_key=GEMINI_API_KEY,
    model_name=GEMINI_MODEL,
    prompt_path=PIG_NEWS_PROMPT_PATH,
    temperature=DEFAULT_TEMPERATURE
):
    """
    아기돼지 삼형제 7턴 뉴스 시나리오 생성 (Gemini용 함수형)
    """
    # 프롬프트 로딩
    prompt = load_prompt(prompt_path)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt_text = f"{prompt}\n\n{user_input}"

    response = model.generate_content(
        [
            {"role": "user", "parts": [{"text": prompt_text}]}
        ],
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 10000
        }
    )
    result = response.candidates[0].content.parts[0].text
    try:
        clean_result = extract_json(result)
        news_json = json.loads(clean_result)
    except Exception as e:
        print("[파싱 에러] 원본 LLM 응답 출력:\n", result)
        raise e
    return news_json

def save_json_to_dir(data, dir_path="news_json_files", base_filename="news_json"):
    # 디렉토리 자동 생성 (최초 실행 때만 실제 생성됨)
    os.makedirs(dir_path, exist_ok=True)
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(dir_path, f"{base_filename}_{now_str}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[저장됨] {file_path}")
    return file_path
