import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from Base.base_driver import BaseAppiumDriver
from Login.test_Login_passed import login_successful

# 스크린샷 헬퍼 함수
from Utils.screenshot_helper import save_screenshot_on_failure

# 동적 Xpath 생성 함수
from Utils.valid_credentials import get_user_data

# Xpath 저장소에서 HomeViewKilLocators 임포트
from Xpath.xpath_repository import HomeViewKilLocators

#인사말 확인 (10)
def test_greeting_message_view(flow_tester):
    """
    홈 화면에서 사용자 이름이 포함된 인사말이 노출되는지 확인합니다.
    """
    print("\n--- 홈 화면 인사말 노출 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # --- 플랫폼에 맞는 로케이터 동적 선택 ---
    if flow_tester.platform == 'android':
        locators = HomeViewKilLocators.AOS
    else: # iOS 또는 기본값
        locators = HomeViewKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    try:
        # 1. 테스트 데이터 로드
        # valid_credentials.txt 파일의 경로를 현재 파일 위치 기준으로 설정
        data_file_path = os.path.join(os.path.dirname(__file__), '..', 'Login', 'valid_credentials.txt')
        user_info = get_user_data(data_file_path)
        print(f"💡 테스트 사용자 이름: {user_info['username']}")

        # 2. 동적 XPath 생성 (저장소의 템플릿 사용)
        # [수정] username만 사용하도록 템플릿 적용
        dynamic_greeting_xpath = locators.greeting_xpath_template.format(username=user_info['username'])
        print(f"💡 생성된 동적 XPath: {dynamic_greeting_xpath}")

        # 3. 인사말 노출 확인
        print("인사말 요소 노출을 확인합니다.")
        try:
            greeting_element = flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, dynamic_greeting_xpath)),
                 message=f"'{user_info['username']}'이 포함된 인사말 요소를 20초 내에 찾지 못했습니다."
            )
            print(f"✅ '{greeting_element.text}' 인사말이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "홈 화면 인사말 노출 확인 성공."
        except TimeoutException as e:
             result_message = f"인사말 노출 확인 실패 (타임아웃): {e}"
             print(f"❌ {result_message}")
             save_screenshot_on_failure(flow_tester.driver, "greeting_message_timeout")
             return False, result_message
        except Exception as e:
            result_message = f"인사말 노출 확인 중 오류 발생: {e}"
            print(f"❌ {result_message}")
            save_screenshot_on_failure(flow_tester.driver, "greeting_message_error")
            return False, result_message

    except FileNotFoundError:
        result_message = f"테스트 데이터 파일을 찾을 수 없습니다: {data_file_path}"
        print(f"🚨 {result_message}")
        return False, result_message
    except KeyError as e:
        result_message = f"테스트 데이터 파일 형식 오류: 키 '{e}'를 찾을 수 없습니다."
        print(f"🚨 {result_message}")
        return False, result_message
    except Exception as e:
        result_message = f"시나리오 실행 중 예상치 못한 오류 발생: {e}"
        print(f"🚨 {result_message}")
        save_screenshot_on_failure(flow_tester.driver, "greeting_message_unexpected_error")
        return False, result_message
    finally:
        print("--- 홈 화면 인사말 노출 확인 시나리오 종료 ---\n")

    return scenario_passed, result_message




# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from Utils.screenshot_helper import save_screenshot_on_failure
#
# def test_verify_greeting_message_in_menu(flow_tester):
#     """
#     전체 메뉴를 열고 "안녕하세요. 무엇을 도와드릴까요?" 버튼이 노출되는지 검증합니다.
#     """
#     print("\n--- 전체 메뉴 > 인사말 버튼 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. '전체메뉴' 버튼 클릭
#         menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#         print(f"'{menu_button_xpath}' (전체메뉴) 버튼을 클릭합니다.")
#         try:
#             menu_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, menu_button_xpath))
#             )
#             menu_button.click()
#             time.sleep(2)  # 메뉴가 열리는 애니메이션을 기다립니다.
#         except TimeoutException:
#             error_msg = "실패: '전체메뉴' 버튼을 찾거나 클릭할 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "greeting_menu_button_not_found")
#             return False, error_msg
#
#         # 2. "안녕하세요. 무엇을 도와드릴까요?" 버튼 노출 확인
#         greeting_button_xpath = '//android.widget.Button[@text="안녕하세요. 무엇을 도와드릴까요?"]'
#         print(f"'{greeting_button_xpath}' 버튼이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, greeting_button_xpath))
#             )
#             print("✅ 인사말 버튼이 성공적으로 노출되었습니다.")
#
#             # 3. 사이드 메뉴 내 특정 버튼 클릭
#             sidenav_button_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
#             print(f"'{sidenav_button_xpath}' 버튼을 클릭합니다.")
#             try:
#                 sidenav_button = WebDriverWait(flow_tester.driver, 10).until(
#                     EC.element_to_be_clickable((AppiumBy.XPATH, sidenav_button_xpath))
#                 )
#                 sidenav_button.click()
#                 print("✅ 사이드 메뉴 버튼을 성공적으로 클릭했습니다.")
#             except TimeoutException:
#                 error_msg = "실패: 사이드 메뉴 버튼을 찾거나 클릭할 수 없습니다."
#                 save_screenshot_on_failure(flow_tester.driver, "sidenav_button_not_found")
#                 return False, error_msg
#             # --- 로직 추가 종료 ---
#
#             return True, "전체 메뉴 내 인사말 버튼 확인 성공."
#
#         except TimeoutException:
#             error_msg = "실패: 전체 메뉴에서 인사말 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "greeting_message_button_not_found")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"인사말 버튼 확인 중 예외 발생: {e}"
#     finally:
#         print("--- 전체 메뉴 > 인사말 버튼 노출 확인 시나리오 종료 ---")