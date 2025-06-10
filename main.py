# main.py

from tools.news_tool import generate_news_scenario, save_json_to_dir
from tools.result_tool import get_latest_json_file, generate_result

def main():
    # 1. 테마 선택
    themes = ["pig", "food", "magic", "moon"]
    print("테마를 선택하세요:")
    for i, theme in enumerate(themes):
        print(f"{i+1}. {theme}")
    choice = input("번호를 입력하세요 (1~4): ").strip()
    try:
        theme = themes[int(choice)-1]
    except (ValueError, IndexError):
        print("잘못된 입력입니다. 기본 테마 'pig'로 진행합니다.")
        theme = "pig"
    print(f"선택된 테마: {theme}")

    # 2. 유저 입력 정의
    user_input = f"{theme} 테마 기반 7턴짜리 게임 시나리오를 작성해줘."

    # 3. 뉴스 시나리오 생성
    print("1. 뉴스 시나리오 생성 중...")
    news_json = generate_news_scenario(user_input, theme=theme)

    # 4. 저장 (파일명 자동 생성, news_json_files 디렉토리 사용)
    print("2. 뉴스 JSON 파일 저장 중...")
    save_json_to_dir(news_json)

    # 5. 뉴스 불러오기
    print("3. 최신 뉴스 파일 불러오기...")
    get_latest_json_file()

    # 6. 최종 시나리오 생성
    print("4. 최종 시나리오(result) 생성 중...")
    result_json = generate_result(user_input, news_json, theme=theme)

    # 7. 결과 저장
    print("5. 결과(result) 파일 저장 중...")
    save_json_to_dir(result_json, dir_path="result_json_files", base_filename="result_json")

if __name__ == "__main__":
    main()