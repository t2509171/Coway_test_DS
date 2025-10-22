# # PythonProject/Login/test_login.py
#
# from appium import webdriver
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from appium.options.android import UiAutomator2Options
# import unittest
# import time
#
# # 새로 생성된 base_driver 모듈에서 BaseAppiumDriver 클래스를 임포트합니다.
# from Base.base_driver import BaseAppiumDriver
#
# class AppiumLoginviewTest(BaseAppiumDriver):
#
#     def __init__(self):
#         # 부모 클래스(BaseAppiumDriver)의 생성자를 platform 인자와 함께 호출합니다.
#         super().__init__()
#         self._login_ui_elements_ok = False
#         self.element_verification_results = {}
#
# def test_login_main_view(flow_tester):
#
#     print("\n--- 로그인 페이지 진입 및 타이틀 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 로그인 화면 UI 노출 확인
#     print("\n--- 로그인 화면 UI 요소 확인 시작 ---")
#     login_page_title_xpath = '//android.widget.TextView[@text="디지털 세일즈"]'
#     login_page_id_title_xpath = '//android.widget.TextView[@text="아이디"]'
#     login_page_pw_title_xpath = '//android.widget.TextView[@text="비밀번호"]'
#     login_page_pw_change_xpath = '//android.widget.Button[@text="비밀번호 변경"]'
#     login_page_pw_reset_xpath = '//android.widget.Button[@text="비밀번호 초기화"]'
#
#     try:
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_title_xpath)))
#         print("✅ '로그인 화면 타이틀'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_id_title_xpath)))
#         print("✅ '아이디 타이틀'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_pw_title_xpath)))
#         print("✅ '비빌번호 타이틀'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_pw_change_xpath)))
#         print("✅ '비밀번호 변경 버튼'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_pw_reset_xpath)))
#         print("✅ '비밀번호 초기화 버튼'이 성공적으로 노출되었습니다.")
#
#         scenario_passed = True
#         result_message = "로그인 화면 UI 요소 확인 성공."
#
#     except Exception as e:
#         result_message = f"로그인 화면 UI 요소 노출 확인 실패: {e}"
#         return False, result_message
#     finally:
#         print("--- 로그인 화면 UI 요소 노출 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message

# PythonProject/Login/test_login.py

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.options.android import UiAutomator2Options
import unittest
import time

# 새로 생성된 base_driver 모듈에서 BaseAppiumDriver 클래스를 임포트합니다.
from Base.base_driver import BaseAppiumDriver

# Xpath 저장소에서 LoginLocators 임포트
from Xpath.xpath_repository import LoginLocators

class AppiumLoginviewTest(BaseAppiumDriver):

    def __init__(self):
        # 부모 클래스(BaseAppiumDriver)의 생성자를 platform 인자와 함께 호출합니다.
        super().__init__()
        self._login_ui_elements_ok = False
        self.element_verification_results = {}

def test_login_main_view(flow_tester):

    print("\n--- 로그인 페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # 현재 플랫폼에 맞는 로케이터 세트를 선택합니다. (AOS 가정)
    locators = LoginLocators.AOS

    # 로그인 화면 UI 노출 확인
    print("\n--- 로그인 화면 UI 요소 확인 시작 ---")
    # XPath 변수를 locators 객체에서 가져오도록 수정
    login_page_title_xpath = locators.login_page_title_xpath
    login_page_id_title_xpath = locators.login_page_id_title_xpath
    login_page_pw_title_xpath = locators.login_page_pw_title_xpath
    login_page_pw_change_xpath = locators.password_change_button_xpath
    login_page_pw_reset_xpath = locators.password_reset_button_xpath

    try:
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_title_xpath)))
        print("✅ '로그인 화면 타이틀'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_id_title_xpath)))
        print("✅ '아이디 타이틀'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_pw_title_xpath)))
        print("✅ '비빌번호 타이틀'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_pw_change_xpath)))
        print("✅ '비밀번호 변경 버튼'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_page_pw_reset_xpath)))
        print("✅ '비밀번호 초기화 버튼'이 성공적으로 노출되었습니다.")

        scenario_passed = True
        result_message = "로그인 화면 UI 요소 확인 성공."

    except Exception as e:
        result_message = f"로그인 화면 UI 요소 노출 확인 실패: {e}"
        return False, result_message
    finally:
        print("--- 로그인 화면 UI 요소 노출 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message