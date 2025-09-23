# -*- coding: utf-8 -*-

# 라이브러리 임포트
import time
import os
import sys

# ----------------- ▼ 이 부분을 추가하면 개별 실행이 편리해집니다 ▼ -----------------
# 현재 파일의 상위 폴더(My_page_kil)의 그 상위 폴더(프로젝트 루트)를 시스템 경로에 추가합니다.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -----------------------------------------------------------------------------------

# Appium 라이브러리
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 프로젝트 내부 유틸리티
from Utils.screenshot_helper import save_screenshot_on_failure


# --- 함수 1: '마이페이지' 버튼 노출 확인 ---
def test_my_page_button_visibility(flow_tester):
    """
    전체 메뉴를 열고 '마이페이지' 버튼이 노출되는지 확인하는 테스트
    """
    print("\n--- [함수 1] '마이페이지' 버튼 노출 확인 테스트 시작 ---")
    try:
        # 1. 전체 메뉴 버튼을 클릭합니다.
        # 참고: '전체메뉴' 버튼의 XPath는 앱 버전에 따라 변경될 수 있습니다.
        # 아래는 content-desc를 이용한 예시이며, 더 안정적인 식별자입니다.
        full_menu_button_xpath = '//android.widget.Button[@content-desc="전체메뉴"]'
        print(f"전체 메뉴 버튼 클릭 시도 (XPath: {full_menu_button_xpath})")

        full_menu_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, full_menu_button_xpath)),
            message="'전체 메뉴' 버튼을 찾지 못했습니다."
        )
        full_menu_button.click()
        print("✅ '전체 메뉴' 버튼 클릭 완료.")
        time.sleep(2)  # 메뉴 애니메이션 대기

        # 2. '마이페이지' 버튼이 화면에 보이는지 확인합니다.
        my_page_button_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        print(f"'마이페이지' 메뉴 버튼 노출 확인 시도 (XPath: {my_page_button_xpath})")

        WebDriverWait(flow_tester.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, my_page_button_xpath))
        )

        print("✅ Pass: '마이페이지' 메뉴 버튼이 성공적으로 노출되었습니다.")
        return True, "마이페이지 메뉴 버튼 노출 확인 성공"

    except (TimeoutException, NoSuchElementException) as e:
        error_message = f"Fail: '마이페이지' 메뉴 버튼을 찾지 못했습니다. - {e}"
        print(f"❌ {error_message}")
        save_screenshot_on_failure(flow_tester.driver, "my_page_visibility_fail")
        return False, error_message
    except Exception as e:
        error_message = f"예상치 못한 오류 발생: {e}"
        print(f"🚨 {error_message}")
        save_screenshot_on_failure(flow_tester.driver, "my_page_visibility_fail")
        return False, error_message


# --- 함수 2: '마이페이지' 페이지 이동 확인 ---
def test_my_page_navigation(flow_tester):
    """
    '마이페이지' 버튼 클릭 후, 해당 페이지로 정상적으로 이동하는지 확인하는 테스트
    (주의: 이 함수는 test_my_page_button_visibility 함수 실행 직후에 호출되어야 합니다.)
    """
    print("\n--- [함수 2] '마이페이지' 페이지 이동 확인 테스트 시작 ---")
    try:
        # 1. '마이페이지' 메뉴 버튼을 클릭합니다. (이전 함수에서 메뉴가 열린 상태)
        my_page_button_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        print(f"'마이페이지' 메뉴 버튼 클릭 시도 (XPath: {my_page_button_xpath})")

        my_page_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, my_page_button_xpath)),
            message="'마이페이지' 메뉴 버튼을 찾지 못했습니다."
        )
        my_page_button.click()
        print("✅ '마이페이지' 메뉴 버튼 클릭 완료.")
        time.sleep(3)  # 페이지 전환 대기

        # 2. '마이페이지' 페이지로 이동했는지 페이지 타이틀을 통해 확인합니다.
        my_page_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        print(f"'마이페이지' 페이지 타이틀 노출 확인 시도 (XPath: {my_page_title_xpath})")

        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, my_page_title_xpath))
        )

        print("✅ Pass: '마이페이지' 페이지로 성공적으로 이동했습니다.")
        return True, "마이페이지 페이지 이동 성공"

    except (TimeoutException, NoSuchElementException) as e:
        error_message = f"Fail: '마이페이지'로 이동하지 못했거나 페이지 타이틀을 찾을 수 없습니다. - {e}"
        print(f"❌ {error_message}")
        save_screenshot_on_failure(flow_tester.driver, "my_page_navigation_fail")
        return False, error_message
    except Exception as e:
        error_message = f"예상치 못한 오류 발생: {e}"
        print(f"🚨 {error_message}")
        save_screenshot_on_failure(flow_tester.driver, "my_page_navigation_fail")
        return False, error_message


if __name__ == "__main__":
    # 이 스크립트는 테스트 스위트의 일부로 실행되도록 설계되었습니다.
    # BaseAppiumDriver 인스턴스(flow_tester)가 필요하므로 단독으로 실행할 수 없습니다.
    print("이 파일은 '마이페이지' 진입 자동화 테스트 케이스 2개를 포함하고 있습니다.")
    print("메인 테스트 실행 파일(예: DS_checklist_run.py)을 통해 실행해주세요.")