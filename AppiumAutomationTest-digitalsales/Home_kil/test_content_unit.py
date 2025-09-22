# Home_kil/test_content_unit.py (수정 완료)

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

def test_home_content_unit(flow_tester):
    """
    홈 화면의 콘텐츠 유닛을 확인하는 테스트 시나리오입니다.
    '홈' UI 위에 콘텐츠 유닛이 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
    """
    print("\n--- 홈 > 콘텐츠 유닛 확인 시나리오 시작 ---")

    try:
        # 1. XPath 정의
        content_unit_container_xpath = '//android.widget.TextView[@text="1"]'
        home_container_xpath = '//android.view.View[@content-desc="홈"]'

        # 2. '콘텐츠' 유닛 컨테이너가 '홈' UI 위에 보일 때까지 스크롤
        print("콘텐츠 유닛이 보일 때까지 스크롤합니다.")
        max_scroll_attempts = 10
        element_in_view = False
        for i in range(max_scroll_attempts):
            try:
                content_element = flow_tester.driver.find_element(AppiumBy.XPATH, content_unit_container_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if content_element.is_displayed():
                    content_rect = content_element.rect
                    home_rect = home_element.rect
                    if (content_rect['y'] + content_rect['height']) < home_rect['y']:
                        print("✅ 위치 조건 충족! 콘텐츠 유닛이 하단 '홈' UI보다 위에 있습니다.")
                        element_in_view = True
                        break
                    else:
                         print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. 스크롤합니다.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) 콘텐츠 유닛이 아직 보이지 않습니다. 스크롤합니다.")
            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) 콘텐츠 유닛을 찾는 중... 스크롤합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            save_screenshot_on_failure(flow_tester.driver, "content_unit_not_in_view")
            return False, f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 콘텐츠 유닛을 찾지 못했습니다."

        # 3. 모든 콘텐츠 항목을 수집하고 개수 확인 (스와이프 포함)
        print("스와이프를 통해 모든 콘텐츠 항목을 수집하고 개수를 확인합니다.")
        base_item_xpath   = '//android.widget.TextView[@text="'
        container_element = flow_tester.driver.find_element(AppiumBy.XPATH, content_unit_container_xpath)
        swipe_area = container_element.rect
        start_x = swipe_area['x'] + swipe_area['width'] * 1.0
        end_x = swipe_area['x'] + swipe_area['width'] * 0.1
        y = swipe_area['y'] + swipe_area['height'] / 2

        item_index = 1
        total_items_found = 0

        while item_index <= 5:
            indexed_xpath = f'{base_item_xpath}{item_index}"]'
            try:
                print(f"콘텐츠 유닛 [{item_index}] 확인 시도...{indexed_xpath}")
                flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
                print(f"✅ 콘텐츠 유닛 [{item_index}] 발견.{indexed_xpath}")
                total_items_found = item_index
                item_index += 1
                continue
            except NoSuchElementException:
                print(f"콘텐츠 유닛 [{item_index}] 없음. 스와이프를 시도합니다.")
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
                                                                                                                y).release()
                actions.perform()
                time.sleep(2)
                try:
                    print(f"스와이프 후, 콘텐츠 유닛 [{item_index}] 다시 확인...{indexed_xpath}")
                    flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
                    print(f"✅ 스와이프 후, 콘텐츠 유닛 [{item_index}] 발견.{indexed_xpath}")
                    total_items_found = item_index
                    item_index += 1
                except NoSuchElementException:
                    print(f"스와이프 후에도 콘텐츠 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
                    break

        print(f"✅ 탐색 완료. 발견된 총 콘텐츠 유닛 수: {total_items_found}개")

        if total_items_found < 3:
            return False, f"테스트에 필요한 최소 유닛(3개)을 찾지 못했습니다. (발견된 수: {total_items_found}개)"

        # 4. 3번째 항목 클릭하여 상세 페이지로 이동
        print("콘텐츠 항목을 클릭합니다.")
        target_item_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        target_item = flow_tester.driver.find_element(AppiumBy.XPATH, target_item_xpath)
        target_item.click()
        time.sleep(5)

        # 5. 상세 페이지 진입 확인
        content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]'
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
            message="콘텐츠 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 상세 페이지로 성공적으로 이동했습니다.")

        # 6. 뒤로 가기
        print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back()
        time.sleep(3)

        return True, f"콘텐츠 유닛 순차 탐색 및 3번 항목 클릭 후 상세 페이지 이동 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
        return False, f"콘텐츠 유닛 테스트 중 오류 발생: {e}"
    finally:
        print("--- 홈 > 콘텐츠 유닛 확인 시나리오 종료 ---")