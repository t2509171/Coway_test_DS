import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utils.screenshot_helper import save_screenshot_on_failure

def test_verify_home_button_visibility(flow_tester):
    """
    홈 화면의 특정 버튼이 노출되는지 검증합니다.
    """
    print("\n--- 홈 화면 > 특정 버튼 노출 확인 시나리오 시작 ---")
    try:
        # ※ 사전 조건: 앱 실행 후 홈 화면에 진입한 상태

        # 1. 확인할 버튼의 XPath 정의
        home_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
        print(f"홈 화면에서 버튼({home_button_xpath})이 노출되는지 확인합니다.")

        # 2. 버튼이 화면에 나타나는지 최대 15초간 대기
        try:
            WebDriverWait(flow_tester.driver, 15).until(
                EC.presence_of_element_located((AppiumBy.XPATH, home_button_xpath))
            )
            print("✅ 버튼이 성공적으로 노출되었습니다.")
            return True, "홈 화면 버튼 노출 확인 성공."
        except TimeoutException:
            error_msg = f"실패: 홈 화면에서 버튼을 찾을 수 없습니다. (XPath: {home_button_xpath})"
            save_screenshot_on_failure(flow_tester.driver, "home_button_not_visible")
            return False, error_msg

    except Exception as e:
        return False, f"홈 화면 버튼 확인 중 예외 발생: {e}"
    finally:
        print("--- 홈 화면 > 특정 버튼 노출 확인 시나리오 종료 ---")