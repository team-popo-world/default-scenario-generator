import os
import json
import requests
from config import API_URL

chapter_id_map = {
    "pig": "1111",
    "food": "2222",
    "magic": "3333",
    "moon": "4444"
}

base_folder = "result_json_files"

scenario_list = []

for theme, chapter_id in chapter_id_map.items():
    theme_dir = os.path.join(base_folder, theme)
    if not os.path.isdir(theme_dir):
        continue
    for filename in os.listdir(theme_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(theme_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                scenario_json = json.load(f)
            scenario_data = {
                "chapterId": chapter_id,
                "story": json.dumps(scenario_json, ensure_ascii=False),  # 문자열 변환
                "isCustom": False
            }
            scenario_list.append(scenario_data)

print(f"총 {len(scenario_list)}개 시나리오 준비 완료!")

# 하나씩 반복 전송
success = 0
fail = 0

for idx, scenario_data in enumerate(scenario_list, 1):
    response = requests.post(API_URL, json=scenario_data)
    if response.status_code == 200 or response.status_code == 201:
        print(f"[{idx}] 성공: {response.status_code}")
        success += 1
    else:
        print(f"[{idx}] 실패: {response.status_code} | {response.text}")
        fail += 1

print(f"업로드 완료! 성공: {success}개, 실패: {fail}개")
