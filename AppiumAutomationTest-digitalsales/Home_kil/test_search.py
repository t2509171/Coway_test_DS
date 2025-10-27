import sys
import os
import time

import unittest
from appium import webdriver
from Utils.click_coordinate import w3c_click_coordinate
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # 추가

import logging

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_search_button_click(flow_tester):
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    # 검색 버튼 클릭 확인
    print("검색 버튼을 찾고 클릭합니다.")
    search_button_xpath = locators.search_button_xpath
    try:
        search_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, search_button_xpath)),
            message=f"'{search_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        search_button.click()
        print("검색 버튼 클릭 완료.")
        time.sleep(2)  # 페이지 전환 대기
        result_message = "검색 페이지로 이동한다."

        print("검색 페이지로 이동했는지 확인합니다.")
        search_page_title_xpath = locators.search_page_title_xpath # 수정됨 (notice_page_title_xpath -> search_page_title_xpath)
        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, search_page_title_xpath)),
            message="검색 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 검색 상세 페이지로 성공적으로 이동했습니다.")

        print("뒤로가기를 눌러 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back() # 검색 상세 -> 홈
        time.sleep(1)
        # 키보드가 열려있을 수 있으므로 추가 뒤로가기 (AOS)
        if flow_tester.platform == 'android':
             try:
                  # 키보드가 보이는지 확인 (더 안정적인 방법 필요 시 is_keyboard_shown 사용)
                  # 현재는 검색 입력 필드가 포커스를 잃었는지 확인하는 방식으로 대체
                  WebDriverWait(flow_tester.driver, 1).until_not(
                       EC.element_attribute_to_include((AppiumBy.XPATH, '//android.widget.EditText'), 'focused')
                  )
             except TimeoutException:
                  print("키보드가 여전히 활성 상태일 수 있습니다. 추가 뒤로가기 실행.")
                  flow_tester.driver.back() # 키보드 닫기 or 이전 화면

        time.sleep(3)
        return True, result_message

    except Exception as e:
        result_message = f"검색 버튼 클릭 중 오류 발생: {e}"
        # 실패 시에도 홈으로 돌아가도록 시도
        try:
            flow_tester.driver.back()
            time.sleep(1)
            if flow_tester.platform == 'android':
                flow_tester.driver.back()
            time.sleep(1)
        except Exception:
            print("검색 실패 후 뒤로가기 중 오류 발생 (무시)")
        return False, result_message



# import sys
# import os
# import time
#
# import unittest
# from appium import webdriver
# from Utils.click_coordinate import w3c_click_coordinate
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# import logging
#
# def test_search_button_click(flow_tester):
#     # 검색 버튼 클릭 확인
#     print("검색 버튼을 찾고 클릭합니다.")
#     search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
#     try:
#         search_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, search_button_xpath)),
#             message=f"'{search_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         search_button.click()
#         print("검색 버튼 클릭 완료.")
#         time.sleep(2)  # 페이지 전환 대기
#         result_message = "검색 페이지로 이동한다."
#
#         print("검색 페이지로 이동했는지 확인합니다.")
#         notice_page_title_xpath = '//android.widget.TextView[@text="검색"]'
#         WebDriverWait(flow_tester.driver, 10).until(
#             EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath)),
#             message="공지사항 상세 페이지로 이동하지 못했습니다."
#         )
#         print("✅ 공지사항 상세 페이지로 성공적으로 이동했습니다.")
#
#         print("뒤로가기를 눌러 홈 화면으로 돌아갑니다.")
#         flow_tester.driver.back()
#         time.sleep(1)
#         #키보드가 켜져서 2번 뒤로가야 홈화면으로 복귀 가능
#         flow_tester.driver.back()
#
#         time.sleep(3)
#         return True, result_message
#
#     except Exception as e:
#         result_message = f"검색 버튼 클릭 중 오류 발생: {e}"
#         time.sleep(2)
#         return False, result_message