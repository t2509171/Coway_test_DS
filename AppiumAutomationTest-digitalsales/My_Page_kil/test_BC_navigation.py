# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure

def test_business_card_navigation(flow_tester):
    """마이페이지 > 명함설정: 명함설정 버튼 선택 시 명함설정 페이지로 이동"""
    print("\n--- 명함설정 페이지 이동 시나리오 시작 ---")

    # 이 테스트는 '마이페이지'에 진입한 상태에서 시작한다고 가정합니다.
    business_card_button_xpath = '//android.widget.Button[@text="명함설정"]'
    # 명함설정 페이지의 대표적인 요소 '이미지 명함 다운로드' 버튼으로 이동을 확인
    page_verification_xpath = '//android.widget.Button[@text="이미지 명함 다운로드"]'

    try:
        # 1. '명함설정' 버튼 클릭
        print(f"'{business_card_button_xpath}' 버튼을 찾습니다...")
        business_card_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, business_card_button_xpath))
        )
        print("✅ 버튼을 찾았습니다. 클릭합니다.")
        business_card_button.click()
        time.sleep(3)

        # 2. 명함설정 페이지로 이동했는지 확인
        print(f"'{page_verification_xpath}' 요소를 통해 페이지 이동을 확인합니다...")
        WebDriverWait(flow_tester.driver, 15).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, page_verification_xpath))
        )
        print("✅ 성공: 명함설정 페이지로 정상적으로 이동했습니다.")
        return True, "명함설정 페이지 이동 성공"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_navigation_fail")
        return False, f"실패: 명함설정 페이지 이동 중 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_navigation_fail")
        return False, f"실패: 명함설정 페이지 이동 중 오류 발생: {e}"
    finally:
        print("--- 명함설정 페이지 이동 시나리오 종료 ---")