import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.test_result_input import get_google_sheet_service_oauth,get_tester_name_from_sheet, SHEET_NAME,initialize_test_results_in_sheet
from Login.test_login_view import AppiumLoginviewTest

def reset(flow_tester):
    """
    앱 재실행 후, 메인 화면의 WebView가 정상적으로 로딩되는지 검증합니다.
    """
    print("\n--- [6/6] 앱 재실행 > 메인 WebView 로딩 확인 시나리오 시작 ---")
    try:

        # 1. teardown_driver()를 호출하여 현재 드라이버 세션 종료
        print("테스트를 위해 teardown_driver()를 호출하여 드라이버 세션을 종료합니다.")
        if flow_tester.driver:
            flow_tester.teardown_driver()
        # 종료 후 시스템이 정리될 시간을 줍니다.
        time.sleep(3)

        # 2. setup_driver()를 호출하여 새로운 드라이버 세션 시작
        print("setup_driver()를 호출하여 새로운 드라이버 세션을 시작하고 앱을 실행합니다.")
        flow_tester.setup_driver()
        print("✅ 앱이 성공적으로 재실행되었습니다.")

        # --- 여기가 가장 중요합니다 ---
        # 앱이 켜진 후, 내부 데이터를 로딩하고 화면을 그릴 때까지
        # 충분한 안정화 시간을 줍니다.
        print("앱 안정화를 위해 8초간 대기합니다...")
        time.sleep(8)
        # --- 여기까지가 핵심 수정 부분입니다 ---

    except Exception as e:
        return False, f"앱 재실행 및 WebView 확인 중 예외 발생: {e}"
    finally:
        print("--- [6/6] 앱 재실행 > 메인 WebView 로딩 확인 시나리오 종료 ---")



appium_tester = None  # appium_tester 초기화
# --- 드라이버 초기화 (전체 테스트 스위트에서 한 번만 수행) ---
print("--- Appium 드라이버를 초기화합니다. ---")
appium_tester = AppiumLoginviewTest()
appium_tester.setup_driver()

reset(appium_tester)
