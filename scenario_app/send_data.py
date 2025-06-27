import os
import json
import requests
import logging
from .config import API_URL
from .summary_generator import generate_story_summary_with_llm, generate_story_summary, initialize_llm

def send_data():
    # LLM 초기화
    initialize_llm()
    
    # logging 설정 (파일 + 콘솔 둘 다 기록)
    log_path = os.path.join(os.path.dirname(__file__), 'scenario_send_log.log')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()  # 이 줄이 핵심! Airflow UI에서 로그가 잘 보임
        ]
    )

    chapter_id_map = {
        "pig": "1111",
        "food": "2222",
        "magic": "3333",
        "moon": "4444"
    }

    base_path = os.path.dirname(os.path.abspath(__file__))
    base_folder = os.path.join(base_path, "result_json_files")

    scenario_list = []

    for theme, chapter_id in chapter_id_map.items():
        theme_dir = os.path.join(base_folder, theme)
        if not os.path.isdir(theme_dir):
            continue
        for filename in os.listdir(theme_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(theme_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        scenario_json = json.load(f)
                    
                    # JSON을 문자열로 변환
                    story_str = json.dumps(scenario_json, ensure_ascii=False)
                    
                    # LLM을 통한 요약 생성
                    try:
                        summary = generate_story_summary_with_llm(story_str)
                        logging.info(f"[요약생성 성공] {filename}: {summary[:50]}...")
                    except Exception as summary_error:
                        summary = generate_story_summary(story_str)
                        logging.warning(f"[요약생성 실패, 기본요약 사용] {filename}: {summary_error}")
                    
                    scenario_data = {
                        "chapterId": chapter_id,
                        "story": story_str,  # 문자열 변환
                        "summary": summary,  # 요약 추가
                        "isCustom": False
                    }
                    scenario_list.append(scenario_data)
                    logging.info(f"[파일로드 성공] {file_path}")
                except Exception as e:
                    logging.error(f"[파일로드 실패] {file_path}: {e}")

    print(f"총 {len(scenario_list)}개 시나리오 준비 완료!")  # 이 print도 Web UI에 바로 표시됨
    logging.info(f"총 {len(scenario_list)}개 시나리오 준비 완료!")

    # 하나씩 반복 전송
    success = 0
    fail = 0

    for idx, scenario_data in enumerate(scenario_list, 1):
        try:
            response = requests.post(API_URL, json=scenario_data, timeout=10)
            if response.status_code == 200 or response.status_code == 201:
                msg = f"[{idx}] 업로드 성공: {response.status_code}"
                print(msg)
                logging.info(msg)
                success += 1
            else:
                msg = f"[{idx}] 업로드 실패: {response.status_code} | {response.text}"
                print(msg)
                logging.error(msg)
                fail += 1
        except Exception as e:
            msg = f"[{idx}] 예외 발생: {e}"
            print(msg)
            logging.error(msg)
            fail += 1

    result_msg = f"업로드 완료! 성공: {success}개, 실패: {fail}개"
    print(result_msg)
    logging.info(result_msg)

if __name__ == "__main__":
    send_data()