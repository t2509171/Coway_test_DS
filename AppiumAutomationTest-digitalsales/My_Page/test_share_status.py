# 라이브러리 임포트
import re
import sys
import os
import time
from unittest import result

# xpath 임포트
from Xpath.test_xpath import MyPageXpath

# 프로젝트 루트를 Python Path에 추가합니다.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Utils.locator_manager import LocatorManager

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from My_Page.test_my_page_view import test_my_page_button_click

# 스크린샷 헬퍼 함수
from Utils.screenshot_helper import save_screenshot_on_failure

# 동적 Xpath 생성 함수
from Utils.valid_credentials import get_user_data

# 공유하기 탭 클릭 및 노출 확인 (57)
def test_sharing_tab_click_view(flow_tester):
    # 마이페이지 버튼 클릭 (이전 단계)
    try:
        # test_my_page_button_click 함수가 반환하는 두 값을 명확히 받습니다.
        result, message = test_my_page_button_click(flow_tester)
        if not result:
            print(f"❌ 마이페이지 버튼 클릭 실패: {message}")
            return False, message
    except Exception as e:
        result_message = f"마이페이지 버튼 클릭 처리 중 오류 발생: {e}"
        print(f"🚨 {result_message}")
        save_screenshot_on_failure(flow_tester.driver, "failure_mypage_button_click")
        return False, result_message

    # MyPageXpath 함수를 사용하여 Xpath를 동적으로 가져오는 코드
    #wait = WebDriverWait(flow_tester.driver, 3)

    # 공유하기 탭 노출 확인
    #my_page_button_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'

    try:
        locator_manager = LocatorManager(platform='android', locator_file_name='my_page.json')

        # 로케이터를 JSON 파일에서 가져옵니다.
        my_page_button_view_locator = locator_manager.get_locator("my_page_button_view")

        # 공유하기 탭 노출 확인
        print("공유하기 탭 노출을 확인합니다.")
        flow_tester.wait.until(
            EC.presence_of_element_located(my_page_button_view_locator),
            message="공유하기 탭을 20초 내에 찾지 못했습니다."
        )

        """
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, my_page_button_view_xpath)),
            message=f"'{my_page_button_view_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
        )
        # MyPageXpath 함수를 사용하여 Xpath를 동적으로 가져오는 코드
        MyPageXpath.my_page_button_view = flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, MyPageXpath.my_page_button_view)),
            message=f"'{MyPageXpath.my_page_button_view}' 타이틀을 20초 내에 찾지 못했습니다."
        )
        """
        print("✅ 공유하기 탭이 성공적으로 노출되었습니다.")
        # 성공 시 명시적으로 True와 메시지를 반환하도록 수정
        return True, "공유하기 탭 노출 성공"
    except Exception as e:
        result_message = f"공유하기 탭 노출 확인 실패: {e}"
        time.sleep(3)
        # ===== 스크린샷 함수 호출 추가 =====
        save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
        # =================================
        return False, result_message

# 공유하기 건수 카운트를 찾아 숫자를 추출하는 함수 (로깅 제거 및 반환 값 수정)
def extract_count_from_text(text):
    """
        텍스트에서 '건' 앞의 숫자를 추출하는 헬퍼 함수
        예: '15건' -> 15
        :param text: 건수 정보가 포함된 문자열
        :return: 추출된 정수, 실패 시 -1
        """
    if not isinstance(text, str):
        return -1
    match = re.search(r'(\d+)\s*건', text)
    if match:
        return int(match.group(1))
    return -1

# 공유하기 건수 확인 (58)
def test_share_count_consistency(flow_tester):
    """
    카카오톡과 문자의 건수를 합산하여 공유하기 총 건수와 비교하는 테스트.
    """
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    wait = flow_tester.wait

    try:
        # Step 1: 카카오톡 건수 추출
        print("💡 카카오톡 공유 건수 확인...")
        # 수정된 XPath: '카카오톡' 텍스트를 포함하는 항목을 찾고, 그 안에서 '건' 텍스트를 찾습니다.
        kakao_count_xpath = '//android.view.View[./android.view.View/android.widget.TextView[@text="카카오톡"]]//android.widget.TextView[contains(@text, "건")]'
        kakao_count_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, kakao_count_xpath)),
            message="카카오톡 건수 요소를 찾지 못했습니다."
        )
        kakao_count_text = kakao_count_element.text
        kakao_count = extract_count_from_text(kakao_count_text)

        if kakao_count == -1:
            return False, f"카카오톡 건수 텍스트에서 숫자를 추출할 수 없습니다: '{kakao_count_text}'"

        print(f"✅ 카카오톡 건수: {kakao_count} 건")

        # Step 2: 문자(내 휴대폰 연락처) 건수 추출
        print("💡 문자(내 휴대폰 연락처) 공유 건수 확인...")
        # 수정된 XPath: '문자(내 휴대폰 연락처)' 텍스트를 포함하는 항목을 찾고, 그 안에서 '건' 텍스트를 찾습니다.
        sms_count_xpath = '//android.view.View[./android.view.View/android.widget.TextView[@text="문자(내 휴대폰 연락처)"]]//android.widget.TextView[contains(@text, "건")]'
        sms_count_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, sms_count_xpath)),
            message="문자(내 휴대폰 연락처) 건수 요소를 찾지 못했습니다."
        )
        sms_count_text = sms_count_element.text
        sms_count = extract_count_from_text(sms_count_text)

        if sms_count == -1:
            return False, f"문자 건수 텍스트에서 숫자를 추출할 수 없습니다: '{sms_count_text}'"

        print(f"✅ 문자(내 휴대폰 연락처) 건수: {sms_count} 건")

        # Step 3: 문자(방문관리) 건수 추출
        print("💡 문자(방문관리) 공유 건수 확인...")
        # 수정된 XPath: '문자(방문관리)' 텍스트를 포함하는 항목을 찾고, 그 안에서 '건' 텍스트를 찾습니다.
        sms_visit_management_count_xpath = '//android.view.View[./android.view.View/android.widget.TextView[@text="문자(방문관리)"]]//android.widget.TextView[contains(@text, "건")]'
        sms_visit_management_count_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, sms_visit_management_count_xpath)),
            message="문자(방문관리) 건수 요소를 찾지 못했습니다."
        )
        sms_visit_management_count_text = sms_visit_management_count_element.text
        sms_visit_management_count = extract_count_from_text(sms_visit_management_count_text)

        if sms_visit_management_count == -1:
            return False, f"문자 건수 텍스트에서 숫자를 추출할 수 없습니다: '{sms_visit_management_count_text}'"

        print(f"✅ 문자(방문관리) 건수: {sms_visit_management_count} 건")

        # Step 4: 문자(자가관리) 건수 추출
        print("💡 문자(자가관리) 공유 건수 확인...")
        # 수정된 XPath: '문자(자가관리)' 텍스트를 포함하는 항목을 찾고, 그 안에서 '건' 텍스트를 찾습니다.
        sms_self_management_count_xpath = '//android.view.View[./android.view.View/android.widget.TextView[@text="문자(자가관리)"]]//android.widget.TextView[contains(@text, "건")]'
        sms_self_management_count_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, sms_self_management_count_xpath)),
            message="문자(자가관리) 건수 요소를 찾지 못했습니다."
        )
        sms_self_management_count_text = sms_self_management_count_element.text
        sms_self_management_count = extract_count_from_text(sms_self_management_count_text)

        if sms_self_management_count == -1:
            return False, f"문자 건수 텍스트에서 숫자를 추출할 수 없습니다: '{sms_self_management_count_text}'"

        print(f"✅ 문자(자가관리) 건수: {sms_self_management_count} 건")

        # Step 5: 총 공유하기 건수 추출
        print("💡 공유하기 총 건수 확인...")
        # 총 공유하기 건수를 찾는 XPath는 이미 올바른 것으로 보이지만, 안정성을 위해 다시 확인합니다.
        #total_share_count_xpath = '//android.widget.TextView[@text="공유하기"]/following-sibling::android.widget.TextView[1]'
        total_share_count_xpath = '//android.view.View[./android.view.View/android.widget.TextView[@text="공유하기"]]//android.widget.TextView[contains(@text, "건")]'
        total_share_count_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, total_share_count_xpath)),
            message="공유하기 총 건수 요소를 찾지 못했습니다."
        )
        total_share_count_text = total_share_count_element.text
        total_share_count = extract_count_from_text(total_share_count_text)

        if total_share_count == -1:
            return False, f"공유하기 총 건수 텍스트에서 숫자를 추출할 수 없습니다: '{total_share_count_text}'"

        print(f"✅ 공유하기 총 건수: {total_share_count} 건")

        # Step 6: 합산 및 결과 비교
        calculated_sum = kakao_count + sms_count + sms_visit_management_count + sms_self_management_count
        print(f"💡 카카오톡 건수({kakao_count}) + 문자 건수({sms_count}) + 문자 건수({sms_visit_management_count}) + 문자 건수({sms_self_management_count}) = 합계({calculated_sum})")

        if calculated_sum == total_share_count:
            scenario_passed = True
            result_message = f"🎉 성공: 합산 건수({calculated_sum})와 총 공유하기 건수({total_share_count})가 일치합니다."
        else:
            scenario_passed = False
            result_message = f"❌ 실패: 합산 건수({calculated_sum})와 총 공유하기 건수({total_share_count})가 일치하지 않습니다."

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "failure_share_status_failure")
        result_message = f"테스트 실패: 요소를 찾지 못했거나 타임아웃 발생 - {e}"
        scenario_passed = False
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "failure_share_status_failure")
        result_message = f"테스트 실행 중 예상치 못한 오류 발생: {e}"
        scenario_passed = False
    finally:
        print("--- 테스트 완료 ---\n")

    return scenario_passed, result_message








if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")