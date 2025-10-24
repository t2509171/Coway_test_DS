import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure


def test_verify_update_alert(flow_tester):
    """
    앱 실행 시 '설치 권한' 얼럿을 먼저 처리한 후, '업데이트' 얼럿이 노출되는지와 텍스트를 검증합니다.
    """

    print("\n--- 앱 실행 시 업데이트 관련 얼럿 전체 시나리오 시작 ---")
    try:

        # ======================================================================
        # 1단계 (선택적): '설치 권한' 관련 얼럿 확인 및 처리
        # ======================================================================
        print("\n[1단계] '설치 권한' 얼럿이 있는지 먼저 확인합니다 (5초 대기).")
        try:
            # 권한 얼럿이 있는지 5초만 기다려봄
            permission_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
            alert_element = WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, permission_alert_msg_xpath))
            )

            # 얼럿이 있다면, 텍스트 내용을 확인하여 '설치 권한' 관련 얼럿이 맞는지 검사
            alert_text = alert_element.text
            if "설정으로 이동하여 설치 권한" in alert_text:
                print(f"✅ '설치 권한' 얼럿을 발견했습니다. 권한 설정 로직을 시작합니다.")
                print(f" - 얼럿 내용: '{alert_text}'")

                # 1-1. [설정] 또는 [확인] 버튼 클릭
                confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
                confirm_button = flow_tester.driver.find_element(AppiumBy.XPATH, confirm_button_xpath)
                confirm_button.click()
                print(" - '확인' 버튼을 클릭하여 설정 화면으로 이동합니다.")
                time.sleep(2)  # 화면 전환 대기

                # 1-2. 스위치 터치
                switch_xpath = '//android.widget.Switch[@resource-id="android:id/switch_widget"]'
                switch_element = WebDriverWait(flow_tester.driver, 10).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, switch_xpath))
                )
                switch_element.click()
                print(" - '이 출처 허용' 스위치를 ON으로 변경했습니다.")
                time.sleep(1)

                # 1-3. 뒤로가기
                flow_tester.driver.back()
                print(" - 뒤로가기를 실행하여 이전 화면으로 복귀합니다.")
                time.sleep(2)  # 화면 전환 대기
            else:
                # 찾은 얼럿이 '설치 권한' 관련이 아닌 경우 (예: 메인 업데이트 얼럿)
                print(" - '설치 권한'이 아닌 다른 얼럿이 먼저 노출되었습니다. 다음 단계를 진행합니다.")

        except TimeoutException:
            # 5초 내에 어떤 얼럿도 나타나지 않으면, 권한이 이미 설정된 것으로 간주
            print(" - '설치 권한' 얼럿이 없습니다. 권한이 이미 허용된 상태로 보입니다.")
            pass  # 에러가 아니라 정상 상황이므로 그냥 넘어감

        # ======================================================================
        # 2단계 (필수): 메인 '업데이트' 얼럿 확인 및 텍스트 검증
        # ======================================================================
        print("\n[2단계] 메인 '업데이트' 얼럿이 노출되는지 확인합니다 (10초 대기).")
        update_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
        expected_text = "업데이트가 있습니다. 앱을 이용하시려면 최신 버전으로 업데이트 해주세요."
        try:
            alert_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, update_alert_msg_xpath))
            )
            print("✅ 메인 업데이트 얼럿이 성공적으로 노출되었습니다.")

            actual_text = alert_element.text
            print(f" - 실제 얼럿 텍스트: '{actual_text}'")

            if expected_text in actual_text:
                print("✅ 얼럿의 텍스트 내용이 예상과 일치합니다.")
                return True, "업데이트 얼럿 노출 및 텍스트 검증 성공."
            else:
                error_msg = f"실패: 얼럿의 텍스트가 예상과 다릅니다.\n - 예상: {expected_text}\n - 실제: {actual_text}"
                save_screenshot_on_failure(flow_tester.driver, "update_alert_wrong_text")
                return False, error_msg

        except TimeoutException:
            error_msg = "실패: 메인 업데이트 얼럿이 노출되지 않았습니다. 앱이 최신버전일 수 있습니다."
            save_screenshot_on_failure(flow_tester.driver, "update_alert_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"업데이트 얼럿 확인 중 예외 발생: {e}"
    finally:
        print("--- 앱 실행 시 업데이트 관련 얼럿 전체 시나리오 종료 ---")


# test_verify_update_alert 함수는 그대로 두고 아래 함수를 추가합니다.

def test_perform_app_update(flow_tester):
    """
    업데이트 얼럿의 '확인' 버튼을 누른 후, 앱 업데이트 설치 과정을 검증합니다.
    """
    print("\n--- 앱 업데이트 설치 및 실행 확인 시나리오 시작 ---")
    try:
        # ※ 사전 조건: 'test_verify_update_alert'가 성공하여 업데이트 얼럿이 떠 있는 상태

        confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'

        # 1. 업데이트 얼럿의 [확인] 버튼 클릭
        print("1단계: 업데이트 얼럿의 '확인' 버튼을 클릭합니다.")
        try:
            confirm_button1 = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, confirm_button_xpath))
            )
            confirm_button1.click()
            time.sleep(1)
        except TimeoutException:
            error_msg = "실패: 업데이트 얼럿의 '확인' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "update_alert_confirm_btn_not_found")
            return False, error_msg

        # 2. '출처를 알 수 없는 앱' 관련 [설정] 또는 [확인] 버튼 클릭
        print("2단계: '출처를 알 수 없는 앱' 관련 '확인' 버튼을 클릭합니다.")
        try:
            confirm_button2 = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, confirm_button_xpath))
            )
            confirm_button2.click()
        except TimeoutException:
            error_msg = "실패: '출처를 알 수 없는 앱' 관련 '확인' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "unknown_source_confirm_btn_not_found")
            return False, error_msg

        # 3. '알림 허용' 화면 확인 및 스위치 토글
        allow_notification_switch_xpath = '//android.widget.Switch[@content-desc="알림 허용"]'
        print(f"3단계: '{allow_notification_switch_xpath}' (알림 허용) 화면을 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, allow_notification_switch_xpath))
            )
            print("✅ '알림 허용' 화면이 확인되었습니다. 스위치를 클릭합니다.")

            switch_widget_xpath = '//android.widget.Switch[@content-desc="알림 허용"]'
            switch_widget = flow_tester.driver.find_element(AppiumBy.XPATH, switch_widget_xpath)
            switch_widget.click()

            print("뒤로가기를 실행합니다.")
            flow_tester.driver.back()
            time.sleep(1)
        except TimeoutException:
            error_msg = "실패: '알림 허용' 화면 또는 스위치를 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "allow_notification_screen_not_found")
            return False, error_msg

        # 4. 패키지 설치 화면 확인 및 '업데이트' 버튼 클릭
        install_confirm_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_confirm_question_update"]'
        print(f"4단계: '{install_confirm_xpath}' (설치 확인 문구)가 노출되는지 확인합니다.")
        try:
            time.sleep(5)
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, install_confirm_xpath))
            )
            print("✅ 설치 확인 화면이 확인되었습니다. '업데이트' 버튼을 클릭합니다.")
            update_button = flow_tester.driver.find_element(AppiumBy.XPATH,
                                                            confirm_button_xpath)  # '업데이트' 버튼도 동일한 ID를 사용
            update_button.click()
        except TimeoutException:
            error_msg = "실패: 앱 설치 확인 화면을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "install_confirm_screen_not_found")
            return False, error_msg

        # 5. 설치 완료 대기 및 확인
        install_success_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_success"]'
        print(f"5단계: '{install_success_xpath}' (설치 완료) 메시지가 나타날 때까지 대기합니다. (최대 2분)")
        try:
            # 앱 설치는 시간이 오래 걸릴 수 있으므로 대기 시간을 120초(2분)로 길게 설정
            WebDriverWait(flow_tester.driver, 120).until(
                EC.presence_of_element_located((AppiumBy.XPATH, install_success_xpath))
            )
            print("✅ 앱이 성공적으로 업데이트되었습니다. '열기' 버튼을 클릭합니다.")
            open_button = flow_tester.driver.find_element(AppiumBy.XPATH, confirm_button_xpath)  # '열기' 버튼도 동일한 ID를 사용
            open_button.click()
        except TimeoutException:
            error_msg = "실패: 2분 내에 앱 설치가 완료되지 않았습니다."
            save_screenshot_on_failure(flow_tester.driver, "update_installation_failed")
            return False, error_msg

        # 6. 앱 정상 실행 확인 (로그인 화면의 특정 요소로 확인)
        print("6단계: 업데이트 후 앱이 정상적으로 실행되었는지 확인합니다.")
        try:
            # 로그인 화면의 '아이디' 입력 필드와 같은 확실한 요소로 실행 여부를 확인
            login_id_field_xpath = '//android.webkit.WebView[@text="Coway"]'
            WebDriverWait(flow_tester.driver, 20).until(
                EC.presence_of_element_located((AppiumBy.XPATH, login_id_field_xpath))
            )
            print("✅ 업데이트된 앱이 성공적으로 실행되었습니다.")
        except TimeoutException:
            error_msg = "실패: '열기' 버튼 클릭 후 앱이 정상적으로 실행되지 않았습니다."
            save_screenshot_on_failure(flow_tester.driver, "app_launch_failed_after_update")
            return False, error_msg

        return True, "앱 업데이트 전체 과정 검증 성공."

    except Exception as e:
        return False, f"앱 업데이트 과정 중 예상치 못한 예외 발생: {e}"
    finally:
        print("--- 앱 업데이트 설치 및 실행 확인 시나리오 종료 ---")



