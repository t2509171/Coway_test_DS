import sys
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException

# Import the specific test functions
from Login.test_login_view import AppiumLoginviewTest
from Test_Run.test_Scenario_01 import test_login
from Test_Run.test_lifestory_view import test_lifestory_view_run
from Utils.test_result_input import get_google_sheet_service_oauth,get_tester_name_from_sheet, SHEET_NAME,initialize_test_results_in_sheet
from Test_Run.test_mobile_order_view import test_mobile_order_view
from Test_Run.test_search_view import test_search_view_run
from Test_Run.test_my_page_view import test_my_page_view_run

# 추가: 로그인 기능을 캡슐화한 헬퍼 함수
def login_with_credentials(flow_tester, username, password):
    """지정된 계정 정보로 로그인 절차를 수행합니다."""
    print(f"\n--- 계정 '{username}'로 로그인 시도 ---")
    try:
        id_field = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="id"]')))
        id_field.clear()
        id_field.send_keys(username)
        print(f"아이디 '{username}' 입력 완료.")

        pwd_field = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="pwd"]')))
        pwd_field.clear()
        pwd_field.send_keys(password)
        print("비밀번호 입력 완료.")

        login_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="로그인"]')))
        login_button.click()
        print("로그인 버튼 클릭.")
        time.sleep(5)

        main_page_element_locator = (AppiumBy.XPATH,
                                     '//android.widget.TextView[@text="디지털세일즈"]')
        flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator))
        print(f"✅ 계정 '{username}' 로그인 성공.")
        return True, "로그인 성공"
    except TimeoutException:
        print(f"❌ 계정 '{username}' 로그인 실패: 메인 페이지 요소가 로딩되지 않았습니다.")
        return False, "로그인 실패: 메인 페이지 로딩 타임아웃."
    except Exception as e:
        print(f"🚨 계정 '{username}' 로그인 중 예상치 못한 오류 발생: {e}")
        return False, f"로그인 중 오류 발생: {e}"

def fist_login_with_credentials(flow_tester, username, password):
    """지정된 계정 정보로 로그인 절차를 수행합니다."""
    print(f"\n--- 계정 '{username}'로 로그인 시도 ---")
    try:
        id_field = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="id"]')))
        id_field.clear()
        id_field.send_keys(username)
        print(f"아이디 '{username}' 입력 완료.")

        pwd_field = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="pwd"]')))
        pwd_field.clear()
        pwd_field.send_keys(password)
        print("비밀번호 입력 완료.")

        login_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="로그인"]')))
        login_button.click()
        print("로그인 버튼 클릭.")
        time.sleep(5)
        try:
            # 권한 요청 메시지가 있는지 5초간 확인
            permission_message_xpath = '//android.widget.TextView[@resource-id="com.android.permissioncontroller:id/permission_message"]'
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, permission_message_xpath))
            )
            print("✅ 시스템 접근 권한 팝업을 발견했습니다.")

            # '앱 사용 중에만 허용' 버튼 클릭
            allow_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
            allow_button = flow_tester.driver.find_element(AppiumBy.XPATH, allow_button_xpath)
            allow_button.click()
            print(" - '앱 사용 중에만 허용' 버튼을 클릭했습니다.")
            time.sleep(2)  # 팝업이 사라지고 UI가 안정될 때까지 대기

            main_page_element_locator = (AppiumBy.XPATH,
                                         '//android.widget.TextView[@text="디지털세일즈"]')
            flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator))
            print("✅ 로그인 성공 후 홈 화면으로 정상적으로 이동했습니다.")
        except TimeoutException:
            # 5초 내에 팝업이 없으면 이미 권한이 있거나 팝업이 없는 경우로 간주
            print(" - 시스템 접근 권한 팝업이 없습니다. 다음 단계로 진행합니다.")
            pass

        print(f"✅ 계정 '{username}' 로그인 성공.")
        return True, "로그인 성공"
    except TimeoutException:
        print(f"❌ 계정 '{username}' 로그인 실패: 메인 페이지 요소가 로딩되지 않았습니다.")
        return False, "로그인 실패: 메인 페이지 로딩 타임아웃."
    except Exception as e:
        print(f"🚨 계정 '{username}' 로그인 중 예상치 못한 오류 발생: {e}")
        return False, f"로그인 중 오류 발생: {e}"




def get_credentials_from_file(file_path):
    """지정된 파일에서 총국장과 코디 계정 정보를 읽어옵니다."""
    credentials = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split(',')
                if data:
                    if "총국장" in data:
                        credentials['general_manager_id'] = data[0]
                        credentials['general_manager_pw'] = data[1]
                    elif "코디" in data:
                        credentials['cody_id'] = data[0]
                        credentials['cody_pw'] = data[1]
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {file_path} 파일을 찾을 수 없습니다.")
    except ValueError:
        raise ValueError(f"Error: {file_path} 파일의 형식이 잘못되었습니다. 'id,pw,name,role,...' 형식이여야 합니다.")

    # 필수 계정 정보가 모두 로드되었는지 확인
    if 'general_manager_id' not in credentials or 'cody_id' not in credentials:
        raise ValueError("파일에서 '총국장' 또는 '코디' 계정 정보를 찾을 수 없습니다.")

    return credentials