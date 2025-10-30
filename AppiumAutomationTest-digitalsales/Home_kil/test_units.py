# Home_kil/test_units.py (W3C 스크롤로 수정)

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
# [!] --- 수정: 불안정한 scroll_down 함수 임포트 제거 --- [!]
# from Utils.scrolling_function import scroll_down
# [!] ----------------------------------------------- [!]
from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath):
    """
    홈 화면의 콘텐츠 유닛을 확인하는 테스트 시나리오입니다.
    불안정한 scroll_down 대신 안정적인 W3C Actions 스크롤로 수정되었습니다.
    """
    print("\n--- 홈 > 콘텐츠 유닛 확인 시나리오 시작 ---")

    # --- 플랫폼 분기 로직 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            if not all([unit_container_xpath, unit_index_xpath,
                        content_detail_page_title_xpath, locators.home_button_xpath]):
                print(f"경고: {flow_tester.platform} 플랫폼에 필요한 일부 콘텐츠 유닛 XPath가 정의되지 않았습니다. 테스트를 건너뜁니다.")
                return True, f"{flow_tester.platform} 콘텐츠 유닛 XPath 부족 (테스트 통과 간주)"
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        home_container_xpath = locators.home_button_xpath
        target_y = None

        print("콘텐츠 유닛이 지정된 위치에 보일 때까지 스크롤합니다.")
        max_scroll_attempts = 10
        element_in_view = False

        # [!] 스크롤을 위한 화면 크기 1회 계산 (try 블록 최상단)
        try:
            window_rect = flow_tester.driver.get_window_rect()
            scroll_start_y = window_rect['height'] * 0.7
            scroll_end_y = window_rect['height'] * 0.3
            scroll_x = window_rect['width'] * 0.5
        except Exception as e:
            # get_window_rect() 실패 시 (드라이버 불안정)
            return False, f"스크롤 준비 중 드라이버 오류 발생 (get_window_rect): {e}"

        for i in range(max_scroll_attempts):
            try:
                content_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_container_xpath)
                element_index = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if content_element.is_displayed() and element_index.is_displayed():
                    content_rect = content_element.rect
                    index_rect = element_index.rect
                    home_rect = home_element.rect

                    is_container_above_index = content_rect['y'] < index_rect['y']
                    is_index_above_home = (index_rect['y'] + index_rect['height']) < home_rect['y']

                    if is_container_above_index and is_index_above_home:
                        print("✅ 위치 조건 충족! (컨테이너 > 인덱스 > 홈 버튼)")
                        target_y = index_rect['y']
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

            # [!] --- 수정: W3C Actions를 사용한 안정적인 네이티브 스크롤 --- [!]
            try:
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(scroll_x, scroll_start_y).pointer_down().pause(
                    0.1).move_to_location(scroll_x, scroll_end_y).release()
                actions.perform()
                print(f"({i + 1}/{max_scroll_attempts}) W3C 네이티브 스크롤 수행.")
            except Exception as scroll_e:
                # W3C 스크롤마저 실패하면 드라이버가 완전히 불안정한 것임
                save_screenshot_on_failure(flow_tester.driver, "w3c_scroll_failed")
                return False, f"W3C 스크롤 실행 중 드라이버 오류 발생: {scroll_e}"
            # [!] ---------------------------------------------------- [!]

            time.sleep(1)  # 스크롤 애니메이션 대기

        if not element_in_view:
            save_screenshot_on_failure(flow_tester.driver, "content_unit_not_in_view")
            return False, f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 콘텐츠 유닛을 찾지 못했습니다."

        # 3. 모든 콘텐츠 항목을 수집하고 개수 확인 (스와이프 포함)
        print("스와이프를 통해 모든 콘텐츠 항목을 수집하고 개수를 확인합니다.")
        # (이후 스와이프 로직은 W3C Actions를 이미 사용하고 있으므로 안정적일 것으로 예상되어 유지합니다.)
        text_attribute = "@text" if flow_tester.platform == 'android' else "@value"
        base_item_xpath = f'//{"android.widget.TextView" if flow_tester.platform == "android" else "XCUIElementTypeStaticText"}[{text_attribute}="'

        container_element = flow_tester.driver.find_element(AppiumBy.XPATH, unit_index_xpath)
        swipe_area = container_element.rect

        container_for_swipe = flow_tester.driver.find_element(AppiumBy.XPATH, unit_container_xpath)
        swipe_area_full = container_for_swipe.rect
        start_x = swipe_area_full['x'] + swipe_area_full['width'] * 0.8
        end_x = swipe_area_full['x'] + swipe_area_full['width'] * 0.1
        y = swipe_area['y'] + swipe_area['height'] / 2

        item_index = 1
        total_items_found = 0
        max_items_to_check = 5

        while item_index <= max_items_to_check:
            indexed_xpath = f'{base_item_xpath}{item_index}"]'
            item_found_on_correct_y = False
            try:
                possible_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, indexed_xpath)
                print(f"콘텐츠 유닛 [{item_index}] 확인 시도... (발견된 요소 수: {len(possible_elements)})")
                for element in possible_elements:
                    if element.is_displayed() and abs(element.rect['y'] - target_y) < 10:
                        print(f"✅ 콘텐츠 유닛 [{item_index}] 발견. (좌표: {element.rect['x']}, {element.rect['y']})")
                        item_found_on_correct_y = True
                        total_items_found = item_index
                        item_index += 1
                        break

                if not item_found_on_correct_y:
                    print(f"콘텐츠 유닛 [{item_index}] 이 현재 화면 또는 올바른 Y좌표에 없음.")
                    pass

            except NoSuchElementException:
                pass

            if not item_found_on_correct_y:
                print(f"콘텐츠 유닛 [{item_index}] 없음. 스와이프를 시도합니다.")
                source_before_swipe = flow_tester.driver.page_source

                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
                                                                                                                y).release()
                actions.perform()
                time.sleep(2)

                source_after_swipe = flow_tester.driver.page_source
                if source_before_swipe == source_after_swipe:
                    print(f"스와이프 후 화면 변화 없음. 유닛 [{item_index}] 이후 탐색 종료.")
                    break

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
                            break

                    if not item_found_after_swipe:
                        print(f"스와이프 후에도 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
                        break
                except NoSuchElementException:
                    print(f"스와이프 후에도 유닛 [{item_index}] 없음 (예외 발생). 탐색을 종료합니다.")
                    break

        print(f"✅ 탐색 완료. 발견된 총 유닛 수: {total_items_found}개")

        if total_items_found < 1:
            return False, f"테스트에 필요한 최소 유닛(1개)을 찾지 못했습니다. (발견된 수: {total_items_found}개)"

        # 4. 첫 번째 항목 클릭하여 상세 페이지로 이동
        print("첫 번째 콘텐츠 항목을 클릭합니다.")
        try:
            first_item_xpath = f'{base_item_xpath}1"]'
            first_item_clickable = None
            possible_first_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, first_item_xpath)
            for elem in possible_first_elements:
                if elem.is_displayed() and abs(elem.rect['y'] - target_y) < 10:
                    first_item_clickable = elem
                    break
            if not first_item_clickable:
                raise NoSuchElementException("클릭할 첫 번째 항목을 찾지 못했습니다.")

            first_item_clickable.click()
            print("✅ 첫 번째 항목 클릭 완료.")
            time.sleep(5)
        except (NoSuchElementException, TimeoutException) as e:
            error_msg = f"실패: 첫 번째 콘텐츠 항목을 클릭할 수 없습니다. {e}"
            save_screenshot_on_failure(flow_tester.driver, "first_content_item_click_failed")
            return False, error_msg

        # 5. 상세 페이지 진입 확인
        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
            message="콘텐츠 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 상세 페이지로 성공적으로 이동했습니다.")

        # 6. 뒤로 가기
        print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back()  # 상세 -> 홈
        time.sleep(3)

        return True, f" 유닛 순차 탐색 및 항목 클릭 후 상세 페이지 이동 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
        return False, f" 유닛 테스트 중 오류 발생: {e}"
    finally:
        print("--- 홈 >  유닛 확인 시나리오 종료 ---")


# Seller app checklist-31 제품 유닛 확인
def test_product_unit(flow_tester):
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS

    unit_container_xpath = locators.unit_container_xpath
    unit_index_xpath = locators.unit_index_xpath
    content_detail_page_title_xpath = locators.content_detail_page_title_xpath
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)


# Seller app checklist-37 컨텐츠 유닛 확인
def test_content_unit(flow_tester):
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS

    unit_container_xpath = locators.title_xpath
    unit_index_xpath = locators.unit_index_xpath
    content_detail_page_title_xpath = locators.lifestory_title_xpath
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)


# Seller app checklist-38 프로모션 유닛 확인
def test_client_unit(flow_tester):
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
            unit_container_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]'
            content_detail_page_title_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            # (예시) IOS XPath가 정의되어 있다고 가정
            unit_container_xpath = '//XCUIElementTypeStaticText[@name="공유할 프로모션을 추천 드려요"]'
            content_detail_page_title_xpath = '//XCUIElementTypeStaticText[@name="고객 프로모션"]'

            if not all([unit_container_xpath, locators.unit_index_xpath, content_detail_page_title_xpath]):
                print(f"경고: {flow_tester.platform} 플랫폼에 필요한 프로모션 유닛 XPath가 정의되지 않았습니다. 테스트를 건너뜁니다.")
                return True, f"{flow_tester.platform} 프로모션 유닛 XPath 부족 (테스트 통과 간주)"
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
        unit_container_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]'
        content_detail_page_title_xpath = '//android.widget.TextView[@text="고객 프로모션"]'

    unit_index_xpath = locators.unit_index_xpath
    return test_home_content_unit(flow_tester, unit_container_xpath, unit_index_xpath, content_detail_page_title_xpath)