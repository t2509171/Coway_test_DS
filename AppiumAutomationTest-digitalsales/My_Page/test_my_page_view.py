import re
import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
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

# 마이페이지 버튼 노출 확인 (49)
def test_my_page_button_view(flow_tester):
    # 마이페이지 버튼 노출 확인
    print("마이페이지 버튼 노출을 확인합니다.")
    my_page_button_view_xpath = '//android.widget.TextView[@text="마이페이지"]'
    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, my_page_button_view_xpath)),
            message=f"'{my_page_button_view_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
        )
        print("✅ 마이페이지 버튼이 성공적으로 노출되었습니다.")
        scenario_passed = True
        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "마이페이지 버튼 노출 성공"
    except Exception as e:
        result_message = f"마이페이지 버튼 노출 확인 실패: {e}"
        time.sleep(2)
        scenario_passed = False
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message

# 마이페이지 버튼 클릭 확인 (50)
def test_my_page_button_click(flow_tester):
    # 마이페이지 버튼 노출 확인
    print("마이페이지 버튼을 찾고 클릭합니다.")
    my_page_button_xpath = '//android.view.View[@content-desc="마이페이지"]'
    try:
        my_page_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, my_page_button_xpath)),
            message=f"'{my_page_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        my_page_button.click()
        print("마이페이지 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기

        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "마이페이지 버튼 클릭 성공"

    except Exception as e:
        result_message = f"마이페이지 버튼 클릭 중 오류 발생: {e}"
        time.sleep(3)
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message




if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")
