# 라이브러리 임포트
import os
import sys
import subprocess
import time
import re

# Import the specific test functions
from Utils.login_with_credentials import login_with_credentials,get_credentials_from_file
from Login.test_login_view import AppiumLoginviewTest
from Test_Run.test_Scenario_01 import test_login
from Test_Run.test_promotion_view import test_promotion_view
from Test_Run.test_self_pv_view import test_self_pv_view
from Test_Run.test_fullMenu_view import test_fullMenu_run
from Test_Run.test_lifestory_view import test_lifestory_view_run
from Utils.test_result_input import get_google_sheet_service_oauth,get_tester_name_from_sheet, SHEET_NAME,initialize_test_results_in_sheet
from Test_Run.test_mobile_order_view import test_mobile_order_view
from Test_Run.test_search_view import test_search_view_run
from Test_Run.test_my_page_view import test_my_page_view_run
from Test_Run.test_shared_content_kil_view import test_my_page_kil_view_run
from Test_Run.test_home_kil_view import test_home_kil_view_run
from Test_Run.test_my_page_kil_view import test_my_page_kil_view_run


if __name__ == "__main__":
    print("=========================================")
    print("   Appium 테스트 스위트 실행 시작")
    print("=========================================\n")

    overall_start_time = time.time()  # 전체 테스트 스위트 시작 시간 기록

    # Google Sheet 서비스 초기화 (OAuth 버전)
    sheets_service = get_google_sheet_service_oauth()
    if not sheets_service:
        print("Google Sheet 서비스 초기화에 실패하여 테스트 결과를 스프레드시트에 기록할 수 없습니다.")
        sys.exit(1)  # 서비스 초기화 실패 시 스크립트 종료

    # 테스트 시작 전에 L, M, N열을 초기화후, 'No Run' 자동 입력.
    print("\n--- 스프레드시트 테스트 결과 초기화 시작 ---")
    initialize_test_results_in_sheet(sheets_service, SHEET_NAME)
    print("--- 스프레드시트 테스트 결과 초기화 완료 ---\n")

    # 스프레드시트에서 테스터 이름을 가져옵니다.
    tester_name = get_tester_name_from_sheet(sheets_service, SHEET_NAME)
    print(f"테스트를 실행하는 테스터 이름: {tester_name}")

    overall_results = {}
    appium_tester = None  # appium_tester 초기화

    # --- 드라이버 초기화 (전체 테스트 스위트에서 한 번만 수행) ---
    print("--- Appium 드라이버를 초기화합니다. ---")
    appium_tester = AppiumLoginviewTest()
    appium_tester.setup_driver()
    print("--- 드라이버 초기화 완료. ---")
    print("-" * 50)

    # # --- test_login 시나리오 실행 ---
    # print("\n--- '로그인 테스트' 시나리오 시작 ---")
    # # sheets_service와 tester_name을 test_login 함수로 전달
    # login_passed, login_message = test_login(appium_tester, sheets_service, tester_name)
    # print("테스트 케이스 5 완료.")
    # print("-" * 50)
    """
    # --- test_fullMenu_view 시나리오 실행 ---
    print("\n--- '전체메뉴' 시나리오 시작 ---")
    # sheets_service와 tester_name을 test_login 함수로 전달
    full_menu_passed, full_menu_message = test_fullMenu_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    
    # --- test_self_pv_view 시나리오 실행 ---
    print("\n--- '셀프홍보영상 클릭 테스트' 시나리오 시작 ---")
    # sheets_service와 tester_name을 test_login 함수로 전달
    self_pv_passed, self_pv_message = test_self_pv_view(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    """
    # -- test_promotion_view 시나리오 실행 ---
    # print("\n--- '프로모션 테스트' 시나리오 시작 ---")
    # # sheets_service와 tester_name을 test_login 함수로 전달
    # full_menu_passed, full_menu_message = test_promotion_view(appium_tester, sheets_service, tester_name)
    # print("테스트 케이스 5 완료.")
    # print("-" * 50)
    """
    # --- test_lifestory_view_run 시나리오 실행 ---
    print("\n--- '라이프스토리' 시나리오 시작 ---")
    # sheets_service와 tester_name을 test_login 함수로 전달
    life_story_passed, life_story_message = test_lifestory_view_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    
    # --- test_mobile_order_view 시나리오 실행 ---
    print("\n--- '모바일주문 테스트' 시나리오 시작 ---")
    # sheets_service와 tester_name을 test_login 함수로 전달
    mobile_order_passed, mobile_order_message = test_mobile_order_view(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
  
    # --- test_search_view_run 시나리오 실행 ---
    print("\n--- 검색 시나리오 시작 ---")
    # sheets_service와 tester_name을 test_login 함수로 전달
    search_passed, search_message = test_search_view_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    
    # --- test_my_page_view_run 시나리오 실행 ---
    print("\n--- 검색 시나리오 시작 ---")
    # sheets_service와 tester_name을 test_login 함수로 전달
    my_page_passed, my_page_message = test_my_page_view_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    """

    """
    # --- test_home_kil_view_run 시나리오 실행 ---
    # sheets_service와 tester_name을 test_login 함수로 전달
    print("\n--- 홈 시나리오 시작 ---")
    my_page_passed, my_page_message = test_home_kil_view_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    """
    """
    # --- test_my_page_kil_view_run 시나리오 실행 ---
    # sheets_service와 tester_name을 test_login 함수로 전달
    print("\n--- 마이페이지 시나리오 시작 ---")
    my_page_passed, my_page_message = test_my_page_kil_view_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    """
    # --- test_shared_content_kil_view 시나리오 실행 ---
    print("\n--- 공유 콘텐츠 / 자료실 시나리오 시작 ---")
    my_page_passed, my_page_message = test_my_page_kil_view_run(appium_tester, sheets_service, tester_name)
    print("테스트 케이스 5 완료.")
    print("-" * 50)
    """
overall_end_time = time.time()  # 전체 테스트 스위트 종료 시간 기록
overall_duration = overall_end_time - overall_start_time  # 총 실행 시간 계산

# --- 최종 테스트 결과 종합 ---
print("\n=========================================")
print("   Appium 테스트 스위트 최종 종합 결과")
print("=========================================")

all_passed_overall = True
for test_name, result in overall_results.items():
    status = "✅ 성공" if result["passed"] else "❌ 실패"
    print(f"테스트명: {test_name}")
    print(f"결과: {status}")
    print(f"메시지: {result['message']}")
    print("-" * 30)
    if not result["passed"]:
        all_passed_overall = False

if all_passed_overall:
    print("\n🎉 모든 요청된 테스트 시나리오가 성공적으로 호출되었습니다!")
else:
    print("\n⚠️ 일부 요청된 테스트 시나리오 실행 중 오류가 발생했습니다. 로그를 확인하세요.")

print(f"전체 테스트 스위트 실행 시간: {overall_duration:.2f} 초")
print("   Appium 테스트 스위트 종료")
print("=========================================\n")

# 전체 테스트 스위트 종료 시 드라이버 정리
if appium_tester:
    appium_tester.teardown_driver()
    """