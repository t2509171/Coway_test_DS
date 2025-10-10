# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


def test_greeting_message_edit_and_verify(flow_tester):
    """
    마이페이지 > 명함설정: 인사말 편집 시 기존 텍스트가 유지되는지 검증
    1. '인사말' 레이블과 기존 문구를 확인하고 변수에 저장
    2. '편집' 버튼 클릭
    3. 편집 필드에 기존 문구가 그대로 노출되는지 확인
    4. 확인 버튼을 눌러 편집 모드 종료
    """
    print("\n--- 명함설정 인사말 편집 및 텍스트 검증 시나리오 시작 ---")

    # --- XPath 로케이터 정의 ---
    greeting_label_xpath = '//android.widget.TextView[@text="인사말"]'
    initial_greeting_text_xpath = '//android.widget.TextView[@text="항상 고객님만을 생각하겠습니다!!"]'
    edit_button_xpath = '//android.widget.Button[@text="편집"]'
    # Dialog의 확인 버튼은 resource-id가 없는 경우가 많아, XPath 계층 구조를 사용
    dialog_confirm_button_xpath = '//android.app.Dialog/android.widget.Button'

    try:
        wait = WebDriverWait(flow_tester.driver, 10)

        # 1. '인사말' 레이블이 노출되었는지 확인 (선행 조건)
        print(f"'{greeting_label_xpath}' 레이블을 확인합니다...")
        wait.until(EC.presence_of_element_located((AppiumBy.XPATH, greeting_label_xpath)))
        print("✅ '인사말' 레이블이 노출되었습니다.")

        # 2. 편집 전 인사말 텍스트를 찾아 변수 'a'에 저장
        print(f"'{initial_greeting_text_xpath}'에서 기존 인사말을 가져옵니다...")
        greeting_text_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, initial_greeting_text_xpath))
        )
        a = greeting_text_element.text
        print(f"✅ 기존 인사말을 변수에 저장했습니다: '{a}'")

        # 3. '편집' 버튼 클릭
        print(f"'{edit_button_xpath}' 버튼을 클릭합니다.")
        edit_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, edit_button_xpath))
        )
        edit_button.click()

        # 4. EditText에 변수 'a'의 텍스트가 그대로 들어있는지 확인
        # XPath를 동적으로 생성하여 정확히 일치하는 요소를 찾음
        edit_field_xpath = f'//android.widget.EditText[@text="{a}"]'
        print(f"'{edit_field_xpath}' 입력 필드가 나타나는지 확인합니다...")
        wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, edit_field_xpath)))
        print("✅ 성공: 편집 필드에 기존 인사말이 정확하게 표시됩니다.")

        # 5. 확인(Dialog) 버튼 클릭하여 편집 모드 종료
        print(f"'{dialog_confirm_button_xpath}' 확인 버튼을 클릭합니다.")
        confirm_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, dialog_confirm_button_xpath))
        )
        confirm_button.click()

        return True, "인사말 편집 모드 진입 시 텍스트 검증 및 복귀 성공"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_greeting_edit_verify_fail")
        return False, f"실패: 인사말 편집 검증 중 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_greeting_edit_unexpected_error")
        return False, f"실패: 인사말 편집 검증 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 명함설정 인사말 편집 및 텍스트 검증 시나리오 종료 ---")