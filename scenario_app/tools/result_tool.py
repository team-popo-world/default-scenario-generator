import google.generativeai as genai
from ..util import extract_json, load_prompt
import json
from ..config import GEMINI_API_KEY, GEMINI_MODEL, DEFAULT_TEMPERATURE


def generate_result(
    theme,
    news_json,
    api_key=GEMINI_API_KEY,
    model_name=GEMINI_MODEL,
    temperature=DEFAULT_TEMPERATURE
):
    """
    아기돼지 삼형제 7턴 뉴스 시나리오 생성 (Gemini용 함수형)
    """
    # 프롬프트 로딩
    prompt = load_prompt(theme, "result")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt_text = f"{prompt}\n{news_json}"

    response = model.generate_content(
        [
            {"role": "user", "parts": [{"text": prompt_text}]}
        ],
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 15000
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