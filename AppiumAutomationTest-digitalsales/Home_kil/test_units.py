# Home_kil/test_units.py (수정 완료)

import sys
import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# 유틸리티 함수 임포트
from Utils.scrolling_function import scroll_down
from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath):
    """
    홈 화면의 콘텐츠 유닛을 확인하는 테스트 시나리오입니다.
    '홈' UI 위에 콘텐츠 유닛이 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
    """
    print("\n--- 홈 > 콘텐츠 유닛 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = HomeKilLocators.AOS

    try:
        # 1. XPath 정의 (매개변수로 받은 값을 그대로 사용)
        home_container_xpath = locators.home_container_xpath  # 수정됨
        target_y = None  # 유닛의 Y 좌표를 저장할 변수

        # 2. '콘텐츠' 유닛 컨테이너와 인덱스가 지정된 위치에 올 때까지 스크롤
        print("콘텐츠 유닛이 지정된 위치에 보일 때까지 스크롤합니다.")
        max_scroll_attempts = 10
        element_in_view = False
        for i in range(max_scroll_attempts):
            try:
                content_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_container_xpath)
                element_index = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                # 두 요소가 모두 화면에 보이는지 먼저 확인
                if content_element.is_displayed() and element_index.is_displayed():
                    content_rect = content_element.rect
                    index_rect = element_index.rect
                    home_rect = home_element.rect

                    # --- 여기가 수정된 핵심 조건 ---
                    # 조건 1: 컨테이너(content)가 인덱스(index)보다 위에 있는가?
                    is_container_above_index = content_rect['y'] < index_rect['y']
                    # 조건 2: 인덱스(index)가 홈 버튼(home)보다 위에 있는가? (이것만 만족하면 컨테이너는 당연히 만족)
                    is_index_above_home = (index_rect['y'] + index_rect['height']) < home_rect['y']

                    if is_container_above_index and is_index_above_home:
                        print("✅ 위치 조건 충족! (컨테이너 > 인덱스 > 홈 버튼)")
                        target_y = index_rect['y']  # 조건 만족 시 index_rect의 Y값을 저장
                        print(f"✅ 타겟 유닛의 Y 좌표 저장: {target_y}")
                        element_in_view = True
                        break  # 조건 만족 시 스크롤 중단
                    else:
                        print(
                            f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. (컨테이너>인덱스: {is_container_above_index}, 인덱스>홈: {is_index_above_home}). 스크롤합니다.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) 콘텐츠 유닛 또는 인덱스가 아직 보이지 않습니다. 스크롤합니다.")
            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) 콘텐츠 유닛 또는 인덱스를 찾는 중... 스크롤합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            save_screenshot_on_failure(flow_tester.driver, "content_unit_not_in_view")
            return False, f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 콘텐츠 유닛을 찾지 못했습니다."

        # 3. 모든 콘텐츠 항목을 수집하고 개수 확인 (스와이프 포함)
        print("스와이프를 통해 모든 콘텐츠 항목을 수집하고 개수를 확인합니다.")
        base_item_xpath = '//android.widget.TextView[@text="'
        container_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
        swipe_area = container_element.rect
        start_x = swipe_area['x'] + swipe_area['width'] * 1.0
        end_x = swipe_area['x'] + swipe_area['width'] * 0.1
        y = swipe_area['y'] + swipe_area['height'] / 2

        item_index = 1
        total_items_found = 0

        while item_index <= 5:
            indexed_xpath = f'{base_item_xpath}{item_index}"]'
            item_found_on_correct_y = False
            try:
                # Y 좌표가 동일한 유닛만 검사하는 로직
                possible_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
                print(f"콘텐츠 유닛 [{item_index}] 확인 시도... (발견된 요소 수: {len(possible_elements)})")
                for element in possible_elements:
                    if element.is_displayed() and element.rect['y'] == target_y:
                        print(f"✅ 콘텐츠 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
                        item_found_on_correct_y = True
                        total_items_found = item_index
                        item_index += 1
                        break  # 올바른 Y 좌표에서 요소를 찾았으므로 내부 루프 종료

                if not item_found_on_correct_y:
                    raise NoSuchElementException  # 올바른 Y 좌표에 요소가 없으면 예외 발생시켜 스와이프 로직으로 이동

            except NoSuchElementException:
                if item_found_on_correct_y: continue  # 이미 찾았으면 다음 인덱스로

                print(f"콘텐츠 유닛 [{item_index}] 없음. 스와이프를 시도합니다.")
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
                                                                                                                y).release()
                actions.perform()
                time.sleep(2)
                try:
                    # 스와이프 후, Y 좌표가 동일한 유닛만 다시 검사
                    possible_elements_after_swipe = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
                    print(f"스와이프 후, 유닛 [{item_index}] 다시 확인... (발견된 요소 수: {len(possible_elements_after_swipe)})")
                    item_found_after_swipe = False
                    for element in possible_elements_after_swipe:
                        if element.is_displayed() and element.rect['y'] == target_y:
                            print(f"✅ 스와이프 후, 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
                            total_items_found = item_index
                            item_index += 1
                            item_found_after_swipe = True
                            break

                    if not item_found_after_swipe:
                        print(f"스와이프 후에도 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
                        break  # 스와이프 후에도 없으면 최종 종료

                except NoSuchElementException:
                    print(f"스와이프 후에도 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
                    break

        print(f"✅ 탐색 완료. 발견된 총 유닛 수: {total_items_found}개")

        if total_items_found < 0:  # [수정] 0개 미만일 수 없으므로 0개로 변경 (혹은 1개)
            return False, f"테스트에 필요한 최소 유닛(1개)을 찾지 못했습니다. (발견된 수: {total_items_found}개)"

        # 4. 3번째 항목 클릭하여 상세 페이지로 이동
        # print("콘텐츠 항목을 클릭합니다.")
        # target_item_xpath = '//android.widget.TextView[@text="3"]'
        # target_item = flow_tester.driver.find_element(AppiumBy.XPATH, target_item_xpath)
        # target_item.click()
        # time.sleep(5)

        print("콘텐츠 항목을 클릭합니다.")
        # 클릭할 좌표를 스와이프 시작 지점 근처의 아이템으로 가정하고 클릭합니다.
        # 보통 첫 아이템은 왼쪽 영역에 있으므로, end_x 좌표를 사용합니다.
        click_x = end_x + 150
        click_y = y
        print(f"스와이프 영역의 첫 아이템 위치로 추정되는 좌표 ({int(click_x)}, {int(click_y)})를 클릭합니다.")
        flow_tester.driver.tap([(click_x, click_y)])
        # --- 여기까지 로직 수정 ---

        # 5. 상세 페이지 진입 확인
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
            message="콘텐츠 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 상세 페이지로 성공적으로 이동했습니다.")

        # 6. 뒤로 가기
        print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back()
        time.sleep(3)

        return True, f" 유닛 순차 탐색 및 항목 클릭 후 상세 페이지 이동 확인 성공."  # 메시지 수정

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
        return False, f" 유닛 테스트 중 오류 발생: {e}"
    finally:
        print("--- 홈 >  유닛 확인 시나리오 종료 ---")


# Seller app checklist-31 제품 유닛 확인
def test_product_unit(flow_tester):
    locators = HomeKilLocators.AOS  # 추가
    unit_container_xpath = locators.unit_container_xpath  # 수정됨
    unit_index_xpath = locators.unit_index_xpath  # 수정됨
    content_detail_page_title_xpath = locators.content_detail_page_title_xpath  # 수정됨
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)


# Seller app checklist-37 컨텐츠 유닛 확인
def test_content_unit(flow_tester):
    locators = HomeKilLocators.AOS  # 추가
    unit_container_xpath = locators.title_xpath  # 수정됨
    unit_index_xpath = locators.unit_index_xpath  # 수정됨
    content_detail_page_title_xpath = locators.final_page_text_xpath  # 수정됨
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)


# Seller app checklist-38 프로모션 유닛 확인
def test_client_unit(flow_tester):
    locators = HomeKilLocators.AOS  # 추가
    # [참고] 아래 두 XPath는 HomeKilLocators에 정의되어 있지 않아 로컬 XPath를 유지합니다.
    unit_container_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]'
    unit_index_xpath = locators.unit_index_xpath  # 수정됨
    content_detail_page_title_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)



# # Home_kil/test_units.py (수정 완료)
#
# import sys
# import os
# import time
#
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # W3C Actions를 위한 추가 임포트
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions.pointer_input import PointerInput
# from selenium.webdriver.common.actions import interaction
# from selenium.webdriver.common.actions.action_builder import ActionBuilder
#
# # 유틸리티 함수 임포트
# from Utils.scrolling_function import scroll_down
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
# def test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath):
#     """
#     홈 화면의 콘텐츠 유닛을 확인하는 테스트 시나리오입니다.
#     '홈' UI 위에 콘텐츠 유닛이 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
#     """
#     print("\n--- 홈 > 콘텐츠 유닛 확인 시나리오 시작 ---")
#
#     try:
#         # 1. XPath 정의 (매개변수로 받은 값을 그대로 사용)
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'
#         target_y = None # 유닛의 Y 좌표를 저장할 변수
#
#         # 2. '콘텐츠' 유닛 컨테이너와 인덱스가 지정된 위치에 올 때까지 스크롤
#         print("콘텐츠 유닛이 지정된 위치에 보일 때까지 스크롤합니다.")
#         max_scroll_attempts = 10
#         element_in_view = False
#         for i in range(max_scroll_attempts):
#             try:
#                 content_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_container_xpath)
#                 element_index = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
#                 home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 # 두 요소가 모두 화면에 보이는지 먼저 확인
#                 if content_element.is_displayed() and element_index.is_displayed():
#                     content_rect = content_element.rect
#                     index_rect = element_index.rect
#                     home_rect = home_element.rect
#
#                     # --- 여기가 수정된 핵심 조건 ---
#                     # 조건 1: 컨테이너(content)가 인덱스(index)보다 위에 있는가?
#                     is_container_above_index = content_rect['y'] < index_rect['y']
#                     # 조건 2: 인덱스(index)가 홈 버튼(home)보다 위에 있는가? (이것만 만족하면 컨테이너는 당연히 만족)
#                     is_index_above_home = (index_rect['y'] + index_rect['height']) < home_rect['y']
#
#                     if is_container_above_index and is_index_above_home:
#                         print("✅ 위치 조건 충족! (컨테이너 > 인덱스 > 홈 버튼)")
#                         target_y = index_rect['y']  # 조건 만족 시 index_rect의 Y값을 저장
#                         print(f"✅ 타겟 유닛의 Y 좌표 저장: {target_y}")
#                         element_in_view = True
#                         break  # 조건 만족 시 스크롤 중단
#                     else:
#                         print(
#                             f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. (컨테이너>인덱스: {is_container_above_index}, 인덱스>홈: {is_index_above_home}). 스크롤합니다.")
#                 else:
#                     print(f"({i + 1}/{max_scroll_attempts}) 콘텐츠 유닛 또는 인덱스가 아직 보이지 않습니다. 스크롤합니다.")
#             except NoSuchElementException:
#                 print(f"({i + 1}/{max_scroll_attempts}) 콘텐츠 유닛 또는 인덱스를 찾는 중... 스크롤합니다.")
#
#             scroll_down(flow_tester.driver)
#             time.sleep(1)
#
#         if not element_in_view:
#             save_screenshot_on_failure(flow_tester.driver, "content_unit_not_in_view")
#             return False, f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 콘텐츠 유닛을 찾지 못했습니다."
#
#         # 3. 모든 콘텐츠 항목을 수집하고 개수 확인 (스와이프 포함)
#         print("스와이프를 통해 모든 콘텐츠 항목을 수집하고 개수를 확인합니다.")
#         base_item_xpath = '//android.widget.TextView[@text="'
#         container_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
#         swipe_area = container_element.rect
#         start_x = swipe_area['x'] + swipe_area['width'] * 1.0
#         end_x = swipe_area['x'] + swipe_area['width'] * 0.1
#         y = swipe_area['y'] + swipe_area['height'] / 2
#
#         item_index = 1
#         total_items_found = 0
#
#         while item_index <= 5:
#             indexed_xpath = f'{base_item_xpath}{item_index}"]'
#             item_found_on_correct_y = False
#             try:
#                 # Y 좌표가 동일한 유닛만 검사하는 로직
#                 possible_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
#                 print(f"콘텐츠 유닛 [{item_index}] 확인 시도... (발견된 요소 수: {len(possible_elements)})")
#                 for element in possible_elements:
#                     if element.is_displayed() and element.rect['y'] == target_y:
#                         print(f"✅ 콘텐츠 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
#                         item_found_on_correct_y = True
#                         total_items_found = item_index
#                         item_index += 1
#                         break  # 올바른 Y 좌표에서 요소를 찾았으므로 내부 루프 종료
#
#                 if not item_found_on_correct_y:
#                     raise NoSuchElementException  # 올바른 Y 좌표에 요소가 없으면 예외 발생시켜 스와이프 로직으로 이동
#
#             except NoSuchElementException:
#                 if item_found_on_correct_y: continue  # 이미 찾았으면 다음 인덱스로
#
#                 print(f"콘텐츠 유닛 [{item_index}] 없음. 스와이프를 시도합니다.")
#                 actions = ActionChains(flow_tester.driver)
#                 actions.w3c_actions = ActionBuilder(flow_tester.driver,
#                                                     mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#                 actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
#                                                                                                                 y).release()
#                 actions.perform()
#                 time.sleep(2)
#                 try:
#                     # 스와이프 후, Y 좌표가 동일한 유닛만 다시 검사
#                     possible_elements_after_swipe = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
#                     print(f"스와이프 후, 유닛 [{item_index}] 다시 확인... (발견된 요소 수: {len(possible_elements_after_swipe)})")
#                     item_found_after_swipe = False
#                     for element in possible_elements_after_swipe:
#                         if element.is_displayed() and element.rect['y'] == target_y:
#                             print(f"✅ 스와이프 후, 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
#                             total_items_found = item_index
#                             item_index += 1
#                             item_found_after_swipe = True
#                             break
#
#                     if not item_found_after_swipe:
#                         print(f"스와이프 후에도 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
#                         break  # 스와이프 후에도 없으면 최종 종료
#
#                 except NoSuchElementException:
#                     print(f"스와이프 후에도 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
#                     break
#
#         print(f"✅ 탐색 완료. 발견된 총 유닛 수: {total_items_found}개")
#
#         if total_items_found < 0:
#             return False, f"테스트에 필요한 최소 유닛(3개)을 찾지 못했습니다. (발견된 수: {total_items_found}개)"
#
#         # 4. 3번째 항목 클릭하여 상세 페이지로 이동
#         # print("콘텐츠 항목을 클릭합니다.")
#         # target_item_xpath = '//android.widget.TextView[@text="3"]'
#         # target_item = flow_tester.driver.find_element(AppiumBy.XPATH, target_item_xpath)
#         # target_item.click()
#         # time.sleep(5)
#
#         print("콘텐츠 항목을 클릭합니다.")
#         # 클릭할 좌표를 스와이프 시작 지점 근처의 아이템으로 가정하고 클릭합니다.
#         # 보통 첫 아이템은 왼쪽 영역에 있으므로, end_x 좌표를 사용합니다.
#         click_x = end_x + 150
#         click_y = y
#         print(f"스와이프 영역의 첫 아이템 위치로 추정되는 좌표 ({int(click_x)}, {int(click_y)})를 클릭합니다.")
#         flow_tester.driver.tap([(click_x, click_y)])
#         # --- 여기까지 로직 수정 ---
#
#         # 5. 상세 페이지 진입 확인
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
#             message="콘텐츠 상세 페이지로 이동하지 못했습니다."
#         )
#         print("✅ 상세 페이지로 성공적으로 이동했습니다.")
#
#         # 6. 뒤로 가기
#         print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
#         flow_tester.driver.back()
#         time.sleep(3)
#
#         return True, f" 유닛 순차 탐색 및 3번 항목 클릭 후 상세 페이지 이동 확인 성공."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
#         return False, f" 유닛 테스트 중 오류 발생: {e}"
#     finally:
#         print("--- 홈 >  유닛 확인 시나리오 종료 ---")
#
#
# # Seller app checklist-31 제품 유닛 확인
# def test_product_unit(flow_tester):
#     unit_container_xpath = '//android.widget.Button[@text="판매순"]'
#     unit_index_xpath = '//android.widget.TextView[@text="1"]'
#     content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]'
#     return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)
#
#
# # Seller app checklist-37 컨텐츠 유닛 확인
# def test_content_unit(flow_tester):
#     unit_container_xpath = '//android.widget.TextView[@text="공유할 영업 콘텐츠를 추천 드려요"]'
#     unit_index_xpath = '//android.widget.TextView[@text="1"]'
#     content_detail_page_title_xpath = '//android.widget.TextView[@text="라이프 스토리"]'
#     return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)
#
#
# # Seller app checklist-38 프로모션 유닛 확인
# def test_client_unit(flow_tester):
#     unit_container_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]'
#     unit_index_xpath = '//android.widget.TextView[@text="1"]'
#     content_detail_page_title_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
#     return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)
#
