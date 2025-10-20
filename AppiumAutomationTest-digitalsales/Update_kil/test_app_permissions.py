import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# FlowTester 클래스를 직접 import 합니다.
from Login.test_login_view import AppiumLoginviewTest
from Base.base_driver import BaseAppiumDriver
# 로그인 관련 함수들을 import 합니다.
from Utils.login_with_credentials import login_with_credentials
from Utils.scrolling_function import scroll_down
from Utils.screenshot_helper import save_screenshot_on_failure

def test_verify_permission_guide_title(flow_tester):
    """
    화면 특정 좌표를 터치한 후, '접근 권한 안내' 타이틀이 노출되는지 검증합니다.
    """
    print("\n--- [1/4] 접근 권한 안내 화면 > 타이틀 노출 확인 시나리오 시작 ---")
    try:
        # 1. 화면 활성화를 위해 좌표 터치
        coords_to_tap = (550, 550)
        print(f"화면 활성화를 위해 {coords_to_tap} 좌표를 클릭합니다.")
        try:
            flow_tester.driver.tap([coords_to_tap])
            time.sleep(1)
        except Exception as e:
            error_msg = f"실패: 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "permission_screen_tap_failed")
            return False, error_msg

        # 2. 접근 권한 안내 타이틀 노출 확인
        title_xpath = '//android.widget.TextView[@text="디지털세일즈 앱 사용 접근 권한 안내"]'
        print(f"'{title_xpath}' (안내 타이틀)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, title_xpath))
            )
            print("✅ '접근 권한 안내' 타이틀이 성공적으로 노출되었습니다.")
            return True, "접근 권한 안내 타이틀 확인 성공."
        except TimeoutException:
            error_msg = "실패: 좌표 터치 후 '접근 권한 안내' 타이틀을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "permission_title_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"접근 권한 타이틀 확인 중 예외 발생: {e}"
    finally:
        print("--- [1/4] 접근 권한 안내 화면 > 타이틀 노출 확인 시나리오 종료 ---")


def test_verify_required_permissions(flow_tester):
    """
    '필수적 접근권한' 섹션이 노출되는지 검증합니다.
    """
    print("\n--- [2/4] 접근 권한 안내 화면 > '필수적 접근권한' 확인 시나리오 시작 ---")
    try:
        # '필수적 접근권한' 텍스트 노출 확인
        required_perms_xpath = '//android.widget.TextView[@text="필수적 접근권한"]'
        print(f"'{required_perms_xpath}' (필수적 접근권한)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, required_perms_xpath))
            )
            print("✅ '필수적 접근권한' 섹션이 성공적으로 노출되었습니다.")
            return True, "'필수적 접근권한' 확인 성공."
        except TimeoutException:
            error_msg = "실패: '필수적 접근권한' 섹션을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "required_permissions_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"'필수적 접근권한' 확인 중 예외 발생: {e}"
    finally:
        print("--- [2/4] 접근 권한 안내 화면 > '필수적 접근권한' 확인 시나리오 종료 ---")


def test_verify_optional_permissions_with_scroll(flow_tester):
    """
    '선택적 접근권한' 섹션과 모든 항목들이 스크롤하며 노출되는지 검증합니다.
    """
    print("\n--- [3/4] 접근 권한 안내 화면 > '선택적 접근권한' 확인 시나리오 시작 ---")
    try:
        # 1. '선택적 접근권한' 타이틀 확인
        optional_perms_xpath = '//android.widget.TextView[@text="선택적 접근권한"]'
        print(f"'{optional_perms_xpath}' (선택적 접근권한)이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, optional_perms_xpath))
            )
            print("✅ '선택적 접근권한' 섹션이 확인되었습니다.")
        except TimeoutException:
        # 선택적 접근권한은 스크롤해야 보일 수 있으므로, 바로 실패처리하지 않고 스크롤 로직으로 넘어감
            print(" - '선택적 접근권한' 섹션이 바로 보이지 않습니다. 스크롤하며 확인합니다.")

    # 2. 스크롤하며 모든 선택 권한 항목 확인
        permissions_to_find = {
            "전화 및 통화기록": '//android.view.View[@text="전화 및 통화기록"]',
            "문자": '//android.view.View[@text="문자"]',
            "주소록": '//android.view.View[@text="주소록"]',
            "위치": '//android.view.View[@text="위치"]',
            "마이크 및 음성인식": '//android.view.View[@text="마이크 및 음성인식"]',
            "저장소": '//android.view.View[@text="저장소"]'
        }
        found_permissions = set()
        max_scrolls = 5

        for i in range(max_scrolls):
            # 현재 화면에서 보이는 모든 권한 항목을 찾음
            for name, xpath in permissions_to_find.items():
                if name not in found_permissions:  # 아직 못 찾은 항목만 확인
                    try:
                        flow_tester.driver.find_element(AppiumBy.XPATH, xpath)
                        print(f"   ✅ '{name}' 항목을 찾았습니다.")
                        found_permissions.add(name)
                    except NoSuchElementException:
                        pass  # 현재 화면에 없으면 그냥 넘어감

            # 모든 권한을 다 찾았으면 루프 종료
            if len(found_permissions) == len(permissions_to_find):
                break

            # 다 못 찾았으면 스크롤
            if i < max_scrolls - 1:
                print(f"({i + 1}/{max_scrolls}) 아직 모든 항목을 찾지 못했습니다. 스크롤 다운.")
                scroll_down(flow_tester.driver)
                time.sleep(1)

        # 3. 최종 결과 판정
        if len(found_permissions) == len(permissions_to_find):
            print("✅ 스크롤을 통해 모든 '선택적 접근권한' 항목을 성공적으로 찾았습니다.")
            return True, "'선택적 접근권한' 항목 확인 성공."
        else:
            # 찾지 못한 항목들을 계산하여 에러 메시지 생성
            missing_permissions = set(permissions_to_find.keys()) - found_permissions
            error_msg = f"실패: {max_scrolls}번 스크롤 후에도 다음 '선택적 접근권한' 항목을 찾지 못했습니다: {list(missing_permissions)}"
            save_screenshot_on_failure(flow_tester.driver, "optional_permissions_missing")
            return False, error_msg
    except Exception as e:
        return False, f"'선택적 접근권한' 확인 중 예외 발생: {e}"
    finally:
        print("--- [3/4] 접근 권한 안내 화면 > '선택적 접근권한' 확인 시나리오 종료 ---")


def test_confirm_permissions_and_navigate_to_login(flow_tester):
    """
    권한 안내 화면의 '확인' 버튼을 클릭하고 '로그인' 버튼이 노출되는지 검증합니다.
    """
    print("\n--- [4/4] 접근 권한 '확인' 후 로그인 화면 이동 확인 시나리오 시작 ---")
    try:
        # 1. '확인' 버튼 클릭
        confirm_button_xpath = '//android.widget.Button[@text="확인"]'
        print(f"'{confirm_button_xpath}' (확인) 버튼을 클릭합니다.")
        try:
            confirm_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, confirm_button_xpath))
            )
            confirm_button.click()
        except TimeoutException:
            error_msg = "실패: 접근 권한 안내 화면의 '확인' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "permission_confirm_btn_not_found")
            return False, error_msg

        # 2. '로그인' 버튼 노출 확인
        login_button_xpath = '//android.widget.Button[@text="로그인"]'
        print(f"'{login_button_xpath}' (로그인) 버튼이 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, login_button_xpath))
            )
            print("✅ '로그인' 버튼이 성공적으로 노출되었습니다.")
            return True, "권한 확인 후 로그인 화면 이동 성공."
        except TimeoutException:
            error_msg = "실패: '확인' 버튼 클릭 후 '로그인' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "login_button_not_found_after_permission")
            return False, error_msg

    except Exception as e:
        return False, f"권한 확인 후 로그인 화면 이동 중 예외 발생: {e}"
    finally:
        print("--- [4/4] 접근 권한 '확인' 후 로그인 화면 이동 확인 시나리오 종료 ---")



# 기존 test_verify_no_update_alert_after_relaunch 함수를 아래 코드로 교체하세요.

def test_login_after_relaunch_and_verify_version(flow_tester):
    """
    앱을 재시작한 후, 자동 로그인하여 최신 버전 요소가 노출되는지 검증합니다.
    """
    print("\n--- [5/6] 앱 재실행 > 자동 로그인 및 최신 버전 확인 시나리오 시작 ---")
    try:
        # 2. 자동 로그인 수행
        print("자동 로그인을 시작합니다.")
        try:
            user_id ="CWDS#QCL1"
            user_pw ="Test1234!"
            login_successful, message = login_with_credentials(flow_tester, user_id, user_pw)

            if not login_successful:
                return False, message

            print("\n[추가 단계] 시스템 접근 권한 팝업이 있는지 확인합니다 (5초 대기).")


        except Exception as login_e:
            error_msg = f"실패: 자동 로그인 과정에서 예외가 발생했습니다: {login_e}"
            save_screenshot_on_failure(flow_tester.driver, "auto_login_exception_after_relaunch")
            return False, error_msg

        # 3. 전체 메뉴에서 '최신 버전 입니다.' 텍스트 확인
        print("\n[3단계] 전체 메뉴에서 '최신 버전 입니다.' 텍스트를 스크롤하여 확인합니다.")
        try:
            menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
            menu_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
            )
            menu_button.click()
            print(" - 전체 메뉴 버튼을 클릭했습니다.")
            time.sleep(2)

            latest_version_xpath = '//android.widget.TextView[@text="최신 버전 입니다."]'
            max_scrolls = 7
            element_found = False

            for i in range(max_scrolls):
                try:
                    flow_tester.driver.find_element(AppiumBy.XPATH, latest_version_xpath)
                    print(f"✅ '최신 버전 입니다.' 텍스트를 찾았습니다. (시도: {i + 1}번)")
                    element_found = True
                    break
                except NoSuchElementException:
                    print(f"({i + 1}/{max_scrolls}) 텍스트를 찾지 못했습니다. 아래로 스크롤합니다.")
                    scroll_down(flow_tester.driver)
                    time.sleep(0.5)

            if not element_found:
                error_msg = f"실패: {max_scrolls}번 스크롤 후에도 '최신 버전 입니다.' 텍스트를 찾지 못했습니다."
                save_screenshot_on_failure(flow_tester.driver, "latest_version_text_not_found")
                return False, error_msg

        except Exception as e:
            error_msg = f"실패: 최신 버전 확인 중 예외가 발생했습니다: {e}"
            save_screenshot_on_failure(flow_tester.driver, "verify_version_exception")
            return False, error_msg


        return True, "앱 재실행, 자동 로그인, 최신 버전 확인 모두 성공."

    except Exception as e:
        return False, f"앱 재실행 및 버전 확인 중 예외 발생: {e}"
    finally:
        print("--- [5/6] 앱 재실행 > 자동 로그인 및 최신 버전 확인 시나리오 종료 ---")


# 기존 test_relaunch_and_verify_webview 함수를 아래 코드로 교체합니다.

def test_verify_no_permission_guide_after_relaunch(flow_tester):
    """
    앱 재실행 후, 이전에 확인했던 '접근권한 안내' 화면이 다시 노출되지 않는지 검증합니다.
    """
    flow_tester.driver.back()
    flow_tester.driver.back()
    time.sleep(2)
    flow_tester.teardown_driver()
    time.sleep(3)

    print("\n--- [6/6] 앱 재실행 > 접근 권한 안내 미노출 확인 시나리오 시작 ---")
    try:
        # 1. teardown_driver()와 setup_driver()를 이용한 앱 재실행
        print("테스트를 위해 teardown_driver()를 호출하여 드라이버 세션을 종료합니다.")
        if flow_tester.driver:
            flow_tester.teardown_driver()
        time.sleep(3)

        print("setup_driver()를 호출하여 새로운 드라이버 세션을 시작하고 앱을 실행합니다.")
        flow_tester.setup_driver()
        print("✅ 앱이 성공적으로 재실행되었습니다.")

        print("앱 안정화를 위해 8초간 대기합니다...")
        time.sleep(8)

        # 2. 접근권한 안내 화면이 '나타나지 않는지' 확인 (로직 수정)
        permission_title_xpath = '//android.widget.TextView[@text="디지털세일즈 앱 사용 접근 권한 안내"]'
        print(f"'{permission_title_xpath}' (접근 권한 안내)가 노출되지 않는지 확인합니다 (5초 대기).")
        try:
            # 5초 내에 요소가 '발견되면' 테스트 실패
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, permission_title_xpath))
            )
            # 이 코드가 실행된다는 것은 요소가 화면에 나타났다는 의미이므로 실패 처리
            error_msg = "실패: 앱 재실행 후 접근 권한 안내 화면이 다시 노출되었습니다."
            save_screenshot_on_failure(flow_tester.driver, "permission_guide_reappeared")
            return False, error_msg

        except TimeoutException:
            # 5초 동안 요소를 찾지 못하면 TimeoutException이 발생하며, 이것이 성공 케이스
            print("✅ 접근 권한 안내 화면이 노출되지 않았습니다. (성공)")
            print("테스트를 위해 teardown_driver()를 호출하여 드라이버 세션을 종료합니다.")
            if flow_tester.driver:
                flow_tester.teardown_driver()
            time.sleep(3)

            print("setup_driver()를 호출하여 새로운 드라이버 세션을 시작하고 앱을 실행합니다.")
            flow_tester.setup_driver()
            print("✅ 앱이 성공적으로 재실행되었습니다.")

            print("앱 안정화를 위해 8초간 대기합니다...")
            time.sleep(8)
            return True, "앱 재실행 후 접근 권한 안내 미노출 확인 성공."

    except Exception as e:
        return False, f"접근 권한 미노출 확인 중 예외 발생: {e}"
    finally:
        print("--- [6/6] 앱 재실행 > 접근 권한 안내 미노출 확인 시나리오 종료 ---")
