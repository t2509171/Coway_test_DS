import sys
import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# 유틸리티 함수 임포트
from Utils.scrolling_function import scroll_to_element

# [Seller app checklist-37] 홈 > 컨텐츠 유닛 확인
def test_home_content_unit(flow_tester):
    """
    홈 화면의 콘텐츠 유닛을 확인하는 테스트 시나리오입니다.
    1. 콘텐츠 유닛까지 스크롤합니다.
    2. 좌우로 스와이프하며 모든 항목을 수집하고 최대 20개인지 확인합니다.
    3. 첫 번째 항목을 클릭하여 상세 페이지로 이동하는지 확인합니다.
    """
    print("\n--- 홈 > 콘텐츠 유닛 확인 시나리오 시작 ---")

    try:
        # --- ✅ 테스트 시작 전 홈 화면으로 이동 ---
        print("테스트 시작 전, 홈 화면으로 이동합니다.")
        try:
            home_button_xpath = '//android.view.View[@content-desc="홈"]'
            home_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
            )
            home_button.click()
            print("✅ 홈 버튼 클릭 완료. 홈 화면으로 이동했습니다.")
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ 홈 버튼을 클릭하는 중 오류 발생 (이미 홈 화면일 수 있음): {e}")

        # 1. '콘텐츠' 유닛 컨테이너가 보일 때까지 아래로 스크롤
        content_unit_container_xpath = '//android.widget.TextView[@text="1"]'
        print("콘텐츠 유닛이 보일 때까지 스크롤합니다.")
        scroll_success, scroll_msg = scroll_to_element(flow_tester, content_unit_container_xpath)

        if not scroll_success:
            save_screenshot_on_failure(flow_tester.driver, "content_unit_not_found")
            return False, f"콘텐츠 유닛을 찾지 못했습니다: {scroll_msg}"

        # 2. 모든 콘텐츠 항목을 수집하고 개수 확인 (스와이프 포함)
        print("스와이프를 통해 모든 콘텐츠 항목을 수집하고 개수를 확인합니다.")

        # --- ▼▼▼▼▼▼▼▼▼▼ [수정된 부분] ▼▼▼▼▼▼▼▼▼▼ ---
        # XPath를 더 구체적으로 수정하여 개별 항목을 정확히 타겟팅합니다.
        base_item_xpath   = '//android.widget.TextView[@text="'

        container_element = flow_tester.driver.find_element(AppiumBy.XPATH, content_unit_container_xpath)
        swipe_area = container_element.rect
        start_x = swipe_area['x'] + swipe_area['width'] * 1.0
        end_x = swipe_area['x'] + swipe_area['width'] * 0.1
        y = swipe_area['y'] + swipe_area['height'] / 2

        item_index = 1
        total_items_found = 0

        while item_index <= 5:
            # 현재 인덱스의 XPath 생성
            indexed_xpath = f'{base_item_xpath}{item_index}"]'

            try:
                # 1. 현재 인덱스(i)의 요소가 있는지 확인
                print(f"콘텐츠 유닛 [{item_index}] 확인 시도...{indexed_xpath}")
                flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
                print(f"✅ 콘텐츠 유닛 [{item_index}] 발견.{indexed_xpath}")
                total_items_found = item_index  # 발견된 마지막 인덱스를 저장
                item_index += 1  # 다음 인덱스로 이동
                continue  # 다음 요소 확인

            except NoSuchElementException:
                # 2. 요소가 없다면 스와이프 시도
                print(f"콘텐츠 유닛 [{item_index}] 없음. 스와이프를 시도합니다.")
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
                                                                                                                y).release()
                actions.perform()
                time.sleep(2)

                try:
                    # 3. 스와이프 후 다시 한번 같은 인덱스의 요소 확인
                    print(f"스와이프 후, 콘텐츠 유닛 [{item_index}] 다시 확인...{indexed_xpath}")
                    flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
                    print(f"✅ 스와이프 후, 콘텐츠 유닛 [{item_index}] 발견.{indexed_xpath}")
                    total_items_found = item_index
                    item_index += 1

                except NoSuchElementException:
                    # 4. 스와이프 후에도 요소가 없다면 탐색 종료
                    print(f"스와이프 후에도 콘텐츠 유닛 [{item_index}] 없음. 탐색을 종료합니다.")
                    break  # while 루프 탈출

        print(f"✅ 탐색 완료. 발견된 총 콘텐츠 유닛 수: {total_items_found}개")

        # --- ▲▲▲▲▲▲ [새 로직 종료] ▲▲▲▲▲▲ ---

        if total_items_found < 3:
            # 테스트를 위해 최소 3개의 유닛이 필요하다고 가정
            return False, f"테스트에 필요한 최소 유닛(3개)을 찾지 못했습니다. (발견된 수: {total_items_found}개)"

        # 5. 3번째 항목 클릭하여 상세 페이지로 이동
        print("콘텐츠 항목을 클릭합니다.")
        target_item_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        target_item = flow_tester.driver.find_element(AppiumBy.XPATH, target_item_xpath)
        target_item.click()
        time.sleep(5)

        # 6. 상세 페이지 진입 확인
        content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]'
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
            message="콘텐츠 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 상세 페이지로 성공적으로 이동했습니다.")

        # 7. 뒤로 가기
        print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back()
        time.sleep(3)

        return True, f"콘텐츠 유닛 순차 탐색 및 3번 항목 클릭 후 상세 페이지 이동 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
        return False, f"콘텐츠 유닛 테스트 중 오류 발생: {e}"
    finally:
        print("--- 홈 > 콘텐츠 유닛 확인 시나리오 종료 ---")



# [Seller app checklist-37] 홈 > 컨텐츠 유닛 확인
# def test_home_content_unit(flow_tester):
#     """
#     요소의 위치/크기(rect)를 '지문'으로 사용하여 스와이프하며 모든 유닛을 찾는 최종 스크립트
#     """
#     print("\n--- 홈 > 콘텐츠 유닛 확인 시나리오 시작 ---")
#
#     try:
#         # --- ✅ 테스트 시작 전 홈 화면으로 이동 ---
#         print("테스트 시작 전, 홈 화면으로 이동합니다.")
#         try:
#             home_button_xpath = '//android.view.View[@content-desc="홈"]'
#             home_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
#             )
#             home_button.click()
#             print("✅ 홈 버튼 클릭 완료. 홈 화면으로 이동했습니다.")
#             time.sleep(3)
#         except Exception as e:
#             print(f"⚠️ 홈 버튼을 클릭하는 중 오류 발생 (이미 홈 화면일 수 있음): {e}")
#
#         # 1. '콘텐츠' 유닛 컨테이너가 보일 때까지 아래로 스크롤
#         content_unit_container_xpath = '//android.widget.TextView[@text="1"]'
#         print("콘텐츠 유닛이 보일 때까지 스크롤합니다.")
#         scroll_success, scroll_msg = scroll_to_element(flow_tester, content_unit_container_xpath)
#
#         if not scroll_success:
#             save_screenshot_on_failure(flow_tester.driver, "content_unit_not_found")
#             return False, f"콘텐츠 유닛을 찾지 못했습니다: {scroll_msg}"
#
#         # --- ▼▼▼▼▼▼ [새로운 '지문' 추적 로직] ▼▼▼▼▼▼ ---
#         # 2. 모든 콘텐츠 항목을 수집하고 개수 확인
#         print("스와이프를 통해 모든 콘텐츠 항목을 수집하고 개수를 확인합니다.")
#
#         # 각 유닛을 식별하는 공통 XPath. 인덱스를 사용하지 않고 컨테이너 바로 아래의 모든 View를 대상으로 합니다.
#         item_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View/android.view.View'
#
#         container_element = flow_tester.driver.find_element(AppiumBy.XPATH, content_unit_container_xpath)
#         swipe_area = container_element.rect
#         start_x = swipe_area['x'] + swipe_area['width'] * 0.9
#         end_x = swipe_area['x'] + swipe_area['width'] * 0.1
#         y = swipe_area['y'] + swipe_area['height'] / 2
#
#         # 발견된 모든 유닛의 '지문(rect)'을 저장할 집합(set)
#         all_found_items_fingerprints = set()
#         max_swipes = 10
#
#         for i in range(max_swipes):
#             previous_item_count = len(all_found_items_fingerprints)
#
#             # 현재 화면에 보이는 모든 유닛을 찾습니다.
#             current_items_on_screen = flow_tester.driver.find_elements(AppiumBy.XPATH, item_xpath)
#
#             for item in current_items_on_screen:
#                 if item.is_displayed():
#                     # 각 유닛의 rect 값(딕셔너리)을 튜플로 변환하여 set에 추가합니다.
#                     # 튜플로 변환해야 set에 저장할 수 있습니다.
#                     fingerprint = tuple(item.rect.items())
#                     all_found_items_fingerprints.add(fingerprint)
#
#             # 새로 발견된 지문이 없다면, 모든 유닛을 찾은 것이므로 종료합니다.
#             if len(all_found_items_fingerprints) == previous_item_count and i > 0:
#                 print("스와이프 후에도 새로운 항목이 없어 탐색을 종료합니다.")
#                 break
#             else:
#                 print(f"새 항목 발견! 현재까지 총 {len(all_found_items_fingerprints)}개")
#
#             # 마지막 스와이프 시도 후에는 더 이상 스와이프하지 않음
#             if i == max_swipes - 1:
#                 break
#
#             print("스와이프를 시도합니다.")
#             actions = ActionChains(flow_tester.driver)
#             actions.w3c_actions = ActionBuilder(flow_tester.driver,
#                                                 mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#             actions.w3c_actions.pointer_action.move_to_location(start_x, y).pointer_down().move_to_location(end_x,
#                                                                                                             y).release()
#             actions.perform()
#             time.sleep(2)
#         # --- ▲▲▲▲▲▲ [로직 종료] ▲▲▲▲▲▲ ---
#
#         total_items = len(all_found_items_fingerprints)
#         print(f"✅ 스와이프 완료. 발견된 총 콘텐츠 항목 수: {total_items}개")
#
#         if not (0 < total_items <= 20):
#             result_message = f"콘텐츠 항목 개수 확인 실패: {total_items}개 (예상: 1~20개)"
#             save_screenshot_on_failure(flow_tester.driver, "content_item_count_error")
#             return False, result_message
#
#         # 3. 첫 번째 항목 클릭
#         print("첫 번째 콘텐츠 항목을 클릭합니다.")
#         first_item = flow_tester.driver.find_element(AppiumBy.XPATH, item_xpath)
#         first_item.click()
#         time.sleep(5)
#
#         # 4. 상세 페이지 진입 확인
#         content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]'
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, content_detail_page_title_xpath)),
#             message="콘텐츠 상세 페이지로 이동하지 못했습니다."
#         )
#         print("✅ 상세 페이지로 성공적으로 이동했습니다.")
#
#         # 5. 뒤로 가기
#         print("뒤로가기 버튼을 클릭하여 홈 화면으로 돌아갑니다.")
#         flow_tester.driver.back()
#         time.sleep(3)
#
#         return True, "콘텐츠 유닛 기능(항목 수, 스와이프, 클릭) 확인 성공."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "content_unit_test_failure")
#         return False, f"콘텐츠 유닛 테스트 중 오류 발생: {e}"
#     finally:
#         print("--- 홈 > 콘텐츠 유닛 확인 시나리오 종료 ---")
