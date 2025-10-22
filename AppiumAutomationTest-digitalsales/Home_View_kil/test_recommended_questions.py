# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Xpath 저장소에서 HomeViewKilLocators 임포트
from Xpath.xpath_repository import HomeViewKilLocators

# 스크린샷 헬퍼 임포트
from Utils.screenshot_helper import save_screenshot_on_failure

# [Seller app checklist-141] AI 코디 비서 > 추천 질문 선택
def test_select_recommended_question(flow_tester):
    """AI 코디 비서 화면에서 추천 질문 선택 후 답변 확인"""
    print("\n--- AI 코디 비서 추천 질문 선택 시나리오 시작 (checklist-141) ---")

    # --- 플랫폼에 맞는 로케이터 동적 선택 ---
    if flow_tester.platform == 'android':
        locators = HomeViewKilLocators.AOS
    else: # iOS 또는 기본값
        locators = HomeViewKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    wait = WebDriverWait(flow_tester.driver, 15) # 답변 대기 시간 고려
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # ※ 사전 조건: AI 코디 비서 화면에 진입한 상태

        # 1. 첫 번째 추천 질문 요소 찾기 및 텍스트 저장
        print("💡 첫 번째 추천 질문 찾기 및 텍스트 저장...")
        first_question_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.first_recommended_question_xpath)),
            message="첫 번째 추천 질문을 찾지 못했습니다."
        )
        # [수정] 텍스트 가져오는 방식 변경
        question_text = ""
        if flow_tester.platform == 'android':
             question_text = first_question_element.text
        else: # iOS
             question_text = first_question_element.get_attribute("label") or first_question_element.get_attribute("value")

        print(f"✅ 첫 번째 추천 질문 텍스트: '{question_text}'")

        # 2. 첫 번째 추천 질문 클릭
        print("💡 추천 질문 클릭...")
        first_question_element.click()
        print("✅ 추천 질문 클릭 완료.")
        print("⏳ AI 답변 대기 중...")
        time.sleep(5) # AI 답변 생성 시간 대기

        # 3. 질문이 입력 필드 위 채팅 영역에 표시되는지 확인
        print(f"💡 채팅 영역에서 질문 '{question_text}' 확인...")
        # 질문 텍스트가 포함된 요소를 찾음 (XPath 수정 필요 시 진행)
        # 예: //*[contains(@text, "{question_text}")] (Android)
        #     //XCUIElementTypeStaticText[contains(@value, "{question_text}")] (iOS)
        # 저장소에 chat_message_xpath_template 정의 필요
        chat_message_xpath = locators.chat_message_xpath_template.format(message_text=question_text) # 가정
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, chat_message_xpath)),
            message=f"채팅 영역에서 질문 '{question_text}'을(를) 찾지 못했습니다."
        )
        print("✅ 질문이 채팅 영역에 정상적으로 표시되었습니다.")

        # 4. 답변 영역 확인 (답변이 최소 1개 이상 나타나는지)
        print("💡 답변 영역 확인...")
        # locator.answer_area_xpath 가 답변 전체를 감싸는 컨테이너라고 가정
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.answer_area_xpath)),
             message="답변 영역을 찾지 못했습니다."
        )
        # 답변 영역 내에 텍스트 요소가 있는지 추가 확인
        text_element_in_answer_xpath = ""
        if flow_tester.platform == 'android':
             text_element_in_answer_xpath = f"{locators.answer_area_xpath}//android.widget.TextView"
        else: # iOS
             text_element_in_answer_xpath = f"{locators.answer_area_xpath}//XCUIElementTypeStaticText"

        wait.until(
             EC.presence_of_element_located((AppiumBy.XPATH, text_element_in_answer_xpath)),
             message="답변 영역 내 텍스트를 찾지 못했습니다."
        )
        print("✅ 답변이 성공적으로 노출되었습니다.")

        # --- 최종 성공 처리 ---
        scenario_passed = True
        result_message = "🎉 성공: 추천 질문 선택 후 질문 표시 및 답변 확인 완료."

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "recommended_question_fail")
        result_message = f"❌ 실패: 요소를 찾지 못했거나 타임아웃 발생 - {e}"
        scenario_passed = False
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "recommended_question_error")
        result_message = f"❌ 실패: 테스트 실행 중 예상치 못한 오류 발생: {e}"
        scenario_passed = False
    finally:
        # 테스트 종료 후 원래 화면으로 돌아가기 (뒤로가기)
        print("💡 테스트 종료 후 뒤로가기...")
        try:
            flow_tester.driver.back() # AI 비서 -> 홈 (Android 기준)
            # iOS는 back 대신 다른 네비게이션 필요할 수 있음
            print("✅ 뒤로가기 완료.")
            time.sleep(2) # 홈 화면 안정화 대기
        except Exception as back_err:
             print(f"⚠️ 뒤로가기 중 오류 발생: {back_err}")

        print(f"--- AI 코디 비서 추천 질문 선택 시나리오 종료 ---\n")
        # 최종 결과를 튜플 형태로 반환
        return scenario_passed, result_message







# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from Utils.screenshot_helper import save_screenshot_on_failure
#
# def test_verify_recommended_questions_for_managed_customers(flow_tester):
#     """
#     '관리고객' 버튼 클릭 후, 추천 질문 텍스트가 노출되는지 검증합니다.
#     """
#     print("\n--- '관리고객' 추천 질문 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. '관리고객' 버튼 클릭
#         time.sleep(2)  # 화면이 로드될 시간을 기다립니다.
#         managed_customer_button_xpath = '//android.widget.Button[@text="관리고객"]'
#         print(f"'{managed_customer_button_xpath}' 버튼을 클릭합니다.")
#         try:
#             managed_customer_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, managed_customer_button_xpath))
#             )
#             managed_customer_button.click()
#             time.sleep(2)  # 화면이 로드될 시간을 기다립니다.
#         except TimeoutException:
#             error_msg = "실패: '관리고객' 버튼을 찾거나 클릭할 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "managed_customer_button_not_found")
#             return False, error_msg
#
#         # 2. 추천 질문 텍스트 노출 확인
#         recommendation_text_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[2]'
#         print(f"'{recommendation_text_xpath}' 텍스트가 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, recommendation_text_xpath))
#             )
#             print("✅ 추천 질문 텍스트가 성공적으로 노출되었습니다.")
#             return True, "'관리고객' 추천 질문 확인 성공."
#         except TimeoutException:
#             error_msg = "실패: '관리고객' 버튼 클릭 후 추천 질문 텍스트를 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "recommended_question_text_not_found")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"추천 질문 확인 중 예외 발생: {e}"
#     finally:
#         print("--- '관리고객' 추천 질문 노출 확인 시나리오 종료 ---");('ㅣ'
#                                                      ' ㅜ ㅡ')