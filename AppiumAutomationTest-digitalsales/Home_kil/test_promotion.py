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

"""
미사용중인 test_recommended_promotion 함수는 그대로 유지
"""

def test_scroll_and_navigate_to_salesperson_promotion(flow_tester):
    """
    '판매인 프로모션' 메뉴를 스크롤하여 찾고, 클릭 후 화면 이동을 검증합니다.
    """
    print("\n--- '판매인 프로모션' 스크롤, 클릭, 화면 이동 확인 시나리오 시작 ---")

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. 스크롤하며 '판매인 프로모션' 메뉴 찾기
        target_menu_xpath = locators.target_menu_xpath
        max_scrolls = 10
        menu_element = None

        print(f"'{target_menu_xpath}' 메뉴를 찾기 위해 최대 {max_scrolls}번 스크롤합니다.")
        for i in range(max_scrolls):
            try:
                # 현재 화면에서 메뉴 요소를 찾습니다.
                menu_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_menu_xpath)
                # is_displayed()로 실제로 보이는지 확인 후 루프 종료
                if menu_element.is_displayed():
                    print(f"✅ '판매인 프로모션' 메뉴를 찾았습니다. (시도: {i + 1}번)")
                    break
                else:
                    raise NoSuchElementException  # 보이지 않으면 예외를 발생시켜 스크롤하도록 함
            except NoSuchElementException:
                # 마지막 시도 전까지만 스크롤
                if i < max_scrolls - 1:
                    print(f"({i + 1}/{max_scrolls}) 메뉴를 찾지 못했습니다. 아래로 스크롤합니다.")
                    scroll_down(flow_tester.driver)
                    time.sleep(1)
                else:
                    # 마지막 시도에도 못 찾으면 루프 종료
                    menu_element = None
                    break

        # 루프 종료 후에도 요소를 찾지 못했다면 테스트 실패
        if menu_element is None:
            error_msg = f"실패: {max_scrolls}번 스크롤 후에도 '판매인 프로모션' 메뉴를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "salesperson_promotion_menu_not_found")
            return False, error_msg

        # 2. 찾은 '판매인 프로모션' 메뉴 클릭
        print("'판매인 프로모션' 메뉴를 클릭합니다.")
        try:
            # 안정적인 클릭을 위해 WebDriverWait 사용
            clickable_menu = WebDriverWait(flow_tester.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, target_menu_xpath))
            )
            clickable_menu.click()
        except TimeoutException:
            error_msg = "'판매인 프로모션' 메뉴를 찾았지만 클릭할 수 없는 상태입니다."
            save_screenshot_on_failure(flow_tester.driver, "salesperson_promotion_menu_not_clickable")
            return False, error_msg

        # 3. '프로모션' 화면 타이틀 노출 확인
        final_title_xpath = locators.promotion_title_xpath # 수정됨 (final_title_xpath -> promotion_title_xpath)
        print(f"'{final_title_xpath}' 타이틀이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, final_title_xpath))
            )
            print("✅ '프로모션' 화면으로 성공적으로 이동했습니다.")
            flow_tester.driver.back() # 프로모션 화면 -> 홈
            time.sleep(2)
            return True, "'판매인 프로모션' 메뉴 이동 및 확인 성공."
        except TimeoutException:
            error_msg = "실패: '판매인 프로모션' 메뉴 클릭 후 '프로모션' 타이틀을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "promotion_title_not_found")
            return False, error_msg

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "salesperson_promotion_test_exception") # 스크린샷 파일명 수정
        return False, f"판매인 프로모션 테스트 중 예외 발생: {e}"
    finally:
        print("--- '판매인 프로모션' 스크롤, 클릭, 화면 이동 확인 시나리오 종료 ---")



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
#
# """
# 미사용중
# def test_recommended_promotion(flow_tester):
#
#     # 홈 화면의 '공유할 프로모션을 추천 드려요' 섹션을 테스트합니다.
#     # 1. 섹션이 하단 '홈' UI보다 위에 보일 때까지 스크롤합니다.
#     # 2. '1'번 프로모션을 클릭합니다.
#     # 3. '고객 프로모션' 페이지로 이동했는지 확인합니다.
#
#     print("\n--- 홈 > 추천 프로모션 확인 시나리오 시작 ---")
#     try:
#         # 1. XPath 정의
#         title_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]'
#         target_click_xpath = '//android.widget.TextView[@text="1"]'
#         final_check_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'  # 위치 비교 기준
#
#         max_scroll_attempts = 10
#         section_found_and_clickable = False
#
#         # 2. 지정된 횟수만큼 스크롤하며 요소의 위치를 확인하는 루프
#         for i in range(max_scroll_attempts):
#             try:
#                 title_element = flow_tester.driver.find_element(AppiumBy.XPATH, title_xpath)
#                 home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 if title_element.is_displayed():
#                     print("✅ '프로모션 추천' 섹션을 찾았습니다. 위치를 비교합니다.")
#                     title_rect = title_element.rect
#                     home_rect = home_container_element.rect
#
#                     title_bottom_y = title_rect['y'] + title_rect['height']
#                     home_top_y = home_rect['y']
#
#                     if title_bottom_y < home_top_y:
#                         print("✅ 위치 조건 충족! 대상이 하단 '홈' UI보다 위에 있습니다.")
#                         section_found_and_clickable = True
#                         break
#                     else:
#                         print("⚠️ 위치 조건 불충족. 대상이 '홈' UI에 가려져 있습니다. 스크롤합니다.")
#             except NoSuchElementException:
#                 print(f"({i + 1}/{max_scroll_attempts}) '프로모션 추천' 섹션을 찾는 중... 스크롤합니다.")
#
#             scroll_down(flow_tester.driver)
#
#         # 3. 루프 종료 후, 섹션을 찾았는지 확인
#         if not section_found_and_clickable:
#             error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 섹션을 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "promotion_section_not_found")
#             return False, error_msg
#
#         # 4. '1'번 프로모션을 클릭
#         print(f"'{target_click_xpath}' 요소를 클릭합니다.")
#         try:
#             wait = WebDriverWait(flow_tester.driver, 5)
#             target_to_click = wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, target_click_xpath))
#             )
#             target_to_click.click()
#             time.sleep(3)
#         except TimeoutException:
#             error_msg = f"실패: '{target_click_xpath}' 요소를 클릭할 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "promotion_item_click_failed")
#             return False, error_msg
#
#         # 5. 최종 페이지 확인
#         print(f"최종 페이지에서 '{final_check_xpath}' 텍스트를 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, final_check_xpath))
#             )
#             print("✅ Pass: '고객 프로모션' 페이지로 성공적으로 이동했습니다.")
#             return True, "추천 프로모션 확인 시나리오 성공."
#         except TimeoutException:
#             error_msg = f"실패: '{final_check_xpath}' 텍스트를 찾지 못해 페이지 이동을 확인할 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "promotion_page_verification_failed")
#             return False, error_msg
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "promotion_test_exception")
#         return False, f"추천 프로모션 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 > 추천 프로모션 확인 시나리오 종료 ---")
# """
#
# def test_scroll_and_navigate_to_salesperson_promotion(flow_tester):
#     """
#     '판매인 프로모션' 메뉴를 스크롤하여 찾고, 클릭 후 화면 이동을 검증합니다.
#     """
#     print("\n--- '판매인 프로모션' 스크롤, 클릭, 화면 이동 확인 시나리오 시작 ---")
#     try:
#         # 1. 스크롤하며 '판매인 프로모션' 메뉴 찾기
#         target_menu_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'
#         max_scrolls = 10
#         menu_element = None
#
#         print(f"'{target_menu_xpath}' 메뉴를 찾기 위해 최대 {max_scrolls}번 스크롤합니다.")
#         for i in range(max_scrolls):
#             try:
#                 # 현재 화면에서 메뉴 요소를 찾습니다.
#                 menu_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_menu_xpath)
#                 # is_displayed()로 실제로 보이는지 확인 후 루프 종료
#                 if menu_element.is_displayed():
#                     print(f"✅ '판매인 프로모션' 메뉴를 찾았습니다. (시도: {i + 1}번)")
#                     break
#                 else:
#                     raise NoSuchElementException  # 보이지 않으면 예외를 발생시켜 스크롤하도록 함
#             except NoSuchElementException:
#                 # 마지막 시도 전까지만 스크롤
#                 if i < max_scrolls - 1:
#                     print(f"({i + 1}/{max_scrolls}) 메뉴를 찾지 못했습니다. 아래로 스크롤합니다.")
#                     scroll_down(flow_tester.driver)
#                     time.sleep(1)
#                 else:
#                     # 마지막 시도에도 못 찾으면 루프 종료
#                     menu_element = None
#                     break
#
#         # 루프 종료 후에도 요소를 찾지 못했다면 테스트 실패
#         if menu_element is None:
#             error_msg = f"실패: {max_scrolls}번 스크롤 후에도 '판매인 프로모션' 메뉴를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "salesperson_promotion_menu_not_found")
#             return False, error_msg
#
#         # 2. 찾은 '판매인 프로모션' 메뉴 클릭
#         print("'판매인 프로모션' 메뉴를 클릭합니다.")
#         try:
#             # 안정적인 클릭을 위해 WebDriverWait 사용
#             clickable_menu = WebDriverWait(flow_tester.driver, 5).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, target_menu_xpath))
#             )
#             clickable_menu.click()
#         except TimeoutException:
#             error_msg = "'판매인 프로모션' 메뉴를 찾았지만 클릭할 수 없는 상태입니다."
#             save_screenshot_on_failure(flow_tester.driver, "salesperson_promotion_menu_not_clickable")
#             return False, error_msg
#
#         # 3. '프로모션' 화면 타이틀 노출 확인
#         final_title_xpath = '//android.widget.TextView[@text="프로모션"]'
#         print(f"'{final_title_xpath}' 타이틀이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, final_title_xpath))
#             )
#             print("✅ '프로모션' 화면으로 성공적으로 이동했습니다.")
#             flow_tester.driver.back()
#             time.sleep(2)
#             return True, "'판매인 프로모션' 메뉴 이동 및 확인 성공."
#         except TimeoutException:
#             error_msg = "실패: '판매인 프로모션' 메뉴 클릭 후 '프로모션' 타이틀을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "promotion_title_not_found")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"판매인 프로모션 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- '판매인 프로모션' 스크롤, 클릭, 화면 이동 확인 시나리오 종료 ---")
