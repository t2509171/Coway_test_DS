# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


def test_image_card_download(flow_tester):
    """마이페이지 > 명함설정: 이미지 명함 다운로드 기능 확인"""
    print("\n--- 이미지 명함 다운로드 시나리오 시작 ---")

    download_button_xpath = '//android.widget.Button[@text="이미지 명함 다운로드"]'
    # 안드로이드의 기본 토스트 메시지 XPath
    toast_message_xpath = '//android.widget.Toast'

    try:
        # 1. '이미지 명함 다운로드' 버튼 클릭
        print(f"'{download_button_xpath}' 버튼을 찾습니다...")
        download_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, download_button_xpath))
        )
        print("✅ 버튼을 찾았습니다. 클릭합니다.")
        download_button.click()

        # 2. '저장되었습니다' 토스트 메시지가 나타나는지 확인
        print("다운로드 완료 토스트 메시지를 확인합니다...")
        toast_element = WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
        )

        message_text = toast_element.text
        if "저장되었습니다" in message_text:
            print(f"✅ 성공: 토스트 메시지 '{message_text}'가 노출되었습니다.")
            return True, "이미지 명함 다운로드 및 '저장' 알림 확인 성공"
        else:
            save_screenshot_on_failure(flow_tester.driver, "bc_image_download_toast_wrong_text")
            return False, f"실패: 예상과 다른 토스트 메시지 출력 - '{message_text}'"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_image_download_fail")
        return False, f"실패: 다운로드 버튼 또는 토스트 메시지를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_image_download_fail")
        return False, f"실패: 이미지 명함 다운로드 중 오류 발생: {e}"
    finally:
        print("--- 이미지 명함 다운로드 시나리오 종료 ---")