# PythonProject/Home/test_Home_01.py

import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy  # AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Deprecated된 TouchAction 대신 W3C Actions 관련 모듈 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder # Appium 2.x 이상에서 TouchAction 대체 시 필요

from Base.base_driver import BaseAppiumDriver
#from Login.test_login_view import AppiumLoginviewTest

# 새롭게 추가된 배너 스와이프 헬퍼 메서드
def perform_home_banner_swipe(flow_tester):
    """
    홈 화면에서 배너를 우측에서 좌측으로 3회 스와이프하는 W3C Actions 스크립트.
    """
    # --- 추가된 부분: 메인 화면 로딩 완료 확인 ---
    print("\n--- 메인 화면 로딩 완료 확인 시작 ---")
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]' # 메인 화면 로딩을 나타내는 요소
    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")
    except TimeoutException:
        print("❌ 메인 화면 로딩 타임아웃: '전체메뉴' 요소를 찾을 수 없습니다.")
        return False, "메인 화면 로딩 실패: '전체메뉴' 요소 타임아웃."
    except Exception as e:
        print(f"❌ 메인 화면 로딩 확인 중 오류 발생: {e}")
        return False, f"메인 화면 로딩 확인 실패: {e}"
    print("--- 메인 화면 로딩 완료 확인 종료 ---\n")
    time.sleep(5)

    # 3. 배너가 보일 때까지 스크롤 (최대 5회 시도)
    print(" 배너가 보일 때까지 스크롤을 시도합니다. (배너 가시성 확인 제외)")
    max_scroll_attempts = 1  # 스크롤 시도 횟수

    # --- 수정된 부분: 배너 가시성 확인 스크립트 제외 ---
    for i in range(max_scroll_attempts):
        print(f"스크롤 다운 ({i + 1}/{max_scroll_attempts})...")
        actions = ActionChains(flow_tester.driver)
        actions.w3c_actions = ActionBuilder(flow_tester.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(556, 1991)  # 스크롤 시작 좌표 (예: 화면 하단)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(553, 1100)  # 스크롤 끝 좌표 (예: 화면 상단)
        actions.w3c_actions.pointer_action.release()
        actions.perform()  # 스크롤 액션 실행
        time.sleep(2)  # 스크롤 후 요소 로딩 대기
    # --- 수정된 부분 끝 ---

    # 스크롤이 완료되면 배너가 나타났다고 가정하고 다음 단계로 진행
    print("✅ 지정된 횟수만큼 스크롤을 완료했습니다. 이제 배너 스와이프를 시도합니다.")

    # 7. 홈 화면 배너 스와이프 (우측에서 좌측으로)
    print("\n--- 홈 화면 배너 스와이프 시도 (우측에서 좌측으로) ---")
    try:
        screen_size = flow_tester.driver.get_window_size()
        start_x = screen_size['width'] * 0.9  # 화면 우측 90% 지점에서 시작
        end_x = screen_size['width'] * 0.1  # 화면 좌측 10% 지점까지 스와이프
        mid_y = screen_size['height'] // 3  # 화면 높이의 1/3 지점 (배너가 보통 이 위치에 있을 것이라고 가정)

        # 배너 스와이프를 3회 수행
        for i in range(3):
            # W3C Actions JSON 형식으로 스와이프 수행
            actions_payload = {
                "actions": [
                    {
                        "type": "pointer",
                        "id": "finger1",
                        "parameters": {"pointerType": "touch"},
                        "actions": [
                            {"type": "pointerMove", "duration": 0, "x": 929, "y": 551},
                            {"type": "pointerDown", "button": 0},
                            {"type": "pointerMove", "duration": 100, "x": 14, "y": 565},
                            {"type": "pointerUp", "button": 0}
                        ]
                    }
                ]
            }

            flow_tester.driver.execute("actions",
                                       actions_payload)  # driver.perform() 대신 driver.execute("actions", ...) 사용

            print(f"✅ 배너 스와이프 (우측 -> 좌측) {i + 1}회 완료.")
            time.sleep(3)  # 스와이프 후 배너 전환 대기 (각 스와이프마다 대기)

        # 배너 클릭
        print("\n--- 배너 클릭 시도 ---")
        click_x = 556  # 화면 중앙 X 좌표
        click_y = 670  # 배너의 예상 Y 좌표 (스와이프에 사용된 mid_y 재활용)

        actions = ActionChains(flow_tester.driver)
        actions.w3c_actions = ActionBuilder(flow_tester.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(int(click_x), int(click_y))
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(int(click_x), int(click_y))
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print(f"✅ 배너 클릭 완료 (좌표: {click_x}, {click_y}).")
        time.sleep(3)  # 클릭 후 페이지 로딩 대기
        # 배너 클릭 완료

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 홈 페이지로 돌아오는 시간 대기

    except Exception as e:
        print(f"❌ 배너 스와이프 중 오류 발생: {e}")
        return False, f"배너 스와이프 기능 실패: {e}"  # 오류 발생 시 실패 반환
    print("--- 홈 화면 배너 스와이프 종료 ---\n")
    return True, "배너 스와이프 기능 성공."

def run_home_navigation_scenario(flow_tester):
    """
    홈 화면에서 검색 아이콘 클릭 -> 뒤로가기 -> 공지사항 버튼 클릭 -> 공지사항 상세화면 진입 -> 뒤로가기
    시나리오를 실행합니다.
    """
    print("\n--- 홈 화면 내비게이션 시나리오 시작 ---")

    scenario_passed = False

    try:
        print("앱이 성공적으로 실행되었습니다.")

        # 1. 검색 아이콘 클릭
        print(" '검색 아이콘'을 찾고 클릭합니다.")
        search_icon_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
        try:
            search_icon_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, search_icon_xpath)),
                message=f"'{search_icon_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            search_icon_button.click()
            print(" '검색 아이콘' 클릭 완료.")
            time.sleep(3)  # 페이지 전환 대기
        except Exception as e:
            print(f" '검색 아이콘' 클릭 중 오류 발생: {e}")
            return False, f"검색 아이콘 클릭 실패: {e}"

        # 2. 뒤로가기 (Back) 액션 수행 (키보드 해제)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 홈 페이지로 돌아오는 시간 대기

        # 2. 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 홈 페이지로 돌아오는 시간 대기

        # 3. 공지사항 버튼이 보일 때까지 스크롤 (최대 5회 시도)
        print(" '공지사항' 버튼이 보일 때까지 스크롤을 시도합니다.")
        max_scroll_attempts = 5
        notice_button_found = False
        notice_button_xpath = '//android.view.View[@content-desc="공지사항"]'  # The XPath for the notice button

        for i in range(max_scroll_attempts):
            try:
                # 공지사항 버튼이 현재 보이는지 확인
                notice_button = flow_tester.driver.find_element(AppiumBy.XPATH, notice_button_xpath)
                if notice_button.is_displayed():
                    print(f"✅ '공지사항' 버튼이 화면에 노출되었습니다. 스크롤 시도 {i + 1}회.")
                    notice_button_found = True
                    break
            except NoSuchElementException:
                print(f"공지사항 버튼을 찾을 수 없습니다. 스크롤 다운 ({i + 1}/{max_scroll_attempts})...")
                # 화면 크기를 가져와서 스크롤 시작점과 끝점 계산
                screen_size = flow_tester.driver.get_window_size()
                start_x = screen_size['width'] // 2
                start_y = screen_size['height'] * 0.8  # 화면 하단 80% 지점에서 시작
                end_y = screen_size['height'] * 0.2  # 화면 상단 20% 지점까지 스크롤

                # W3C Actions를 사용하여 스크롤 구현
                finger = PointerInput(interaction.POINTER_TOUCH, "finger")
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver, mouse=finger)

                # 스크롤 동작 정의 (누르고, 이동하고, 떼기)
                actions.w3c_actions.pointer_action.move_to_location(int(start_x), int(start_y))
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.2)  # 짧은 일시 정지
                actions.w3c_actions.pointer_action.move_to_location(int(start_x), int(end_y))
                actions.w3c_actions.pointer_action.release()

                # 액션 실행
                actions.perform()
                time.sleep(2)  # 스크롤 후 요소 로딩 대기

        if not notice_button_found:
            print("❌ '공지사항' 버튼을 찾을 수 없거나 스크롤 후에도 나타나지 않았습니다.")
            return False, "공지사항 버튼을 찾을 수 없습니다."

        # 4. 공지사항 버튼 클릭
        print(" '공지사항' 버튼을 찾고 클릭합니다.")
        notice_button_xpath = '//android.view.View[@content-desc="공지사항"]'
        try:
            notice_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, notice_button_xpath)),
                message=f"'{notice_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            notice_button.click()
            print(" '공지사항' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기

            print("공지사항 상세화면 진입 후, 특정 좌표(675, 675)를 터치하여 상호작용을 시도합니다.")
            actions = ActionChains(flow_tester.driver)
            actions.w3c_actions = ActionBuilder(flow_tester.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(675, 675)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            print("좌표 (675, 675) 터치 완료.")
            time.sleep(2)  # 터치 후 반응 대기
            # ************************************************************

        except TimeoutException:
            print("❌ 메인 페이지 요소 확인 타임아웃: 로그인 성공 후 예상되는 메인 페이지 요소를 찾을 수 없습니다.")
            return False, "메인 페이지 요소 확인 타임아웃: 로그인 성공 후 예상되는 메인 페이지 요소를 찾을 수 없습니다."
        except Exception as e:
            print(f" '공지사항' 버튼 클릭 중 오류 발생: {e}")
            return False, f"공지사항 버튼 클릭 실패: {e}"

        # 5. 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 홈 페이지로 돌아오는 시간 대기
        """
        # 4. 공지사항 상세화면 진입 확인
        print("공지사항 상세화면 진입을 확인합니다.")
        notice_detail_screen_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[3]/android.widget.ListView/android.view.View[1]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, notice_detail_screen_xpath)),
                message="공지사항 상세화면 요소를 20초 내에 찾지 못했습니다."
            )
            print("✅ 공지사항 상세화면 진입 확인 완료.")
        except Exception as e:
            print(f"공지사항 상세화면 진입 확인 실패: {e}")
            return False, f"공지사항 상세화면 진입 실패: {e}"

        # 5. 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 홈 페이지로 돌아오는 시간 대기
        """
        # 홈 화면으로 성공적으로 돌아왔는지 UI 요소 재확인 (예: 전체 메뉴 버튼)
        print("\n--- 뒤로가기 후 홈 화면 UI 요소 재확인 시작 ---")
        home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
                message="뒤로가기 후 홈 화면의 '전체메뉴' 요소를 찾지 못했습니다."
            )
            print("✅ 뒤로가기 후 홈 화면으로 성공적으로 돌아왔음을 확인했습니다.")
            scenario_passed = True
        except Exception as e:
            print(f"❌ 뒤로가기 후 홈 화면으로 돌아왔는지 확인 실패: {e}")
            scenario_passed = False
        print("--- 홈 화면 UI 요소 재확인 종료 ---\n")

    except Exception as e:
        print(f"🚨 홈 화면 내비게이션 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        return scenario_passed, f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 홈 화면 내비게이션 시나리오 종료 ---\n")

    if scenario_passed:
        return True, "홈 화면 내비게이션 시나리오 성공."
    else:
        return False, "홈 화면 내비게이션 시나리오 실패."

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, test_Scenario_01.py에서 호출됩니다.")