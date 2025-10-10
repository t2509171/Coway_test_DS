import re
import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from Base.base_driver import BaseAppiumDriver
from Login.test_Login_passed import login_successful

# 스크린샷 헬퍼 함수
from Utils.screenshot_helper import save_screenshot_on_failure

# 동적 Xpath 생성 함수
from Utils.valid_credentials import get_user_data


#명함 설정 페이지 노출 확인 (52)
# def test_business_card_page_view(flow_tester):
#     scenario_passed = True
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#     error_messages = []
#
#     try:
#         # 1. 테스트 데이터 로드
#         data_file_path = os.path.join(os.path.dirname(__file__), '..', 'Login', 'valid_credentials.txt')
#         user_info = get_user_data(data_file_path)
#
#         # 명함 설정 페이지 노출 확인
#         print("명함 설정 페이지의 '사용자명','직함','소속','연락처'를 확인합니다.")
#
#         # 2. 동적 XPath 생성
#         dynamic_username_xpath = f'//android.widget.TextView[@text="안녕하세요 {user_info["username"]} {user_info["title"]}입니다."]'
#         dynamic_title_xpath = f'//android.widget.TextView[@text="{user_info["title"]}"]'
#         #dynamic_affiliation_xpath = f'//android.widget.TextView[@text=" {user_info["affiliation"]}"]'
#         dynamic_affiliation_xpath = f'//android.widget.TextView[contains(@text, "{user_info["affiliation"]}")]'
#         dynamic_contact_information_xpath = f'//android.widget.TextView[@text="{user_info["contact_information"]}"]'
#
#         elements_to_check = [
#             (dynamic_username_xpath, "사용자명"),
#             (dynamic_title_xpath, "직함"),
#             (dynamic_affiliation_xpath, "소속"),
#             (dynamic_contact_information_xpath, "연락처")
#         ]
#
#         # 3. 모든 요소에 대해 순차적으로 노출 확인
#         for xpath, name in elements_to_check:
#             print(f"'{name}' 요소 노출을 확인합니다.")
#             try:
#                 flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#                 print(f"✅ '{name}' 요소가 성공적으로 노출되었습니다.")
#             except Exception as e:
#                 error_msg = f"❌ '{name}' 요소 노출 확인 실패: {e}"
#                 print(error_msg)
#                 error_messages.append(error_msg)
#                 scenario_passed = False  # 하나라도 실패하면 전체 시나리오 실패로 설정
#
#         # 모든 요소 확인 후 최종 결과 메시지 정리
#         if not scenario_passed:
#             result_message = "명함 설정 페이지의 일부 UI 요소 노출 확인 실패."
#             save_screenshot_on_failure(flow_tester.driver, "business_card_page_view_failure")
#             print(f"⚠️ {result_message}")
#             return False, "\n".join(error_messages)
#
#         print(f"✅ 명함 설정 페이지의 모든 UI 요소 노출 확인 완료.")
#         return True, result_message
#
#     except TimeoutException as e:
#         result_message = f"명함 설정 페이지의 UI 요소 노출 확인 중 타임아웃 오류 발생: {e}"
#         print(f"❌ {result_message}")
#         save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
#         return False, result_message
#     except Exception as e:
#         result_message = f"명함 설정 페이지의 UI 요소 노출 확인 중 예상치 못한 오류 발생: {e}"
#         print(f"🚨 {result_message}")
#         save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
#         return False, result_message




#명함 설정 페이지 노출 확인 (52)

def test_business_card_page_view(flow_tester):
    scenario_passed = True
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    error_messages = []

    try:
        # 1. 테스트 데이터 로드
        data_file_path = os.path.join(os.path.dirname(__file__), '..', 'Login', 'valid_credentials.txt')
        user_info = get_user_data(data_file_path)

        # 명함 설정 페이지 노출 확인
        print(f'명함 설정 페이지의  {user_info["username"]}, {user_info["title"]}, {user_info["title"]}, {user_info["affiliation"]}, {user_info["contact_information"]}  를 확인합니다.')

        # 2. 동적 XPath 생성
        dynamic_username_xpath = f'//android.widget.TextView[@text="안녕하세요\n{user_info["username"]} {user_info["title"]}입니다."]'
        dynamic_title_xpath = f'//android.widget.TextView[@text="{user_info["title"]}"]'
        dynamic_affiliation_xpath = f'//android.widget.TextView[contains(@text, "{user_info["affiliation"]}")]'
        dynamic_contact_information_xpath = f'//android.widget.TextView[@text="{user_info["contact_information"]}"]'
        # dynamic_username_xpath = '//android.widget.TextView[@text="안녕하세요 권정숙 코디입니다."]'
        print(dynamic_username_xpath)
        print(dynamic_title_xpath)
        print(dynamic_affiliation_xpath)
        print(dynamic_contact_information_xpath)

        elements_to_check = [
            (dynamic_username_xpath, "사용자명"),
            (dynamic_title_xpath, "직함"),
            (dynamic_affiliation_xpath, "소속"),
            (dynamic_contact_information_xpath, "연락처")
        ]

        # 3. 모든 요소에 대해 순차적으로 노출 확인
        for xpath, name in elements_to_check:
            print(f"'{name}' 요소 노출을 확인합니다.")
            try:
                flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
                print(f"✅ '{name}' 요소가 성공적으로 노출되었습니다.")
            except Exception as e:
                error_msg = f"❌ '{name}' 요소 노출 확인 실패: {e}"
                print(error_msg)
                error_messages.append(error_msg)
                scenario_passed = False  # 하나라도 실패하면 전체 시나리오 실패로 설정

        # 모든 요소 확인 후 최종 결과 메시지 정리
        if not scenario_passed:
            result_message = "명함 설정 페이지의 일부 UI 요소 노출 확인 실패."
            save_screenshot_on_failure(flow_tester.driver, "business_card_page_view_failure")
            print(f"⚠️ {result_message}")
            return False, "\n".join(error_messages)

        print(f"✅ 명함 설정 페이지의 모든 UI 요소 노출 확인 완료.")
        return True, result_message

    except TimeoutException as e:
        result_message = f"명함 설정 페이지의 UI 요소 노출 확인 중 타임아웃 오류 발생: {e}"
        print(f"❌ {result_message}")
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        return False, result_message
    except Exception as e:
        result_message = f"명함 설정 페이지의 UI 요소 노출 확인 중 예상치 못한 오류 발생: {e}"
        print(f"🚨 {result_message}")
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        return False, result_message