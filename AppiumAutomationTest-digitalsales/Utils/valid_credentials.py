import os
from appium.webdriver.common.appiumby import AppiumBy

import sys
import time

# Ensure the project root is in the path to import Base and Login modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy # AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_user_data(file_path):
    """
    지정된 파일에서 사용자 데이터를 읽어옵니다.
    :param file_path: 사용자 정보 파일 경로
    :return: 딕셔너리 형태의 사용자 데이터
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"'{file_path}' 파일을 찾을 수 없습니다.")

    with open(file_path, 'r', encoding='utf-8') as f:
        # 파일의 첫 번째 줄만 읽기
        user_line = f.readline().strip()

    # 쉼표로 데이터를 분리
    user_data = user_line.split(',')

    # 데이터 구조에 따라 사용자명(index 2)과 직함(index 3) 추출
    username = user_data[2]
    title = user_data[3]
    affiliation = user_data[4]
    contact_information = user_data[5]


    return {"username": username, "title": title, "affiliation" : affiliation, "contact_information" : contact_information}


# valid_credentials.txt 파일 경로 설정 (경로에 맞게 수정 필요)
# 예: 현재 스크립트가 Login 폴더에 있다고 가정
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
file_path = os.path.join(project_root, 'Login', 'valid_credentials.txt')

# file_path = os.path.join(os.path.dirname(__file__), 'valid_credentials.txt')

# 사용자 데이터 가져오기
try:
    user_info = get_user_data(file_path)
    user_username = user_info["username"]
    user_title = user_info["title"]
    user_affiliation = user_info["affiliation"]
    user_contact_information = user_info["contact_information"]

    # 동적으로 XPath 문자열 생성 (username)
    #dynamic_username = (f"안녕하세요 "{user_name} {user_title}입니다.")
    dynamic_username = f'안녕하세요\\n {user_info["username"]} {user_info["title"]}입니다.'
    #dynamic_username = f'''//android.widget.TextView[@text="안녕하세요
    #{user_info["username"]} {user_info["title"]}입니다."]'''
    dynamic_username_xpath = f'//android.widget.TextView[@text="{dynamic_username}"]'

    # 동적으로 XPath 문자열 생성 (username)
    dynamic_title = f"{user_title}"
    dynamic_title_xpath = f'//android.widget.TextView[@text="{dynamic_title}"]'

    # 동적으로 XPath 문자열 생성 (username)
    dynamic_affiliation = f"{user_affiliation}"
    dynamic_affiliation_xpath = f'//android.widget.TextView[@text=" {dynamic_affiliation}"]'

    # 동적으로 XPath 문자열 생성 (username)
    dynamic_contact_information = f"{user_contact_information}"
    dynamic_contact_information_xpath = f'//android.widget.TextView[@text="{dynamic_contact_information}"]'

    # ===== 아래는 테스트 코드에 적용하는 예시입니다 =====
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC

    # 명시적 대기를 사용하여 요소가 나타날 때까지 기다립니다.
    # try:
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((AppiumBy.XPATH, dynamic_xpath))
    #     )
    #     print("✅ '사용자명' 요소가 성공적으로 노출되었습니다.")
    # except Exception as e:
    #     print(f"❌ '{dynamic_xpath}' 요소를 찾을 수 없습니다. 오류: {e}")

except FileNotFoundError as e:
    print(f"❌ 오류: {e}")