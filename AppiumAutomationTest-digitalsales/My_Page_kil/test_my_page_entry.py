# # -*- coding: utf-8 -*-
#
# import time
# import re
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
# # --- 기존 함수 (이름만 명확하게 수정) ---
# def test_share_status_page_navigation(flow_tester):
#     """마이페이지 > 공유현황: '공유하기' 버튼 선택 시 공유현황 페이지로 이동"""
#     print("\n--- 공유현황 페이지 이동 시나리오 시작 ---")
#
#     share_button_xpath = '//android.view.View[@text="공유하기"]'
#     share_page_title_xpath = '//android.widget.TextView[@text="공유하기"]'
#
#     try:
#         print(f"'{share_button_xpath}' 버튼을 찾습니다...")
#         share_button = WebDriverWait(flow_tester.driver, 10).until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, share_button_xpath))
#         )
#         print("✅ 버튼을 찾았습니다. 클릭합니다.")
#         share_button.click()
#         time.sleep(3)
#
#         print(f"'{share_page_title_xpath}' 페이지 타이틀의 노출을 확인합니다...")
#         WebDriverWait(flow_tester.driver, 15).until(
#             EC.visibility_of_element_located((AppiumBy.XPATH, share_page_title_xpath))
#         )
#
#         print("✅ 성공: 공유현황 페이지로 정상적으로 이동했습니다.")
#         return True, "공유현황 페이지 이동 확인 성공"
#
#     except (TimeoutException, NoSuchElementException) as e:
#         save_screenshot_on_failure(flow_tester.driver, "share_status_navigation_fail")
#         return False, f"실패: 공유현황 페이지 이동 중 요소를 찾지 못했습니다. - {e}"
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "share_status_navigation_error")
#         return False, f"실패: 공유현황 페이지 이동 중 예상치 못한 오류 발생: {e}"
#     finally:
#         print("--- 공유현황 페이지 이동 시나리오 종료 ---")
#
#
# # --- ▼▼▼ 새로 추가된 함수 ▼▼▼ ---
#
# def extract_count_from_text(text):
#     """ "10건"과 같은 텍스트에서 숫자만 추출하여 정수로 반환합니다. """
#     match = re.search(r'\d+', text)
#     if match:
#         return int(match.group(0))
#     return -1  # 숫자를 찾지 못한 경우 -1 반환
#
#
# def test_share_status_count_validation(flow_tester):
#     """공유현황: 월별 총 공유 수 및 항목별 건수 노출 확인"""
#     print("\n--- 공유현황 건수 검증 시나리오 시작 ---")
#
#     wait = WebDriverWait(flow_tester.driver, 10)
#
#     try:
#         # --- 1. 월별 총 공유 수 합산 검증 ---
#         print("\n--- 1. 월별 총 공유 수 합산 검증 시작 ---")
#
#         total_share_count_xpath = '//android.widget.TextView[contains(@text, "총 공유")]'
#
#         # 채널별 XPath 정의
#         channels = {
#             "문자(방문관리)": '//android.view.View[.//android.widget.TextView[@text="문자(방문관리)"]]//android.widget.TextView[contains(@text, "건")]',
#             "문자(자가관리)": '//android.view.View[.//android.widget.TextView[@text="문자(자가관리)"]]//android.widget.TextView[contains(@text, "건")]',
#             "문자(내 핸드폰 연락처)": '//android.view.View[.//android.widget.TextView[@text="문자(내 핸드폰 연락처)"]]//android.widget.TextView[contains(@text, "건")]',
#             "카카오톡": '//android.view.View[.//android.widget.TextView[@text="카카오톡"]]//android.widget.TextView[contains(@text, "건")]'
#         }
#
#         calculated_total = 0
#         for channel, xpath in channels.items():
#             print(f"💡 '{channel}' 공유 건수 확인...")
#             try:
#                 element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#                 count = extract_count_from_text(element.text)
#                 if count == -1:
#                     raise ValueError(f"'{channel}' 건수 텍스트에서 숫자 추출 실패: '{element.text}'")
#
#                 print(f"✅ '{channel}' 건수: {count} 건")
#                 calculated_total += count
#             except TimeoutException:
#                 # 건수가 0이면 요소가 없을 수 있으므로 실패처리 하지 않고 0으로 간주
#                 print(f"⚠️ '{channel}' 건수 요소를 찾지 못함 (0건으로 처리).")
#
#         # 화면에 표시된 '총 공유' 건수 가져오기
#         print("💡 '총 공유' 건수 확인...")
#         total_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, total_share_count_xpath)))
#         displayed_total = extract_count_from_text(total_element.text)
#         if displayed_total == -1:
#             return False, f"'총 공유' 텍스트에서 숫자 추출 실패: '{total_element.text}'"
#
#         print(f"✅ 화면상 '총 공유' 건수: {displayed_total} 건")
#         print(f"🧮 채널별 합산 건수: {calculated_total} 건")
#
#         if calculated_total != displayed_total:
#             save_screenshot_on_failure(flow_tester.driver, "share_count_mismatch")
#             return False, f"실패: 채널별 합산({calculated_total}건)이 총 공유 수({displayed_total}건)와 일치하지 않습니다."
#
#         print("✅ 성공: 월별 총 공유 수가 채널별 합산과 일치합니다.")
#
#         # --- 2. 항목별 총 건수 노출 확인 ---
#         print("\n--- 2. 항목별 총 건수 노출 확인 시작 ---")
#
#         items_to_check = [
#             "제품", "제품 비교", "라이프 스토리", "고객 프로모션",
#             "라이브러리", "슬립 케어", "갤러리 체험", "상조"
#         ]
#
#         missing_items = []
#         for item in items_to_check:
#             print(f"💡 '{item}' 항목 노출 확인...")
#             # 각 항목의 텍스트가 존재하는지 확인하는 XPath
#             item_xpath = f'//android.widget.TextView[@text="{item}"]'
#             try:
#                 wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, item_xpath)))
#                 print(f"✅ '{item}' 항목이 노출되었습니다.")
#             except TimeoutException:
#                 print(f"❌ '{item}' 항목을 찾을 수 없습니다.")
#                 missing_items.append(item)
#
#         if missing_items:
#             save_screenshot_on_failure(flow_tester.driver, "share_item_missing")
#             return False, f"실패: 다음 항목들이 노출되지 않았습니다 - {', '.join(missing_items)}"
#
#         print("✅ 성공: 모든 항목이 정상적으로 노출됩니다.")
#         return True, "공유현황 건수 및 항목 검증 성공"
#
#     except (TimeoutException, NoSuchElementException) as e:
#         save_screenshot_on_failure(flow_tester.driver, "share_status_count_fail")
#         return False, f"실패: 공유현황 검증 중 요소를 찾지 못했습니다. - {e}"
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "share_status_count_error")
#         return False, f"실패: 공유현황 검증 중 예상치 못한 오류 발생: {e}"
#     finally:
#         print("--- 공유현황 건수 검증 시나리오 종료 ---")


# -*- coding: utf-8 -*-

import time
import re
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 MyPageKilLocators 임포트
from Xpath.xpath_repository import MyPageKilLocators


# --- 기존 함수 (이름만 명확하게 수정) ---
def test_share_status_page_navigation(flow_tester):
    """마이페이지 > 공유현황: '공유하기' 버튼 선택 시 공유현황 페이지로 이동"""
    print("\n--- 공유현황 페이지 이동 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = MyPageKilLocators.AOS

    share_button_xpath = locators.share_button_xpath  # 수정됨
    share_page_title_xpath = locators.share_page_title_xpath  # 수정됨

    try:
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


# --- ▼▼▼ 새로 추가된 함수 ▼▼▼ ---

def extract_count_from_text(text):
    """ "10건"과 같은 텍스트에서 숫자만 추출하여 정수로 반환합니다. """
    match = re.search(r'\d+', text)
    if match:
        return int(match.group(0))
    return -1  # 숫자를 찾지 못한 경우 -1 반환


def test_share_status_count_validation(flow_tester):
    """공유현황: 월별 총 공유 수 및 항목별 건수 노출 확인"""
    print("\n--- 공유현황 건수 검증 시나리오 시작 ---")

    wait = WebDriverWait(flow_tester.driver, 10)

    # AOS 로케이터 세트 선택
    locators = MyPageKilLocators.AOS

    try:
        # --- 1. 월별 총 공유 수 합산 검증 ---
        print("\n--- 1. 월별 총 공유 수 합산 검증 시작 ---")

        total_share_count_xpath = locators.total_share_count_xpath  # 수정됨

        # 채널별 XPath 정의 (템플릿 사용)
        channels = {
            "문자(방문관리)": locators.channel_count_xpath_template.format(channel_name="문자(방문관리)"),  # 수정됨
            "문자(자가관리)": locators.channel_count_xpath_template.format(channel_name="문자(자가관리)"),  # 수정됨
            "문자(내 핸드폰 연락처)": locators.channel_count_xpath_template.format(channel_name="문자(내 핸드폰 연락처)"),  # 수정됨
            "카카오톡": locators.channel_count_xpath_template.format(channel_name="카카오톡")  # 수정됨
        }

        calculated_total = 0
        for channel, xpath in channels.items():
            print(f"💡 '{channel}' 공유 건수 확인...")
            try:
                element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
                count = extract_count_from_text(element.text)
                if count == -1:
                    raise ValueError(f"'{channel}' 건수 텍스트에서 숫자 추출 실패: '{element.text}'")

                print(f"✅ '{channel}' 건수: {count} 건")
                calculated_total += count
            except TimeoutException:
                # 건수가 0이면 요소가 없을 수 있으므로 실패처리 하지 않고 0으로 간주
                print(f"⚠️ '{channel}' 건수 요소를 찾지 못함 (0건으로 처리).")

        # 화면에 표시된 '총 공유' 건수 가져오기
        print("💡 '총 공유' 건수 확인...")
        total_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, total_share_count_xpath)))
        displayed_total = extract_count_from_text(total_element.text)
        if displayed_total == -1:
            return False, f"'총 공유' 텍스트에서 숫자 추출 실패: '{total_element.text}'"

        print(f"✅ 화면상 '총 공유' 건수: {displayed_total} 건")
        print(f"🧮 채널별 합산 건수: {calculated_total} 건")

        if calculated_total != displayed_total:
            save_screenshot_on_failure(flow_tester.driver, "share_count_mismatch")
            return False, f"실패: 채널별 합산({calculated_total}건)이 총 공유 수({displayed_total}건)와 일치하지 않습니다."

        print("✅ 성공: 월별 총 공유 수가 채널별 합산과 일치합니다.")

        # --- 2. 항목별 총 건수 노출 확인 ---
        print("\n--- 2. 항목별 총 건수 노출 확인 시작 ---")

        items_to_check = [
            "제품", "제품 비교", "라이프 스토리", "고객 프로모션",
            "라이브러리", "슬립 케어", "갤러리 체험", "상조"
        ]

        missing_items = []
        for item in items_to_check:
            print(f"💡 '{item}' 항목 노출 확인...")
            # 각 항목의 텍스트가 존재하는지 확인하는 XPath (템플릿 사용)
            item_xpath = locators.item_xpath_template.format(item=item)  # 수정됨
            try:
                wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, item_xpath)))
                print(f"✅ '{item}' 항목이 노출되었습니다.")
            except TimeoutException:
                print(f"❌ '{item}' 항목을 찾을 수 없습니다.")
                missing_items.append(item)

        if missing_items:
            save_screenshot_on_failure(flow_tester.driver, "share_item_missing")
            return False, f"실패: 다음 항목들이 노출되지 않았습니다 - {', '.join(missing_items)}"

        print("✅ 성공: 모든 항목이 정상적으로 노출됩니다.")
        return True, "공유현황 건수 및 항목 검증 성공"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "share_status_count_fail")
        return False, f"실패: 공유현황 검증 중 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "share_status_count_error")
        return False, f"실패: 공유현황 검증 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 공유현황 건수 검증 시나리오 종료 ---")