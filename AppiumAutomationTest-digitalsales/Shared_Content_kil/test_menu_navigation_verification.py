import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure

def test_menu_navigation_and_verification(flow_tester):
    """
    전체 메뉴에서 e카탈로그, 제품 사용설명서의 위치를 확인하고 각 화면으로 정상 이동하는지 검증합니다.
    """
    print("\n--- 전체 메뉴 > e카탈로그/제품 사용설명서 네비게이션 및 화면 검증 시나리오 시작 ---")
    try:
        # =================================================================
        # 1. 'e카탈로그' 메뉴 검증
        # =================================================================
        print("\n[1단계: 'e카탈로그' 검증 시작]")

        # 1-1. XPath 정의
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        home_item_xpath = '//android.view.View[@content-desc="홈"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'

        # 1-2. 전체 메뉴 버튼 클릭
        print("전체 메뉴 버튼을 클릭합니다.")
        try:
            menu_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
            )
            menu_button.click()
            time.sleep(2)  # 메뉴 애니메이션 대기
        except TimeoutException:
            error_msg = "실패: '전체메뉴' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_ecatalog")
            return False, error_msg

        # 1-3. 'e카탈로그' 메뉴 위치 확인 및 클릭
        print("'e카탈로그' 메뉴가 '홈' 메뉴보다 위에 있는지 확인합니다.")
        try:
            ecatalog_item = flow_tester.driver.find_element(AppiumBy.XPATH, ecatalog_item_xpath)
            home_item = flow_tester.driver.find_element(AppiumBy.XPATH, home_item_xpath)

            if not ecatalog_item.is_displayed():
                raise NoSuchElementException("'e카탈로그' 메뉴가 화면에 노출되지 않았습니다.")

            ecatalog_y = ecatalog_item.location['y']
            home_y = home_item.location['y']
            print(f"'e카탈로그' 위치: {ecatalog_y}, '홈' 위치: {home_y}")

            if ecatalog_y >= home_y:
                raise Exception("'e카탈로그' 메뉴가 '홈' 메뉴보다 아래에 위치합니다.")

            print("✅ 위치 확인 완료. 'e카탈로그' 메뉴를 클릭합니다.")
            ecatalog_item.click()

        except (NoSuchElementException, Exception) as e:
            error_msg = f"실패: 'e카탈로그' 메뉴 위치 검증 또는 클릭 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "ecatalog_verification_failed")
            return False, error_msg

        # 1-4. '라이브러리' 화면으로 이동했는지 확인
        print("'라이브러리' 화면으로 이동했는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, library_text_xpath))
            )
            print("✅ '라이브러리' 텍스트가 성공적으로 확인되었습니다.")
            print("[1단계: 'e카탈로그' 검증 성공]")
        except TimeoutException:
            error_msg = "실패: 'e카탈로그' 클릭 후 '라이브러리' 화면을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "library_view_not_found_for_ecatalog")
            return False, error_msg

        # =================================================================
        # 2. '제품 사용설명서' 메뉴 검증
        # =================================================================
        print("\n[2단계: '제품 사용설명서' 검증 시작]")

        # 2-1. XPath 정의
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        # menu_button_xpath, home_item_xpath, library_text_xpath는 위와 동일하므로 재사용

        # 2-2. 전체 메뉴 버튼 다시 클릭
        print("전체 메뉴 버튼을 다시 클릭합니다.")
        try:
            menu_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
            )
            menu_button.click()
            time.sleep(2)
        except TimeoutException:
            error_msg = "실패: '제품 사용설명서' 검증을 위해 '전체메뉴' 버튼을 다시 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_manual")
            return False, error_msg

        # 2-3. '제품 사용설명서' 메뉴 위치 확인 및 클릭
        print("'제품 사용설명서' 메뉴가 '홈' 메뉴보다 위에 있는지 확인합니다.")
        try:
            manual_item = flow_tester.driver.find_element(AppiumBy.XPATH, manual_item_xpath)
            home_item = flow_tester.driver.find_element(AppiumBy.XPATH, home_item_xpath)

            if not manual_item.is_displayed():
                raise NoSuchElementException("'제품 사용설명서' 메뉴가 화면에 노출되지 않았습니다.")

            manual_y = manual_item.location['y']
            home_y = home_item.location['y']
            print(f"'제품 사용설명서' 위치: {manual_y}, '홈' 위치: {home_y}")

            if manual_y >= home_y:
                raise Exception("'제품 사용설명서' 메뉴가 '홈' 메뉴보다 아래에 위치합니다.")

            print("✅ 위치 확인 완료. '제품 사용설명서' 메뉴를 클릭합니다.")
            manual_item.click()

        except (NoSuchElementException, Exception) as e:
            error_msg = f"실패: '제품 사용설명서' 메뉴 위치 검증 또는 클릭 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "manual_verification_failed")
            return False, error_msg

        # 2-4. '라이브러리' 화면으로 이동했는지 확인
        print("'라이브러리' 화면으로 이동했는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, library_text_xpath))
            )
            print("✅ '라이브러리' 텍스트가 성공적으로 확인되었습니다.")
            print("[2단계: '제품 사용설명서' 검증 성공]")
        except TimeoutException:
            error_msg = "실패: '제품 사용설명서' 클릭 후 '라이브러리' 화면을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "library_view_not_found_for_manual")
            return False, error_msg

        return True, "전체 메뉴 네비게이션 및 화면 검증 성공."

    except Exception as e:
        # 예상치 못한 에러 처리
        return False, f"전체 메뉴 검증 테스트 중 예외 발생: {e}"
    finally:
        print("--- 전체 메뉴 > e카탈로그/제품 사용설명서 네비게이션 및 화면 검증 시나리오 종료 ---")