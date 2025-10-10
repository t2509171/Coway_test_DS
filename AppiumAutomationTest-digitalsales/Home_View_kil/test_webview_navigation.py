import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utils.screenshot_helper import save_screenshot_on_failure

def test_navigate_to_webview_from_home(flow_tester):
    """
    홈 화면의 특정 버튼을 클릭하여 WebView가 노출되는지 검증합니다.
    """
    print("\n--- 홈 화면 > 버튼 클릭 > WebView 노출 확인 시나리오 시작 ---")
    try:
        # 1. 홈 화면의 버튼 클릭
        home_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
        print(f"홈 화면의 버튼({home_button_xpath})을 클릭합니다.")
        try:
            # 요소가 클릭 가능한 상태가 될 때까지 최대 10초간 기다립니다.
            button_to_click = WebDriverWait(flow_tester.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
            )
            button_to_click.click()
        except TimeoutException:
            error_msg = f"실패: 홈 화면에서 버튼을 찾을 수 없습니다. (XPath: {home_button_xpath})"
            save_screenshot_on_failure(flow_tester.driver, "home_webview_button_not_found")
            return False, error_msg

        # 2. WebView가 노출되었는지 확인
        webview_xpath = '//android.webkit.WebView[@text="Seller AI"]'
        print(f"'{webview_xpath}' (WebView)가 노출되는지 확인합니다 (20초 대기).")
        try:
            # WebView는 로딩이 느릴 수 있으므로 대기 시간을 20초로 넉넉하게 설정합니다.
            WebDriverWait(flow_tester.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, webview_xpath))
            )
            print("✅ WebView가 성공적으로 노출되었습니다.")

            time.sleep(2)
            # flow_tester.driver.back()
            # time.sleep(3)
            return True, "홈 화면 버튼 클릭 후 WebView 이동 성공."

        except TimeoutException:
            error_msg = "실패: 버튼 클릭 후 WebView를 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "webview_not_found_after_click")
            return False, error_msg

    except Exception as e:
        return False, f"WebView 이동 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 화면 > 버튼 클릭 > WebView 노출 확인 시나리오 종료 ---")