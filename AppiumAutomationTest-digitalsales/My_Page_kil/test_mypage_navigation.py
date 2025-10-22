# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
#
# def test_verify_mypage_icon_in_menu(flow_tester):
#     """
#     전체 메뉴를 열고 '마이페이지' 아이콘이 노출되는지 검증합니다.
#     """
#     print("\n--- 전체 메뉴 > '마이페이지' 아이콘 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. '전체메뉴' 버튼 클릭
#         menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#         print(f"'{menu_button_xpath}' (전체메뉴) 버튼을 클릭합니다.")
#         try:
#             menu_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
#             )
#             menu_button.click()
#             time.sleep(2) # 메뉴 애니메이션 대기
#         except TimeoutException:
#             error_msg = "실패: '전체메뉴' 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "menu_button_for_mypage_not_found")
#             return False, error_msg
#
#         # 2. '마이페이지' 아이콘 노출 확인
#         mypage_icon_xpath = '(//android.view.View[@content-desc="마이페이지"])[1]'
#         print(f"'{mypage_icon_xpath}' (마이페이지 아이콘)이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, mypage_icon_xpath))
#             )
#             print("✅ '마이페이지' 아이콘이 성공적으로 노출되었습니다.")
#         except TimeoutException:
#             error_msg = "실패: 전체 메뉴에서 '마이페이지' 아이콘을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "mypage_icon_not_found")
#             return False, error_msg
#
#         return True, "'마이페이지' 아이콘 노출 확인 성공."
#
#     except Exception as e:
#         return False, f"'마이페이지' 아이콘 확인 중 예외 발생: {e}"
#     finally:
#         print("--- 전체 메뉴 > '마이페이지' 아이콘 노출 확인 시나리오 종료 ---")
#
#
# def test_navigate_to_mypage(flow_tester):
#     """
#     '마이페이지' 아이콘을 클릭하여 '마이페이지' 화면으로 이동하고 타이틀을 검증합니다.
#     """
#     print("\n--- '마이페이지' 화면 이동 및 타이틀 확인 시나리오 시작 ---")
#     try:
#         # ※ 사전 조건: 이전 테스트('test_verify_mypage_icon_in_menu')가 성공하여 전체 메뉴가 열려있는 상태
#
#         # 1. '마이페이지' 아이콘 클릭
#         mypage_icon_xpath = '(//android.view.View[@content-desc="마이페이지"])[1]'
#         print(f"'{mypage_icon_xpath}' (마이페이지 아이콘)을 클릭합니다.")
#         try:
#             mypage_icon = flow_tester.driver.find_element(AppiumBy.XPATH, mypage_icon_xpath)
#             mypage_icon.click()
#         except Exception as e:
#             error_msg = f"실패: '마이페이지' 아이콘 클릭 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "mypage_icon_click_failed")
#             return False, error_msg
#
#         # 2. '마이페이지' 화면 타이틀 노출 확인
#         mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
#         print(f"'{mypage_title_xpath}' (마이페이지 타이틀)이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath))
#             )
#             print("✅ '마이페이지' 화면으로 성공적으로 이동했으며, 타이틀이 확인되었습니다.")
#         except TimeoutException:
#             error_msg = "실패: '마이페이지' 화면으로 이동하지 못했거나 타이틀을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "mypage_title_not_found")
#             return False, error_msg
#
#         return True, "'마이페이지' 화면 이동 및 타이틀 확인 성공."
#
#     except Exception as e:
#         return False, f"'마이페이지' 화면 이동 중 예외 발생: {e}"
#     finally:
#         print("--- '마이페이지' 화면 이동 및 타이틀 확인 시나리오 종료 ---")

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 MyPageKilLocators 임포트
from Xpath.xpath_repository import MyPageKilLocators


def test_verify_mypage_icon_in_menu(flow_tester):
    """
    전체 메뉴를 열고 '마이페이지' 아이콘이 노출되는지 검증합니다.
    """
    print("\n--- 전체 메뉴 > '마이페이지' 아이콘 노출 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = MyPageKilLocators.AOS

    try:
        # 1. '전체메뉴' 버튼 클릭
        menu_button_xpath = locators.menu_button_xpath  # 수정됨
        print(f"'{menu_button_xpath}' (전체메뉴) 버튼을 클릭합니다.")
        try:
            menu_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
            )
            menu_button.click()
            time.sleep(2)  # 메뉴 애니메이션 대기
        except TimeoutException:
            error_msg = "실패: '전체메뉴' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "menu_button_for_mypage_not_found")
            return False, error_msg

        # 2. '마이페이지' 아이콘 노출 확인
        mypage_icon_xpath = locators.mypage_icon_xpath  # 수정됨
        print(f"'{mypage_icon_xpath}' (마이페이지 아이콘)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_icon_xpath))
            )
            print("✅ '마이페이지' 아이콘이 성공적으로 노출되었습니다.")
        except TimeoutException:
            error_msg = "실패: 전체 메뉴에서 '마이페이지' 아이콘을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "mypage_icon_not_found")
            return False, error_msg

        return True, "'마이페이지' 아이콘 노출 확인 성공."

    except Exception as e:
        return False, f"'마이페이지' 아이콘 확인 중 예외 발생: {e}"
    finally:
        print("--- 전체 메뉴 > '마이페이지' 아이콘 노출 확인 시나리오 종료 ---")


def test_navigate_to_mypage(flow_tester):
    """
    '마이페이지' 아이콘을 클릭하여 '마이페이지' 화면으로 이동하고 타이틀을 검증합니다.
    """
    print("\n--- '마이페이지' 화면 이동 및 타이틀 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = MyPageKilLocators.AOS

    try:
        # ※ 사전 조건: 이전 테스트('test_verify_mypage_icon_in_menu')가 성공하여 전체 메뉴가 열려있는 상태

        # 1. '마이페이지' 아이콘 클릭
        mypage_icon_xpath = locators.mypage_icon_xpath  # 수정됨
        print(f"'{mypage_icon_xpath}' (마이페이지 아이콘)을 클릭합니다.")
        try:
            mypage_icon = flow_tester.driver.find_element(AppiumBy.XPATH, mypage_icon_xpath)
            mypage_icon.click()
        except Exception as e:
            error_msg = f"실패: '마이페이지' 아이콘 클릭 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "mypage_icon_click_failed")
            return False, error_msg

        # 2. '마이페이지' 화면 타이틀 노출 확인
        mypage_title_xpath = locators.mypage_title_xpath  # 수정됨
        print(f"'{mypage_title_xpath}' (마이페이지 타이틀)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath))
            )
            print("✅ '마이페이지' 화면으로 성공적으로 이동했으며, 타이틀이 확인되었습니다.")
        except TimeoutException:
            error_msg = "실패: '마이페이지' 화면으로 이동하지 못했거나 타이틀을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "mypage_title_not_found")
            return False, error_msg

        return True, "'마이페이지' 화면 이동 및 타이틀 확인 성공."

    except Exception as e:
        return False, f"'마이페이지' 화면 이동 중 예외 발생: {e}"
    finally:
        print("--- '마이페이지' 화면 이동 및 타이틀 확인 시나리오 종료 ---")