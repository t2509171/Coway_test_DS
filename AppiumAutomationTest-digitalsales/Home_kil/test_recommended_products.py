import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 사용자님의 코드 스타일을 기억하여 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

def test_find_shared_products_section(flow_tester):
    """
    홈 화면에서 '공유할 제품을 추천 드려요' 섹션이 보일 때까지 스크롤하고,
    '판매순' 버튼이 노출되는지 확인합니다.
    """
    print("\n--- 홈 > 공유할 제품 추천 섹션 확인 시나리오 시작 ---")
    try:
        # 1. '공유할 제품을 추천 드려요' 텍스트가 보일 때까지 아래로 스크롤
        target_text_xpath = '//android.widget.Button[@text="판매순"]'
        print(f"'{target_text_xpath}' 텍스트가 보일 때까지 스크롤합니다.")

        max_scroll_attempts = 10
        element_found = False
        for i in range(max_scroll_attempts):
            try:
                # 요소가 화면에 보이는지 확인
                if flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath).is_displayed():
                    print("✅ '공유할 제품을 추천 드려요' 텍스트를 찾았습니다.")
                    element_found = True
                    break
            except NoSuchElementException:
                # 요소가 없으면 스크롤 다운
                print(f"({i+1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")
                scroll_down(flow_tester.driver)

        if not element_found:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 '공유할 제품을 추천 드려요'를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "shared_product_section_not_found")
            return False, error_msg

        # 2. '판매순' 버튼이 나타나는지 확인
        sales_sort_button_xpath = '//android.widget.Button[@text="판매순"]'
        print(f"'{sales_sort_button_xpath}' (판매순 버튼)이 노출되는지 확인합니다.")
        try:
            # 요소가 화면에 나타날 때까지 최대 10초 대기
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, sales_sort_button_xpath))
            )
            print("✅ 판매순 버튼이 성공적으로 노출되었습니다.")
        except TimeoutException:
            error_msg = "실패: '판매순' 버튼을 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "sales_sort_button_not_found")
            return False, error_msg

        # 모든 검증이 통과하면 성공을 반환
        return True, "공유할 제품 추천 섹션 및 판매순 버튼 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "shared_product_test_failure")
        return False, f"공유할 제품 추천 섹션 확인 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 공유할 제품 추천 섹션 확인 시나리오 종료 ---")