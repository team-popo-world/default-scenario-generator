import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 읽기 (API 키, 경로 등)
load_dotenv()

# OpenAI API 키
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 사용할 LLM 모델명
OPENAI_MODEL = "gpt-4.1-mini"

# 디폴트 temperature
DEFAULT_TEMPERATURE = 0.8

# 프롬프트 경로
PIG_NEWS_PROMPT_PATH = "./templates/pig/news_prompt.txt"
PIG_RESULT_PROMPT_PATH = "./templates/pig/result_prompt.txt"
# Gemini API 키
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 사용할 LLM 모델명
GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"