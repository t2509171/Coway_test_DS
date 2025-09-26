import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utils.screenshot_helper import save_screenshot_on_failure


def test_cody_secretary_keyboard_and_input(flow_tester):
    """
    코디비서 화면의 입력 필드를 터치했을 때, 키패드가 노출되고 텍스트 입력이 가능한지 검증합니다.
    """
    print("\n--- 코디비서 > 입력 필드 터치 및 키패드 노출, 텍스트 입력 확인 시나리오 시작 ---")
    try:
        # ※ 사전 조건: 코디비서 화면에 진입한 상태
        # TODO: 코디비서 화면으로 진입하는 코드를 이 부분에 추가하거나, 테스트 실행 파일에서 미리 호출해야 합니다.
        # 예: flow_tester.driver.find_element(AppiumBy.XPATH, '코디비서_아이콘_XPATH').click()
        # time.sleep(2)

        # 1. 하단 입력 필드 찾기 및 클릭
        # TODO: 아래 input_field_xpath 변수에 실제 입력 필드의 XPath를 입력하세요.
        input_field_xpath = '//android.widget.EditText[@resource-id="txtBotMessage"]'
        print(f"'{input_field_xpath}' (입력 필드)를 클릭하여 키패드를 활성화합니다.")
        try:
            input_field = WebDriverWait(flow_tester.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, input_field_xpath))
            )
            input_field.click()
            time.sleep(1)  # 키패드가 올라올 시간을 기다립니다.
        except TimeoutException:
            error_msg = "실패: 코디비서 입력 필드를 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "cody_secretary_input_field_not_found")
            return False, error_msg

        # 2. 키패드가 노출되었는지 확인
        print("키패드가 노출되었는지 확인합니다.")
        if flow_tester.driver.is_keyboard_shown():
            print("✅ 키패드가 성공적으로 노출되었습니다.")
        else:
            error_msg = "실패: 입력 필드를 클릭했지만 키패드가 노출되지 않았습니다."
            save_screenshot_on_failure(flow_tester.driver, "keyboard_not_shown")
            return False, error_msg

        # 3. 텍스트 입력 및 확인
        test_text = "제품 추천해줘"
        print(f"입력 필드에 테스트 텍스트 '{test_text}'를 입력합니다.")
        try:
            # 입력 필드를 다시 찾아 텍스트 입력
            input_field_after_click = flow_tester.driver.find_element(AppiumBy.XPATH, input_field_xpath)
            input_field_after_click.send_keys(test_text)

            # 입력된 텍스트가 맞는지 확인
            entered_text = input_field_after_click.text
            if entered_text == test_text:
                print(f"✅ 입력 필드에 텍스트 '{entered_text}'가 정확히 입력되었습니다.")
            else:
                error_msg = f"실패: 텍스트가 잘못 입력되었습니다. (입력: {test_text}, 실제: {entered_text})"
                save_screenshot_on_failure(flow_tester.driver, "text_input_mismatch")
                return False, error_msg
                # --- 로직 추가 시작 ---
                # 4. '전송' 버튼 클릭
            send_button_xpath = '//android.widget.Button[@text="전송"]'
            print(f"'{send_button_xpath}' 버튼을 클릭합니다.")
            try:
                send_button = WebDriverWait(flow_tester.driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, send_button_xpath))
                )
                send_button.click()
                time.sleep(2)  # 전송 후 응답 대기
            except TimeoutException:
                error_msg = "실패: '전송' 버튼을 찾거나 클릭할 수 없습니다."
                save_screenshot_on_failure(flow_tester.driver, "send_button_not_found")
                return False, error_msg

            # # 5. 뒤로가기 실행
            # print("뒤로가기를 실행하여 이전 화면으로 돌아갑니다.")
            # flow_tester.driver.back()
            # time.sleep(1)
            # # --- 로직 추가 종료 ---

        except Exception as e:
            error_msg = f"실패: 텍스트 입력 또는 확인 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "text_input_error")
            return False, error_msg

        return True, "코디비서 입력 필드 및 키패드 검증 성공."

    except Exception as e:
        return False, f"코디비서 입력 필드 테스트 중 예외 발생: {e}"
    finally:
        # 테스트 종료 전 키패드를 숨기고 싶다면 아래 코드의 주석을 해제하세요.
        # if flow_tester.driver.is_keyboard_shown():
        #     flow_tester.driver.hide_keyboard()
        print("--- 코디비서 > 입력 필드 터치 및 키패드 노출, 텍스트 입력 확인 시나리오 종료 ---")