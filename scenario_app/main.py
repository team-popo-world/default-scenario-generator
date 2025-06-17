# main.py
import os
import logging
import traceback
from .tools.news_tool import generate_news_scenario
from .tools.result_tool import generate_result
from .util import save_json_to_dir, get_latest_json_file

def main(theme, n):
    logging.basicConfig(
        filename=os.path.join(os.path.dirname(__file__),'scenario_generator_log.log'),
        level=logging.INFO,
        encoding="utf-8")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    news_dir = os.path.join(base_path, "news_json_files", theme)
    result_dir = os.path.join(base_path, "result_json_files", theme)
    os.makedirs(news_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    success_count = 0
    total_attempts = 0
    max_attempts = n * 2  # 무한루프 방지

    while success_count < n and total_attempts < max_attempts:
        total_attempts += 1
        try:
            # 1. 뉴스 생성
            try:
                logging.info(f"[{theme}][{success_count+1}] [뉴스 생성] 시작")
                news_json = generate_news_scenario(theme)
                logging.info(f"[{theme}][{success_count+1}] [뉴스 생성] 성공")
            except Exception as e:
                logging.error(f"[{theme}][{success_count+1}] [뉴스 생성] 실패: {e}")
                logging.error(traceback.format_exc())
                print(f"[{theme}] {success_count+1}번째 뉴스 생성 실패: {e}")
                continue  # 다음 시도

            # 2. 뉴스 저장
            try:
                logging.info(f"[{theme}][{success_count+1}] [뉴스 저장] 시작")
                save_json_to_dir(news_json, news_dir, f"{theme}_news_json_{success_count+1}")
                logging.info(f"[{theme}][{success_count+1}] [뉴스 저장] 성공")
            except Exception as e:
                logging.error(f"[{theme}][{success_count+1}] [뉴스 저장] 실패: {e}")
                logging.error(traceback.format_exc())
                print(f"[{theme}] {success_count+1}번째 뉴스 저장 실패: {e}")
                continue

            # 3. 최신 뉴스 파일 불러오기 (옵션)
            try:
                logging.info(f"[{theme}][{success_count+1}] [뉴스 불러오기] 시작")
                get_latest_json_file(theme, news_dir)
                logging.info(f"[{theme}][{success_count+1}] [뉴스 불러오기] 성공")
            except Exception as e:
                logging.error(f"[{theme}][{success_count+1}] [뉴스 불러오기] 실패: {e}")
                logging.error(traceback.format_exc())
                print(f"[{theme}] {success_count+1}번째 뉴스 불러오기 실패: {e}")
                continue

            # 4. 결과 생성
            try:
                logging.info(f"[{theme}][{success_count+1}] [결과 생성] 시작")
                result_json = generate_result(theme, news_json)
                logging.info(f"[{theme}][{success_count+1}] [결과 생성] 성공")
            except Exception as e:
                logging.error(f"[{theme}][{success_count+1}] [결과 생성] 실패: {e}")
                logging.error(traceback.format_exc())
                print(f"[{theme}] {success_count+1}번째 결과 생성 실패: {e}")
                continue

            # 5. 결과 저장
            try:
                logging.info(f"[{theme}][{success_count+1}] [결과 저장] 시작")
                save_json_to_dir(result_json, result_dir, f"{theme}_result_json_{success_count+1}")
                logging.info(f"[{theme}][{success_count+1}] [결과 저장] 성공")
            except Exception as e:
                logging.error(f"[{theme}][{success_count+1}] [결과 저장] 실패: {e}")
                logging.error(traceback.format_exc())
                print(f"[{theme}] {success_count+1}번째 결과 저장 실패: {e}")
                continue

            # 성공 카운트
            success_count += 1
            logging.info(f"[{theme}][{success_count}]번째 시나리오 전체 성공 (총 시도 {total_attempts})")

        except Exception as e:
            logging.error(f"[{theme}][{success_count+1}] [전체 시도] 예기치 못한 오류: {e}")
            logging.error(traceback.format_exc())
            print(f"[{theme}] {success_count+1}번째 전체 시도 오류: {e}")

    if success_count < n:
        logging.error(f"[{theme}] {n}개를 생성하지 못했습니다. (성공 {success_count}개)")
        print(f"[{theme}] {n}개를 생성하지 못했습니다. (성공 {success_count}개)")
        raise Exception(f"[{theme}] {n}개를 생성하지 못했습니다. (성공 {success_count}개)")

    logging.info(f"[{theme}] 최종 {n}개 생성/저장 완료! (총 시도 {total_attempts}회)")
    print(f"\n[{theme}] 최종 {n}개 생성/저장 완료! (총 시도 {total_attempts}회)")

if __name__ == "__main__":
    # 로컬 실행 시 원하는 값 직접 입력
    theme = input("테마를 입력하세요(pig, food, magic, moon): ").strip().lower()
    n = int(input("몇 개의 시나리오를 생성할까요? (숫자): ").strip())
    main(theme, n)

