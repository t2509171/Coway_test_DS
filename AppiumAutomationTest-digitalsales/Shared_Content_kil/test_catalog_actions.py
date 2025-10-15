import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down  # 스크롤 함수 추가

def test_share_catalog_to_facebook(flow_tester):
    """
    (Checklist-89) e카탈로그를 페이스북으로 공유하는 기능을 검증합니다.
    공유 버튼 선택 > 채널 선택 > 페이스북 선택 > 광고성 정보 동의 > 페이스북 앱 호출 > 뒤로가기 > 삭제
    """
    print("\n--- (Checklist-89) e카탈로그 페이스북 공유 시나리오 시작 ---")
    try:
        # 0 e카탈로그 화면 진입
        # 1-1. XPath 정의
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        home_item_xpath = '//android.view.View[@content-desc="홈"]'
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



        # 0 '공유하기' 버튼 활성화를 위해 좌표 클릭 (driver.tap 방식)
        print("'공유하기' 버튼 활성화를 위해 (880, 857) 좌표를 클릭합니다.")
        try:
            # driver.tap은 [(x, y)] 형태의 리스트를 인자로 받습니다.
            flow_tester.driver.tap([(880, 857)])
            print("✅ driver.tap 동작이 실행되었습니다.")
            time.sleep(3)  # UI 반응 시간을 넉넉하게 3초로 줍니다.
            flow_tester.driver.back()
            time.sleep(2)
        except Exception as e:
            error_msg = f"실패: driver.tap을 이용한 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "driver_tap_error")
            return False, error_msg

        # UI가 반응할 시간을 넉넉하게 줍니다.
        print("UI 반응 대기 중... (5초)")

        # 1. '공유하기' 버튼 클릭
        share_button_xpath = '//android.widget.Button[@text="공유하기"]' # 실제 앱의 XPath로 수정 필요
        print(f"'{share_button_xpath}' (공유하기) 버튼을 클릭합니다.")
        try:
            share_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, share_button_xpath))
            )
            share_button.click()
        except TimeoutException:
            error_msg = "실패: '공유하기' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "share_button_not_found")
            return False, error_msg

        # 2. '채널 선택' 팝업에서 '페이스북' 아이콘 클릭
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        print(f"'{facebook_xpath}' (페이스북) 아이콘을 클릭합니다.")
        try:
            facebook_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, facebook_xpath))
            )
            facebook_button.click()
        except TimeoutException:
            error_msg = "실패: 공유 채널 팝업에서 '페이스북' 아이콘을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "facebook_icon_not_found")
            return False, error_msg

        # 3. '광고성 정보 전송에 따른 의무사항' 팝업창 노출 확인
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'
        print(f"'{legal_notice_xpath}' 팝업이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, legal_notice_xpath))
            )
            print("✅ '광고성 정보' 팝업이 성공적으로 확인되었습니다.")
        except TimeoutException:
            error_msg = "실패: '광고성 정보' 팝업을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "legal_notice_popup_not_found")
            return False, error_msg

        # 4. '동의' 버튼 클릭
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        print(f"'{agree_button_xpath}' (동의) 버튼을 클릭합니다.")
        try:
            agree_button = flow_tester.driver.find_element(AppiumBy.XPATH, agree_button_xpath)
            agree_button.click()
        except Exception as e:
            error_msg = f"실패: '동의' 버튼 클릭 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "agree_button_click_failed")
            return False, error_msg

        # 5. 페이스북 앱이 호출되었는지 확인
        print("페이스북 앱이 실행되었는지 확인합니다.")
        time.sleep(5) # 앱 전환 대기
        current_package = flow_tester.driver.current_package
        print(f"현재 활성화된 패키지: {current_package}")

        if 'com.facebook' not in current_package:
            error_msg = f"실패: 페이스북 앱이 호출되지 않았습니다. (현재 패키지: {current_package})"
            save_screenshot_on_failure(flow_tester.driver, "facebook_app_not_launched")
            return False, error_msg
        print("✅ 페이스북 앱이 성공적으로 호출되었습니다.")

        # 6. 뒤로가기 실행
        print("뒤로가기를 실행하여 게시글 작성 화면을 나갑니다.")
        flow_tester.driver.back()
        time.sleep(2)

        # 7. 페이스북 포스트 '삭제' 버튼 클릭하여 원래 앱으로 최종 복귀
        print("페이스북의 '삭제' 확인 버튼을 클릭합니다.")
        # resource-id의 경우, 앱 버전에 따라 변경될 수 있으므로 text 속성을 함께 사용하는 것이 안정적입니다.
        delete_button_xpath = '//android.widget.Button[@text="삭제"]' # '삭제' 텍스트를 가진 버튼을 우선적으로 찾음
        try:
            delete_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, delete_button_xpath))
            )
            delete_button.click()
            print("✅ '삭제' 버튼을 클릭하여 원래 앱으로 복귀를 시도합니다.")
            time.sleep(3) # 화면이 완전히 돌아올 때까지 대기
        except TimeoutException:
            error_msg = "실패: 페이스북에서 '삭제' 버튼을 찾을 수 없어 원래 앱으로 돌아가지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "facebook_delete_button_not_found")
            return False, error_msg

        return True, "페이스북 공유 기능 검증 성공."

    except Exception as e:
        return False, f"페이스북 공유 테스트 중 예외 발생: {e}"
    finally:
        print("--- (Checklist-89) e카탈로그 페이스북 공유 시나리오 종료 ---")


def test_download_catalog(flow_tester):
    """
    (Checklist-90) e카탈로그 다운로드 기능을 검증합니다. (AOS 기준)
    다운로드 버튼 선택 > 다운로드 Confirm창 노출 > 확인 버튼 선택
    """
    print("\n--- (Checklist-90) e카탈로그 다운로드 시나리오 시작 ---")
    try:
        # ※ 사전 조건: e카탈로그 상세 화면에 진입한 상태라고 가정합니다.

        # 1. '다운로드' 버튼 클릭
        download_button_xpath = '//android.widget.Button[@text="다운로드"]'
        print(f"'{download_button_xpath}' (다운로드) 버튼을 클릭합니다.")
        try:
            download_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, download_button_xpath))
            )
            download_button.click()
        except TimeoutException:
            error_msg = "실패: '다운로드' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "download_button_not_found")
            return False, error_msg

        # 2. '다운로드 Confirm' 팝업창에서 '확인' 버튼 노출 확인 및 클릭
        confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
        print(f"다운로드 확인 팝업에서 '{confirm_button_xpath}' (확인) 버튼을 찾아 클릭합니다.")
        try:
            confirm_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, confirm_button_xpath))
            )
            print("✅ 다운로드 확인 팝업이 성공적으로 노출되었습니다.")
            confirm_button.click()
            print("다운로드를 시작했습니다.")
            flow_tester.driver.back()
            time.sleep(2)
            flow_tester.driver.back()
            time.sleep(2)
        except TimeoutException:
            error_msg = "실패: 다운로드 확인 팝업 또는 '확인' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "download_confirm_popup_not_found")
            return False, error_msg

        # ※ 참고: 실제 파일 다운로드 완료 여부는 Appium 테스트 범위를 벗어날 수 있으므로,
        # '확인' 버튼 클릭까지만 검증합니다.
        time.sleep(2)
        return True, "카탈로그 다운로드 기능 검증 성공."

    except Exception as e:
        return False, f"카탈로그 다운로드 테스트 중 예외 발생: {e}"
    finally:
        print("--- (Checklist-90) e카탈로그 다운로드 시나리오 종료 ---")