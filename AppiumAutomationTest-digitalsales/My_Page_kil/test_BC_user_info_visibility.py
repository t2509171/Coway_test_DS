# -*- coding: utf-8 -*-

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from Utils.screenshot_helper import save_screenshot_on_failure

def test_user_info_visibility(flow_tester):
    """마이페이지 > 명함설정: 사용자명, 직함, 소속, 연락처 노출 확인"""
    print("\n--- 명함설정 사용자 정보 노출 확인 시나리오 시작 ---")

    # 각 정보 필드를 대표하는 XPath (실제 앱의 구조에 맞게 조정 필요)
    # 예시: '사용자명'이라는 TextView와 그 값을 포함하는 형제 View를 찾는 방식
    info_xpaths = {
        "사용자명": '//android.widget.TextView[@text="사용자명"]/following-sibling::android.view.View',
        "직함": '//android.widget.TextView[@text="직함"]/following-sibling::android.view.View',
        "소속": '//android.widget.TextView[@text="소속"]/following-sibling::android.view.View',
        "연락처": '//android.widget.TextView[@text="연락처"]/following-sibling::android.view.View'
    }

    try:
        all_info_visible = True
        missing_elements = []

        # 1. 각 정보 필드가 존재하는지 순차적으로 확인
        for field, xpath in info_xpaths.items():
            print(f"'{field}' 정보가 노출되는지 확인합니다...")
            try:
                WebDriverWait(flow_tester.driver, 5).until(
                    EC.visibility_of_element_located((AppiumBy.XPATH, xpath))
                )
                print(f"✅ '{field}' 정보가 노출됩니다.")
            except TimeoutException:
                print(f"❌ 실패: '{field}' 정보를 찾을 수 없습니다.")
                all_info_visible = False
                missing_elements.append(field)

        # 2. 최종 결과 반환
        if all_info_visible:
            return True, "모든 사용자 정보(이름, 직함, 소속, 연락처)가 정상 노출됩니다."
        else:
            save_screenshot_on_failure(flow_tester.driver, "bc_user_info_missing")
            return False, f"실패: 다음 정보가 누락되었습니다 - {', '.join(missing_elements)}"

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_user_info_failure")
        return False, f"실패: 사용자 정보 확인 중 오류 발생: {e}"
    finally:
        print("--- 명함설정 사용자 정보 노출 확인 시나리오 종료 ---")