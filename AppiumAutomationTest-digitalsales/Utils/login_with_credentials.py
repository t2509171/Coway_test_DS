import sys
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException

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