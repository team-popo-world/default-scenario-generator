import google.generativeai as genai
from util import extract_json, load_prompt
from config import GEMINI_API_KEY, GEMINI_MODEL, DEFAULT_TEMPERATURE
import json

def generate_news_scenario(
    theme,
    api_key=GEMINI_API_KEY,
    model_name=GEMINI_MODEL,
    temperature=DEFAULT_TEMPERATURE
):
    """
    테마별 7턴 뉴스 시나리오 생성 (Gemini용 함수형)
    """
    # 프롬프트 로딩 (테마별!)
    prompt_text = load_prompt(theme, "news")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

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