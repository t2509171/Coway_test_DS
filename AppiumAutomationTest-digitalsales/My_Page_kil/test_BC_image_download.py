# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.tost_message import watch_for_any_toast


# def test_image_card_download_with_permission_handling(flow_tester):
#     """
#     마이페이지 > 명함설정: 이미지 명함 다운로드 및 권한 팝업 처리 기능 확인
#     """
#     print("\n--- 이미지 명함 다운로드 (권한 처리 포함) 시나리오 시작 ---")
#
#     # --- XPath 로케이터 정의 ---
#     # 앱 내 요소
#     download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'
#
#     # 시스템 팝업 요소 (Android OS 기본 ID)
#     dialog_message_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
#     dialog_confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
#
#     # 시스템 권한 요청 팝업 요소 (Permission Controller)
#     permission_allow_once_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
#     permission_allow_all_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_all_button"]'
#
#     # 최종 확인용 토스트 메시지
#     toast_message_xpath = '//android.widget.Toast'
#
#     try:
#         wait = WebDriverWait(flow_tester.driver, 10)
#
#         # 1. '명함 다운로드' 버튼 클릭
#         print(f"'{download_button_xpath}' 버튼을 찾습니다...")
#         download_button = wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, download_button_xpath))
#         )
#         print("✅ 버튼을 찾았습니다. 클릭합니다.")
#         download_button.click()
#
#
#         # 2. 시스템 확인 팝업 대기 및 '확인' 클릭
#         print(f"'{dialog_message_xpath}' 시스템 팝업 메시지를 확인합니다...")
#         wait.until(EC.presence_of_element_located((AppiumBy.XPATH, dialog_message_xpath)))
#         print("✅ 시스템 팝업이 나타났습니다. 확인 버튼을 클릭합니다.")
#
#         confirm_button = wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, dialog_confirm_button_xpath))
#         )
#         confirm_button.click()
#
#         # 3. (선택적) '사진 및 동영상' 접근 권한 팝업 처리
#         try:
#             short_wait = WebDriverWait(flow_tester.driver, 1)
#             print(f"'{permission_allow_once_button_xpath}' 권한 요청 팝업을 확인합니다...")
#             allow_once_button = short_wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, permission_allow_once_button_xpath))
#             )
#             print("✅ 접근 권한 팝업이 나타났습니다. '허용' 버튼을 클릭합니다.")
#             allow_once_button.click()
#         except TimeoutException:
#             print("INFO: '사진 및 동영상' 권한 팝업이 나타나지 않았습니다. 계속 진행합니다.")
#             pass
#
#         # 4. '모든 파일' 접근 권한 팝업 처리 (이 팝업은 나타날 수도, 안 나타날 수도 있음)
#         # 이 단계는 유연하게 처리하기 위해 짧은 대기시간을 사용합니다.
#         try:
#             print(f"'{permission_allow_all_button_xpath}' 추가 권한 팝업을 확인합니다...")
#             allow_all_button = WebDriverWait(flow_tester.driver, 1).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, permission_allow_all_button_xpath))
#             )
#             print("✅ 추가 권한 팝업이 나타났습니다. '모든 파일 허용' 버튼을 클릭합니다.")
#             allow_all_button.click()
#         except TimeoutException:
#             # 5초 내에 팝업이 나타나지 않으면 이미 권한이 있거나 필요 없는 경우이므로 통과시킴
#             print("INFO: '모든 파일 허용' 권한 팝업은 나타나지 않았습니다. 계속 진행합니다.")
#             pass
#         # 5. 최종 토스트 메시지 출현을 지속적으로 감시
#         is_toast_found, result_message = watch_for_any_toast(flow_tester, max_wait_seconds=30)
#
#         return is_toast_found, result_message
#
#     except (TimeoutException, NoSuchElementException) as e:
#         save_screenshot_on_failure(flow_tester.driver, "bc_image_download_permission_fail")
#         return False, f"실패: 다운로드 버튼 또는 시스템/권한 팝업을 찾지 못했습니다. - {e}"
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "bc_image_download_unexpected_error")
#         return False, f"실패: 이미지 명함 다운로드 중 예상치 못한 오류 발생: {e}"
#     finally:
#         print("--- 이미지 명함 다운로드 (권한 처리 포함) 시나리오 종료 ---")


def test_image_card_download_with_permission_handling(flow_tester):
    """
    마이페이지 > 명함설정: 다운로드 클릭 후 나타나는 모든 팝업과 토스트 메시지를
    하나의 감시 루프 안에서 동적으로 감지하고 처리합니다.
    """
    print("\n--- 이미지 명함 다운로드 (동적 감지 및 처리) 시나리오 시작 ---")

    # --- XPath 로케이터 정의 ---
    download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'

    # 처리해야 할 가능성이 있는 모든 팝업 버튼 정의
    popups_to_handle = {
        "SYSTEM_CONFIRM": '//android.widget.Button[@resource-id="android:id/button1"]',
        "PERMISSION_ALLOW_ONCE": '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]',
        "PERMISSION_ALLOW_ALL": '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_all_button"]',
    }

    # 최종 성공 조건인 토스트 메시지
    toast_message_xpath = '//android.widget.Toast'

    try:
        # 1. '명함 다운로드' 버튼을 찾아 클릭
        print(f"'{download_button_xpath}' 버튼을 찾습니다...")
        download_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, download_button_xpath))
        )
        print("✅ 버튼을 찾았습니다. 즉시 클릭하고 감시를 시작합니다.")
        download_button.click()

        # 2. 감시 루프 시작 (최대 30초간 실행)
        start_time = time.time()
        max_wait_seconds = 30
        download_complete = False

        while time.time() - start_time < max_wait_seconds:
            try:
                # 2-1. [최우선] 최종 성공 조건인 토스트 메시지를 1초간 확인
                WebDriverWait(flow_tester.driver, 1).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
                )
                print("✅ 성공: 최종 확인 토스트 메시지가 화면에 노출되었습니다.")
                download_complete = True
                break  # 성공했으므로 루프 탈출

            except TimeoutException:
                # 토스트가 없으면 다른 팝업들을 확인
                pass

            popup_handled = False
            for popup_name, popup_xpath in popups_to_handle.items():
                try:
                    # 2-2. 처리해야 할 팝업 버튼이 있는지 1초간 확인
                    popup_button = WebDriverWait(flow_tester.driver, 1).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, popup_xpath))
                    )
                    print(f"INFO: '{popup_name}' 팝업을 감지했습니다. 즉시 클릭합니다.")
                    popup_button.click()
                    popup_handled = True
                    # 팝업을 처리했으면, 다음 팝업을 기다리기 위해 루프의 처음으로 돌아감
                    break
                except TimeoutException:
                    # 해당 팝업이 없으면 다음 팝업 확인
                    continue

            if popup_handled:
                # 팝업을 처리했다면, 다음 상태를 즉시 확인하기 위해 루프 처음으로
                continue

            # 아무런 요소도 발견되지 않으면 1초 대기
            print(f"감시 중... (경과 시간: {int(time.time() - start_time)}초)")
            time.sleep(1)

        # 3. 최종 결과 반환
        if download_complete:
            return True, "이미지 명함 다운로드 및 모든 팝업 처리 후 최종 확인 성공"
        else:
            failure_message = f"실패: {max_wait_seconds}초 내에 최종 확인(토스트 메시지)이 이루어지지 않았습니다."
            save_screenshot_on_failure(flow_tester.driver, "bc_download_timeout")
            return False, failure_message

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_download_unexpected_error")
        return False, f"실패: 이미지 명함 다운로드 시나리오 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 이미지 명함 다운로드 (동적 감지 및 처리) 시나리오 종료 ---")