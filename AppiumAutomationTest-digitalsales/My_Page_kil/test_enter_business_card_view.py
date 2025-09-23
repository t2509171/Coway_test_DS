# -*- coding: utf-8 -*-

# 라이브러리 임포트
import time
import os
import sys

# Appium 라이브러리
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 프로젝트 내부 모듈
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.locator_manager import get_locator

# 명함 설정 버튼 클릭 및 명함 설정 페이지 노출 확인 (TC: Seller app checklist-54)
def test_enter_business_card_view(flow_tester):
    """
    마이페이지에서 명함 설정 버튼을 클릭하여 명함 설정 화면으로 진입하는 테스트
    """
    print("--- 명함 설정 화면 진입 테스트 시작 ---")
    try:
        # 1. '마이페이지' 버튼을 찾아 클릭합니다.
        # locators/My_page.json 파일에서 로케이터 정보를 가져옵니다.
        my_page_locator_info = get_locator("My_page", "my_page_button_view")
        my_page_button_xpath = my_page_locator_info.get('android', '').replace('xpath://', '') # "xpath://" prefix 제거

        if not my_page_button_xpath:
            raise ValueError("마이페이지 버튼의 로케이터를 찾을 수 없습니다.")

        print(f"마이페이지 버튼(XPath: {my_page_button_xpath})을 클릭합니다.")
        my_page_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, my_page_button_xpath)),
            message="'마이페이지' 버튼을 20초 내에 찾지 못했습니다."
        )
        my_page_button.click()
        print("✅ '마이페이지' 버튼 클릭 완료.")
        time.sleep(3)  # 페이지 전환 대기

        # 2. '명함설정' 버튼을 찾아 클릭합니다.
        business_card_button_xpath = '//android.widget.Button[@text="명함설정"]'
        print(f"명함설정 버튼(XPath: {business_card_button_xpath})을 클릭합니다.")
        business_card_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, business_card_button_xpath)),
            message="'명함설정' 버튼을 20초 내에 찾지 못했습니다."
        )
        business_card_button.click()
        print("✅ '명함설정' 버튼 클릭 완료.")
        time.sleep(3)  # 페이지 전환 대기

        # 3. 명함 설정 페이지가 정상적으로 로드되었는지 확인합니다.
        # '안녕하세요'로 시작하는 인사말 텍스트 뷰가 있는지 확인하여 페이지 진입을 검증합니다.
        welcome_text_xpath = '//android.widget.TextView[contains(@text, "안녕하세요")]'
        print(f"명함 설정 페이지의 환영 메시지(XPath: {welcome_text_xpath}) 노출을 확인합니다.")
        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, welcome_text_xpath))
        )
        print("✅ 명함 설정 페이지 진입을 성공적으로 확인했습니다.")

        return True, "명함 설정 화면 진입 성공"

    except (TimeoutException, NoSuchElementException) as e:
        error_message = f"테스트 실패: UI 요소를 시간 내에 찾지 못했습니다. ({e})"
        print(f"❌ {error_message}")
        save_screenshot_on_failure(flow_tester.driver, "enter_business_card_view_fail")
        return False, error_message
    except Exception as e:
        error_message = f"예상치 못한 오류 발생: {e}"
        print(f"🚨 {error_message}")
        save_screenshot_on_failure(flow_tester.driver, "enter_business_card_view_fail")
        return False, error_message

if __name__ == "__main__":
    # 이 스크립트는 테스트 스위트의 일부로 실행되도록 설계되었습니다.
    # BaseAppiumDriver 인스턴스(flow_tester)가 필요하므로 단독으로 실행할 수 없습니다.
    print("이 파일은 '명함 설정' 화면 진입 자동화 테스트 케이스를 포함하고 있습니다.")
    print("테스트 실행기(예: DS_checklist_run.py)를 통해 실행해주세요.")