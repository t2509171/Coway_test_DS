# Home_kil/test_product_shortcuts.py (요청하신 시나리오에 맞춘 최종 수정안)

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 사용자님의 코드 스타일을 기억하여 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

def test_verify_product_shortcuts_exist(flow_tester):
    """
    홈 화면에서 '제품 바로가기' 섹션과 '정수기' 아이콘이 존재하는지 확인합니다.
    """
    print("\n--- 홈 > 제품 바로가기 > '정수기' 아이콘 존재 확인 시나리오 시작 ---")
    try:
        # 1. '제품 바로가기' 텍스트가 보일 때까지 아래로 스크롤
        target_text_xpath = '//android.widget.TextView[@text="제품 바로가기"]'
        print(f"'{target_text_xpath}' 텍스트가 보일 때까지 스크롤합니다.")

        max_scroll_attempts = 10
        element_found = False
        for i in range(max_scroll_attempts):
            try:
                if flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath).is_displayed():
                    print("✅ '제품 바로가기' 텍스트를 찾았습니다.")
                    element_found = True
                    break
            except NoSuchElementException:
                print(f"({i+1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")
                scroll_down(flow_tester.driver)

        if not element_found:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 '제품 바로가기'를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "product_shortcut_not_found")
            return False, error_msg

        # 2. '정수기' 아이콘이 존재하는지 확인 (클릭 X)
        water_purifier_xpath = '//android.view.View[@content-desc="정수기"]'
        print(f"'{water_purifier_xpath}' (정수기) 아이콘이 존재하는지 확인합니다.")
        try:
            # 요소가 화면에 나타날 때까지 최대 5초 대기
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, water_purifier_xpath))
            )
            print("✅ '정수기' 아이콘이 성공적으로 확인되었습니다.")
        except TimeoutException:
            error_msg = "실패: '정수기' 아이콘을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "water_purifier_icon_not_found")
            return False, error_msg

        # 모든 검증이 통과하면 성공을 반환
        return True, "제품 바로가기 섹션 및 정수기 아이콘 존재 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "verify_product_shortcut_failure")
        return False, f"제품 바로가기 존재 확인 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 제품 바로가기 > '정수기' 아이콘 존재 확인 시나리오 종료 ---")