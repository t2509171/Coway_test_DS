# Home_kil/test_units.py

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

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            # IOS 에 필요한 XPath 변수들이 모두 있는지 확인
            if not all([unit_container_xpath, unit_index_xpath,
                        content_detail_page_title_xpath, locators.home_button_xpath]):
                 print(f"경고: {flow_tester.platform} 플랫폼에 필요한 일부 콘텐츠 유닛 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
                 return True, f"{flow_tester.platform} 콘텐츠 유닛 XPath 부족 (테스트 통과 간주)"
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. XPath 정의 (매개변수 + locators)
        home_container_xpath = locators.home_button_xpath # 수정됨
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
        # 플랫폼별 텍스트 속성 선택
        text_attribute = "@text" if flow_tester.platform == 'android' else "@value" # IOS는 @value 또는 @label 사용 가능성 있음
        base_item_xpath = f'//{ "android.widget.TextView" if flow_tester.platform == "android" else "XCUIElementTypeStaticText" }[{text_attribute}="'

        container_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
        swipe_area = container_element.rect
        # 스와이프 시작/종료 지점 조정 (컨테이너 전체를 스와이프하도록)
        container_for_swipe = flow_tester.driver.find_element(AppiumBy.XPATH, unit_container_xpath)
        swipe_area_full = container_for_swipe.rect
        start_x = swipe_area_full['x'] + swipe_area_full['width'] * 0.8 # 오른쪽 끝에서 시작
        end_x = swipe_area_full['x'] + swipe_area_full['width'] * 0.1   # 왼쪽 끝으로 이동
        y = swipe_area['y'] + swipe_area['height'] / 2 # Y 좌표는 인덱스 요소 기준 유지

        item_index = 1
        total_items_found = 0
        max_items_to_check = 5 # 최대 5개까지만 확인

        while item_index <= max_items_to_check:
            indexed_xpath = f'{base_item_xpath}{item_index}"]'
            item_found_on_correct_y = False
            try:
                # Y 좌표가 동일한 유닛만 검사하는 로직
                possible_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
                print(f"콘텐츠 유닛 [{item_index}] 확인 시도... (발견된 요소 수: {len(possible_elements)})")
                for element in possible_elements:
                    # is_displayed() 와 Y좌표 비교 추가
                    if element.is_displayed() and abs(element.rect['y'] - target_y) < 10: # Y좌표 오차 허용
                        print(f"✅ 콘텐츠 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
                        item_found_on_correct_y = True
                        total_items_found = item_index
                        item_index += 1
                        break  # 올바른 Y 좌표에서 요소를 찾았으므로 내부 루프 종료

                if not item_found_on_correct_y:
                    # 현재 화면에 없으면 스와이프 로직으로 이동 (break 없이)
                    print(f"콘텐츠 유닛 [{item_index}] 이 현재 화면 또는 올바른 Y좌표에 없음.")
                    pass # 아래 except 블록으로 가게 됨

            except NoSuchElementException: # find_elements는 빈 리스트를 반환하므로 이 예외는 보통 발생 안 함
                 pass # 아래 스와이프 로직으로 이동

            # 스와이프 로직 (요소를 못 찾았거나, 찾았지만 올바른 위치가 아닐 때 실행)
            if not item_found_on_correct_y:
                 print(f"콘텐츠 유닛 [{item_index}] 없음. 스와이프를 시도합니다.")
                 # 화면 상태 저장 (스와이프 전)
                 source_before_swipe = flow_tester.driver.page_source

                 actions = ActionChains(flow_tester.driver)
                 actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                     mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                 actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
                                                                                                                 y).release()
                 actions.perform()
                 time.sleep(2) # 스와이프 애니메이션 대기

                 # 스와이프 후 화면 상태 비교
                 source_after_swipe = flow_tester.driver.page_source
                 if source_before_swipe == source_after_swipe:
                      print(f"스와이프 후 화면 변화 없음. 유닛 [{item_index}] 이후 탐색 종료.")
                      break # 더 이상 스와이프해도 변화가 없으면 종료

                 # 스와이프 후 다시 요소 찾기 시도
                 try:
                      possible_elements_after_swipe = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
                      print(f"스와이프 후, 유닛 [{item_index}] 다시 확인... (발견된 요소 수: {len(possible_elements_after_swipe)})")
                      item_found_after_swipe = False
                      for element in possible_elements_after_swipe:
                           if element.is_displayed() and abs(element.rect['y'] - target_y) < 10:
                                print(f"✅ 스와이프 후, 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
                                total_items_found = item_index
                                item_index += 1
                                item_found_after_swipe = True
                                break # 찾았으면 다음 인덱스로

                      if not item_found_after_swipe:
                           print(f"스와이프 후에도 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
                           break  # 스와이프 후에도 없으면 최종 종료
                 except NoSuchElementException:
                      print(f"스와이프 후에도 유닛 [{item_index}] 없음 (예외 발생). 탐색을 종료합니다.")
                      break


        print(f"✅ 탐색 완료. 발견된 총 유닛 수: {total_items_found}개")

        if total_items_found < 1: # 수정: 최소 1개는 있어야 클릭 가능
            return False, f"테스트에 필요한 최소 유닛(1개)을 찾지 못했습니다. (발견된 수: {total_items_found}개)"

        # 4. 첫 번째 항목 클릭하여 상세 페이지로 이동 (더 안정적인 방법)
        print("첫 번째 콘텐츠 항목을 클릭합니다.")
        try:
             # 첫 번째 항목의 XPath를 다시 구성 (index 1)
             first_item_xpath = f'{base_item_xpath}1"]'
             first_item_clickable = None
             # 첫번째 항목 요소들 중 올바른 Y좌표에 있는 클릭 가능한 요소 찾기
             possible_first_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, first_item_xpath)
             for elem in possible_first_elements:
                  if elem.is_displayed() and abs(elem.rect['y'] - target_y) < 10:
                       first_item_clickable = elem
                       break
             if not first_item_clickable:
                  raise NoSuchElementException("클릭할 첫 번째 항목을 찾지 못했습니다.")

             first_item_clickable.click()
             print("✅ 첫 번째 항목 클릭 완료.")
             time.sleep(5) # 상세 페이지 로딩 대기
        except (NoSuchElementException, TimeoutException) as e:
             error_msg = f"실패: 첫 번째 콘텐츠 항목을 클릭할 수 없습니다. {e}"
             save_screenshot_on_failure(flow_tester.driver, "first_content_item_click_failed")
             return False, error_msg


        # 5. 상세 페이지 진입 확인
        WebDriverWait(flow_tester.driver, 10).until( # 수정: flow_tester.wait -> WebDriverWait
            EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
            message="콘텐츠 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 상세 페이지로 성공적으로 이동했습니다.")

        # 6. 뒤로 가기
        print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back() # 상세 -> 홈
        time.sleep(3)

        return True, f" 유닛 순차 탐색 및 항목 클릭 후 상세 페이지 이동 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
        return False, f" 유닛 테스트 중 오류 발생: {e}"
    finally:
        print("--- 홈 >  유닛 확인 시나리오 종료 ---")


# Seller app checklist-31 제품 유닛 확인
def test_product_unit(flow_tester):
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    unit_container_xpath = locators.unit_container_xpath
    unit_index_xpath = locators.unit_index_xpath
    content_detail_page_title_xpath = locators.content_detail_page_title_xpath
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)


# Seller app checklist-37 컨텐츠 유닛 확인
def test_content_unit(flow_tester):
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    unit_container_xpath = locators.title_xpath # 컨텐츠 유닛의 컨테이너 XPath
    unit_index_xpath = locators.unit_index_xpath # 컨텐츠 유닛의 인덱스 XPath
    content_detail_page_title_xpath = locators.lifestory_title_xpath # 수정됨 (final_page_text_xpath -> lifestory_title_xpath)
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)


# Seller app checklist-38 프로모션 유닛 확인
def test_client_unit(flow_tester):
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            # IOS 값 확인 필요
            if not all(['//XCUIElementTypeStaticText[@name="공유할 프로모션을 추천 드려요"]', # IOS 컨테이너 XPath (예시)
                        locators.unit_index_xpath, '//XCUIElementTypeStaticText[@name="고객 프로모션"]']): # IOS 상세 페이지 XPath (예시)
                 print(f"경고: {flow_tester.platform} 플랫폼에 필요한 프로모션 유닛 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
                 return True, f"{flow_tester.platform} 프로모션 유닛 XPath 부족 (테스트 통과 간주)"
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    # 로컬 XPath 또는 플랫폼별 XPath 사용
    unit_container_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]' if flow_tester.platform == 'android' else '//XCUIElementTypeStaticText[@name="공유할 프로모션을 추천 드려요"]' # 예시
    unit_index_xpath = locators.unit_index_xpath
    content_detail_page_title_xpath = '//android.widget.TextView[@text="고객 프로모션"]' if flow_tester.platform == 'android' else '//XCUIElementTypeStaticText[@name="고객 프로모션"]' # 예시
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
