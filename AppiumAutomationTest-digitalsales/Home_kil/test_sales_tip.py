# Home_kil/test_sales_tip.py (수정 완료)

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ActionChains를 사용하기 위해 필요한 import 구문
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# 유틸리티 함수 임포트
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

def test_sales_tip_interaction(flow_tester):
    """Seller app checklist-18: 판매 팁 기능 확인 (스와이프 및 터치)"""
    print("\n--- 판매 팁 기능 확인 시나리오 시작 (checklist-18) ---")

    sales_tip_xpath = '//android.widget.TextView[@text="공지사항으로 이동하기 >"]'
    home_container_xpath = '//android.view.View[@content-desc="홈"]'

    try:
        # 1. 판매 팁 요소가 화면에 나타날 때까지 대기
        print("판매 팁 요소를 찾습니다...")
        try:
            sales_tip_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, sales_tip_xpath))
            )
            # 홈 UI와 위치 비교 (일반적으로 상단에 있어 불필요하나, 안정성을 위해 추가)
            home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
            if (sales_tip_element.rect['y'] + sales_tip_element.rect['height']) < home_element.rect['y']:
                 print("✅ 판매 팁 요소를 찾았습니다.")
            else:
                save_screenshot_on_failure(flow_tester.driver, "sales_tip_obstructed")
                return False, "실패: 판매 팁이 홈 UI에 가려져 있습니다."

        except TimeoutException:
            save_screenshot_on_failure(flow_tester.driver, "sales_tip_not_found")
            return False, "실패: 판매 팁 요소를 찾지 못했습니다."


        # 2. ActionChains 스와이프 로직
        print("스와이프 동작을 확인합니다...")
        location = sales_tip_element.location
        size = sales_tip_element.size
        center_y = location['y'] + size['height'] // 2
        start_x = location['x'] + size['width'] * 0.8
        end_x = location['x'] + size['width'] * 0.1

        def perform_swipe(start_x, start_y, end_x, end_y, duration_ms=500):
            actions = ActionChains(flow_tester.driver)
            actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y).pointer_down().pause(duration_ms / 1000).move_to_location(end_x, end_y).release()
            actions.perform()
            print(f"  - 스와이프 수행: ({int(start_x)}, {int(start_y)}) -> ({int(end_x)}, {int(end_y)})")

        perform_swipe(start_x, center_y, end_x, center_y)
        time.sleep(1)
        perform_swipe(end_x, center_y, start_x, center_y)
        time.sleep(1)
        print("✅ 스와이프 동작이 오류 없이 수행되었습니다.")

        # 3. 터치 동작 확인 로직
        print("터치 시 화면 변화가 없는지 확인합니다...")
        source_before_tap = flow_tester.driver.page_source
        sales_tip_element.click()
        time.sleep(2)
        source_after_tap = flow_tester.driver.page_source

        if source_before_tap != source_after_tap:
            save_screenshot_on_failure(flow_tester.driver, "sales_tip_tap_error")
            return False, "실패: 판매 팁 터치 후 화면 UI가 변경되었습니다."

        print("✅ 성공: 터치 후 화면에 아무런 변화가 없습니다.")
        return True, "판매 팁 기능(스와이프, 터치) 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "sales_tip_failure")
        return False, f"판매 팁 테스트 중 오류 발생: {e}"
    finally:
        print("--- 판매 팁 기능 확인 시나리오 종료 ---")