# -*- coding: utf-8 -*-

import time
import re
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure

#
# # --- Helper Function ---
# def extract_count_from_text(text):
#     """ "10건", "총 58 건"과 같은 텍스트에서 숫자만 추출하여 정수로 반환합니다. """
#     match = re.search(r'\d+', text)
#     if match:
#         return int(match.group(0))
#     return -1  # 숫자를 찾지 못한 경우
#
#
# # --- Test Case Functions ---
#

def test_verify_share_status_elements(flow_tester):
    """
    '공유하기' 탭으로 이동하여 관련 요소가 노출되는지 검증합니다.
    """
    print("\n--- 마이페이지 > 공유하기 탭 요소 노출 확인 시나리오 시작 ---")
    try:
        # 1. '공유하기' 탭 클릭 (좌표 기반)
        share_status_coords = (400, 310)
        print(f"'공유하기' 탭 위치인 {share_status_coords} 좌표를 클릭합니다.")
        try:
            flow_tester.driver.tap([share_status_coords])
            time.sleep(2) # 탭 전환 애니메이션 대기
        except Exception as e:
            error_msg = f"실패: '공유하기' 탭 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "share_status_tap_failed")
            return False, error_msg

        # (주석 처리된 기존 XPath 방식)
        # share_tab_xpath = '//android.view.View[@text="공유하기"]'
        # share_tab = WebDriverWait(flow_tester.driver, 10).until(
        #     EC.presence_of_element_located((AppiumBy.XPATH, share_tab_xpath))
        # )
        # share_tab.click()

        # 2. '공유하기' 화면의 특정 요소가 노출되는지 확인하는 로직 (필요 시 XPath 수정)
        print("'공유하기' 화면의 요소들을 확인합니다.")
        try:
            share_element_xpath = '//android.widget.TextView[@text="콘텐츠 공유 현황"]'
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, share_element_xpath))
            )
            print("✅ '콘텐츠 공유 현황' 텍스트가 성공적으로 노출되었습니다.")
            return True, "'공유하기' 탭으로 성공적으로 이동했습니다."
        except TimeoutException:
            error_msg = "실패: '공유하기' 탭으로 이동 후 '콘텐츠 공유 현황' 텍스트를 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "share_status_element_missing")
            return False, error_msg

    except Exception as e:
        return False, f"공유하기 탭 요소 확인 중 예외 발생: {e}"
    finally:
        print("--- 마이페이지 > 공유하기 탭 요소 노출 확인 시나리오 종료 ---")



def test_share_status_page_navigation(flow_tester):
    """Seller app checklist-60 마이페이지 > 공유현황: '공유하기' 버튼 선택 시 공유현황 페이지로 이동"""
    print("\n--- 공유현황 페이지 이동 시나리오 시작 ---")
    # ... (기존 탐색 코드는 변경 없음) ...
    share_button_xpath = '//android.view.View[@text="공유하기"]'
    share_page_title_xpath = '//android.widget.TextView[@text="공유하기"]'
    try:
        # 1. '공유하기' 탭 클릭 (좌표 기반)
        share_status_coords = (400, 310)
        print(f"'공유하기' 탭 위치인 {share_status_coords} 좌표를 클릭합니다.")
        try:
            flow_tester.driver.tap([share_status_coords])
            time.sleep(2)  # 탭 전환 애니메이션 대기
        except Exception as e:
            error_msg = f"실패: '공유하기' 탭 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "share_status_tap_failed")
            return False, error_msg

        print(f"'{share_button_xpath}' 버튼을 찾습니다...")
        share_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, share_button_xpath))
        )
        print("✅ 버튼을 찾았습니다. 클릭합니다.")
        share_button.click()
        time.sleep(3)
        print(f"'{share_page_title_xpath}' 페이지 타이틀의 노출을 확인합니다...")
        WebDriverWait(flow_tester.driver, 15).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, share_page_title_xpath))
        )
        print("✅ 성공: 공유현황 페이지로 정상적으로 이동했습니다.")
        return True, "공유현황 페이지 이동 확인 성공"
    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "share_status_navigation_fail")
        return False, f"실패: 공유현황 페이지 이동 중 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "share_status_navigation_error")
        return False, f"실패: 공유현황 페이지 이동 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 공유현황 페이지 이동 시나리오 종료 ---")

#
# def test_total_share_count_validation(flow_tester):
#     """Seller app checklist-62: 월별 총 공유 수가 채널별 합산과 일치하는지 검증 (최종 안정화 버전)"""
#     print("\n--- 월별 총 공유 수 합산 검증 시나리오 시작 (checklist-61) ---")
#
#     wait = WebDriverWait(flow_tester.driver, 15)
#     calculated_total = 0
#
#     try:
#         # --- 안정성 확보: 채널 목록 전체가 로드될 때까지 대기 ---
#         # 가장 마지막에 위치할 가능성이 높은 '카카오톡'을 기준으로 기다립니다.
#         print("💡 채널 목록이 모두 로드될 때까지 대기합니다...")
#         wait.until(
#             EC.visibility_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="카카오톡"]')),
#             message="공유 현황 채널 목록을 시간 내에 찾지 못했습니다."
#         )
#         print("✅ 채널 목록이 확인되었습니다.")
#
#         # --- 각 채널의 부모 View를 먼저 찾고, 그 안에서 건수를 찾는 가장 안정적인 방식 ---
#         # 부모 View를 찾는 XPath 템플릿
#         parent_view_xpath_template = '//android.widget.TextView[@text="{channel_name}"]/ancestor::android.view.View[1]'
#         # 부모 View 안에서 건수를 찾는 XPath
#         count_text_xpath_inside_parent = './/android.widget.TextView[contains(@text, "건")]'
#
#         channels = ["문자(방문관리)", "문자(자가관리)", "문자(내 휴대폰 연락처)", "카카오톡"]
#
#         for channel_name in channels:
#             print(f"💡 '{channel_name}' 공유 건수 확인...")
#             try:
#                 # 1. 채널 이름으로 부모 View를 찾습니다.
#                 parent_view_locator = parent_view_xpath_template.format(channel_name=channel_name)
#                 parent_view = wait.until(
#                     EC.presence_of_element_located((AppiumBy.XPATH, parent_view_locator))
#                 )
#
#                 # 2. 찾은 부모 View 안에서만 '건' 텍스트를 찾습니다.
#                 count_element = parent_view.find_element(AppiumBy.XPATH, count_text_xpath_inside_parent)
#
#                 count = extract_count_from_text(count_element.text)
#                 if count > -1:
#                     calculated_total += count
#                     print(f"✅ '{channel_name}' 건수: {count} 건 (현재 합계: {calculated_total} 건)")
#                 else:
#                     # 숫자를 추출하지 못한 경우, 오류로 간주하고 로그를 남깁니다.
#                     print(f"⚠️ '{channel_name}' 건수 텍스트에서 숫자 추출 실패: '{count_element.text}' (0건으로 처리).")
#
#             except (NoSuchElementException, TimeoutException):
#                 print(f"⚠️ '{channel_name}' 건수 요소를 찾지 못함 (0건으로 처리).")
#
#         # --- 최종 합계 비교 ---
#         total_share_count_xpath = '//android.widget.TextView[contains(@text, "총 공유")]'
#         print("💡 화면의 '총 공유' 건수 확인...")
#         total_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, total_share_count_xpath)))
#         displayed_total = extract_count_from_text(total_element.text)
#
#         if displayed_total == -1:
#             return False, f"실패: '총 공유' 텍스트에서 숫자 추출 실패: '{total_element.text}'"
#
#         print(f"✅ 화면상 '총 공유' 건수: {displayed_total} 건")
#         print(f"🧮 최종 합산 건수: {calculated_total} 건")
#
#         if calculated_total == displayed_total:
#             print("✅ 성공: 채널별 합산이 총 공유 수와 일치합니다.")
#             return True, "총 공유 수 합산 검증 성공"
#         else:
#             error_message = f"실패: 채널별 합산({calculated_total}건)이 총 공유 수({displayed_total}건)와 일치하지 않습니다."
#             save_screenshot_on_failure(flow_tester.driver, "total_share_count_mismatch")
#             return False, error_message
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "total_share_count_error")
#         return False, f"실패: 총 공유 수 검증 중 예상치 못한 오류 발생: {e}"
#     finally:
#         print("--- 월별 총 공유 수 합산 검증 시나리오 종료 ---")
#
# def test_channel_share_count_visibility(flow_tester):
#     """Seller app checklist-62: 각 채널별 공유 수가 정상적으로 노출되는지 검증"""
#     print("\n--- 채널별 공유 수 노출 확인 시나리오 시작 (checklist-63) ---")
#
#     wait = WebDriverWait(flow_tester.driver, 10)
#     channels_to_verify = ["문자(방문관리)", "문자(자가관리)", "문자(내 핸드폰 연락처)", "카카오톡"]
#     mismatched_channels = []
#
#     try:
#         for channel in channels_to_verify:
#             print(f"💡 '{channel}' 항목의 건수 노출을 확인합니다...")
#             # XPath: 특정 텍스트를 가진 View 내에서 '건'을 포함하는 TextView 찾기
#             xpath = f'//android.view.View[.//android.widget.TextView[@text="{channel}"]]//android.widget.TextView[contains(@text, "건")]'
#
#             try:
#                 element = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
#                 count = extract_count_from_text(element.text)
#
#                 if count >= 0:
#                     print(f"✅ '{channel}' 항목의 건수가 '{count}건'으로 정상 노출됩니다.")
#                 else:
#                     mismatched_channels.append(f"'{channel}' (텍스트에서 숫자 추출 실패: {element.text})")
#
#             except TimeoutException:
#                 # 0건일 경우 요소가 없을 수 있으므로, 이 경우는 통과로 간주할 수 있습니다.
#                 # 만약 0건이라도 반드시 요소가 있어야 한다면 이 부분을 수정해야 합니다.
#                 print(f"✅ '{channel}' 항목의 건수가 노출되지 않음 (0건으로 추정).")
#
#         if not mismatched_channels:
#             print("✅ 성공: 모든 채널의 공유 건수가 정상적으로 표시됩니다.")
#             return True, "채널별 공유 수 노출 확인 성공"
#         else:
#             error_message = f"실패: 다음 채널의 건수 표시가 잘못되었습니다 - {', '.join(mismatched_channels)}"
#             save_screenshot_on_failure(flow_tester.driver, "channel_count_visibility_fail")
#             return False, error_message
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "channel_count_visibility_error")
#         return False, f"실패: 채널별 공유 수 확인 중 예상치 못한 오류 발생: {e}"
#     finally:
#         print("--- 채널별 공유 수 노출 확인 시나리오 종료 ---")

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
