# Home_kil/test_recommended_products.py (수정 완료)

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

def test_find_shared_products_section(flow_tester):
    """
    홈 화면에서 '공유할 제품을 추천 드려요' 섹션이 '홈' UI 위에 보일 때까지 스크롤하고,
    '판매순' 버튼이 노출되는지 확인합니다.
    """
    print("\n--- 홈 > 공유할 제품 추천 섹션 확인 시나리오 시작 ---")
    try:
        # 1. XPath 정의
        target_text_xpath = '//android.widget.Button[@text="판매순"]' # 대표적인 요소로 '판매순' 버튼을 사용
        home_container_xpath = '//android.view.View[@content-desc="홈"]'

        max_scroll_attempts = 10
        element_in_view = False

        # 2. '판매순' 버튼이 '홈' UI 위에 보일 때까지 스크롤
        print(f"'{target_text_xpath}' 버튼이 보일 때까지 스크롤합니다.")
        for i in range(max_scroll_attempts):
            try:
                target_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if target_element.is_displayed():
                    target_rect = target_element.rect
                    home_rect = home_element.rect
                    if (target_rect['y'] + target_rect['height']) < home_rect['y']:
                        print("✅ '공유할 제품 추천' 섹션을 클릭 가능한 위치에서 찾았습니다.")
                        element_in_view = True
                        break
                    else:
                        print(f"({i+1}/{max_scroll_attempts}) 섹션이 홈 UI에 가려져 있습니다. 스크롤 다운.")
                else:
                     print(f"({i+1}/{max_scroll_attempts}) 섹션이 보이지 않습니다. 스크롤 다운.")
            except NoSuchElementException:
                print(f"({i+1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 '공유할 제품을 추천 드려요'를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "shared_product_section_not_in_view")
            return False, error_msg

        # 3. '판매순' 버튼이 최종적으로 노출되는지 재확인
        sales_sort_button_xpath = '//android.widget.Button[@text="판매순"]'
        print(f"'{sales_sort_button_xpath}' (판매순 버튼)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, sales_sort_button_xpath))
            )
            print("✅ 판매순 버튼이 성공적으로 노출되었습니다.")
        except TimeoutException:
            error_msg = "실패: '판매순' 버튼을 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "sales_sort_button_not_found_final")
            return False, error_msg

        return True, "공유할 제품 추천 섹션 및 판매순 버튼 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "shared_product_test_failure")
        return False, f"공유할 제품 추천 섹션 확인 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 공유할 제품 추천 섹션 확인 시나리오 종료 ---")