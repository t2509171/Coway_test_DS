import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utils.screenshot_helper import save_screenshot_on_failure

def test_verify_greeting_message_in_menu(flow_tester):
    """
    전체 메뉴를 열고 "안녕하세요. 무엇을 도와드릴까요?" 버튼이 노출되는지 검증합니다.
    """
    print("\n--- 전체 메뉴 > 인사말 버튼 노출 확인 시나리오 시작 ---")
    try:
        # 1. '전체메뉴' 버튼 클릭
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        print(f"'{menu_button_xpath}' (전체메뉴) 버튼을 클릭합니다.")
        try:
            menu_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, menu_button_xpath))
            )
            menu_button.click()
            time.sleep(2)  # 메뉴가 열리는 애니메이션을 기다립니다.
        except TimeoutException:
            error_msg = "실패: '전체메뉴' 버튼을 찾거나 클릭할 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "greeting_menu_button_not_found")
            return False, error_msg

        # 2. "안녕하세요. 무엇을 도와드릴까요?" 버튼 노출 확인
        greeting_button_xpath = '//android.widget.Button[@text="안녕하세요. 무엇을 도와드릴까요?"]'
        print(f"'{greeting_button_xpath}' 버튼이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, greeting_button_xpath))
            )
            print("✅ 인사말 버튼이 성공적으로 노출되었습니다.")

            # 3. 사이드 메뉴 내 특정 버튼 클릭
            sidenav_button_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
            print(f"'{sidenav_button_xpath}' 버튼을 클릭합니다.")
            try:
                sidenav_button = WebDriverWait(flow_tester.driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, sidenav_button_xpath))
                )
                sidenav_button.click()
                print("✅ 사이드 메뉴 버튼을 성공적으로 클릭했습니다.")
            except TimeoutException:
                error_msg = "실패: 사이드 메뉴 버튼을 찾거나 클릭할 수 없습니다."
                save_screenshot_on_failure(flow_tester.driver, "sidenav_button_not_found")
                return False, error_msg
            # --- 로직 추가 종료 ---

            return True, "전체 메뉴 내 인사말 버튼 확인 성공."

        except TimeoutException:
            error_msg = "실패: 전체 메뉴에서 인사말 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "greeting_message_button_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"인사말 버튼 확인 중 예외 발생: {e}"
    finally:
        print("--- 전체 메뉴 > 인사말 버튼 노출 확인 시나리오 종료 ---")