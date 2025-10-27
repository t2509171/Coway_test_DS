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

# [Seller app checklist-142] AI 코디 비서 > 웹뷰 이동
def test_navigate_to_webview_from_home(flow_tester):
    """AI 코디 비서 답변 내 링크 클릭 시 관련 웹뷰 화면 이동 확인"""
    print("\n--- AI 코디 비서 웹뷰 이동 시나리오 시작 (checklist-142) ---")

    # --- 플랫폼에 맞는 로케이터 동적 선택 ---
    if flow_tester.platform == 'android':
        locators = HomeViewKilLocators.AOS
    else: # iOS 또는 기본값
        locators = HomeViewKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    wait = WebDriverWait(flow_tester.driver, 15)
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # ※ 사전 조건: AI 코디 비서 화면에 진입한 상태
        #    이전 테스트(추천 질문 또는 텍스트 입력)에서 답변에 링크가 포함되어 있다고 가정

        # 1. 답변 영역에서 클릭 가능한 링크 찾기
        print("💡 답변 영역에서 링크 찾기 및 클릭...")
        # 링크는 보통 특정 텍스트나 버튼 형태일 수 있음
        # locator.answer_link_xpath가 답변 내 링크 요소라고 가정
        link_element = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.answer_link_xpath)),
            message="답변 영역에서 클릭 가능한 링크를 찾지 못했습니다."
        )
        # 링크 텍스트 확인 (선택 사항)
        link_text = ""
        if flow_tester.platform == 'android':
             link_text = link_element.text
        else:
             link_text = link_element.get_attribute("label") or link_element.get_attribute("value")
        print(f" - 찾은 링크 텍스트: '{link_text}'")

        link_element.click()
        print("✅ 링크 클릭 완료.")
        time.sleep(5) # 웹뷰 로딩 대기

        # 2. 웹뷰 화면 확인
        print("💡 웹뷰 화면 확인...")
        # 웹뷰 화면을 식별할 수 있는 요소 확인 (예: 웹뷰 자체, 웹뷰 내 특정 제목)
        # locator.webview_element_xpath가 웹뷰 컨테이너 또는 특정 제목이라고 가정
        wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.webview_element_xpath)),
            message="웹뷰 화면 요소를 찾지 못했습니다."
        )
        print("✅ 웹뷰 화면으로 성공적으로 이동했습니다.")

        # --- 최종 성공 처리 ---
        scenario_passed = True
        result_message = "🎉 성공: AI 코디 비서 답변 링크 클릭 후 웹뷰 이동 확인 완료."

        # 3. 테스트 종료 후 원래 화면으로 돌아가기 (뒤로가기)
        print("💡 테스트 종료 후 뒤로가기...")
        flow_tester.driver.back() # 웹뷰 -> AI 비서
        time.sleep(1)
        flow_tester.driver.back() # AI 비서 -> 홈 (Android 기준)
        # iOS는 back 대신 다른 네비게이션 필요할 수 있음
        print("✅ 뒤로가기 완료.")
        time.sleep(2) # 홈 화면 안정화 대기

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "webview_nav_fail")
        result_message = f"❌ 실패: 요소를 찾지 못했거나 타임아웃 발생 - {e}"
        scenario_passed = False
         # 실패 시에도 뒤로가기 시도
        try:
            flow_tester.driver.back()
            time.sleep(1)
            flow_tester.driver.back()
            print("⚠️ 실패 후 뒤로가기 시도 완료.")
        except Exception:
            print("⚠️ 실패 후 뒤로가기 중 오류 발생.")
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "webview_nav_error")
        result_message = f"❌ 실패: 테스트 실행 중 예상치 못한 오류 발생: {e}"
        scenario_passed = False
         # 실패 시에도 뒤로가기 시도
        try:
            flow_tester.driver.back()
            time.sleep(1)
            flow_tester.driver.back()
            print("⚠️ 실패 후 뒤로가기 시도 완료.")
        except Exception:
            print("⚠️ 실패 후 뒤로가기 중 오류 발생.")
    finally:
        print(f"--- AI 코디 비서 웹뷰 이동 시나리오 종료 ---\n")
        # 최종 결과를 튜플 형태로 반환
        return scenario_passed, result_message



# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from Utils.screenshot_helper import save_screenshot_on_failure
#
# def test_navigate_to_webview_from_home(flow_tester):
#     """
#     홈 화면의 특정 버튼을 클릭하여 WebView가 노출되는지 검증합니다.
#     """
#     print("\n--- 홈 화면 > 버튼 클릭 > WebView 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. 홈 화면의 버튼 클릭
#         home_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
#         print(f"홈 화면의 버튼({home_button_xpath})을 클릭합니다.")
#         try:
#             # 요소가 클릭 가능한 상태가 될 때까지 최대 10초간 기다립니다.
#             button_to_click = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
#             )
#             button_to_click.click()
#         except TimeoutException:
#             error_msg = f"실패: 홈 화면에서 버튼을 찾을 수 없습니다. (XPath: {home_button_xpath})"
#             save_screenshot_on_failure(flow_tester.driver, "home_webview_button_not_found")
#             return False, error_msg
#
#         # 2. WebView가 노출되었는지 확인
#         webview_xpath = '//android.webkit.WebView[@text="Seller AI"]'
#         print(f"'{webview_xpath}' (WebView)가 노출되는지 확인합니다 (20초 대기).")
#         try:
#             # WebView는 로딩이 느릴 수 있으므로 대기 시간을 20초로 넉넉하게 설정합니다.
#             WebDriverWait(flow_tester.driver, 20).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, webview_xpath))
#             )
#             print("✅ WebView가 성공적으로 노출되었습니다.")
#
#             time.sleep(2)
#             # flow_tester.driver.back()
#             # time.sleep(3)
#             return True, "홈 화면 버튼 클릭 후 WebView 이동 성공."
#
#         except TimeoutException:
#             error_msg = "실패: 버튼 클릭 후 WebView를 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "webview_not_found_after_click")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"WebView 이동 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 화면 > 버튼 클릭 > WebView 노출 확인 시나리오 종료 ---")