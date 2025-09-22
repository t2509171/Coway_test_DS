import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수들을 import 합니다.
from Utils.scrolling_function import scroll_down
from Utils.screenshot_helper import save_screenshot_on_failure

def test_banner_swipe(flow_tester):
    """
    배너를 찾아 스와이프하고, 터치한 뒤 사라지는지 최종 검증합니다.
    """
    print("\n--- 배너 스와이프 > 터치 > 소멸 확인 최종 시나리오 시작 ---")
    try:
        # ⭐️ 1. (중요) 테스트할 배너의 XPath를 여기에 정확하게 입력해주세요.
        banner_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[3]/android.view.View'

        # 2. 화면을 아래로 한 번 스크롤합니다.
        print("화면을 아래로 한 번 스크롤합니다.")
        scroll_down(flow_tester.driver)
        time.sleep(2)

        # 3. 스크롤 후 배너를 찾습니다.
        print(f"테스트할 배너를 찾습니다: '{banner_xpath}'")
        try:
            wait = WebDriverWait(flow_tester.driver, 10)
            banner_element = wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, banner_xpath))
            )
            print("✅ 배너를 찾았습니다.")
        except TimeoutException:
            error_msg = "실패: 스크롤 후 배너를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "banner_not_found_initial")
            return False, error_msg

        # 4. 배너를 왼쪽으로 1회 스와이프합니다.
        print("배너를 왼쪽으로 스와이프합니다.")
        rect = banner_element.rect
        start_x = rect['x'] + rect['width'] * 0.8
        end_x = rect['x'] + rect['width'] * 0.2
        y = rect['y'] + rect['height'] / 2
        flow_tester.driver.swipe(start_x, y, end_x, y, 500)
        time.sleep(2) # 스와이프 애니메이션 대기
        print("스와이프 동작을 완료했습니다.")

        # 5. 스와이프 후 배너를 다시 찾아 터치합니다.
        print(f"스와이프 후 배너를 다시 찾아 터치합니다: '{banner_xpath}'")
        try:
            # 스와이프 후에도 요소가 바로 클릭 가능하도록 명시적으로 기다려줍니다.
            wait = WebDriverWait(flow_tester.driver, 5)
            banner_to_touch = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, banner_xpath))
            )
            banner_to_touch.click()
            print("✅ 배너를 터치했습니다.")
            time.sleep(2) # 터치 후 UI 반응 대기
        except TimeoutException:
            error_msg = "실패: 스와이프 후 배너를 터치할 수 없거나 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "banner_not_clickable_after_swipe")
            return False, error_msg

        # 6. 터치 후 배너가 최종적으로 사라졌는지 확인합니다.
        print(f"터치 후 배너('{banner_xpath}')가 사라졌는지 최종 확인합니다...")
        try:
            wait = WebDriverWait(flow_tester.driver, 5)
            wait.until(
                EC.invisibility_of_element_located((AppiumBy.XPATH, banner_xpath))
            )
            print("✅ Pass: 배너가 성공적으로 사라졌습니다.")
            
            return True, "배너 스와이프, 터치, 소멸 확인 시나리오 성공."
        except TimeoutException:
            error_msg = "실패: 배너를 터치했지만 사라지지 않았습니다."
            save_screenshot_on_failure(flow_tester.driver, "banner_dismiss_fail_final")
            return False, error_msg

        print("✅ Pass: 배너가 확인 끝 뒤로 돌아갑니다.")
        flow_tester.driver.back()
        time.sleep(3)
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "banner_swipe_exception")
        return False, f"배너 스와이프 테스트 중 예외 발생: {e}"
    finally:
        print("--- 배너 스와이프 > 터치 > 소멸 확인 최종 시나리오 종료 ---")