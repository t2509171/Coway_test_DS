import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy # AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Xpath 저장소에서 HomeViewKilLocators 임포트
from Xpath.xpath_repository import HomeViewKilLocators

# 스크린샷 헬퍼 임포트
from Utils.screenshot_helper import save_screenshot_on_failure

#홈 버튼 노출 확인 (11)
def test_home_button_visibility(flow_tester):
    """
    홈 화면 하단에 홈, 관리고객, 모바일 주문, 마이페이지 버튼이 노출되는지 확인합니다.
    """
    print("\n--- 홈 화면 하단 네비게이션 버튼 노출 확인 시나리오 시작 ---")
    scenario_passed = True
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    error_messages = []

    # --- 플랫폼에 맞는 로케이터 동적 선택 ---
    if flow_tester.platform == 'android':
        locators = HomeViewKilLocators.AOS
    else: # iOS 또는 기본값
        locators = HomeViewKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    try:
        print("홈 화면 하단 네비게이션 버튼들의 노출을 확인합니다.")

        # 검증할 버튼 목록 (XPath와 버튼 이름)
        buttons_to_check = [
            (locators.home_button_xpath, "홈"),
            (locators.managed_customer_button_xpath, "관리고객"),
            (locators.mobile_order_button_xpath, "모바일 주문"),
            (locators.my_page_button_xpath, "마이페이지")
        ]

        # 모든 버튼에 대해 순차적으로 노출 확인
        for xpath, name in buttons_to_check:
            print(f"'{name}' 버튼 노출을 확인합니다.")
            try:
                flow_tester.wait.until(
                    EC.presence_of_element_located((AppiumBy.XPATH, xpath)),
                     message=f"'{name}' 버튼 요소를 20초 내에 찾지 못했습니다."
                )
                print(f"✅ '{name}' 버튼이 성공적으로 노출되었습니다.")
            except TimeoutException as e:
                error_msg = f"'{name}' 버튼 노출 확인 실패 (타임아웃): {e}"
                print(f"❌ {error_msg}")
                error_messages.append(error_msg)
                scenario_passed = False # 하나라도 실패하면 전체 시나리오 실패
            except Exception as e:
                error_msg = f"'{name}' 버튼 노출 확인 중 오류 발생: {e}"
                print(f"❌ {error_msg}")
                error_messages.append(error_msg)
                scenario_passed = False

        # 모든 버튼 확인 후 최종 결과 메시지 정리
        if scenario_passed:
            result_message = "홈 화면 하단 네비게이션 버튼 모두 노출 확인 성공."
            print(f"✅ {result_message}")
        else:
            result_message = "홈 화면 하단 네비게이션 버튼 중 일부 노출 확인 실패."
            save_screenshot_on_failure(flow_tester.driver, "bottom_nav_visibility_failure")
            print(f"⚠️ {result_message}")
            # 상세 실패 메시지를 반환
            return False, "\n".join(error_messages)

    except Exception as e:
        result_message = f"시나리오 실행 중 예상치 못한 오류 발생: {e}"
        print(f"🚨 {result_message}")
        save_screenshot_on_failure(flow_tester.driver, "bottom_nav_visibility_unexpected_error")
        return False, result_message
    finally:
        print("--- 홈 화면 하단 네비게이션 버튼 노출 확인 시나리오 종료 ---\n")

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