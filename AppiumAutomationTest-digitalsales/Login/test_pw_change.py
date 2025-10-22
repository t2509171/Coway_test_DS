# PythonProject/Login/test_password_change_flow.py

import sys
import os
import time

# Ensure the project root is in the path to import Base and Login modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy  # AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Base.base_driver import BaseAppiumDriver
#from Login.test_login_view import AppiumLoginviewTest # 이 임포트는 더 이상 필요 없을 수 있습니다.

# Xpath 저장소에서 LoginLocators 임포트
from Xpath.xpath_repository import LoginLocators


def run_password_change_button_back_scenario(flow_tester):
    """
    로그인 페이지에서 '비밀번호 변경' 버튼 클릭 후 뒤로가기하여
    다시 로그인 페이지로 이동하는 시나리오를 실행합니다.
    """
    print("\n--- 비밀번호 변경 페이지 진입 후 뒤로가기 시나리오 시작 ---")

    # 현재 플랫폼에 맞는 로케이터 세트를 선택합니다. (AOS 가정)
    locators = LoginLocators.AOS

    scenario_passed = True

    try:
        print("앱이 성공적으로 실행되었습니다.")

        # '비밀번호 변경' 버튼 클릭
        print(" '비밀번호 변경' 버튼을 찾고 클릭합니다.")
        password_change_button_xpath = locators.password_change_button_xpath # 수정됨
        try:
            password_change_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, password_change_button_xpath)),
                message=f"'{password_change_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            password_change_button.click()
            print(" '비밀번호 변경' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            print(f" '비밀번호 변경' 버튼 클릭 중 오류 발생: {e}")
            return False, f"비밀번호 변경 버튼 클릭 실패: {e}"

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 로그인 페이지로 돌아오는 시간 대기

        # 로그인 페이지로 돌아왔는지 확인 (예: 로그인 버튼 존재 확인)
        print("로그인 페이지로 복귀했는지 확인합니다.")
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, locators.login_button)), # 수정됨
                message="뒤로가기 후 로그인 버튼을 찾을 수 없습니다."
            )
            print("✅ 로그인 페이지로 성공적으로 복귀했습니다.")
            scenario_passed = True
        except TimeoutException:
            print("❌ 뒤로가기 후 로그인 페이지 복귀 확인 실패.")
            scenario_passed = False


    except Exception as e:
        print(f"🚨 비밀번호 변경 페이지 진입 후 뒤로가기 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        return scenario_passed, f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        #flow_tester.teardown_driver()
        print("--- 비밀번호 변경 페이지 진입 후 뒤로가기 시나리오 종료 ---\n")

    if scenario_passed:
        return True, "로그인 페이지에서 '비밀번호 변경' 후 뒤로가기 성공."
    else:
        return False, "로그인 페이지에서 '비밀번호 변경' 후 뒤로가기 실패."


def run_password_reset_button_back_scenario(flow_tester):
    """
    로그인 페이지에서 '비밀번호 초기화' 버튼 클릭 후 뒤로가기하여
    다시 로그인 페이지로 이동하는 시나리오를 실행합니다.
    """
    print("\n--- 비밀번호 초기화 페이지 진입 후 뒤로가기 시나리오 시작 ---")

    # 현재 플랫폼에 맞는 로케이터 세트를 선택합니다. (AOS 가정)
    locators = LoginLocators.AOS

    scenario_passed = True

    try:
        print("앱이 성공적으로 실행되었습니다.")

        # '비밀번호 초기화' 버튼 클릭
        print(" '비밀번호 초기화' 버튼을 찾고 클릭합니다.")
        password_reset_button_xpath = locators.password_reset_button_xpath # 수정됨
        try:
            password_reset_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, password_reset_button_xpath)),
                message=f"'{password_reset_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            password_reset_button.click()
            print(" '비밀번호 초기화' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            print(f" '비밀번호 초기화' 버튼 클릭 중 오류 발생: {e}")
            return False, f"비밀번호 초기화 버튼 클릭 실패: {e}"

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 로그인 페이지로 돌아오는 시간 대기

        # 로그인 페이지로 돌아왔는지 확인 (예: 로그인 버튼 존재 확인)
        print("로그인 페이지로 복귀했는지 확인합니다.")
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, locators.login_button)), # 수정됨
                message="뒤로가기 후 로그인 버튼을 찾을 수 없습니다."
            )
            print("✅ 로그인 페이지로 성공적으로 복귀했습니다.")
            scenario_passed = True
        except TimeoutException:
            print("❌ 뒤로가기 후 로그인 페이지 복귀 확인 실패.")
            scenario_passed = False

    except Exception as e:
        print(f"🚨 비밀번호 초기화 페이지 진입 후 뒤로가기 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        return scenario_passed, f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 비밀번호 초기화 페이지 진입 후 뒤로가기 시나리오 종료 ---\n")

    if scenario_passed:
        return True, "로그인 페이지에서 '비밀번호 초기화' 후 뒤로가기 성공."
    else:
        return False, "로그인 페이지에서 '비밀번호 초기화' 후 뒤로가기 실패."


if __name__ == "__main__":
    # 각 시나리오를 개별적으로 실행하려면 아래 주석을 해제하고 사용하세요.
    print("이 파일은 이제 개별 함수를 포함하며, test_Scenario_01.py에서 호출됩니다.")










# # PythonProject/Login/test_password_change_flow.py
#
# import sys
# import os
# import time
#
# # Ensure the project root is in the path to import Base and Login modules
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# # 필요한 라이브러리 임포트
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy  # AppiumBy
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# from Base.base_driver import BaseAppiumDriver
# from Login.test_login_view import AppiumLoginviewTest
#
#
# def run_password_change_button_back_scenario(flow_tester):
#     """
#     로그인 페이지에서 '비밀번호 변경' 버튼 클릭 후 뒤로가기하여
#     다시 로그인 페이지로 이동하는 시나리오를 실행합니다.
#     """
#     print("\n--- 비밀번호 변경 페이지 진입 후 뒤로가기 시나리오 시작 ---")
#
#     scenario_passed = True
#
#     try:
#         print("앱이 성공적으로 실행되었습니다.")
#         """
#         print("\n--- 초기 로그인 화면 UI 요소 노출 테스트 시작 ---")
#         initial_ui_elements_ok = flow_tester.verify_login_ui_elements()
#         if not initial_ui_elements_ok:
#             print("⚠️ 경고: 초기 로그인 화면의 일부 UI 요소가 정상적으로 노출되지 않았습니다. 계속 진행.")
#         print("--- 초기 로그인 화면 UI 요소 노출 테스트 종료 ---\n")
#         """
#         # '비밀번호 변경' 버튼 클릭
#         print(" '비밀번호 변경' 버튼을 찾고 클릭합니다.")
#         password_change_button_xpath = '//android.widget.Button[@text="비밀번호 변경"]'
#         try:
#             password_change_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, password_change_button_xpath)),
#                 message=f"'{password_change_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             password_change_button.click()
#             print(" '비밀번호 변경' 버튼 클릭 완료.")
#             time.sleep(5)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" '비밀번호 변경' 버튼 클릭 중 오류 발생: {e}")
#             return False, f"비밀번호 변경 버튼 클릭 실패: {e}"
#
#         # 뒤로가기 (Back) 액션 수행
#         print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
#         flow_tester.driver.back()
#         print("뒤로가기 액션 수행 완료.")
#         time.sleep(3)  # 로그인 페이지로 돌아오는 시간 대기
#
#         # # 로그인 페이지로 성공적으로 돌아왔는지 UI 요소 재확인
#         # print("\n--- 뒤로가기 후 로그인 화면 UI 요소 재확인 시작 ---")
#         # return_ui_elements_ok = flow_tester.verify_login_ui_elements()
#         # if return_ui_elements_ok:
#         #     print("✅ 뒤로가기 후 모든 로그인 화면 UI 요소가 정상적으로 노출되었습니다.")
#         #     scenario_passed = True
#         # else:
#         #     print("❌ 뒤로가기 후 일부 로그인 화면 UI 요소 노출에 문제가 있습니다. 시나리오 실패.")
#         #     scenario_passed = False
#         # print("--- 뒤로가기 후 로그인 화면 UI 요소 재확인 종료 ---\n")
#
#     except Exception as e:
#         print(f"🚨 비밀번호 변경 페이지 진입 후 뒤로가기 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         return scenario_passed, f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         #flow_tester.teardown_driver()
#         print("--- 비밀번호 변경 페이지 진입 후 뒤로가기 시나리오 종료 ---\n")
#
#     if scenario_passed:
#         return True, "로그인 페이지에서 '비밀번호 변경' 후 뒤로가기 성공."
#     else:
#         return False, "로그인 페이지에서 '비밀번호 변경' 후 뒤로가기 실패."
#
#
# def run_password_reset_button_back_scenario(flow_tester):
#     """
#     로그인 페이지에서 '비밀번호 초기화' 버튼 클릭 후 뒤로가기하여
#     다시 로그인 페이지로 이동하는 시나리오를 실행합니다.
#     """
#     print("\n--- 비밀번호 초기화 페이지 진입 후 뒤로가기 시나리오 시작 ---")
#
#     scenario_passed = True
#
#     try:
#         print("앱이 성공적으로 실행되었습니다.")
#         """
#         print("\n--- 초기 로그인 화면 UI 요소 노출 테스트 시작 ---")
#         initial_ui_elements_ok = flow_tester.verify_login_ui_elements()
#         if not initial_ui_elements_ok:
#             print("⚠️ 경고: 초기 로그인 화면의 일부 UI 요소가 정상적으로 노출되지 않았습니다. 계속 진행.")
#         print("--- 초기 로그인 화면 UI 요소 노출 테스트 종료 ---\n")
#         """
#         # '비밀번호 초기화' 버튼 클릭
#         print(" '비밀번호 초기화' 버튼을 찾고 클릭합니다.")
#         password_reset_button_xpath = '//android.widget.Button[@text="비밀번호 초기화"]'
#         try:
#             password_reset_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, password_reset_button_xpath)),
#                 message=f"'{password_reset_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             password_reset_button.click()
#             print(" '비밀번호 초기화' 버튼 클릭 완료.")
#             time.sleep(5)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" '비밀번호 초기화' 버튼 클릭 중 오류 발생: {e}")
#             return False, f"비밀번호 초기화 버튼 클릭 실패: {e}"
#
#         # 뒤로가기 (Back) 액션 수행
#         print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
#         flow_tester.driver.back()
#         print("뒤로가기 액션 수행 완료.")
#         time.sleep(3)  # 로그인 페이지로 돌아오는 시간 대기
#
#         # # 로그인 페이지로 성공적으로 돌아왔는지 UI 요소 재확인
#         # print("\n--- 뒤로가기 후 로그인 화면 UI 요소 재확인 시작 ---")
#         # return_ui_elements_ok = flow_tester.verify_login_ui_elements()
#         # if return_ui_elements_ok:
#         #     print("✅ 뒤로가기 후 모든 로그인 화면 UI 요소가 정상적으로 노출되었습니다.")
#         #     scenario_passed = True
#         # else:
#         #     print("❌ 뒤로가기 후 일부 로그인 화면 UI 요소 노출에 문제가 있습니다. 시나리오 실패.")
#         #     scenario_passed = False
#         # print("--- 뒤로가기 후 로그인 화면 UI 요소 재확인 종료 ---\n")
#
#     except Exception as e:
#         print(f"🚨 비밀번호 초기화 페이지 진입 후 뒤로가기 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         return scenario_passed, f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 비밀번호 초기화 페이지 진입 후 뒤로가기 시나리오 종료 ---\n")
#
#     if scenario_passed:
#         return True, "로그인 페이지에서 '비밀번호 초기화' 후 뒤로가기 성공."
#     else:
#         return False, "로그인 페이지에서 '비밀번호 초기화' 후 뒤로가기 실패."
#
#
# if __name__ == "__main__":
#     # 각 시나리오를 개별적으로 실행하려면 아래 주석을 해제하고 사용하세요.
#     print("이 파일은 이제 개별 함수를 포함하며, test_Scenario_01.py에서 호출됩니다.")