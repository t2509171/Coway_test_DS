import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

# Xpath 저장소에서 ManagedCustomersKilLocators 임포트
from Xpath.xpath_repository import ManagedCustomersKilLocators


def test_find_customized_sharing_menu(flow_tester):
    """
    전체 메뉴 진입 후, '관리고객 맞춤 공유하기' 메뉴를 스크롤하여 노출되는지 검증합니다.
    """
    print("\n--- 전체 메뉴 > '관리고객 맞춤 공유하기' 메뉴 노출 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = ManagedCustomersKilLocators.AOS

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
            save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_for_managed_customers")
            return False, error_msg

        # 2. 스크롤하며 '관리고객 맞춤 공유하기' 텍스트 찾기
        target_text_xpath = locators.target_text_xpath  # 수정됨
        max_scrolls = 6
        element_found = False

        print(f"'{target_text_xpath}' 텍스트를 찾기 위해 최대 {max_scrolls}번 스크롤을 시작합니다.")
        for i in range(max_scrolls):
            try:
                # 현재 화면에서 텍스트를 찾음
                flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
                print(f"✅ '관리고객 맞춤 공유하기' 텍스트를 찾았습니다. (시도: {i + 1}번)")
                element_found = True
                break  # 찾았으면 루프 종료
            except NoSuchElementException:
                # 못 찾았으면 스크롤
                print(f"({i + 1}/{max_scrolls}) 텍스트를 찾지 못했습니다. 아래로 스크롤합니다.")
                scroll_down(flow_tester.driver)
                time.sleep(1)

        # 3. 최종 결과 판정
        if element_found:
            return True, "'관리고객 맞춤 공유하기' 메뉴 노출 확인 성공."
        else:
            error_msg = f"실패: {max_scrolls}번 스크롤 후에도 '관리고객 맞춤 공유하기' 텍스트를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "customized_sharing_menu_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"'관리고객 맞춤 공유하기' 확인 중 예외 발생: {e}"
    finally:
        print("--- 전체 메뉴 > '관리고객 맞춤 공유하기' 메뉴 노출 확인 시나리오 종료 ---")


def test_navigate_to_customized_sharing_view(flow_tester):
    """
    '관리고객 맞춤 공유하기' 메뉴를 클릭하여 해당 화면으로 이동하고, 화면 타이틀을 검증합니다.
    """
    print("\n--- '관리고객 맞춤 공유하기' 화면 이동 및 타이틀 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = ManagedCustomersKilLocators.AOS

    try:
        # ※ 사전 조건: 이전 테스트가 성공하여 '관리고객 맞춤 공유하기' 메뉴가 화면에 보이는 상태

        # 1. '관리고객 맞춤 공유하기' 메뉴 클릭
        menu_item_xpath = locators.menu_item_xpath  # 수정됨
        print(f"'{menu_item_xpath}' 메뉴를 클릭합니다.")
        try:
            menu_item = flow_tester.driver.find_element(AppiumBy.XPATH, menu_item_xpath)
            menu_item.click()
        except Exception as e:
            error_msg = f"실패: '관리고객 맞춤 공유하기' 메뉴 클릭 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "customized_sharing_menu_click_failed")
            return False, error_msg

        # 2. 화면 전환 후 '관리고객 맞춤 공유하기' 타이틀 노출 확인
        # 화면 전환 후 타이틀의 XPath가 메뉴와 동일하다고 가정합니다.
        title_xpath = locators.title_xpath  # 수정됨
        print(f"'{title_xpath}' (화면 타이틀)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, title_xpath))
            )
            print("✅ '관리고객 맞춤 공유하기' 화면으로 성공적으로 이동했으며, 타이틀이 확인되었습니다.")
            return True, "'관리고객 맞춤 공유하기' 화면 이동 확인 성공."
        except TimeoutException:
            error_msg = "실패: 화면 이동 후 '관리고객 맞춤 공유하기' 타이틀을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "customized_sharing_title_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"'관리고객 맞춤 공유하기' 화면 이동 중 예외 발생: {e}"
    finally:
        print("--- '관리고객 맞춤 공유하기' 화면 이동 및 타이틀 확인 시나리오 종료 ---")


# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
# from Utils.scrolling_function import scroll_down
#
#
# def test_find_customized_sharing_menu(flow_tester):
#     """
#     전체 메뉴 진입 후, '관리고객 맞춤 공유하기' 메뉴를 스크롤하여 노출되는지 검증합니다.
#     """
#     print("\n--- 전체 메뉴 > '관리고객 맞춤 공유하기' 메뉴 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. '전체메뉴' 버튼 클릭
#         menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#         print(f"'{menu_button_xpath}' (전체메뉴) 버튼을 클릭합니다.")
#         try:
#             menu_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
#             )
#             menu_button.click()
#             time.sleep(2)  # 메뉴 애니메이션 대기
#         except TimeoutException:
#             error_msg = "실패: '전체메뉴' 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_for_managed_customers")
#             return False, error_msg
#
#         # 2. 스크롤하며 '관리고객 맞춤 공유하기' 텍스트 찾기
#         target_text_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
#         max_scrolls = 6
#         element_found = False
#
#         print(f"'{target_text_xpath}' 텍스트를 찾기 위해 최대 {max_scrolls}번 스크롤을 시작합니다.")
#         for i in range(max_scrolls):
#             try:
#                 # 현재 화면에서 텍스트를 찾음
#                 flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
#                 print(f"✅ '관리고객 맞춤 공유하기' 텍스트를 찾았습니다. (시도: {i + 1}번)")
#                 element_found = True
#                 break  # 찾았으면 루프 종료
#             except NoSuchElementException:
#                 # 못 찾았으면 스크롤
#                 print(f"({i + 1}/{max_scrolls}) 텍스트를 찾지 못했습니다. 아래로 스크롤합니다.")
#                 scroll_down(flow_tester.driver)
#                 time.sleep(1)
#
#         # 3. 최종 결과 판정
#         if element_found:
#             return True, "'관리고객 맞춤 공유하기' 메뉴 노출 확인 성공."
#         else:
#             error_msg = f"실패: {max_scrolls}번 스크롤 후에도 '관리고객 맞춤 공유하기' 텍스트를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "customized_sharing_menu_not_found")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"'관리고객 맞춤 공유하기' 확인 중 예외 발생: {e}"
#     finally:
#         print("--- 전체 메뉴 > '관리고객 맞춤 공유하기' 메뉴 노출 확인 시나리오 종료 ---")
#
#
# def test_navigate_to_customized_sharing_view(flow_tester):
#     """
#     '관리고객 맞춤 공유하기' 메뉴를 클릭하여 해당 화면으로 이동하고, 화면 타이틀을 검증합니다.
#     """
#     print("\n--- '관리고객 맞춤 공유하기' 화면 이동 및 타이틀 확인 시나리오 시작 ---")
#     try:
#         # ※ 사전 조건: 이전 테스트가 성공하여 '관리고객 맞춤 공유하기' 메뉴가 화면에 보이는 상태
#
#         # 1. '관리고객 맞춤 공유하기' 메뉴 클릭
#         menu_item_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
#         print(f"'{menu_item_xpath}' 메뉴를 클릭합니다.")
#         try:
#             menu_item = flow_tester.driver.find_element(AppiumBy.XPATH, menu_item_xpath)
#             menu_item.click()
#         except Exception as e:
#             error_msg = f"실패: '관리고객 맞춤 공유하기' 메뉴 클릭 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "customized_sharing_menu_click_failed")
#             return False, error_msg
#
#         # 2. 화면 전환 후 '관리고객 맞춤 공유하기' 타이틀 노출 확인
#         # 화면 전환 후 타이틀의 XPath가 메뉴와 동일하다고 가정합니다.
#         title_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
#         print(f"'{title_xpath}' (화면 타이틀)이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, title_xpath))
#             )
#             print("✅ '관리고객 맞춤 공유하기' 화면으로 성공적으로 이동했으며, 타이틀이 확인되었습니다.")
#             return True, "'관리고객 맞춤 공유하기' 화면 이동 확인 성공."
#         except TimeoutException:
#             error_msg = "실패: 화면 이동 후 '관리고객 맞춤 공유하기' 타이틀을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "customized_sharing_title_not_found")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"'관리고객 맞춤 공유하기' 화면 이동 중 예외 발생: {e}"
#     finally:
#         print("--- '관리고객 맞춤 공유하기' 화면 이동 및 타이틀 확인 시나리오 종료 ---")
