import os
import json
import requests
import logging
from .config import API_URL

def send_data():
    # logging 설정
    logging.basicConfig(
        filename=os.path.join(os.path.dirname(__file__),'scenario_send_log.log'),
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s] %(message)s"
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
                    scenario_data = {
                        "chapterId": chapter_id,
                        "story": json.dumps(scenario_json, ensure_ascii=False),  # 문자열 변환
                        "isCustom": False
                    }
                    scenario_list.append(scenario_data)
                    logging.info(f"[파일로드 성공] {file_path}")
                except Exception as e:
                    logging.error(f"[파일로드 실패] {file_path}: {e}")

    print(f"총 {len(scenario_list)}개 시나리오 준비 완료!")
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