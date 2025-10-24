# PythonProject/Home_View_kil/test_home_button_visibility.py

import sys
import os
import time

# Ensure the project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import locators from the repository
from Xpath.xpath_repository import HomeViewKilLocators # 수정: 클래스 임포트

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def test_verify_home_button_visibility(flow_tester):
    """Verifies the visibility of the home button (alternative XPath)."""
    print("\n--- 홈 버튼 (대체 경로) 노출 확인 시작 ---")
    scenario_passed = True
    result_message = "홈 버튼 (대체 경로) 노출 확인 성공."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = HomeViewKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = HomeViewKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = HomeViewKilLocators.AOS

    try:
        print("1. 홈 버튼 (대체 경로) 확인")
        home_button = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.home_button_alt_xpath)) # 공통 로케이터 사용
        )
        # is_displayed() 체크 추가
        if home_button.is_displayed():
            print("   ✅ 홈 버튼 (대체 경로) 확인 완료.")
        else:
            print("   ❌ 홈 버튼 (대체 경로)이 DOM에는 있지만 화면에 보이지 않습니다.")
            scenario_passed = False
            result_message = "홈 버튼 (대체 경로)이 화면에 보이지 않음."
            flow_tester.driver.save_screenshot("failure_home_btn_alt_not_displayed.png")


    except TimeoutException as e:
        scenario_passed = False
        result_message = f"홈 버튼 (대체 경로) 확인 실패 (타임아웃): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_home_btn_alt_timeout.png")
    except NoSuchElementException as e:
        scenario_passed = False
        result_message = f"홈 버튼 (대체 경로) 확인 실패 (요소 찾기 실패): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_home_btn_alt_no_such_element.png")
    except Exception as e:
        scenario_passed = False
        result_message = f"홈 버튼 (대체 경로) 확인 중 예상치 못한 오류 발생: {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_home_btn_alt_unexpected.png")
    finally:
        print("--- 홈 버튼 (대체 경로) 노출 확인 종료 ---")

    return scenario_passed, result_message

# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from Utils.screenshot_helper import save_screenshot_on_failure
#
# def test_verify_home_button_visibility(flow_tester):
#     """
#     홈 화면의 특정 버튼이 노출되는지 검증합니다.
#     """
#     print("\n--- 홈 화면 > 특정 버튼 노출 확인 시나리오 시작 ---")
#     try:
#         # ※ 사전 조건: 앱 실행 후 홈 화면에 진입한 상태
#
#         # 1. 확인할 버튼의 XPath 정의
#         home_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
#         print(f"홈 화면에서 버튼({home_button_xpath})이 노출되는지 확인합니다.")
#
#         # 2. 버튼이 화면에 나타나는지 최대 15초간 대기
#         try:
#             WebDriverWait(flow_tester.driver, 15).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, home_button_xpath))
#             )
#             print("✅ 버튼이 성공적으로 노출되었습니다.")
#             return True, "홈 화면 버튼 노출 확인 성공."
#         except TimeoutException:
#             error_msg = f"실패: 홈 화면에서 버튼을 찾을 수 없습니다. (XPath: {home_button_xpath})"
#             save_screenshot_on_failure(flow_tester.driver, "home_button_not_visible")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"홈 화면 버튼 확인 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 화면 > 특정 버튼 노출 확인 시나리오 종료 ---")