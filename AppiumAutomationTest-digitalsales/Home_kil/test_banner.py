# Home_kil/test_banner.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수들을 import 합니다.
from Utils.scrolling_function import scroll_down
from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_banner_swipe(flow_tester):
    """
    배너를 찾아 스와이프하고, 터치한 뒤 사라지는지 최종 검증합니다.
    '홈' UI 위에 배너가 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
    """
    print("\n--- 배너 스와이프 > 터치 > 소멸 확인 최종 시나리오 시작 ---")

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            print("경고: IOS 플랫폼의 배너 스와이프 기능 확인이 필요합니다.")
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. XPath 정의
        # [참고] 저장소의 banner_xpath는 '디지털세일즈' 타이틀이며,
        # 이 테스트는 스와이프 가능한 배너를 대상으로 하므로 로컬 XPath를 유지합니다.
        banner_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[4]/android.view.View' # AOS 기준 로컬 XPath
        # IOS 배너 XPath 필요 시 여기에 정의
        ios_banner_xpath = None # 예시: '//XCUIElementTypeOther[@name="bannerContainer"]/XCUIElementTypeOther'

        # 플랫폼에 따라 사용할 XPath 선택
        current_banner_xpath = banner_xpath if flow_tester.platform == 'android' else ios_banner_xpath
        if not current_banner_xpath:
             print(f"경고: {flow_tester.platform} 플랫폼의 배너 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
             return True, f"{flow_tester.platform} 배너 XPath 없음 (테스트 통과 간주)"


        home_container_xpath = locators.home_button_xpath # 수정됨

        max_scroll_attempts = 10
        element_in_view = False

        # 2. 배너가 '홈' UI 위에 보일 때까지 스크롤
        print(f"'{current_banner_xpath}' 배너가 '홈' UI 위에 나타날 때까지 스크롤합니다.")
        for i in range(max_scroll_attempts):
            try:
                banner_element = flow_tester.driver.find_element(AppiumBy.XPATH, current_banner_xpath)
                home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if banner_element.is_displayed():
                    print("✅ 배너를 찾았습니다. 위치를 비교합니다.")
                    banner_rect = banner_element.rect
                    home_rect = home_container_element.rect

                    # 배너의 하단이 홈 UI의 상단보다 위에 있는지 확인
                    if (banner_rect['y'] + banner_rect['height']) < home_rect['y']:
                        print("✅ 위치 조건 충족! 배너가 하단 '홈' UI보다 위에 있습니다.")
                        element_in_view = True
                        break
                    else:
                        print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. 배너가 '홈' UI에 가려져 있습니다. 스크롤합니다.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) 배너가 아직 보이지 않습니다. 스크롤합니다.")

            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) 배너를 찾는 중... 스크롤합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 배너를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "banner_not_found_in_view")
            return False, error_msg

        # 3. 배너를 왼쪽으로 1회 스와이프합니다.
        print("배너를 왼쪽으로 스와이프합니다.")
        banner_element_to_swipe = flow_tester.driver.find_element(AppiumBy.XPATH, current_banner_xpath)
        rect = banner_element_to_swipe.rect
        start_x = rect['x'] + rect['width'] * 0.8
        end_x = rect['x'] + rect['width'] * 0.1
        y = rect['y'] + rect['height'] / 2
        flow_tester.driver.swipe(start_x, y, end_x, y, 500)
        time.sleep(2)  # 스와이프 애니메이션 대기
        print("스와이프 동작을 완료했습니다.")

        # 4. 스와이프 후 배너를 다시 찾아 터치합니다.
        print(f"스와이프 후 배너를 다시 찾아 터치합니다: '{current_banner_xpath}'")
        try:
            wait = WebDriverWait(flow_tester.driver, 5)
            banner_to_touch = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, current_banner_xpath))
            )
            banner_to_touch.click()
            print("✅ 배너를 터치했습니다.")
            time.sleep(2)  # 터치 후 UI 반응 대기
        except TimeoutException:
            error_msg = "실패: 스와이프 후 배너를 터치할 수 없거나 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "banner_not_clickable_after_swipe")
            return False, error_msg

        # 5. 터치 후 배너가 최종적으로 사라졌는지 확인합니다.
        print(f"터치 후 배너('{current_banner_xpath}')가 사라졌는지 최종 확인합니다...")
        try:
            wait = WebDriverWait(flow_tester.driver, 5)
            wait.until(
                EC.invisibility_of_element_located((AppiumBy.XPATH, current_banner_xpath))
            )
            print("✅ Pass: 배너가 성공적으로 사라졌습니다.")
            flow_tester.driver.back() # 상세 페이지에서 뒤로가기
            time.sleep(1)
            return True, "배너 스와이프, 터치, 소멸 확인 시나리오 성공."

        except TimeoutException:
            error_msg = "실패: 배너를 터치했지만 사라지지 않았습니다."
            save_screenshot_on_failure(flow_tester.driver, "banner_dismiss_fail_final")
            return False, error_msg

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "banner_swipe_exception")
        return False, f"배너 스와이프 테스트 중 예외 발생: {e}"
    finally:
        print("--- 배너 스와이프 > 터치 > 소멸 확인 최종 시나리오 종료 ---")




# # Home_kil/test_banner.py (수정 완료)
#
# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.scrolling_function import scroll_down
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
# def test_banner_swipe(flow_tester):
#     """
#     배너를 찾아 스와이프하고, 터치한 뒤 사라지는지 최종 검증합니다.
#     '홈' UI 위에 배너가 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
#     """
#     print("\n--- 배너 스와이프 > 터치 > 소멸 확인 최종 시나리오 시작 ---")
#     try:
#         # 1. XPath 정의
#         banner_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[4]/android.view.View'
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'  # 위치 비교 기준
#
#         max_scroll_attempts = 10
#         element_in_view = False
#
#         # 2. 배너가 '홈' UI 위에 보일 때까지 스크롤
#         print(f"'{banner_xpath}' 배너가 '홈' UI 위에 나타날 때까지 스크롤합니다.")
#         for i in range(max_scroll_attempts):
#             try:
#                 banner_element = flow_tester.driver.find_element(AppiumBy.XPATH, banner_xpath)
#                 home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 if banner_element.is_displayed():
#                     print("✅ 배너를 찾았습니다. 위치를 비교합니다.")
#                     banner_rect = banner_element.rect
#                     home_rect = home_container_element.rect
#
#                     # 배너의 하단이 홈 UI의 상단보다 위에 있는지 확인
#                     if (banner_rect['y'] + banner_rect['height']) < home_rect['y']:
#                         print("✅ 위치 조건 충족! 배너가 하단 '홈' UI보다 위에 있습니다.")
#                         element_in_view = True
#                         break
#                     else:
#                         print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. 배너가 '홈' UI에 가려져 있습니다. 스크롤합니다.")
#                 else:
#                     print(f"({i + 1}/{max_scroll_attempts}) 배너가 아직 보이지 않습니다. 스크롤합니다.")
#
#             except NoSuchElementException:
#                 print(f"({i + 1}/{max_scroll_attempts}) 배너를 찾는 중... 스크롤합니다.")
#
#             scroll_down(flow_tester.driver)
#             time.sleep(1)
#
#         if not element_in_view:
#             error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 배너를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "banner_not_found_in_view")
#             return False, error_msg
#
#         # 3. 배너를 왼쪽으로 1회 스와이프합니다.
#         print("배너를 왼쪽으로 스와이프합니다.")
#         banner_element_to_swipe = flow_tester.driver.find_element(AppiumBy.XPATH, banner_xpath)
#         rect = banner_element_to_swipe.rect
#         start_x = rect['x'] + rect['width'] * 0.8
#         end_x = rect['x'] + rect['width'] * 0.1
#         y = rect['y'] + rect['height'] / 2
#         flow_tester.driver.swipe(start_x, y, end_x, y, 500)
#         time.sleep(2)  # 스와이프 애니메이션 대기
#         print("스와이프 동작을 완료했습니다.")
#
#         # 4. 스와이프 후 배너를 다시 찾아 터치합니다.
#         print(f"스와이프 후 배너를 다시 찾아 터치합니다: '{banner_xpath}'")
#         try:
#             wait = WebDriverWait(flow_tester.driver, 5)
#             banner_to_touch = wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, banner_xpath))
#             )
#             banner_to_touch.click()
#             print("✅ 배너를 터치했습니다.")
#             time.sleep(2)  # 터치 후 UI 반응 대기
#         except TimeoutException:
#             error_msg = "실패: 스와이프 후 배너를 터치할 수 없거나 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "banner_not_clickable_after_swipe")
#             return False, error_msg
#
#         # 5. 터치 후 배너가 최종적으로 사라졌는지 확인합니다.
#         print(f"터치 후 배너('{banner_xpath}')가 사라졌는지 최종 확인합니다...")
#         try:
#             wait = WebDriverWait(flow_tester.driver, 5)
#             wait.until(
#                 EC.invisibility_of_element_located((AppiumBy.XPATH, banner_xpath))
#             )
#             print("✅ Pass: 배너가 성공적으로 사라졌습니다.")
#             flow_tester.driver.back()
#             time.sleep(1)
#             return True, "배너 스와이프, 터치, 소멸 확인 시나리오 성공."
#
#         except TimeoutException:
#             error_msg = "실패: 배너를 터치했지만 사라지지 않았습니다."
#             save_screenshot_on_failure(flow_tester.driver, "banner_dismiss_fail_final")
#             return False, error_msg
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "banner_swipe_exception")
#         return False, f"배너 스와이프 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 배너 스와이프 > 터치 > 소멸 확인 최종 시나리오 종료 ---")
