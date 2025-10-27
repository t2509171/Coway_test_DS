# PythonProject/Shared_Content_kil/test_menu_navigation_verification.py

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
from Xpath.xpath_repository import SharedContentKilLocators # 수정: 클래스 임포트

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def verify_menu_navigation(flow_tester, menu_item_xpath, expected_verification_xpath, menu_name):
    """
    Navigates to a specific menu item from the full menu and verifies landing on the correct page.

    Args:
        flow_tester: The test flow execution object.
        menu_item_xpath (str): XPath of the menu item to click in the full menu.
        expected_verification_xpath (str): XPath of an element expected on the target page for verification.
        menu_name (str): Name of the menu being tested (for logging).

    Returns:
        tuple: (bool, str) indicating success/failure and a result message.
    """
    print(f"\n--- 전체 메뉴 > '{menu_name}' 이동 및 확인 테스트 시작 ---")
    scenario_passed = True
    result_message = f"'{menu_name}' 이동 및 확인 성공."

    # 플랫폼 분기 로직 추가 (함수 내에서 한 번만 수행)
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = SharedContentKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = SharedContentKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = SharedContentKilLocators.AOS

    try:
        print("1. 전체 메뉴 버튼 클릭")
        menu_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.menu_button_xpath)) # 공통 로케이터 사용
        )
        menu_button.click()
        print("   전체 메뉴 버튼 클릭 완료.")
        time.sleep(2)

        print(f"2. '{menu_name}' 메뉴 항목 클릭")
        # menu_item_xpath는 인자로 받으므로 locators 객체 불필요
        menu_item = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, menu_item_xpath))
        )
        menu_item.click()
        print(f"   '{menu_name}' 메뉴 항목 클릭 완료.")
        time.sleep(3) # 페이지 로딩 대기

        print(f"3. '{menu_name}' 페이지 확인 (예상 요소: {expected_verification_xpath})")
        # expected_verification_xpath는 인자로 받으므로 locators 객체 불필요
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, expected_verification_xpath))
        )
        print(f"   ✅ '{menu_name}' 페이지 확인 완료.")

        # 홈으로 돌아가기 (다음 테스트를 위해)
        print("4. 홈 버튼 클릭하여 홈으로 복귀")
        home_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.home_button_xpath)) # 공통 로케이터 사용
        )
        home_button.click()
        print("   홈 버튼 클릭 완료.")
        time.sleep(3) # 홈 화면 로딩 대기


    except TimeoutException as e:
        scenario_passed = False
        result_message = f"'{menu_name}' 테스트 실패 (타임아웃): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot(f"failure_menu_nav_{menu_name}_timeout.png")
        # 실패 시 홈으로 복귀 시도
        try:
            # 홈 버튼 XPath를 locators에서 가져오도록 수정
            home_button_on_fail = flow_tester.driver.find_element(AppiumBy.XPATH, locators.home_button_xpath)
            home_button_on_fail.click()
            time.sleep(3)
        except Exception:
             print("홈 복귀 실패 (무시)")
    except NoSuchElementException as e:
        scenario_passed = False
        result_message = f"'{menu_name}' 테스트 실패 (요소 찾기 실패): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot(f"failure_menu_nav_{menu_name}_no_such_element.png")
        # 실패 시 홈으로 복귀 시도
        try:
            # 홈 버튼 XPath를 locators에서 가져오도록 수정
            home_button_on_fail = flow_tester.driver.find_element(AppiumBy.XPATH, locators.home_button_xpath)
            home_button_on_fail.click()
            time.sleep(3)
        except Exception:
             print("홈 복귀 실패 (무시)")
    except Exception as e:
        scenario_passed = False
        result_message = f"'{menu_name}' 테스트 중 예상치 못한 오류 발생: {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot(f"failure_menu_nav_{menu_name}_unexpected.png")
        # 실패 시 홈으로 복귀 시도
        try:
            # 홈 버튼 XPath를 locators에서 가져오도록 수정
            home_button_on_fail = flow_tester.driver.find_element(AppiumBy.XPATH, locators.home_button_xpath)
            home_button_on_fail.click()
            time.sleep(3)
        except Exception:
             print("홈 복귀 실패 (무시)")

    finally:
        print(f"--- 전체 메뉴 > '{menu_name}' 이동 및 확인 테스트 종료 ---")

    return scenario_passed, result_message

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
# 개별 메뉴 테스트 함수 정의
def test_navigate_to_ecatalog(flow_tester):
    # 플랫폼 분기 로직 추가 (테스트 함수 내에서 한 번만 수행)
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = SharedContentKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = SharedContentKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = SharedContentKilLocators.AOS

    return verify_menu_navigation(
        flow_tester,
        locators.ecatalog_item_xpath, # 공통 로케이터 사용
        locators.library_text_xpath, # 공통 로케이터 사용
        "e카탈로그"
    )

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def test_navigate_to_manuals(flow_tester):
    # 플랫폼 분기 로직 추가 (테스트 함수 내에서 한 번만 수행)
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = SharedContentKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = SharedContentKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = SharedContentKilLocators.AOS

    return verify_menu_navigation(
        flow_tester,
        locators.manual_item_xpath, # 공통 로케이터 사용
        locators.library_text_xpath, # 공통 로케이터 사용
        "제품 사용설명서"
    )