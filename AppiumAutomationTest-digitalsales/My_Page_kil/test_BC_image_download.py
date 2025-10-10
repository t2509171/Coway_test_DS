# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


def test_image_card_download_with_permission_handling(flow_tester):
    """
    마이페이지 > 명함설정: 이미지 명함 다운로드 및 권한 팝업 처리 기능 확인
    """
    print("\n--- 이미지 명함 다운로드 (권한 처리 포함) 시나리오 시작 ---")

    # --- XPath 로케이터 정의 ---
    # 앱 내 요소
    download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'

    # 시스템 팝업 요소 (Android OS 기본 ID)
    dialog_message_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
    dialog_confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'

    # 시스템 권한 요청 팝업 요소 (Permission Controller)
    permission_allow_once_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
    permission_allow_all_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_all_button"]'

    # 최종 확인용 토스트 메시지
    toast_message_xpath = '//android.widget.Toast'

    try:
        wait = WebDriverWait(flow_tester.driver, 10)

        # 1. '명함 다운로드' 버튼 클릭
        print(f"'{download_button_xpath}' 버튼을 찾습니다...")
        download_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, download_button_xpath))
        )
        print("✅ 버튼을 찾았습니다. 클릭합니다.")
        download_button.click()

        # 2. 시스템 확인 팝업 대기 및 '확인' 클릭
        print(f"'{dialog_message_xpath}' 시스템 팝업 메시지를 확인합니다...")
        wait.until(EC.presence_of_element_located((AppiumBy.XPATH, dialog_message_xpath)))
        print("✅ 시스템 팝업이 나타났습니다. 확인 버튼을 클릭합니다.")

        confirm_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, dialog_confirm_button_xpath))
        )
        confirm_button.click()

        # 3. (선택적) '사진 및 동영상' 접근 권한 팝업 처리
        try:
            short_wait = WebDriverWait(flow_tester.driver, 1)
            print(f"'{permission_allow_once_button_xpath}' 권한 요청 팝업을 확인합니다...")
            allow_once_button = short_wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, permission_allow_once_button_xpath))
            )
            print("✅ 접근 권한 팝업이 나타났습니다. '허용' 버튼을 클릭합니다.")
            allow_once_button.click()
        except TimeoutException:
            print("INFO: '사진 및 동영상' 권한 팝업이 나타나지 않았습니다. 계속 진행합니다.")
            pass

        # 4. '모든 파일' 접근 권한 팝업 처리 (이 팝업은 나타날 수도, 안 나타날 수도 있음)
        # 이 단계는 유연하게 처리하기 위해 짧은 대기시간을 사용합니다.
        try:
            print(f"'{permission_allow_all_button_xpath}' 추가 권한 팝업을 확인합니다...")
            allow_all_button = WebDriverWait(flow_tester.driver, 1).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, permission_allow_all_button_xpath))
            )
            print("✅ 추가 권한 팝업이 나타났습니다. '모든 파일 허용' 버튼을 클릭합니다.")
            allow_all_button.click()
        except TimeoutException:
            # 5초 내에 팝업이 나타나지 않으면 이미 권한이 있거나 필요 없는 경우이므로 통과시킴
            print("INFO: '모든 파일 허용' 권한 팝업은 나타나지 않았습니다. 계속 진행합니다.")
            pass

        # 5. 최종 '저장되었습니다' 토스트 메시지 확인
        print("다운로드 완료 토스트 메시지를 확인합니다...")
        toast_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
        )

        message_text = toast_element.text
        if "저장되었습니다" in message_text:
            print(f"✅ 성공: 토스트 메시지 '{message_text}'가 노출되었습니다.")
            return True, "이미지 명함 다운로드 및 권한 처리 후 '저장' 알림 확인 성공"
        else:
            save_screenshot_on_failure(flow_tester.driver, "bc_image_download_toast_wrong_text")
            return False, f"실패: 예상과 다른 토스트 메시지 출력 - '{message_text}'"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_image_download_permission_fail")
        return False, f"실패: 다운로드 버튼 또는 시스템/권한 팝업을 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_image_download_unexpected_error")
        return False, f"실패: 이미지 명함 다운로드 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 이미지 명함 다운로드 (권한 처리 포함) 시나리오 종료 ---")