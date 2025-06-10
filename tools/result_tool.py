import google.generativeai as genai
from util import extract_json
import json
from config import GEMINI_API_KEY, GEMINI_MODEL, PIG_RESULT_PROMPT_PATH, DEFAULT_TEMPERATURE
from tools.news_tool import load_prompt
import os


def get_latest_json_file(dir_path="news_json_files", base_filename="news_json"):
    # 해당 디렉토리 내에서 base_filename으로 시작하는 .json 파일 리스트업
    files = [f for f in os.listdir(dir_path) if f.startswith(base_filename) and f.endswith(".json")]
    if not files:
        raise FileNotFoundError("해당 디렉토리에 news_json 파일이 없습니다.")
    # 파일명 기준으로 정렬 (YYYYMMDD_HHMMSS 순서)
    files.sort()
    latest_file = files[-1]
    latest_news_json_path = os.path.join(dir_path, latest_file)
    with open(latest_news_json_path, encoding="utf-8") as f:
        news_json = json.load(f)
    return news_json

def generate_result(
    user_input,
    news_json,
    api_key=GEMINI_API_KEY,
    model_name=GEMINI_MODEL,
    prompt_path=PIG_RESULT_PROMPT_PATH,
    temperature=DEFAULT_TEMPERATURE
):
    """
    아기돼지 삼형제 7턴 뉴스 시나리오 생성 (Gemini용 함수형)
    """
    # 프롬프트 로딩
    prompt = load_prompt(prompt_path)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt_text = f"{prompt}\n{news_json}\n{user_input}"

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
        result_json = json.loads(clean_result)
    except Exception as e:
        print("[파싱 에러] 원본 LLM 응답 출력:\n", result)
        raise e
    print(result_json)
    return result_json