# PythonProject/Home_View_kil/test_cody_secretary_input.py

import sys
import os
import time

# Ensure the project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import locators from the repository
from Xpath.xpath_repository import HomeViewKilLocators # 수정: 클래스 임포트

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def test_cody_secretary_keyboard_and_input(flow_tester):
    """Sends a valid message to the Cody Secretary and verifies the response (placeholder)."""
    print("\n--- 코디 비서 유효 메시지 전송 테스트 시작 ---")
    scenario_passed = True
    result_message = "유효 메시지 전송 및 응답 확인 성공 (플레이스홀더)."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = HomeViewKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = HomeViewKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = HomeViewKilLocators.AOS

    try:
        # 가정: AI 코디 비서 화면에 이미 진입한 상태
        print("1. 입력 필드에 메시지 입력")
        input_field = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.input_field_xpath))
        )
        valid_message = "정수기 추천해줘" # 실제 유효한 메시지로 변경
        input_field.send_keys(valid_message)
        print(f"   메시지 입력 완료: '{valid_message}'")

        print("2. 전송 버튼 클릭")
        send_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.send_button_xpath))
        )
        send_button.click()
        print("   전송 버튼 클릭 완료.")
        time.sleep(5) # 응답 대기 시간

        # TODO: 실제 응답 확인 로직 추가
        # 예: 응답 메시지 요소 확인, 특정 키워드 포함 여부 확인
        print("   (응답 확인 로직 플레이스홀더)")


    except TimeoutException as e:
        scenario_passed = False
        result_message = f"유효 메시지 전송 테스트 실패 (타임아웃): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_cody_valid_msg_timeout.png")
    except Exception as e:
        scenario_passed = False
        result_message = f"유효 메시지 전송 테스트 중 예상치 못한 오류: {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_cody_valid_msg_unexpected.png")
    finally:
        print("--- 코디 비서 유효 메시지 전송 테스트 종료 ---")

    return scenario_passed, result_message

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def test_send_invalid_message(flow_tester):
    """Sends an invalid message and verifies the error response."""
    print("\n--- 코디 비서 유효하지 않은 메시지 전송 테스트 시작 ---")
    scenario_passed = True
    result_message = "유효하지 않은 메시지 전송 및 오류 응답 확인 성공."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = HomeViewKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = HomeViewKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = HomeViewKilLocators.AOS

    try:
        # 가정: AI 코디 비서 화면에 이미 진입한 상태
        print("1. 입력 필드에 유효하지 않은 메시지 입력")
        input_field = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.input_field_xpath))
        )
        invalid_message = "!@#$%^" # 실제 유효하지 않은 메시지로 변경
        input_field.clear() # 이전 메시지 지우기
        input_field.send_keys(invalid_message)
        print(f"   메시지 입력 완료: '{invalid_message}'")

        print("2. 전송 버튼 클릭")
        send_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.send_button_xpath))
        )
        send_button.click()
        print("   전송 버튼 클릭 완료.")
        time.sleep(5) # 응답 대기 시간

        print("3. 오류 메시지 확인")
        error_message = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.error_message_xpath))
        )
        print(f"   ✅ 오류 메시지 확인 완료: '{error_message.text}'")


    except TimeoutException as e:
        scenario_passed = False
        result_message = f"유효하지 않은 메시지 테스트 실패 (타임아웃): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_cody_invalid_msg_timeout.png")
    except Exception as e:
        scenario_passed = False
        result_message = f"유효하지 않은 메시지 테스트 중 예상치 못한 오류: {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_cody_invalid_msg_unexpected.png")
    finally:
        print("--- 코디 비서 유효하지 않은 메시지 전송 테스트 종료 ---")

    return scenario_passed, result_message

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def test_send_ambiguous_message(flow_tester):
    """Sends an ambiguous message and verifies the clarification response."""
    print("\n--- 코디 비서 모호한 메시지 전송 테스트 시작 ---")
    scenario_passed = True
    result_message = "모호한 메시지 전송 및 уточнение 응답 확인 성공."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = HomeViewKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = HomeViewKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = HomeViewKilLocators.AOS

    try:
        # 가정: AI 코디 비서 화면에 이미 진입한 상태
        print("1. 입력 필드에 모호한 메시지 입력")
        input_field = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.input_field_xpath))
        )
        ambiguous_message = "그거" # 실제 모호한 메시지로 변경
        input_field.clear()
        input_field.send_keys(ambiguous_message)
        print(f"   메시지 입력 완료: '{ambiguous_message}'")

        print("2. 전송 버튼 클릭")
        send_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.send_button_xpath))
        )
        send_button.click()
        print("   전송 버튼 클릭 완료.")
        time.sleep(5) # 응답 대기 시간

        print("3. 명료화 요청 메시지 및 버튼 확인")
        clarification_message = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.ambiguous_message_xpath))
        )
        print(f"   ✅ 명료화 요청 메시지 확인 완료: '{clarification_message.text}'")

        other_keyword_button = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.other_keyword_button_xpath))
        )
        print(f"   ✅ '다른 키워드 선택' 버튼 확인 완료.")


    except TimeoutException as e:
        scenario_passed = False
        result_message = f"모호한 메시지 테스트 실패 (타임아웃): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_cody_ambiguous_msg_timeout.png")
    except Exception as e:
        scenario_passed = False
        result_message = f"모호한 메시지 테스트 중 예상치 못한 오류: {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_cody_ambiguous_msg_unexpected.png")
    finally:
        print("--- 코디 비서 모호한 메시지 전송 테스트 종료 ---")

    return scenario_passed, result_message

# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
# # def test_cody_secretary_keyboard_and_input(flow_tester):
# #     """
# #     코디비서 화면의 입력 필드를 터치했을 때, 키패드가 노출되고 텍스트 입력이 가능한지 검증합니다.
# #     "관리고객" 입력 후 특정 에러 발생 시 예외 처리를 포함합니다.
# #     """
# #     print("\n--- 코디비서 > 입력 필드 터치 및 키패드 노출, 텍스트 입력 확인 시나리오 시작 ---")
# #     try:
# #         # ※ 사전 조건: 코디비서 화면에 진입한 상태
# #         # TODO: 코디비서 화면으로 진입하는 코드를 이 부분에 추가하거나, 테스트 실행 파일에서 미리 호출해야 합니다.
# #         # 예: flow_tester.driver.find_element(AppiumBy.XPATH, '코디비서_아이콘_XPATH').click()
# #         # time.sleep(2)
# #
# #         # 1. 하단 입력 필드 찾기 및 클릭
# #         # TODO: 아래 input_field_xpath 변수에 실제 입력 필드의 XPath를 입력하세요.
# #         input_field_xpath = '//android.widget.EditText[@resource-id="txtBotMessage"]'
# #         print(f"'{input_field_xpath}' (입력 필드)를 클릭하여 키패드를 활성화합니다.")
# #         try:
# #             input_field = WebDriverWait(flow_tester.driver, 10).until(
# #                 EC.element_to_be_clickable((AppiumBy.XPATH, input_field_xpath))
# #             )
# #             input_field.click()
# #             time.sleep(1)  # 키패드가 올라올 시간을 기다립니다.
# #         except TimeoutException:
# #             error_msg = "실패: 코디비서 입력 필드를 찾을 수 없습니다."
# #             save_screenshot_on_failure(flow_tester.driver, "cody_secretary_input_field_not_found")
# #             return False, error_msg
# #
# #         # 2. 키패드가 노출되었는지 확인
# #         print("키패드가 노출되었는지 확인합니다.")
# #         if flow_tester.driver.is_keyboard_shown():
# #             print("✅ 키패드가 성공적으로 노출되었습니다.")
# #         else:
# #             error_msg = "실패: 입력 필드를 클릭했지만 키패드가 노출되지 않았습니다."
# #             save_screenshot_on_failure(flow_tester.driver, "keyboard_not_shown")
# #             return False, error_msg
# #
# #         # 3. 텍스트 입력 및 확인
# #         test_text = "관리고객"
# #         print(f"입력 필드에 테스트 텍스트 '{test_text}'를 입력합니다.")
# #         try:
# #             # 입력 필드를 다시 찾아 텍스트 입력
# #             input_field_after_click = flow_tester.driver.find_element(AppiumBy.XPATH, input_field_xpath)
# #             input_field_after_click.send_keys(test_text)
# #
# #             # 입력된 텍스트가 맞는지 확인
# #             entered_text = input_field_after_click.text
# #             if entered_text == test_text:
# #                 print(f"✅ 입력 필드에 텍스트 '{entered_text}'가 정확히 입력되었습니다.")
# #             else:
# #                 error_msg = f"실패: 텍스트가 잘못 입력되었습니다. (입력: {test_text}, 실제: {entered_text})"
# #                 save_screenshot_on_failure(flow_tester.driver, "text_input_mismatch")
# #                 return False, error_msg
# #
# #             # 4. '전송' 버튼 클릭
# #             send_button_xpath = '//android.widget.Button[@text="전송"]'
# #             print(f"'{send_button_xpath}' 버튼을 클릭합니다.")
# #             try:
# #                 send_button = WebDriverWait(flow_tester.driver, 10).until(
# #                     EC.element_to_be_clickable((AppiumBy.XPATH, send_button_xpath))
# #                 )
# #                 send_button.click()
# #                 time.sleep(2)  # 전송 후 응답 대기
# #             except TimeoutException:
# #                 error_msg = "실패: '전송' 버튼을 찾거나 클릭할 수 없습니다."
# #                 save_screenshot_on_failure(flow_tester.driver, "send_button_not_found")
# #                 return False, error_msg
# #
# #             # --- ✨ 로직 추가 시작 ✨ ---
# #             # 5. "답변을 생성할 수 없습니다." 메시지 확인 및 "다른 키워드 선택" 버튼 클릭
# #             error_message_xpath = '(//android.widget.TextView[@text="답변을 생성할 수 없습니다. 잠시 후 다시 시도해 주세요."])[2]'
# #             other_keyword_button_xpath = '//android.widget.Button[@text="다른 키워드 선택"]'
# #             try:
# #                 # 에러 메시지가 나타나는지 8초간 확인
# #                 print(f"'{error_message_xpath}' 메시지가 나타나는지 확인합니다.")
# #                 error_message_element = WebDriverWait(flow_tester.driver, 8).until(
# #                     EC.presence_of_element_located((AppiumBy.XPATH, error_message_xpath))
# #                 )
# #
# #                 # 에러 메시지가 실제로 화면에 보이는 경우
# #                 if error_message_element.is_displayed():
# #                     print("✅ '답변을 생성할 수 없습니다' 메시지가 확인되었습니다.")
# #                     print(f"'{other_keyword_button_xpath}' 버튼을 클릭합니다.")
# #                     try:
# #                         other_keyword_button = WebDriverWait(flow_tester.driver, 10).until(
# #                             EC.element_to_be_clickable((AppiumBy.XPATH, other_keyword_button_xpath))
# #                         )
# #                         other_keyword_button.click()
# #                         time.sleep(1)  # 버튼 클릭 후 잠시 대기
# #                     except TimeoutException:
# #                         error_msg = f"실패: '{other_keyword_button_xpath}' 버튼을 찾거나 클릭할 수 없습니다."
# #                         save_screenshot_on_failure(flow_tester.driver, "other_keyword_button_not_found")
# #                         return False, error_msg
# #             except TimeoutException:
# #                 # 5초 내에 에러 메시지가 나타나지 않으면, 정상 응답으로 간주하고 테스트를 계속 진행합니다.
# #                 print("에러 메시지가 나타나지 않았습니다. 정상 응답으로 간주합니다.")
# #                 pass
# #             # --- ✨ 로직 추가 종료 ✨ ---
# #
# #         except Exception as e:
# #             error_msg = f"실패: 텍스트 입력 또는 확인 중 오류 발생: {e}"
# #             save_screenshot_on_failure(flow_tester.driver, "text_input_error")
# #             return False, error_msg
# #
# #         return True, "코디비서 입력 필드 및 키패드 검증 성공."
# #
# #     except Exception as e:
# #         return False, f"코디비서 입력 필드 테스트 중 예외 발생: {e}"
# #     finally:
# #         # 테스트 종료 전 키패드를 숨기고 싶다면 아래 코드의 주석을 해제하세요.
# #         # if flow_tester.driver.is_keyboard_shown():
# #         #     flow_tester.driver.hide_keyboard()
# #         print("--- 코디비서 > 입력 필드 터치 및 키패드 노출, 텍스트 입력 확인 시나리오 종료 ---")
#
#
# def test_cody_secretary_keyboard_and_input(flow_tester):
#     """
#     코디비서에서 '관리고객' 입력 후, 지정된 응답 메시지가 나타나는지 검증합니다.
#     (시나리오 순서 변경: '파악 불가' 메시지를 먼저 확인)
#     """
#     print("\n--- 코디비서 > 지정 응답 메시지 확인 시나리오 (순서 변경) 시작 ---")
#     try:
#         # 1. 텍스트 입력 및 전송
#         input_field_xpath = '//android.widget.EditText[@resource-id="txtBotMessage"]'
#         send_button_xpath = '//android.widget.Button[@text="전송"]'
#         test_text = "관리고객"
#         try:
#             print(f"'{input_field_xpath}' (입력 필드)를 찾아 '{test_text}'를 입력하고 전송합니다.")
#             input_field = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, input_field_xpath))
#             )
#             input_field.click()
#             time.sleep(1)
#             input_field.send_keys(test_text)
#
#             send_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, send_button_xpath))
#             )
#             send_button.click()
#             time.sleep(3)  # 응답 메시지가 표시될 시간을 기다립니다.
#         except Exception as e:
#             error_msg = f"실패: 텍스트 입력 또는 전송 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "text_input_or_send_error")
#             return False, error_msg
#
#         # --- ✨ 로직 수정 시작 (순서 변경) ✨ ---
#         # 2. 서버 응답 메시지에 따라 분기 처리
#         print("서버 응답 메시지를 확인하여 다음 동작을 결정합니다.")
#
#         # 플래그 변수: 예상 메시지를 찾았는지 여부를 기록
#         message_found = False
#
#         # XPath 정의
#         error_message_xpath = '//android.widget.TextView[@text="답변을 생성할 수 없습니다. 잠시 후 다시 시도해 주세요."]'
#         ambiguous_message_xpath = '//android.widget.TextView[@text="말씀하신 내용을 제가 정확히 파악하기 어렵네요. 혹시 다음 키워드 중 궁금하신 점이 있으신가요?"]'
#         other_keyword_button_xpath = '//android.widget.Button[@text="다른 키워드 선택"]'
#
#         try:
#             # 시나리오 1 (순서 변경): '내용 파악 불가' 메시지가 8초 이내에 나타나는지 확인
#             print(f"시나리오 1: '{ambiguous_message_xpath}' 메시지가 나타나는지 확인합니다.")
#             ambiguous_message_element = WebDriverWait(flow_tester.driver, 8).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, ambiguous_message_xpath))
#             )
#
#             if ambiguous_message_element.is_displayed():
#                 message_found = True  # 메시지를 찾았으므로 플래그를 True로 변경
#                 print("✅ [시나리오 1] '내용을 파악하기 어렵네요' 메시지가 확인되었습니다.")
#                 # 이 시나리오에서는 추가 동작 없이 넘어갑니다.
#
#         except TimeoutException:
#             # '내용 파악 불가' 메시지가 시간 내에 나타나지 않은 경우
#             print("'내용 파악 불가' 메시지가 없어, 다음 시나리오를 확인합니다.")
#             try:
#                 # 시나리오 2 (순서 변경): '답변 생성 불가' 메시지가 있는지 즉시 확인
#                 error_message_element = flow_tester.driver.find_element(AppiumBy.XPATH, error_message_xpath)
#                 if error_message_element.is_displayed():
#                     message_found = True  # 메시지를 찾았으므로 플래그를 True로 변경
#                     print("✅ [시나리오 2] '답변을 생성할 수 없습니다' 메시지가 확인되었습니다.")
#                     print(f"'{other_keyword_button_xpath}' 버튼을 클릭합니다.")
#                     try:
#                         other_keyword_button = WebDriverWait(flow_tester.driver, 10).until(
#                             EC.element_to_be_clickable((AppiumBy.XPATH, other_keyword_button_xpath))
#                         )
#                         other_keyword_button.click()
#                         time.sleep(1)
#                     except TimeoutException:
#                         error_msg = f"실패: 메시지는 찾았지만 '{other_keyword_button_xpath}' 버튼을 클릭할 수 없습니다."
#                         save_screenshot_on_failure(flow_tester.driver, "other_keyword_button_not_found")
#                         return False, error_msg
#             except NoSuchElementException:
#                 # 두 번째 메시지도 찾지 못한 경우. 최종 실패 처리를 위해 넘어갑니다.
#                 print("시나리오 2 메시지도 찾을 수 없습니다.")
#                 pass
#
#         # --- 3. 최종 결과 판정 ---
#         if not message_found:
#             # 두 시나리오 모두 실패한 경우
#             error_msg = "실패: 전송 후 예상되는 응답 메시지('내용 파악 불가' 또는 '답변 생성 불가')가 나타나지 않았습니다."
#             save_screenshot_on_failure(flow_tester.driver, "no_expected_message_found")
#             return False, error_msg
#         # --- ✨ 로직 수정 종료 ✨ ---
#
#         return True, "코디비서 응답 메시지 분기 처리 검증 성공."
#
#     except Exception as e:
#         error_msg = f"테스트 시나리오 중 예외 발생: {e}"
#         save_screenshot_on_failure(flow_tester.driver, "scenario_unexpected_exception")
#         return False, error_msg
#     finally:
#         print("--- 코디비서 > 지정 응답 메시지 확인 시나리오 종료 ---")