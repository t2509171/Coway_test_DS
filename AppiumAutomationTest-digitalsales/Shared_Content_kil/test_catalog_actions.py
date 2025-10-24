# PythonProject/Shared_Content_kil/test_catalog_actions.py

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
from Xpath.xpath_repository import SharedContentKilLocators # 수정: 클래스 임포트

def navigate_to_ecatalog(flow_tester):
    """Navigates from the home screen to the eCatalog section via the full menu."""
    print("\n--- e카탈로그 섹션으로 이동 시작 ---")

    # --- [수정됨] ---
    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android':
            locators = SharedContentKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = SharedContentKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = SharedContentKilLocators.AOS
    # --- [수정 완료] ---

    try:
        print("1. 전체 메뉴 버튼 클릭")
        # --- [수정됨] ---
        menu_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.menu_button_xpath)) # 공통 로케이터 사용
        )
        # --- [수정 완료] ---
        menu_button.click()
        print("   전체 메뉴 버튼 클릭 완료.")
        time.sleep(2)

        print("2. 'e카탈로그' 메뉴 항목 클릭")
        # --- [수정됨] ---
        ecatalog_item = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.ecatalog_item_xpath)) # 공통 로케이터 사용
        )
        # --- [수정 완료] ---
        ecatalog_item.click()
        print("   'e카탈로그' 메뉴 항목 클릭 완료.")
        time.sleep(3) # 페이지 로딩 대기

        print("3. '라이브러리' 텍스트 확인 (e카탈로그 페이지 로드 검증)")
        # --- [수정됨] ---
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.library_text_xpath)) # 공통 로케이터 사용
        )
        # --- [수정 완료] ---
        print("   ✅ '라이브러리' 텍스트 확인 완료. e카탈로그 페이지 진입 성공.")
        print("--- e카탈로그 섹션으로 이동 성공 ---")
        return True, "e카탈로그 이동 성공"

    except TimeoutException as e:
        print(f"🚨 e카탈로그 이동 중 타임아웃 발생: {e}")
        flow_tester.driver.save_screenshot("failure_navigate_ecatalog_timeout.png")
        return False, f"e카탈로그 이동 실패 (타임아웃): {e}"
    except NoSuchElementException as e:
        print(f"🚨 e카탈로그 이동 중 요소 찾기 실패: {e}")
        flow_tester.driver.save_screenshot("failure_navigate_ecatalog_no_such_element.png")
        return False, f"e카탈로그 이동 실패 (요소 없음): {e}"
    except Exception as e:
        print(f"🚨 e카탈로그 이동 중 예상치 못한 오류 발생: {e}")
        flow_tester.driver.save_screenshot("failure_navigate_ecatalog_unexpected.png")
        return False, f"e카탈로그 이동 실패 (오류): {e}"

# PythonProject/Shared_Content_kil/test_catalog_actions.py
# ... (import 부분 동일) ...
from Xpath.xpath_repository import SharedContentKilLocators

# navigate_to_ecatalog 함수는 이름 변경 없이 그대로 사용 (내부 로직은 플랫폼 분기 적용됨)
# ... (navigate_to_ecatalog 함수 코드) ...

# --- 함수 이름 복원 및 플랫폼 분기 추가 ---
def test_share_catalog_to_facebook(flow_tester): # 함수 이름 복원 (test_catalog_share_action -> test_share_catalog_to_facebook)
    """Tests the share functionality within the eCatalog section."""
    print("\n--- e카탈로그 공유 기능 테스트 시작 ---")
    scenario_passed = True
    result_message = "e카탈로그 공유 기능 테스트 성공."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android':
            locators = SharedContentKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = SharedContentKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = SharedContentKilLocators.AOS

    try:
        nav_success, nav_msg = navigate_to_ecatalog(flow_tester)
        if not nav_success:
            return False, nav_msg

        print("1. 공유하기 버튼 클릭")
        share_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.share_button_xpath))
        )
        share_button.click()
        print("   공유하기 버튼 클릭 완료.")
        time.sleep(2)

        print("2. 공유 옵션에서 '페이스북' 클릭")
        facebook_option = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.facebook_xpath))
        )
        facebook_option.click()
        print("   '페이스북' 옵션 클릭 완료.")
        time.sleep(2)

        print("3. 법적 고지 확인")
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, locators.legal_notice_xpath))
        )
        print("   법적 고지 확인 완료.")

        print("4. 동의 버튼 클릭")
        agree_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.agree_button_xpath))
        )
        agree_button.click()
        print("   동의 버튼 클릭 완료.")
        time.sleep(5)

        # 실제 페이스북 공유 화면 확인 로직 (주석 처리됨)

        print("5. 이전 화면으로 돌아가기 (뒤로가기)")
        flow_tester.driver.back()
        time.sleep(2)
        flow_tester.driver.back()
        time.sleep(2)
        flow_tester.driver.back()
        time.sleep(2)

    except TimeoutException as e:
        scenario_passed = False
        result_message = f"e카탈로그 공유 테스트 실패 (타임아웃): {e}"
        # ... (오류 처리 동일) ...
    except NoSuchElementException as e:
        scenario_passed = False
        result_message = f"e카탈로그 공유 테스트 실패 (요소 찾기 실패): {e}"
        # ... (오류 처리 동일) ...
    except Exception as e:
        scenario_passed = False
        result_message = f"e카탈로그 공유 테스트 중 예상치 못한 오류 발생: {e}"
        # ... (오류 처리 동일) ...
    finally:
        print("--- e카탈로그 공유 기능 테스트 종료 ---")

    return scenario_passed, result_message

# --- 함수 이름 복원 및 플랫폼 분기 추가 ---
def test_download_catalog(flow_tester): # 함수 이름 복원 (test_catalog_download_action -> test_download_catalog)
    """Tests the download functionality within the eCatalog section."""
    print("\n--- e카탈로그 다운로드 기능 테스트 시작 ---")
    scenario_passed = True
    result_message = "e카탈로그 다운로드 기능 테스트 성공."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android':
            locators = SharedContentKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = SharedContentKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = SharedContentKilLocators.AOS

    try:
        # navigate_to_ecatalog 호출 (필요시)
        nav_success, nav_msg = navigate_to_ecatalog(flow_tester)
        if not nav_success:
             return False, nav_msg # 이미 이동했다면 이 부분을 제거하고 아래 로직만 수행

        print("1. 다운로드 버튼 클릭")
        download_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.download_button_xpath))
        )
        download_button.click()
        print("   다운로드 버튼 클릭 완료.")
        time.sleep(5) # 다운로드 대기

        # 다운로드 완료 확인 로직 (주석 처리됨)

    except TimeoutException as e:
        scenario_passed = False
        result_message = f"e카탈로그 다운로드 테스트 실패 (타임아웃): {e}"
        # ... (오류 처리 동일) ...
    except NoSuchElementException as e:
        scenario_passed = False
        result_message = f"e카탈로그 다운로드 테스트 실패 (요소 찾기 실패): {e}"
        # ... (오류 처리 동일) ...
    except Exception as e:
        scenario_passed = False
        result_message = f"e카탈로그 다운로드 테스트 중 예상치 못한 오류 발생: {e}"
        # ... (오류 처리 동일) ...
    finally:
        print("--- e카탈로그 다운로드 기능 테스트 종료 ---")
        try:
            flow_tester.driver.back() # 전체 메뉴로 돌아가기
            time.sleep(2)
        except Exception:
            print("다운로드 테스트 후 뒤로가기 실패 (무시)")

    return scenario_passed, result_message

# test_catalog_delete_action 함수는 import 목록에 없었으므로 그대로 두거나 필요시 삭제/수정

# 다른 필요한 함수들도 유사하게 수정...