# main.py

from tools.news_tool import generate_news_scenario
from tools.result_tool import generate_result
from util import save_json_to_dir, get_latest_json_file

def main():
    
    # 1. 테마 선택
    themes = ["pig", "food", "magic", "moon"]
    print("테마를 선택하세요:")
    print(f"가능한 테마: {', '.join(themes)}")

    while True:
        choice = input("원하는 테마를 정확히 입력하세요: ").strip().lower()
        if choice in themes:
            theme = choice
            break
        else:
            print("잘못된 입력입니다. 주어진 테마 중 하나를 다시 입력하세요.")

    print(f"선택된 테마: {theme}")

    # 2. news 시나리오 생성
    print("1. 뉴스 시나리오 생성 중...")
    news_json = generate_news_scenario(theme)

    # 3. 저장 (파일명 자동 생성, news_json_files 디렉토리 사용)
    print("2. 뉴스 JSON 파일 저장 중...")
    save_json_to_dir(news_json, f"news_json_files\{theme}", f"{theme}_news_json")

    # 4. 뉴스 불러오기
    print("3. 테마에 해당하는 최신 뉴스 파일 불러오기...")
    get_latest_json_file(theme, f"news_json_files\{theme}")

    # 5. 최종 시나리오 생성
    print("4. 최종 시나리오(result) 생성 중...")
    result_json = generate_result(theme, news_json)

    # 6. 결과 저장
    print("5. 결과(result) 파일 저장 중...")
    save_json_to_dir(result_json, f"result_json_files\{theme}", f"{theme}_result_json")

if __name__ == "__main__":
    main()

