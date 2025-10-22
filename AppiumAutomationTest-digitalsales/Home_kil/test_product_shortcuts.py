import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_verify_product_shortcuts_exist(flow_tester):
    """
    홈 화면에서 '제품 바로가기' 섹션과 '정수기' 아이콘이 '홈' UI 위에 보일 때까지 스크롤하여 확인합니다.
    """
    print("\n--- 홈 > 제품 바로가기 > '정수기' 아이콘 동시 노출 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = HomeKilLocators.AOS

    try:
        # 1. XPath 정의
        target_text_xpath = locators.target_text_xpath  # 수정됨
        water_purifier_xpath = locators.water_purifier_xpath  # 수정됨
        home_container_xpath = locators.home_container_xpath  # 수정됨

        max_scroll_attempts = 10
        element_in_view = False

        # 2. '제품 바로가기'와 '정수기'가 '홈' UI 위에 보일 때까지 스크롤
        print(f"'{target_text_xpath}'와 '{water_purifier_xpath}'가 '홈' UI 위에 나타날 때까지 스크롤합니다.")
        for i in range(max_scroll_attempts):
            try:
                # 세 개의 요소를 모두 찾습니다. 하나라도 없으면 except로 빠져 스크롤합니다.
                target_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
                icon_element = flow_tester.driver.find_element(AppiumBy.XPATH, water_purifier_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                # '제품 바로가기'와 '정수기' 아이콘이 모두 화면에 보이는지 확인
                if target_element.is_displayed() and icon_element.is_displayed():
                    print("✅ '제품 바로가기'와 '정수기' 아이콘을 찾았습니다. 위치를 비교합니다.")
                    target_rect = target_element.rect
                    icon_rect = icon_element.rect
                    home_rect = home_element.rect

                    # 조건 수정: '제품 바로가기'의 하단과 '정수기' 아이콘의 하단이 모두 홈 UI의 상단보다 위에 있는지 확인
                    if (target_rect['y'] + target_rect['height']) < home_rect['y'] and \
                            (icon_rect['y'] + icon_rect['height']) < home_rect['y']:
                        print("✅ 위치 조건 충족! 모든 요소가 하단 '홈' UI보다 위에 있습니다.")
                        element_in_view = True
                        break  # 조건을 만족했으므로 스크롤 루프 종료
                    else:
                        print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. 요소가 '홈' UI에 가려져 있습니다. 스크롤합니다.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) 두 요소 중 하나 이상이 아직 보이지 않습니다. 스크롤합니다.")

            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾는 중... 스크롤합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 '제품 바로가기'와 '정수기'를 모두 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "product_shortcut_and_icon_not_in_view")
            return False, error_msg

        # 3. 모든 검증이 스크롤 루프 안에서 완료되었으므로, 별도 확인 없이 성공 처리
        return True, "제품 바로가기 섹션 및 정수기 아이콘 동시 노출 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "verify_product_shortcut_failure")
        return False, f"제품 바로가기 존재 확인 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 제품 바로가기 > '정수기' 아이콘 동시 노출 확인 시나리오 종료 ---")



# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
# from Utils.scrolling_function import scroll_down
#
# def test_verify_product_shortcuts_exist(flow_tester):
#     """
#     홈 화면에서 '제품 바로가기' 섹션과 '정수기' 아이콘이 '홈' UI 위에 보일 때까지 스크롤하여 확인합니다.
#     """
#     print("\n--- 홈 > 제품 바로가기 > '정수기' 아이콘 동시 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. XPath 정의
#         target_text_xpath = '//android.widget.TextView[@text="제품 바로가기"]'
#         water_purifier_xpath = '//android.view.View[@content-desc="정수기"]'
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'
#
#         max_scroll_attempts = 10
#         element_in_view = False
#
#         # 2. '제품 바로가기'와 '정수기'가 '홈' UI 위에 보일 때까지 스크롤
#         print(f"'{target_text_xpath}'와 '{water_purifier_xpath}'가 '홈' UI 위에 나타날 때까지 스크롤합니다.")
#         for i in range(max_scroll_attempts):
#             try:
#                 # 세 개의 요소를 모두 찾습니다. 하나라도 없으면 except로 빠져 스크롤합니다.
#                 target_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
#                 icon_element = flow_tester.driver.find_element(AppiumBy.XPATH, water_purifier_xpath)
#                 home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 # '제품 바로가기'와 '정수기' 아이콘이 모두 화면에 보이는지 확인
#                 if target_element.is_displayed() and icon_element.is_displayed():
#                     print("✅ '제품 바로가기'와 '정수기' 아이콘을 찾았습니다. 위치를 비교합니다.")
#                     target_rect = target_element.rect
#                     icon_rect = icon_element.rect
#                     home_rect = home_element.rect
#
#                     # 조건 수정: '제품 바로가기'의 하단과 '정수기' 아이콘의 하단이 모두 홈 UI의 상단보다 위에 있는지 확인
#                     if (target_rect['y'] + target_rect['height']) < home_rect['y'] and \
#                        (icon_rect['y'] + icon_rect['height']) < home_rect['y']:
#                         print("✅ 위치 조건 충족! 모든 요소가 하단 '홈' UI보다 위에 있습니다.")
#                         element_in_view = True
#                         break # 조건을 만족했으므로 스크롤 루프 종료
#                     else:
#                         print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. 요소가 '홈' UI에 가려져 있습니다. 스크롤합니다.")
#                 else:
#                     print(f"({i + 1}/{max_scroll_attempts}) 두 요소 중 하나 이상이 아직 보이지 않습니다. 스크롤합니다.")
#
#             except NoSuchElementException:
#                 print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾는 중... 스크롤합니다.")
#
#             scroll_down(flow_tester.driver)
#             time.sleep(1)
#
#         if not element_in_view:
#             error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 '제품 바로가기'와 '정수기'를 모두 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "product_shortcut_and_icon_not_in_view")
#             return False, error_msg
#
#         # 3. 모든 검증이 스크롤 루프 안에서 완료되었으므로, 별도 확인 없이 성공 처리
#         return True, "제품 바로가기 섹션 및 정수기 아이콘 동시 노출 확인 성공."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "verify_product_shortcut_failure")
#         return False, f"제품 바로가기 존재 확인 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 > 제품 바로가기 > '정수기' 아이콘 동시 노출 확인 시나리오 종료 ---")