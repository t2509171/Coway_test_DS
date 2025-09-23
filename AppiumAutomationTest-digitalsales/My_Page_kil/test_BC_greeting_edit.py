# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


def test_greeting_message_edit(flow_tester):
    """마이페이지 > 명함설정: 인사말 편집 버튼 선택 시 수정 기능 활성화"""
    print("\n--- 명함설정 인사말 편집 기능 확인 시나리오 시작 ---")

    edit_button_xpath = '//android.widget.TextView[contains(@text, "안녕하세요")]/following-sibling::android.widget.Button[@text="편집"]'
    # 편집 버튼 클릭 후 나타나는 EditText로 활성화 여부 판단
    edit_field_xpath = '//android.widget.EditText'

    try:
        # 1. 인사말 옆 '편집' 버튼 클릭
        print(f"'{edit_button_xpath}' 버튼을 찾습니다...")
        edit_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, edit_button_xpath))
        )
        print("✅ 편집 버튼을 찾았습니다. 클릭합니다.")
        edit_button.click()
        time.sleep(1)

        # 2. 수정 가능한 입력 필드(EditText)가 나타나는지 확인
        print(f"'{edit_field_xpath}' 입력 필드가 나타나는지 확인합니다...")
        edit_field = WebDriverWait(flow_tester.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, edit_field_xpath))
        )
        print("✅ 성공: 인사말을 수정할 수 있는 입력 필드가 활성화되었습니다.")

        # (선택) 원래 상태로 돌아가기 위해 '취소'나 '저장' 버튼 클릭 로직 추가 가능
        # 예: flow_tester.driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@text="취소"]').click()

        return True, "인사말 편집 기능이 정상적으로 활성화됩니다."

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_greeting_edit_fail")
        return False, f"실패: 인사말 편집 버튼 또는 입력 필드를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "bc_greeting_edit_fail")
        return False, f"실패: 인사말 편집 기능 확인 중 오류 발생: {e}"
    finally:
        print("--- 명함설정 인사말 편집 기능 확인 시나리오 종료 ---")