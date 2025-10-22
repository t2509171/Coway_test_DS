# -*- coding: utf-8 -*-

import time
import random
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Xpath 저장소에서 HomeViewKilLocators 임포트
from Xpath.xpath_repository import HomeViewKilLocators

# 스크린샷 헬퍼 임포트
from Utils.screenshot_helper import save_screenshot_on_failure

# [Seller app checklist-140] AI 코디 비서 > 텍스트 입력 및 전송
def test_cody_secretary_text_input(flow_tester):
    """AI 코디 비서 화면에서 텍스트 입력 및 전송 후 답변 확인"""
    print("\n--- AI 코디 비서 텍스트 입력 및 전송 시나리오 시작 (checklist-140) ---")

    # --- 플랫폼에 맞는 로케이터 동적 선택 ---
    if flow_tester.platform == 'android':
        locators = HomeViewKilLocators.AOS
    else: # iOS 또는 기본값
        locators = HomeViewKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    wait = WebDriverWait(flow_tester.driver, 15) # 답변 대기 시간 고려하여 증가
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    random_question = f"오늘의 날씨는? {random.randint(1, 100)}" # 동일 질문 방지

    try:
        # ※ 사전 조건: AI 코디 비서 화면에 진입한 상태

        # 1. 입력 필드 찾기 및 텍스트 입력
        print(f"💡 입력 필드에 '{random_question}' 입력...")
        input_field = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.text_input_field_xpath)),
            message="텍스트 입력 필드를 찾지 못했습니다."
        )
        input_field.send_keys(random_question)
        print("✅ 텍스트 입력 완료.")
        time.sleep(1) # 입력 안정화 대기

        # 2. 전송 버튼 클릭
        print("💡 전송 버튼 클릭...")
        send_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.send_button_xpath)),
            message="전송 버튼을 찾지 못했습니다."
        )
        send_button.click()
        print("✅ 전송 버튼 클릭 완료.")
        print("⏳ AI 답변 대기 중...")
        time.sleep(5) # AI 답변 생성 시간 대기 (필요 시 증가)

        # 3. 답변 영역 확인 (답변이 최소 1개 이상 나타나는지)
        # 답변은 여러 개의 View 또는 TextView로 구성될 수 있음
        # 첫 번째 답변 요소가 나타나는지만 확인
        print("💡 답변 영역 확인...")
        # [수정] 답변 영역을 좀 더 일반적인 XPath로 찾도록 시도
        # 예: 답변 컨테이너 또는 첫번째 답변 텍스트
        # answer_elements = flow_tester.driver.find_elements(AppiumBy.XPATH, locators.answer_area_xpath)
        # locator.answer_area_xpath 가 답변 전체를 감싸는 컨테이너라고 가정
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.answer_area_xpath)),
             message="답변 영역을 찾지 못했습니다."
        )
        # 답변 영역 내에 텍스트 요소가 있는지 추가 확인 (더 안정적)
        wait.until(
             EC.presence_of_element_located((AppiumBy.XPATH, f"{locators.answer_area_xpath}//android.widget.TextView")), # Android 기준 예시
             # iOS 예시: EC.presence_of_element_located((AppiumBy.XPATH, f"{locators.answer_area_xpath}//XCUIElementTypeStaticText"))
             message="답변 영역 내 텍스트를 찾지 못했습니다."
        )

        print("✅ 답변이 성공적으로 노출되었습니다.")

        # --- 최종 성공 처리 ---
        scenario_passed = True
        result_message = "🎉 성공: AI 코디 비서에게 질문 전송 후 답변을 받았습니다."

        # 4. 테스트 종료 후 원래 화면으로 돌아가기 (뒤로가기)
        print("💡 테스트 종료 후 뒤로가기...")
        flow_tester.driver.back() # AI 비서 -> 홈 (Android 기준)
        # iOS는 back 대신 다른 네비게이션 필요할 수 있음
        print("✅ 뒤로가기 완료.")
        time.sleep(2) # 홈 화면 안정화 대기


    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "cody_input_fail")
        result_message = f"❌ 실패: 요소를 찾지 못했거나 타임아웃 발생 - {e}"
        scenario_passed = False
        # 실패 시에도 뒤로가기 시도
        try:
            flow_tester.driver.back()
            print("⚠️ 실패 후 뒤로가기 시도 완료.")
        except Exception:
            print("⚠️ 실패 후 뒤로가기 중 오류 발생.")
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "cody_input_error")
        result_message = f"❌ 실패: 테스트 실행 중 예상치 못한 오류 발생: {e}"
        scenario_passed = False
        # 실패 시에도 뒤로가기 시도
        try:
            flow_tester.driver.back()
            print("⚠️ 실패 후 뒤로가기 시도 완료.")
        except Exception:
            print("⚠️ 실패 후 뒤로가기 중 오류 발생.")
    finally:
        print(f"--- AI 코디 비서 텍스트 입력 및 전송 시나리오 종료 ---\n")
        # 최종 결과를 튜플 형태로 반환
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