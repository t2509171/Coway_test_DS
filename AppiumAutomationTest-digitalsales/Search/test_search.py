import re
import sys
import os
import time

import unittest
import random

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.click_coordinate import w3c_click_coordinate



from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from Base.base_driver import BaseAppiumDriver
from Login.test_Login_passed import run_successful_login_scenario

# 검색 버튼 클릭 (44)
def test_search_button_click(flow_tester):
    # 검색 버튼 클릭 확인
    print("검색 버튼을 찾고 클릭합니다.")
    search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
    try:
        search_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, search_button_xpath)),
            message=f"'{search_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        search_button.click()
        print("검색 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기
        result_message = "검색 페이지로 이동한다."
        return True, result_message
    except Exception as e:
        result_message = f"검색 버튼 클릭 중 오류 발생: {e}"
        time.sleep(2)
        return False, result_message

# 최근 검색어 목록 노출 확인 (45)
def test_recent_Search_Words(flow_tester):
    """
    유틸리티 함수에 변수로 다른 좌표를 전달하여 클릭하는 테스트입니다.
    """
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    try:
        # 최근 검색어 탭 좌표 정의 및 클릭
        first_x = 195
        first_y = 480
        print("\n=== 최근 검색어 탭 좌표 클릭 시작 ===")
        w3c_click_coordinate(flow_tester.driver, first_x, first_y)
        print("\n=== 최근 검색어 탭 좌표 클릭 종료 ===")

        # 최근 검색어 목록 노출 확인
        print("최근 검색어 목록 노출을 확인합니다.")
        recent_Search_Words_details_view_xpath = '//android.widget.ListView'
        #ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, recent_Search_Words_details_view_xpath)))
            print("✅ 최근 검색어 목록이 성공적으로 노출되었습니다.")
        #    flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab1_details_view_xpath)))
        #    print("✅ '상세글 뷰'가 성공적으로 노출되었습니다.")
            time.sleep(2)
            scenario_passed = True
            result_message = "최근 검색어 목록 노출 확인 성공."
        except Exception as e:
            result_message = f"최근 검색어 목록 노출 확인 실패: {e}"
            time.sleep(3)
            print(f"오류 발생: {e}")
            return False, result_message

    except Exception as e:
        print(f"🚨 최근 검색어 확인 시나리오 실행 중 치명적인 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
        return False, result_message

    return scenario_passed, result_message

# 최근 본 제품 목록 노출 확인 (46)
def test_recent_product(flow_tester):
    """
    유틸리티 함수에 변수로 다른 좌표를 전달하여 클릭하는 테스트입니다.
    """
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    try:
        # 최근 본 제품 탭 좌표 정의 및 클릭
        first_x = 550
        first_y = 480
        print("\n=== 최근 본 제품 탭 좌표 클릭 시작 ===")
        w3c_click_coordinate(flow_tester.driver, first_x, first_y)
        print("\n=== 최근 본 제품 탭 좌표 클릭 종료 ===")

        # 최근 본 제품 목록 노출 확인
        print("최근 본 제품 목록 노출을 확인합니다.")
        recent_product_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        #ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, recent_product_details_view_xpath)))
            print("✅ 최근 본 제품 목록이 성공적으로 노출되었습니다.")
        #    flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab1_details_view_xpath)))
        #    print("✅ '상세글 뷰'가 성공적으로 노출되었습니다.")
            time.sleep(2)
            scenario_passed = True
            result_message = "최근 본 제품 목록 노출 확인 성공."
        except Exception as e:
            result_message = f"최근 본 제품 목록 노출 확인 실패: {e}"
            time.sleep(3)
            print(f"오류 발생: {e}")
            return False, result_message

    except Exception as e:
        print(f"🚨 최근 본 제품 확인 시나리오 실행 중 치명적인 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
        return False, result_message

    return scenario_passed, result_message

# 인기 검색어 순위 노출 확인 (47)
def test_popular_search(flow_tester):
    """
    유틸리티 함수에 변수로 다른 좌표를 전달하여 클릭하는 테스트입니다.
    """
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    try:
        # 인기 검색어 순위 탭 좌표 정의 및 클릭
        first_x = 910
        first_y = 480
        print("\n=== 인기 검색어 순위 탭 좌표 클릭 시작 ===")
        w3c_click_coordinate(flow_tester.driver, first_x, first_y)
        print("\n=== 인기 검색어 순위 탭 좌표 클릭 종료 ===")

        # 최근 본 제품 목록 노출 확인
        print("인기 검색어 순위 목록 노출을 확인합니다.")
        recent_product_details_view_xpath = '//android.widget.ListView'
        #ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, recent_product_details_view_xpath)))
            print("✅ 인기 검색어 순위 목록이 성공적으로 노출되었습니다.")
        #    flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab1_details_view_xpath)))
        #    print("✅ '상세글 뷰'가 성공적으로 노출되었습니다.")
            time.sleep(2)
            scenario_passed = True
            result_message = "인기 검색어 순위 목록 노출 확인 성공."
        except Exception as e:
            result_message = f"인기 검색어 순위 목록 노출 확인 실패: {e}"
            time.sleep(3)
            print(f"오류 발생: {e}")
            return False, result_message

    except Exception as e:
        print(f"🚨 인기 검색어 순위 확인 시나리오 실행 중 치명적인 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
        return False, result_message

    return scenario_passed, result_message

# search_text.txt 파일에서 무작위 검색어를 가져오는 헬퍼 함수
def _get_random_search_text(filename='search_text.txt'):
    try:
        # 현재 스크립트 파일의 경로를 기준으로 파일 경로를 구성
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)

        # 수정: 파일 이름(filename) 대신 완전한 경로(file_path)를 사용
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 공백이나 빈 줄을 제거하고 리스트로 만듭니다.
            search_texts = [line.strip() for line in lines if line.strip()]
            return random.choice(search_texts)
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")
    except IndexError:
        raise ValueError(f"파일에 검색어가 없습니다: {filename}")

# 제품 검색 확인 (48)
def test_random_search_functionality(flow_tester):
    """
    search_text.txt 파일에서 무작위로 검색어를 선택하여 검색하고 결과가 노출되는지 확인합니다.
    [Seller app checklist-48]
    """
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. search_text.txt에서 무작위 검색어 가져오기
        try:
            random_text = _get_random_search_text()
            print(f"💡 무작위로 선택된 검색어: '{random_text}'")
        except (FileNotFoundError, ValueError) as e:
            return False, f"테스트 데이터 준비 실패: {e}"

        # 2. 검색 페이지로 이동 (test_search_button_click 함수 재사용 가능)
        """
        nav_success, nav_msg = test_search_button_click(flow_tester)
        if not nav_success:
            return False, nav_msg
        """
        print("검색 영역을 찾고 클릭합니다.")
        search_button_xpath = '//android.widget.EditText'
        try:
            search_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, search_button_xpath)),
                message=f"'{search_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            search_button.click()
            print("검색 영역 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"검색 영역 클릭/입력 실패: {e}"
            return False, result_message

        # 3. 검색어 입력
        print(f"'{random_text}' 텍스트를 입력합니다.")
        search_input_xpath = '//android.widget.EditText' #
        try:
            search_input_element = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, search_input_xpath)),
                message=f"'{search_input_xpath}' 검색 입력 필드를 20초 내에 찾지 못했습니다."
            )
            search_input_element.clear()
            search_input_element.send_keys(random_text)
            print("✅ 검색어 입력 완료.")
            time.sleep(2)
        except Exception as e:
            result_message = f"검색 입력 필드 클릭/입력 실패: {e}"
            return False, result_message

        # 4. 검색 버튼 클릭
        print("검색 버튼을 찾고 클릭합니다.")
        # 'KEYCODE_ENTER' 키 이벤트 전송
        flow_tester.driver.press_keycode(66)

        # 5. 검색 결과 노출 확인
        print("검색 결과가 노출되었는지 확인합니다.")
        # 총 143건과 같은 텍스트를 포함하는 요소를 찾아 검색 결과가 있음을 확인합니다.
        search_result_text_xpath = '//android.widget.TextView[contains(@text, "총 ")]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, search_result_text_xpath)),
                message=f"'{random_text}'에 대한 검색 결과가 20초 내에 노출되지 않았습니다."
            )
            print(f"✅ '{random_text}'에 대한 검색 결과가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = f"무작위 검색어 '{random_text}'에 대한 검색 기능 성공."
        except Exception as e:
            result_message = f"'{random_text}'에 대한 검색 결과 노출 확인 실패: {e}"
            return False, result_message

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

        return scenario_passed, result_message

    except Exception as e:
        print(f"🚨 무작위 검색어 검색 시나리오 실행 중 치명적인 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
        return False, result_message

    finally:
        print("--- 무작위 검색어 검색 및 결과 노출 확인 시나리오 종료 ---\n")

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")