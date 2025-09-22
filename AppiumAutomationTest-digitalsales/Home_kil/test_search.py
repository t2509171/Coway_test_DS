import sys
import os
import time

import unittest
from appium import webdriver
from Utils.click_coordinate import w3c_click_coordinate
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging

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

        print("검색 페이지로 이동했는지 확인합니다.")
        notice_page_title_xpath = '//android.widget.TextView[@text="검색"]'
        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath)),
            message="공지사항 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 공지사항 상세 페이지로 성공적으로 이동했습니다.")

        print("뒤로가기를 눌러 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back()
        time.sleep(1)
        #키보드가 켜져서 2번 뒤로가야 홈화면으로 복귀 가능
        flow_tester.driver.back()

        time.sleep(3)
        return True, result_message

    except Exception as e:
        result_message = f"검색 버튼 클릭 중 오류 발생: {e}"
        time.sleep(2)
        return False, result_message