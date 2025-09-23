# -*- coding: utf-8 -*-
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from Utils.screenshot_helper import save_screenshot_on_failure

def test_order_status_visibility(flow_tester):
    """Seller app checklist-59: 마이페이지 - 주문현황 요소 노출 확인"""
    print("\n--- 마이페이지 주문현황 노출 확인 시나리오 시작 (checklist-59) ---")

    # 확인할 요소들의 XPath 정의
    xpaths_to_check = {
        "총주문": '//android.widget.TextView[@text="총주문"]',
        "순주문완료": '//android.widget.TextView[@text="순주문완료"]'
    }
    try:
        # 1. '주문현황' 탭 클릭 (좌표 기반)
        order_status_coords = (150, 310)
        print(f"'주문현황' 탭 위치인 {order_status_coords} 좌표를 클릭합니다.")
        try:
            flow_tester.driver.tap([order_status_coords])
            time.sleep(2)  # 탭 전환 애니메이션 대기
        except Exception as e:
            error_msg = f"실패: '주문현황' 탭 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "order_status_tap_failed")
            return False, error_msg
        missing_elements = []

        # 1. 정의된 XPath 목록을 순회하며 각 요소가 보이는지 확인
        for key, xpath in xpaths_to_check.items():
            print(f"'{key}' 텍스트의 노출을 확인합니다...")
            try:
                WebDriverWait(flow_tester.driver, 10).until(
                    EC.visibility_of_element_located((AppiumBy.XPATH, xpath))
                )
                print(f"✅ '{key}' 텍스트가 노출되었습니다.")
            except TimeoutException:
                print(f"❌ '{key}' 텍스트를 찾을 수 없습니다.")
                missing_elements.append(key)

        # 2. 결과 판정
        if not missing_elements:
            print("✅ 성공: '총주문', '순주문완료' 텍스트가 모두 정상적으로 노출됩니다.")
            return True, "마이페이지 주문현황 요소 노출 확인 성공"
        else:
            error_message = f"실패: 다음 요소가 노출되지 않았습니다 - {', '.join(missing_elements)}"
            save_screenshot_on_failure(flow_tester.driver, "order_status_visibility_fail")
            return False, error_message

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "order_status_visibility_error")
        return False, f"실패: 주문현황 확인 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 마이페이지 주문현황 노출 확인 시나리오 종료 ---")