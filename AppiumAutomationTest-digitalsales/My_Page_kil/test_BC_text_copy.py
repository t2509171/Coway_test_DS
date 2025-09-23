# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


def test_text_card_copy(flow_tester):
    """마이페이지 > 명함설정: 텍스트 명함 클립보드 복사 기능 확인"""
    print("\n--- 텍스트 명함 복사 시나리오 시작 ---")

    copy_button_xpath = '//android.widget.Button[@text="텍스트 명함 복사"]'
    # 안드로이드의 기본 토스트 메시지 XPath
    toast_message_xpath = '//android.widget.Toast'

    try:
        # 1. '텍스트 명함 복사' 버튼 클릭
        print(f"'{copy_button_xpath}' 버튼을 찾습니다...")
        copy_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, copy_button_xpath))
        )
        print("✅ 버튼을 찾았습니다. 클릭합니다.")
        copy_button.click()

        # 2. '복사되었습니다' 토스트 메시지가 나타나는지 확인
        print("복사 완료 토스트 메시지를 확인합니다...")
        toast_element = WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
        )

        message_text = toast_element.text
        if "복사되었습니다" in message_text or "클립보드에 복사" in message_text:
            print(f"✅ 성공: 토스트 메시지 '{message_text}'가 노출되었습니다.")
            return True, "텍스트 명함 복사 및 '복사' 알림 확인 성공"
        else:
            save_screenshot_on_failure(flow_tester.driver, "bc_text_copy_toast_wrong_text")
            return False, f"실패: 예상과 다른 토스트 메시지 출력 - '{message_text}'"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_text_copy_fail")
        return False, f"실패: 복사 버튼 또는 토스트 메시지를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_text_copy_fail")
        return False, f"실패: 텍스트 명함 복사 중 오류 발생: {e}"
    finally:
        print("--- 텍스트 명함 복사 시나리오 종료 ---")