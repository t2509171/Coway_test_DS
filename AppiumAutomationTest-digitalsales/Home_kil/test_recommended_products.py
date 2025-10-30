import pytest
import time
import logging

# Selenium (웹)용 임포트
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# 유틸리티 임포트
from Utils.context_manager import switch_to_webview, switch_to_native
# [!] scroll_down은 더 이상 사용하지 않습니다.
# from Utils.scrolling_function import scroll_down
from Utils.screenshot_helper import save_screenshot_on_failure

# XPath 클래스 임포트
from Xpath.xpath_repository import HomeKilLocators

# 로거 설정
log = logging.getLogger(__name__)


def test_find_shared_products_section(flow_tester):
    """
    (웹뷰 스크롤 수정) 홈 화면에서 '공유할 제품을 추천 드려요' 섹션이 보일 때까지
    [웹뷰 스크롤]을 하고, 해당 텍스트를 확인합니다.
    """
    print("\n--- 홈 > '공유할 제품을 추천 드려요' (웹뷰) 섹션 확인 시나리오 시작 ---")

    # --- 찾으려는 대상 정의 (웹) ---
    # [!] 텍스트를 직접 찾는 XPath로 변경 (h2.h-tit 대신)
    expected_text = "공유할 제품을 추천 드려요"
    recommended_products_xpath = f"//h2[contains(text(), '{expected_text}')]"
    # --- 대상 정의 완료 ---

    max_scroll_attempts = 10
    element_found_and_verified = False
    return_message = ""  # 최종 반환 메시지

    try:
        # --- 1. 초기 웹뷰(WebView)로 컨텍스트 전환 ---
        print("홈 화면 로딩 대기 (5초)...")
        time.sleep(5)

        if not switch_to_webview(flow_tester.driver, timeout=20):
            return (False, "웹뷰 컨텍스트로 전환에 실패했습니다.")

        # --- 2. 요소를 찾을 때까지 스크롤 및 검색 반복 ---
        for i in range(max_scroll_attempts):
            try:
                wait_short = WebDriverWait(flow_tester.driver, 2)

                # [!] XPath로 검색
                print(f"({i + 1}/{max_scroll_attempts}) 웹뷰에서 요소 검색 시도: {recommended_products_xpath}")

                element = wait_short.until(
                    EC.visibility_of_element_located((By.XPATH, recommended_products_xpath))
                )

                # [!] XPath로 텍스트를 이미 검증했으므로, 찾았다면 성공임.
                print(f"✅ 텍스트 검증 성공: '{expected_text}' 요소를 찾음.")
                element_found_and_verified = True
                return_message = "'공유할 제품을 추천 드려요' (웹뷰) 섹션 타이틀 확인 성공."
                break  # 성공, 루프 탈출

            except TimeoutException:
                # 2초 내에 요소를 못찾은 경우 (정상적인 실패)
                print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾지 못했습니다. [웹뷰 스크롤]을 시도합니다.")

                # [!] --- 수정된 스크롤 로직 --- [!]
                # 네이티브로 나가지 않고, 웹뷰(HTML)를 직접 스크롤합니다.
                try:
                    flow_tester.driver.execute_script("window.scrollBy(0, 500);")  # 아래로 500px 스크롤
                    time.sleep(1)  # 스크롤 애니메이션 대기
                except Exception as js_e:
                    # (혹시 모를 JS 오류 발생 시)
                    return_message = f"웹뷰 스크롤(JS) 실행 중 오류: {js_e}"
                    element_found_and_verified = False
                    break  # 루프 중단
                # [!] ---------------------------- [!]

        # --- 3. 최종 결과 확인 ---
        if not element_found_and_verified:
            if not return_message:
                return_message = f"실패: {max_scroll_attempts}번 스크롤 했지만 '{expected_text}' 요소를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "reco_product_title_not_found_webview")

    except Exception as e:
        log.error(f"웹뷰 테스트 중 예외 발생: {e}")
        save_screenshot_on_failure(flow_tester.driver, "verify_reco_product_failure")
        return_message = f"'공유할 제품을 추천 드려요' 확인 테스트 중 예외 발생: {e}"
        element_found_and_verified = False  # 실패로 설정

    finally:
        # --- 4. (필수) 네이티브 앱(NATIVE_APP) 컨텍스트로 복귀 ---
        print("테스트 완료 또는 오류 발생. NATIVE_APP 컨텍스트로 복귀합니다.")
        switch_to_native(flow_tester.driver)
        print("--- 홈 > '공유할 제품을 추천 드려요' (웹뷰) 섹션 확인 시나리오 종료 ---")

    # --- 5. 최종 성공/실패 반환 ---
    return (element_found_and_verified, return_message)