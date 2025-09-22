import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down


def test_recommended_promotion(flow_tester):
    """
    홈 화면의 '공유할 프로모션을 추천 드려요' 섹션을 테스트합니다.
    1. 섹션이 하단 '홈' UI보다 위에 보일 때까지 스크롤합니다.
    2. '1'번 프로모션을 클릭합니다.
    3. '고객 프로모션' 페이지로 이동했는지 확인합니다.
    """
    print("\n--- 홈 > 추천 프로모션 확인 시나리오 시작 ---")
    try:
        # 1. XPath 정의
        title_xpath = '//android.widget.TextView[@text="공유할 프로모션을 추천 드려요"]'
        target_click_xpath = '//android.widget.TextView[@text="1"]'
        final_check_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
        home_container_xpath = '//android.view.View[@content-desc="홈"]'  # 위치 비교 기준

        max_scroll_attempts = 10
        section_found_and_clickable = False

        # 2. 지정된 횟수만큼 스크롤하며 요소의 위치를 확인하는 루프
        for i in range(max_scroll_attempts):
            try:
                title_element = flow_tester.driver.find_element(AppiumBy.XPATH, title_xpath)
                home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if title_element.is_displayed():
                    print("✅ '프로모션 추천' 섹션을 찾았습니다. 위치를 비교합니다.")
                    title_rect = title_element.rect
                    home_rect = home_container_element.rect

                    title_bottom_y = title_rect['y'] + title_rect['height']
                    home_top_y = home_rect['y']

                    if title_bottom_y < home_top_y:
                        print("✅ 위치 조건 충족! 대상이 하단 '홈' UI보다 위에 있습니다.")
                        section_found_and_clickable = True
                        break
                    else:
                        print("⚠️ 위치 조건 불충족. 대상이 '홈' UI에 가려져 있습니다. 스크롤합니다.")
            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) '프로모션 추천' 섹션을 찾는 중... 스크롤합니다.")

            scroll_down(flow_tester.driver)

        # 3. 루프 종료 후, 섹션을 찾았는지 확인
        if not section_found_and_clickable:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 섹션을 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "promotion_section_not_found")
            return False, error_msg

        # 4. '1'번 프로모션을 클릭
        print(f"'{target_click_xpath}' 요소를 클릭합니다.")
        try:
            wait = WebDriverWait(flow_tester.driver, 5)
            target_to_click = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, target_click_xpath))
            )
            target_to_click.click()
            time.sleep(3)
        except TimeoutException:
            error_msg = f"실패: '{target_click_xpath}' 요소를 클릭할 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "promotion_item_click_failed")
            return False, error_msg

        # 5. 최종 페이지 확인
        print(f"최종 페이지에서 '{final_check_xpath}' 텍스트를 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, final_check_xpath))
            )
            print("✅ Pass: '고객 프로모션' 페이지로 성공적으로 이동했습니다.")
            return True, "추천 프로모션 확인 시나리오 성공."
        except TimeoutException:
            error_msg = f"실패: '{final_check_xpath}' 텍스트를 찾지 못해 페이지 이동을 확인할 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "promotion_page_verification_failed")
            return False, error_msg

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "promotion_test_exception")
        return False, f"추천 프로모션 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 추천 프로모션 확인 시나리오 종료 ---")


