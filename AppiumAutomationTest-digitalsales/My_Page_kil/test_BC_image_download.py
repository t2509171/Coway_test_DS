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
    이미지 명함 다운로드 시, WebDriverWait를 사용하여 토스트 메시지를 우선 확인하고
    없을 경우에만 권한 팝업을 처리한 뒤 다시 토스트 메시지를 확인하는 시나리오입니다.
    """
    print("\n--- 이미지 명함 다운로드 (WebDriverWait 분기 처리) 시나리오 시작 ---")

    # --- XPath 로케이터 정의 ---
    download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'
    dialog_confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
    permission_allow_once_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
    permission_allow_all_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_all_button"]'

    # ⭐️ 토스트 메시지 XPath를 여기에 정의합니다.
    toast_message_xpath = '//android.widget.Toast'

    try:
        wait = WebDriverWait(flow_tester.driver, 10)

        # 1. '명함 다운로드' 버튼 클릭
        print(f"'{download_button_xpath}' 버튼을 클릭합니다.")
        download_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, download_button_xpath))
        )
        download_button.click()

        # 2. 시스템 확인 팝업 대기 및 '확인' 클릭
        print("시스템 팝업의 '확인' 버튼을 클릭합니다.")
        confirm_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, dialog_confirm_button_xpath))
        )
        confirm_button.click()

        # --- ✨ 로직 수정 시작 ✨ ---
        # 3. [1차] WebDriverWait를 사용한 토스트 메시지 확인 (짧은 대기)
        print("\n[1차 확인] 시스템 팝업 확인 후 토스트 메시지가 즉시 나타나는지 확인합니다...")
        try:
            # WebDriverWait는 토스트가 나타날 때까지 최대 1초간 기다립니다.
            toast_element = WebDriverWait(flow_tester.driver, 1).until(
                EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
            )
            toast_text = toast_element.text
            print(f"✅ 1차 확인에서 토스트 메시지를 발견했습니다: '{toast_text}'")
            return True, f"성공: 토스트 메시지 '{toast_text}'를 확인했습니다."
        except TimeoutException:
            # 3초 내에 토스트가 나타나지 않으면 TimeoutException이 발생합니다.
            print("\nINFO: 1차 확인에서 토스트가 없어, 권한 팝업 처리 로직을 시작합니다.")
            pass # 예외를 잡고 다음 단계로 넘어갑니다.
        # 4. [1차 실패 시] 권한 팝업 처리 진행
        try:
            short_wait = WebDriverWait(flow_tester.driver, 1)
            print(f"'{permission_allow_once_button_xpath}' 권한 요청 팝업을 확인합니다...")
            allow_once_button = short_wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, permission_allow_once_button_xpath))
            )
            print("✅ 접근 권한 팝업이 나타났습니다. '허용' 버튼을 클릭합니다.")
            allow_once_button.click()
            time.sleep(1)
        except TimeoutException:
            print("INFO: '사진 및 동영상' 권한 팝업이 나타나지 않았습니다.")
            pass

        try:
            # 권한 처리 및 다운로드 시간을 고려하여 최대 15초간 기다립니다.
            toast_element = WebDriverWait(flow_tester.driver, 1).until(
                EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
            )
            toast_text = toast_element.text
            print(f"✅ 2차 확인에서 토스트 메시지를 발견했습니다: '{toast_text}'")
            return True, f"성공: 토스트 메시지 '{toast_text}'를 확인했습니다."
        except TimeoutException:
            pass
        #4. '모든 파일' 접근 권한 팝업 처리 (이 팝업은 나타날 수도, 안 나타날 수도 있음)
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

        # 5. [2차] 권한 처리 후 WebDriverWait를 사용한 최종 토스트 메시지 확인
        print("\n[2차 확인] 권한 팝업 처리 후 최종 토스트 메시지를 확인합니다...")
        try:
            # 권한 처리 및 다운로드 시간을 고려하여 최대 15초간 기다립니다.
            toast_element = WebDriverWait(flow_tester.driver, 3).until(
                EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
            )
            toast_text = toast_element.text
            print(f"✅ 2차 확인에서 토스트 메시지를 발견했습니다: '{toast_text}'")
            return True, f"성공: 토스트 메시지 '{toast_text}'를 확인했습니다."
        except TimeoutException:
            error_msg = "실패: 권한 처리 후에도 최종 토스트 메시지를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "final_toast_not_found")
            return False, error_msg
        # --- ✨ 로직 수정 종료 ✨ ---

    except (TimeoutException, NoSuchElementException) as e:
        error_msg = f"실패: 다운로드 버튼 또는 시스템/권한 팝업을 찾지 못했습니다. - {e}"
        save_screenshot_on_failure(flow_tester.driver, "bc_download_element_not_found")
        return False, error_msg
    except Exception as e:
        error_msg = f"실패: 이미지 명함 다운로드 중 예상치 못한 오류 발생: {e}"
        save_screenshot_on_failure(flow_tester.driver, "bc_download_unexpected_error")
        return False, error_msg
    finally:
        print("--- 이미지 명함 다운로드 (분기 처리) 시나리오 종료 ---")