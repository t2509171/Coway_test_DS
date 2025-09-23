import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down  # 스크롤 함수 추가


def test_menu_navigation_and_verification(flow_tester):
    """
    전체 메뉴에서 e카탈로그, 제품 사용설명서를 스크롤하여 찾고, 위치를 확인한 후 각 화면으로 정상 이동하는지 검증합니다.
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
            time.sleep(2)
        except TimeoutException:
            error_msg = "실패: '전체메뉴' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_ecatalog")
            return False, error_msg

        # 1-3. 스크롤하며 'e카탈로그' 메뉴 찾기
        print("'e카탈로그' 메뉴를 찾기 위해 스크롤을 시작합니다.")
        ecatalog_item = None
        for i in range(5):  # 최대 5번 스크롤
            try:
                ecatalog_item = flow_tester.driver.find_element(AppiumBy.XPATH, ecatalog_item_xpath)
                if ecatalog_item.is_displayed():
                    print(f"✅ 'e카탈로그' 메뉴를 찾았습니다. (시도: {i + 1}번)")
                    break
            except NoSuchElementException:
                print(f"({i + 1}/5) 'e카탈로그' 메뉴를 찾지 못했습니다. 아래로 스크롤합니다.")
                scroll_down(flow_tester.driver)
                time.sleep(1)

        if not ecatalog_item or not ecatalog_item.is_displayed():
            error_msg = "실패: 5번 스크롤 했지만 'e카탈로그' 메뉴를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "ecatalog_not_found_after_scroll")
            return False, error_msg

        # 1-4. 'e카탈로그' 메뉴 위치 확인 및 클릭
        print("'e카탈로그' 메뉴가 '홈' 메뉴보다 위에 있는지 확인합니다.")
        try:
            home_item = flow_tester.driver.find_element(AppiumBy.XPATH, home_item_xpath)
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

        # 1-5. '라이브러리' 화면으로 이동했는지 확인
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
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'

        # 2-1. 전체 메뉴 버튼 다시 클릭
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

        # 2-2. 스크롤하며 '제품 사용설명서' 메뉴 찾기
        print("'제품 사용설명서' 메뉴를 찾기 위해 스크롤을 시작합니다.")
        manual_item = None
        for i in range(5):
            try:
                manual_item = flow_tester.driver.find_element(AppiumBy.XPATH, manual_item_xpath)
                if manual_item.is_displayed():
                    print(f"✅ '제품 사용설명서' 메뉴를 찾았습니다. (시도: {i + 1}번)")
                    break
            except NoSuchElementException:
                print(f"({i + 1}/5) '제품 사용설명서' 메뉴를 찾지 못했습니다. 아래로 스크롤합니다.")
                scroll_down(flow_tester.driver)
                time.sleep(1)

        if not manual_item or not manual_item.is_displayed():
            error_msg = "실패: 5번 스크롤 했지만 '제품 사용설명서' 메뉴를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "manual_not_found_after_scroll")
            return False, error_msg

        # 2-3. '제품 사용설명서' 메뉴 위치 확인 및 클릭
        print("'제품 사용설명서' 메뉴가 '홈' 메뉴보다 위에 있는지 확인합니다.")
        try:
            home_item = flow_tester.driver.find_element(AppiumBy.XPATH, home_item_xpath)
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
        return False, f"전체 메뉴 검증 테스트 중 예외 발생: {e}"
    finally:
        print("--- 전체 메뉴 > e카탈로그/제품 사용설명서 네비게이션 및 화면 검증 시나리오 종료 ---")