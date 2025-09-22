# Home_kil/test_product_shortcuts.py (수정 완료)

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

def test_verify_product_shortcuts_exist(flow_tester):
    """
    홈 화면에서 '제품 바로가기' 섹션이 '홈' UI 위에 보일 때까지 스크롤하고 '정수기' 아이콘을 확인합니다.
    """
    print("\n--- 홈 > 제품 바로가기 > '정수기' 아이콘 존재 확인 시나리오 시작 ---")
    try:
        # 1. XPath 정의
        target_text_xpath = '//android.widget.TextView[@text="제품 바로가기"]'
        home_container_xpath = '//android.view.View[@content-desc="홈"]'

        max_scroll_attempts = 10
        element_in_view = False

        # 2. '제품 바로가기' 텍스트가 '홈' UI 위에 보일 때까지 스크롤
        print(f"'{target_text_xpath}' 텍스트가 보일 때까지 스크롤합니다.")
        for i in range(max_scroll_attempts):
            try:
                target_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if target_element.is_displayed():
                    target_rect = target_element.rect
                    home_rect = home_element.rect
                    if (target_rect['y'] + target_rect['height']) < home_rect['y']:
                        print("✅ '제품 바로가기' 텍스트를 클릭 가능한 위치에서 찾았습니다.")
                        element_in_view = True
                        break
                    else:
                        print(f"({i+1}/{max_scroll_attempts}) '제품 바로가기'가 홈 UI에 가려져 있습니다. 스크롤 다운.")
                else:
                    print(f"({i+1}/{max_scroll_attempts}) '제품 바로가기'가 보이지 않습니다. 스크롤 다운.")
            except NoSuchElementException:
                print(f"({i+1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 '제품 바로가기'를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "product_shortcut_not_in_view")
            return False, error_msg

        # 3. '정수기' 아이콘이 존재하는지 확인
        water_purifier_xpath = '//android.view.View[@content-desc="정수기"]'
        print(f"'{water_purifier_xpath}' (정수기) 아이콘이 존재하는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, water_purifier_xpath))
            )
            print("✅ '정수기' 아이콘이 성공적으로 확인되었습니다.")
        except TimeoutException:
            error_msg = "실패: '정수기' 아이콘을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "water_purifier_icon_not_found")
            return False, error_msg

        return True, "제품 바로가기 섹션 및 정수기 아이콘 존재 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "verify_product_shortcut_failure")
        return False, f"제품 바로가기 존재 확인 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 제품 바로가기 > '정수기' 아이콘 존재 확인 시나리오 종료 ---")