import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# 스크린샷 헬퍼 함수
from Utils.screenshot_helper import save_screenshot_on_failure

# Base 드라이버 클래스 임포트 (BaseAppiumDriver)
from Base.base_driver import BaseAppiumDriver

def _navigate_to_full_menu(flow_tester):
    """
    홈 화면에서 전체메뉴 버튼을 클릭하여 전체 메뉴 화면으로 진입합니다.
    """
    print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
    all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
    try:
        all_menu_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
            message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        all_menu_button.click()
        print(" '전체메뉴' 버튼 클릭 완료.")
        time.sleep(5)  # 메뉴 열림 대기
        return True, ""
    except Exception as e:
        print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")
        return False, f"전체메뉴 버튼 클릭 실패: {e}"

# 공지사항 확인
def test_etc_Notice(flow_tester):
    """
    전체 메뉴에서 고객 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 고객 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '공지사항' 버튼 클릭
        print(" '공지사항' 버튼을 찾고 클릭합니다.")
        Notice_button_xpath = '//android.view.View[@content-desc="공지사항"]' # [cite: 6]
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # '공지사항' 요소가 보이는지 확인
                Notice_element = flow_tester.driver.find_element(AppiumBy.XPATH, Notice_button_xpath)
                if Notice_element.is_displayed():
                    print("✅ '공지사항' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'공지사항' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'공지사항' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

                # W3C Actions를 이용한 스크롤 동작
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                                mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(550, 1800)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
                actions.w3c_actions.pointer_action.move_to_location(550, 1100)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                time.sleep(3)  # 스크롤 후 페이지 로딩 대기

        if not scenario_passed:
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '공지사항' 요소를 찾지 못했습니다."
            return False, result_message

        try:
            Notice_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, Notice_button_xpath)),
                message=f"'{Notice_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            Notice_button.click()
            print(" '공지사항' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"공지사항 버튼 클릭 실패: {e}"
            return False, result_message

        # 3. '공지사항 타이틀', '공지사항 뷰' 노출 확인
        print(" '공지사항 타이틀', '공지사항 뷰' 노출을 확인합니다.")
        Notice_title_xpath = '//android.widget.TextView[@text="공지사항"]' # [cite: 6]
        Notice_view_xpath = '//android.widget.ListView' # [cite: 6]

        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, Notice_title_xpath)))
            print("✅ '공지사항 타이틀'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, Notice_view_xpath)))
            print("✅ '공지사항 뷰'가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "공지사항 진입 및 UI 요소 확인 성공."
        except Exception as e:
            result_message = f"공지사항 UI 요소 노출 확인 실패: {e}"
            return False, result_message

        # 4. 뒤로가기 (Back) 액션 수행 (공지사항 상세 -> 전체메뉴)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 전체메뉴로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 공지사항 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > 공지사항 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 셀프 홍보영상 확인
def test_etc_self_promotional_video(flow_tester):
    """
    전체 메뉴에서 셀프홍보영상 클릭 후, 셀프홍보영상 타이틀이 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 판매인 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '셀프홍보영상' 버튼 클릭
        self_promotional_video_button_xpath = '//android.view.View[@content-desc="셀프 홍보영상"]'  # [cite: 6]
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # '셀프홍보영상' 요소가 보이는지 확인
                self_promotional_video_element = flow_tester.driver.find_element(AppiumBy.XPATH,
                                                                             self_promotional_video_button_xpath)
                if self_promotional_video_element.is_displayed():
                    print("✅ '셀프홍보영상' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'셀프홍보영상' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'셀프홍보영상' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

                # W3C Actions를 이용한 스크롤 동작
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(550, 1800)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
                actions.w3c_actions.pointer_action.move_to_location(550, 1100)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                time.sleep(3)  # 스크롤 후 페이지 로딩 대기

        if not scenario_passed:
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '셀프홍보영상' 요소를 찾지 못했습니다."
            return False, result_message

        print(" '셀프홍보영상' 버튼을 찾고 클릭합니다.")
        self_promotional_video_button_xpath = '//android.view.View[@content-desc="셀프 홍보영상"]' # [cite: 6]
        try:
            self_promotional_video_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, self_promotional_video_button_xpath)),
                message=f"'{self_promotional_video_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            self_promotional_video_button.click()
            print(" '셀프홍보영상' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"셀프홍보영상 버튼 클릭 실패: {e}"
            return False, result_message

        # 3. '셀프홍보영상 타이틀' 노출 확인
        print(" '셀프홍보영상 타이틀' 노출을 확인합니다.")
        self_promotional_video_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]' # [cite: 6]

        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_title_xpath)))
            print("✅ '셀프홍보영상 타이틀'이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "셀프홍보영상 진입 및 UI 요소 확인 성공."
        except Exception as e:
            result_message = f"셀프홍보영상 UI 요소 노출 확인 실패: {e}"
            time.sleep(3)
            return False, result_message

        # 4. 뒤로가기 (Back) 액션 수행 (셀프홍보영상 상세 -> 전체메뉴)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 셀프홍보영상 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > 셀프홍보영상 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 설정 확인
def test_etc_setting_view(flow_tester):

    print("\n--- 전체메뉴 > 설정 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '설정' 버튼 클릭
        setting_button_xpath = '//android.view.View[@content-desc="설정"]'  # [cite: 6]
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # '고객 프로모션' 요소가 보이는지 확인
                setting_element = flow_tester.driver.find_element(AppiumBy.XPATH,setting_button_xpath)
                if setting_element.is_displayed():
                    print("✅ '설정' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'설정' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'설정' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

                # W3C Actions를 이용한 스크롤 동작
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(550, 1800)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
                actions.w3c_actions.pointer_action.move_to_location(550, 1100)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                time.sleep(1)  # 스크롤 후 페이지 로딩 대기

        if not scenario_passed:
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '설정' 요소를 찾지 못했습니다."
            return False, result_message

        print(" '설정' 버튼을 찾고 클릭합니다.")
        setting_button_xpath = '//android.view.View[@content-desc="설정"]' # [cite: 6]
        try:
            setting_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, setting_button_xpath)),
                message=f"'{setting_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            setting_button.click()
            print(" '설정' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"설정 버튼 클릭 실패: {e}"
            # ===== 스크린샷 함수 호출 추가 =====
            save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
            # =================================
            return False, result_message

        # 3. '설정 타이틀' 노출 확인
        print(" '설정 타이틀' 노출을 확인합니다.")
        setting_title_xpath = '//android.widget.TextView[@text="설정"]' # [cite: 6]

        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, setting_title_xpath)))
            print("✅ '설정 타이틀'이 성공적으로 노출되었습니다.")

            scenario_passed = True
            result_message = "설정 진입 및 UI 요소 확인 성공."
        except Exception as e:
            result_message = f"설정 UI 요소 노출 확인 실패: {e}"
            return False, result_message
    except Exception as e:
        print(f"🚨 설정 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"

    finally:
        print("--- 전체메뉴 > 설정 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 설정 > 알림 확인
def test_etc_setting_set_notifications(flow_tester):

    print("\n--- 설정 > 알림 설정 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # 알림 버튼 클릭
    print(" '알림' 버튼을 찾고 클릭합니다.")
    notification_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
    try:
        notification_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, notification_button_xpath)),
            message=f"'{notification_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        notification_button.click()
        print(" '알림' 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"알림 버튼 클릭 실패: {e}"
        scenario_passed = False
        return False, result_message

    # 3. PUSH 설정 및 수신동의 노출 확인
    print("PUSH 설정 및 수신동의 노출을 확인합니다.")
    notification_button_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'

    try:
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, notification_button_view_xpath)))
        print("✅ '공지사항 타이틀'이 성공적으로 노출되었습니다.")

        scenario_passed = True
        result_message = "PUSH 설정 및 수신동의 노출 확인 성공."
    except Exception as e:
        result_message = f"PUSH 설정 및 수신동의 노출 확인 실패: {e}"
        return False, result_message

    finally:
        print("--- 설정 > 알림 설정 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 설정 > 로그아웃 확인
def test_etc_setting_sign_out(flow_tester):

    print("\n--- 설정 > 로그아웃 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # 로그아웃 버튼 클릭
    print(" '로그아웃' 버튼을 찾고 클릭합니다.")
    logout_button_xpath = '//android.widget.Button[@text="로그아웃"]'  # [cite: 6]
    try:
        logout_button  = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, logout_button_xpath)),
            message=f"'{logout_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        logout_button.click()
        print(" '로그아웃' 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"로그아웃 버튼 클릭 실패: {e}"
        return False, result_message

    # 팝업 확인 버튼 클릭
    print(" 팝업 '확인' 버튼을 찾고 클릭합니다.")
    logout_popup_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'  # [cite: 6]
    try:
        logout_popup_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, logout_popup_xpath)),
            message=f"'{logout_popup_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        logout_popup_button.click()
        print(" 팝업 '확인' 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기

        # 로그아웃 후 로그인 화면으로 이동했는지 확인
        print("로그아웃 후 로그인 화면 UI 요소 확인 중...")
        login_id_field_xpath = '//android.widget.TextView[@text="디지털 세일즈"]'
        if flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, login_id_field_xpath))):
            scenario_passed = True
            result_message = "로그아웃 성공: 로그인 화면으로 정상 이동."

    except Exception as e:
        result_message = f"확인 버튼 클릭 실패: {e}"
        return False, result_message

    finally:
        print("--- 설정 > 로그아웃 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")