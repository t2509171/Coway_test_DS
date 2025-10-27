# # Home_kil/test_recommended_products.py
#
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
# # Xpath 저장소에서 HomeKilLocators 임포트
# from Xpath.xpath_repository import HomeKilLocators


# def test_find_shared_products_section(flow_tester):
#     """
#     홈 화면에서 '공유할 제품을 추천 드려요' 섹션이 '홈' UI 위에 보일 때까지 스크롤하고,
#     '판매순' 버튼이 노출되는지 확인합니다.
#     """
#     print("\n--- 홈 > 공유할 제품 추천 섹션 확인 시나리오 시작 ---")
#
#     # --- 플랫폼 분기 로직 추가 ---
#     try:
#         if flow_tester.platform == 'android':
#             locators = HomeKilLocators.AOS
#         elif flow_tester.platform == 'ios':
#             locators = HomeKilLocators.IOS
#             # IOS 는 sales_sort_button_xpath 가 정의되어야 함
#             if not locators.sales_sort_button_xpath:
#                  print(f"경고: {flow_tester.platform} 플랫폼의 판매순 버튼 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
#                  return True, f"{flow_tester.platform} 판매순 버튼 XPath 없음 (테스트 통과 간주)"
#         else:
#             raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
#     except AttributeError:
#         print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
#         locators = HomeKilLocators.AOS
#     # --- 플랫폼 분기 로직 완료 ---
#
#     try:
#         # 1. XPath 정의 (locators 객체 사용)
#         target_text_xpath = locators.sales_sort_button_xpath # 수정됨 ('판매순' 버튼을 대표 요소로 사용)
#         home_container_xpath = locators.home_button_xpath # 수정됨
#
#         max_scroll_attempts = 10
#         element_in_view = False
#
#         # 2. '판매순' 버튼이 '홈' UI 위에 보일 때까지 스크롤
#         print(f"'{target_text_xpath}' 버튼이 보일 때까지 스크롤합니다.")
#         for i in range(max_scroll_attempts):
#             try:
#                 target_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
#                 home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 if target_element.is_displayed():
#                     target_rect = target_element.rect
#                     home_rect = home_element.rect
#                     if (target_rect['y'] + target_rect['height']) < home_rect['y']:
#                         print("✅ '공유할 제품 추천' 섹션을 클릭 가능한 위치에서 찾았습니다.")
#                         element_in_view = True
#                         break
#                     else:
#                         print(f"({i+1}/{max_scroll_attempts}) 섹션이 홈 UI에 가려져 있습니다. 스크롤 다운.")
#                 else:
#                      print(f"({i+1}/{max_scroll_attempts}) 섹션이 보이지 않습니다. 스크롤 다운.")
#             except NoSuchElementException:
#                 print(f"({i+1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")
#
#             scroll_down(flow_tester.driver)
#             time.sleep(1)
#
#         if not element_in_view:
#             error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 '공유할 제품을 추천 드려요'를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "shared_product_section_not_in_view")
#             return False, error_msg
#
#         # 3. '판매순' 버튼이 최종적으로 노출되는지 재확인 (스크롤 후 요소가 다시 로드될 수 있으므로)
#         sales_sort_button_xpath = locators.sales_sort_button_xpath
#         print(f"'{sales_sort_button_xpath}' (판매순 버튼)이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 5).until(
#                 EC.visibility_of_element_located((AppiumBy.XPATH, sales_sort_button_xpath)) # 수정됨: presence -> visibility
#             )
#             print("✅ 판매순 버튼이 성공적으로 노출되었습니다.")
#         except TimeoutException:
#             error_msg = "실패: '판매순' 버튼을 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "sales_sort_button_not_found_final")
#             return False, error_msg
#
#         return True, "공유할 제품 추천 섹션 및 판매순 버튼 확인 성공."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "shared_product_test_failure")
#         return False, f"공유할 제품 추천 섹션 확인 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 > 공유할 제품 추천 섹션 확인 시나리오 종료 ---")


import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down


# (Xpath_repository 임포트는 이미 되어 있다고 가정합니다)
# from Xpath.xpath_repository import HomeKilLocators

def test_find_shared_products_section(flow_tester):
    """
    홈 화면에서 '공유할 제품을 추천 드려요' 섹션이 보일 때까지 스크롤하여 확인합니다.
    (Seller app checklist-30 항목 대응)
    """
    print("\n--- 홈 > '공유할 제품을 추천 드려요' 섹션 확인 시나리오 시작 ---")

    try:
        # --- 찾으려는 대상 정의 ---
        # 1. Accessibility ID (content-desc) - 가장 우선적으로 권장됨
        target_aid = '공유할 제품을 추천 드려요'

        # 2. XPath (text 속성) - 차선책
        # (참고: 플랫폼별로 'android.widget.TextView' 또는 'android.view.View' 일 수 있으므로
        #  와일드카드(*)를 사용하거나, locators에 플랫폼별로 정의하는 것이 좋습니다.)
        if flow_tester.platform == 'android':
            target_text_xpath = '//*[@text="공유할 제품을 추천 드려요"]'
        elif flow_tester.platform == 'ios':
            # iOS는 보통 name과 value가 동일합니다.
            target_text_xpath = f'//XCUIElementTypeStaticText[@name="{target_aid}"]'
        else:
            # 기본값 (AOS)
            target_text_xpath = '//*[@text="공유할 제품을 추천 드려요"]'
        # --- 대상 정의 완료 ---

        max_scroll_attempts = 10
        element_found = False

        print(f"'{target_aid}' 요소가 나타날 때까지 스크롤합니다.")

        for i in range(max_scroll_attempts):
            try:
                # [전략 1] Accessibility ID로 먼저 찾기 (가장 빠르고 안정적)
                element = flow_tester.driver.find_element(AppiumBy.ACCESSIBILITY_ID, target_aid)

                if element.is_displayed():
                    print("✅ 요소 찾기 성공 (Accessibility ID).")
                    element_found = True
                    break  # 요소를 찾았으므로 루프 종료

            except NoSuchElementException:
                # [전략 2] XPath (text 속성)로 찾기
                try:
                    element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)

                    if element.is_displayed():
                        print("✅ 요소 찾기 성공 (XPath by text).")
                        element_found = True
                        break  # 요소를 찾았으므로 루프 종료

                except NoSuchElementException:
                    # 두 전략 모두 실패 시 스크롤
                    print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾는 중... 스크롤합니다.")
                    scroll_down(flow_tester.driver)
                    time.sleep(1)  # 스크롤 후 UI 안정화 대기

        if not element_found:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 '공유할 제품을 추천 드려요' 요소를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "reco_product_title_not_found")
            return False, error_msg

        # 성공
        print("✅ '공유할 제품을 추천 드려요' 섹션 타이틀이 화면에 노출되었습니다.")
        return True, "'공유할 제품을 추천 드려요' 섹션 타이틀 확인 성공."

    except Exception as e:
        # (드라이버 충돌과 같은) 예상치 못한 오류 발생 시
        save_screenshot_on_failure(flow_tester.driver, "verify_reco_product_failure")
        return False, f"'공유할 제품을 추천 드려요' 확인 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > '공유할 제품을 추천 드려요' 섹션 확인 시나리오 종료 ---")

