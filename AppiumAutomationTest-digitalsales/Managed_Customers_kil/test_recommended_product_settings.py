import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utils.screenshot_helper import save_screenshot_on_failure

def test_navigate_to_recommended_product_settings(flow_tester):
    """
    지정된 좌표를 클릭하여 '관리고객 추천 제품 설정' 화면으로 이동하는지 검증합니다.
    """
    print("\n--- '관리고객 추천 제품 설정' 화면 이동 확인 시나리오 시작 ---")
    try:
        time.sleep(2)  # 화면 전환 대기
        # 1. 지정된 좌표 (943, 1426) 클릭
        coords_to_tap = (943, 1426)
        print(f"지정된 좌표 {coords_to_tap}를 클릭합니다.")
        try:
            flow_tester.driver.tap([coords_to_tap])
            time.sleep(2) # 화면 전환 대기
        except Exception as e:
            error_msg = f"실패: 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "settings_coords_tap_failed")
            return False, error_msg

        # 2. '관리고객 추천 제품 설정' 타이틀 노출 확인
        title_xpath = '//android.widget.TextView[@text="관리고객 추천 제품 설정"]'
        print(f"'{title_xpath}' (화면 타이틀)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, title_xpath))
            )
            print("✅ '관리고객 추천 제품 설정' 화면으로 성공적으로 이동했습니다.")

            flow_tester.driver.back()
            time.sleep(2) # 화면 전환 대기
            return True, "'관리고객 추천 제품 설정' 화면 이동 성공."
        except TimeoutException:
            error_msg = "실패: 좌표 클릭 후 '관리고객 추천 제품 설정' 타이틀을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "recommended_product_settings_title_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"추천 제품 설정 화면 이동 중 예외 발생: {e}"
    finally:
        print("--- '관리고객 추천 제품 설정' 화면 이동 확인 시나리오 종료 ---")