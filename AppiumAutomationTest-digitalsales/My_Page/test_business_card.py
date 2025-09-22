# 라이브러리 임포트
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
from Login.test_Login_passed import run_successful_login_scenario

# 스크린샷 헬퍼 함수
from Utils.screenshot_helper import save_screenshot_on_failure

# 동적 Xpath 생성 함수
from Utils.valid_credentials import get_user_data


# 명함 설정 버튼 클릭 및 명함 설정 페이지 노출 확인 (51)
def test_business_card_button_view(flow_tester):
    # 명함 설정 버튼 노출 확인
    print("명함 설정 버튼 노출 및 클릭을 확인합니다.")
    business_card_button_view_xpath = '//android.widget.Button[@text="명함설정"]'
    try:
        business_card_button_view = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, business_card_button_view_xpath)),
            message=f"'{business_card_button_view_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        business_card_button_view.click()
        print("✅ 명함 설정 버튼 클릭 완료.")
        time.sleep(3)  # 페이지 전환 대기
        scenario_passed = True
        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "명함 설정 버튼 클릭 성공"
    except Exception as e:
        result_message = f"명함 설정 버튼 클릭 확인 실패: {e}"
        time.sleep(3)
        scenario_passed = False
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message

# 명함 설정 페이지 노출 확인 (52)
def test_business_card_page_view(flow_tester):
    scenario_passed = True
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    error_messages = []

    try:
        # 1. 테스트 데이터 로드
        data_file_path = os.path.join(os.path.dirname(__file__), '..', 'Login', 'valid_credentials.txt')
        user_info = get_user_data(data_file_path)

        # 명함 설정 페이지 노출 확인
        print("명함 설정 페이지의 '사용자명','직함','소속','연락처'를 확인합니다.")

        # 2. 동적 XPath 생성
        dynamic_username_xpath = f'//android.widget.TextView[@text="안녕하세요\n{user_info["username"]} {user_info["title"]}입니다."]'
        dynamic_title_xpath = f'//android.widget.TextView[@text="{user_info["title"]}"]'
        #dynamic_affiliation_xpath = f'//android.widget.TextView[@text=" {user_info["affiliation"]}"]'
        dynamic_affiliation_xpath = f'//android.widget.TextView[contains(@text, "{user_info["affiliation"]}")]'
        dynamic_contact_information_xpath = f'//android.widget.TextView[@text="{user_info["contact_information"]}"]'

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

# 인사말 노출 및 편집 버큰 클릭 확인 (53)
def test_greeting_edit_button_view(flow_tester):
    # 명함 설정 버튼 노출 확인
    print("인사말 노출 및 편집 버큰 클릭을 확인합니다.")
    greeting_view_xpath = '//android.widget.TextView[@text="항상 고객님만을 생각하겠습니다!"]'
    greeting_edit_button_xpath = '//android.widget.Button[@text="편집"]'
    greeting_edit_popup_exit_button_xpath = '//android.app.Dialog/android.widget.Button'
    try:
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, greeting_view_xpath)))
        print("✅ 인사말이 성공적으로 노출되었습니다.")

        greeting_edit_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, greeting_edit_button_xpath)),
            message=f"'{greeting_edit_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        greeting_edit_button.click()
        print("✅ 인사말 편집 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기

        greeting_edit_popup_exit_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, greeting_edit_popup_exit_button_xpath)),
            message=f"'{greeting_edit_popup_exit_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        greeting_edit_popup_exit_button.click()
        print("✅ 편집 팝업 'X' 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기

        scenario_passed = True
        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "인사말 편집 버튼 클릭 성공"

    except Exception as e:
        result_message = f"인사말 편집 버튼 클릭 확인 실패: {e}"
        time.sleep(3)
        scenario_passed = False
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message

# 명함 다운로드 버큰 클릭 확인 (54)
def test_download_business_card_button_view(flow_tester):
    # 명함 설정 버튼 노출 확인
    print("명함 다운로드 버큰 클릭을 확인합니다.")
    download_business_card_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'
    download_business_card_popup_ok_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
    download_business_card_popup_ok_button_id = 'android:id/button1'
    download_business_card_popup_cancel_button_xpath = '//android.widget.Button[@resource-id="android:id/button2"]'
    try:
        download_business_card_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, download_business_card_button_xpath)),
            message=f"'{download_business_card_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        download_business_card_button.click()
        print("✅ 명함 다운로드 버튼 클릭 완료.")
        time.sleep(2)  # 팝업 노출 대기

        # 명함 다운로드 팝업 '확인' 버튼 클릭 (ID 사용)
        download_business_card_popup_ok_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, download_business_card_popup_ok_button_id)),
            message=f"'{download_business_card_popup_ok_button_id}' 버튼을 20초 내에 찾지 못했습니다."
        )
        download_business_card_popup_ok_button.click()
        print("✅ 명함 다운로드 팝업 '확인' 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기

        scenario_passed = True
        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "명함 다운로드 버튼 클릭 성공"
    except Exception as e:
        result_message = f"명함 다운로드 버튼 클릭 확인 실패: {e}"
        time.sleep(2)
        scenario_passed = False
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message

# 텍스트 명함 복사 버큰 클릭 확인 (55)
def test_copy_text_business_card_button_view(flow_tester):
    # 명함 설정 버튼 노출 확인
    print("텍스트 명함 복사 버큰 클릭을 확인합니다.")
    copy_text_business_card_button_xpath = '//android.widget.Button[@text="텍스트 명함 복사"]'
    try:
        copy_text_business_card_button_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, copy_text_business_card_button_xpath)),
            message=f"'{copy_text_business_card_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        copy_text_business_card_button_button.click()
        print("✅ 텍스트 명함 복사 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기

        # 4. 뒤로가기 (Back) 액션 수행 (프로모션 상세 -> 전체메뉴)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

        scenario_passed = True
        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "텍스트 명함 복사 버튼 클릭 성공"
    except Exception as e:
        result_message = f"텍스트 명함 복사 버튼 클릭 확인 실패: {e}"
        time.sleep(3)
        scenario_passed = False
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")