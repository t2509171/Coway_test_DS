import pytest
import time
import logging

# Selenium (웹)용 임포트
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Appium (네이티브)용 임포트
from appium.webdriver.common.appiumby import AppiumBy

# 유틸리티 임포트
from Utils.context_manager import switch_to_webview, switch_to_native
from Utils.scrolling_function import scroll_down

# XPath 클래스 임포트
from Xpath.xpath_repository import HomeKilLocators

# 로거 설정
log = logging.getLogger(__name__)


def test_banner_interaction_in_webview(flow_tester):
    """
    (수정) 웹뷰 배너 클릭 후, 상위 런처에 (True/False, message) 튜플을 반환합니다.
    """

    WEB_BANNER_CSS_SELECTOR = "section.m-section-banner .swiper-slide-active a"
    max_scrolls = 5
    banner_found = False  # 배너 클릭 성공 여부 플래그

    try:
        # --- 1. 초기 웹뷰(WebView)로 컨텍스트 전환 ---
        print("홈 화면 로딩 대기 (5초)...")
        time.sleep(5)

        if not switch_to_webview(flow_tester.driver, timeout=20):
            # [!] pytest.fail -> return 으로 수정
            return (False, "웹뷰 컨텍스트로 전환에 실패했습니다.")

        # --- 2. 배너를 찾을 때까지 스크롤 및 검색 반복 ---
        for i in range(max_scrolls):
            try:
                wait_short = WebDriverWait(flow_tester.driver, 2)

                print(f"({i + 1}/{max_scrolls}) 웹뷰에서 배너 검색 시도: {WEB_BANNER_CSS_SELECTOR}")

                banner_element = wait_short.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, WEB_BANNER_CSS_SELECTOR))
                )

                print("✅ 웹뷰 배너 요소를 찾았습니다!")

                # --- 3. 배너 클릭 ---
                banner_element.click()
                print("배너 클릭 성공.")
                time.sleep(3)  # 페이지 이동 대기

                banner_found = True  # 성공 플래그 설정
                break  # 검색 루프 탈출

            except TimeoutException:
                print(f"({i + 1}/{max_scrolls}) 배너를 찾지 못했습니다. 네이티브 스크롤을 시도합니다.")

                switch_to_native(flow_tester.driver)
                scroll_down(flow_tester.driver)
                time.sleep(1)

                if not switch_to_webview(flow_tester.driver, timeout=10):
                    # [!] pytest.fail -> return 으로 수정
                    return (False, "스크롤 후 웹뷰로 재전환 실패.")

            except Exception as e:
                # [!] pytest.fail -> return 으로 수정
                return (False, f"배너 검색 중 예기치 않은 오류 발생: {e}")

        # --- 4. 최종 결과 확인 ---
        if not banner_found and i == max_scrolls - 1:
            # [!] pytest.fail -> return 으로 수정
            return (False, f"실패: 최대 스크롤 횟수({max_scrolls}) 내에 배너를 찾지 못했습니다.")

    except Exception as e:
        log.error(f"웹뷰 배너 테스트 중 오류 발생: {e}")
        # [!] pytest.fail -> return 으로 수정
        return (False, f"웹뷰 배너 상호작용 실패: {e}")

    finally:
        # --- 5. (필수) 네이티브 앱(NATIVE_APP) 컨텍스트로 복귀 ---
        print("테스트 완료 또는 오류 발생. NATIVE_APP 컨텍스트로 복귀합니다.")
        switch_to_native(flow_tester.driver)

    # --- '뒤로 가기' 로직 ---
    if banner_found:
        try:
            print("네이티브 '뒤로 가기'를 실행하여 홈 화면으로 복귀합니다.")
            flow_tester.driver.back()
            time.sleep(2)  # 홈 화면이 다시 로드될 시간 대기
        except Exception as e:
            # [!] pytest.fail -> return 으로 수정
            return (False, f"'뒤로 가기' 실행 중 오류 발생: {e}")

    # --- 6. 네이티브 환경에서 다음 테스트 계속 ---
    print("네이티브 컨텍스트에서 다음 동작을 수행합니다.")
    try:
        native_wait = WebDriverWait(flow_tester.driver, 10)

        if flow_tester.platform == 'android':
            menu_xpath = HomeKilLocators.AOS.menu_button_xpath
            print(f"Android '전체 메뉴' 버튼 확인: {menu_xpath}")
            menu_button = native_wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, menu_xpath))
            )
        elif flow_tester.platform == 'ios':
            menu_xpath = HomeKilLocators.IOS.menu_button_xpath
            print(f"iOS '전체 메뉴' 버튼 확인: {menu_xpath}")
            menu_button = native_wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, menu_xpath))
            )
        else:
            # [!] pytest.fail -> return 으로 수정
            return (False, f"알 수 없는 플랫폼입니다: {flow_tester.platform}")

        print("✅ 네이티브 '전체 메뉴' 버튼 확인 완료.")
    except Exception as e:
        # [!] pytest.fail -> return 으로 수정
        return (False, f"네이티브 복귀 후 요소 탐색 실패: {e}")

    # --- [!] --- 최종 성공 반환 --- [!] ---
    # 모든 단계가 성공적으로 완료되었으므로, (True, "메시지")를 반환합니다.
    return (True, "배너 클릭 및 홈 복귀 확인 완료")
    # [!] -------------------------------- [!]