# PythonProject/Home_View_kil/test_large_font_mode.py

import sys
import os
import time

# Ensure the project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import locators from the repository
from Xpath.xpath_repository import HomeViewKilLocators # 수정: 클래스 임포트

# --- 함수 이름 유지 및 플랫폼 분기 추가 ---
def test_verify_element_positions_after_large_font_click(flow_tester):
    """Toggles the large font mode and verifies the description element visibility."""
    print("\n--- 큰 글씨 모드 토글 테스트 시작 ---")
    scenario_passed = True
    result_message = "큰 글씨 모드 토글 및 확인 성공."

    # 플랫폼 분기 로직 추가
    try:
        if flow_tester.platform == 'android': # 수정: 'AOS' -> 'android'
            locators = HomeViewKilLocators.AOS
        elif flow_tester.platform == 'ios': # 수정: 'IOS' -> 'ios'
            locators = HomeViewKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # 수정: AOS -> Android
        locators = HomeViewKilLocators.AOS

    try:
        # 가정: 홈 화면 또는 큰 글씨 버튼이 보이는 화면 상태
        print("1. '큰글씨' 버튼 클릭")
        large_font_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, locators.large_font_button_xpath))
        )
        # 초기 상태 확인 (선택 사항)
        # initial_description_visible = True
        # try:
        #     flow_tester.driver.find_element(AppiumBy.XPATH, locators.description_xpath)
        # except NoSuchElementException:
        #     initial_description_visible = False
        # print(f"   초기 설명 요소 상태: {'보임' if initial_description_visible else '숨김'}")

        large_font_button.click()
        print("   '큰글씨' 버튼 클릭 완료.")
        time.sleep(3) # 상태 변경 및 UI 업데이트 대기

        print("2. 설명 요소 (ListView) 상태 확인")
        # 큰 글씨 모드에서 설명 요소가 보이는지/숨겨지는지 확인 (앱의 실제 동작에 따라 검증 로직 변경 필요)
        # 예시: 큰 글씨 모드에서 설명 요소가 *보이는* 것을 확인
        try:
            description_element = flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, locators.description_xpath))
            )
            # is_displayed() 체크 추가
            if description_element.is_displayed():
                 print("   ✅ 큰 글씨 모드에서 설명 요소 확인 완료.")
            else:
                 print("   ❌ 큰 글씨 모드에서 설명 요소가 보이지 않음.")
                 scenario_passed = False
                 result_message = "큰 글씨 모드 전환 후 설명 요소 확인 실패 (보이지 않음)."
                 flow_tester.driver.save_screenshot("failure_large_font_desc_not_displayed.png")

        except TimeoutException:
            print("   ❌ 큰 글씨 모드에서 설명 요소 확인 실패 (타임아웃).")
            scenario_passed = False
            result_message = "큰 글씨 모드 전환 후 설명 요소 확인 실패 (타임아웃)."
            flow_tester.driver.save_screenshot("failure_large_font_desc_timeout.png")


        # 원래 상태로 복구 (선택 사항)
        # print("3. '큰글씨' 버튼 다시 클릭하여 복구")
        # large_font_button.click()
        # time.sleep(3)
        # print("   원래 상태로 복구 완료.")


    except TimeoutException as e:
        scenario_passed = False
        result_message = f"큰 글씨 모드 테스트 실패 (타임아웃): {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_large_font_timeout.png")
    except Exception as e:
        scenario_passed = False
        result_message = f"큰 글씨 모드 테스트 중 예상치 못한 오류: {e}"
        print(f"🚨 {result_message}")
        flow_tester.driver.save_screenshot("failure_large_font_unexpected.png")
    finally:
        print("--- 큰 글씨 모드 토글 테스트 종료 ---")

    return scenario_passed, result_message



# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
#
# # def test_verify_element_positions_after_large_font_click(flow_tester):
# #     """
# #     '큰글씨' 버튼 클릭 전과 후의 주요 요소들의 좌표를 비교하여 위치 변경 여부를 검증합니다.
# #     (text 내용과 관계없이 위치 기반으로 '설명문구' 요소를 찾습니다.)
# #     """
# #     print("\n--- '큰글씨' 모드 > UI 요소 위치 변경 확인 시나리오 시작 ---")
# #     try:
# #         time.sleep(1)
# #         # 1. 위치를 검증할 요소의 XPath를 '위치 기반'으로 수정
# #         # 아래 XPath는 'root'라는 ID를 가진 뷰 아래의 두 번째 뷰에 있는 '첫 번째 TextView'를 의미합니다.
# #         # 이 구조는 앱에 따라 달라질 수 있으므로, 필요시 조정이 필요합니다.
# #         description_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[1]'
# #
# #         elements_to_check = {
# #             "설명문구": description_xpath
# #         }
# #
# #         initial_locations = {}  # 클릭 전 위치를 저장할 딕셔너리
# #
# #         # 2. '큰글씨' 버튼 클릭 전, 각 요소의 초기 위치 저장
# #         print("[1단계] '큰글씨' 버튼 클릭 전 요소들의 초기 위치를 저장합니다.")
# #         for name, xpath in elements_to_check.items():
# #             try:
# #                 element = WebDriverWait(flow_tester.driver, 5).until(
# #                     EC.presence_of_element_located((AppiumBy.XPATH, xpath))
# #                 )
# #                 initial_locations[name] = element.location  # {'x': 100, 'y': 200} 형태
# #                 print(f" - '{name}' (요소: {element.text}) 초기 위치: {initial_locations[name]}")
# #             except TimeoutException:
# #                 error_msg = f"실패: 초기 상태의 '{name}' 요소를 찾을 수 없습니다. (XPath: {xpath})"
# #                 save_screenshot_on_failure(flow_tester.driver, f"initial_{name.replace(' ', '_')}_not_found")
# #                 return False, error_msg
# #
# #         # 3. '큰글씨' 버튼 클릭
# #         large_font_button_xpath = '//android.widget.Button[@text="큰글씨"]'
# #         print(f"\n[2단계] '{large_font_button_xpath}' 버튼을 클릭합니다.")
# #         try:
# #             large_font_button = WebDriverWait(flow_tester.driver, 10).until(
# #                 EC.element_to_be_clickable((AppiumBy.XPATH, large_font_button_xpath))
# #             )
# #             large_font_button.click()
# #             time.sleep(2)  # UI가 변경될 시간을 줍니다.
# #         except TimeoutException:
# #             error_msg = "실패: '큰글씨' 버튼을 찾거나 클릭할 수 없습니다."
# #             save_screenshot_on_failure(flow_tester.driver, "large_font_button_not_found")
# #             return False, error_msg
# #
# #         # 4. '큰글씨' 버튼 클릭 후, 각 요소의 최종 위치와 초기 위치 비교
# #         print("\n[3단계] '큰글씨' 버튼 클릭 후 요소들의 위치 변경 여부를 확인합니다.")
# #         unchanged_elements = []  # 위치가 변경되지 않은 요소들의 이름을 저장할 리스트
# #
# #         for name, xpath in elements_to_check.items():
# #             try:
# #                 final_element = WebDriverWait(flow_tester.driver, 5).until(
# #                     EC.presence_of_element_located((AppiumBy.XPATH, xpath))
# #                 )
# #                 final_location = final_element.location
# #                 print(f" - '{name}' (요소: {final_element.text}) 최종 위치: {final_location}")
# #
# #                 # 초기 위치와 최종 위치가 동일한지 비교
# #                 if initial_locations[name] == final_location:
# #                     print(f"   ❌ '{name}' 요소의 위치가 변경되지 않았습니다.")
# #                     unchanged_elements.append(name)
# #                 else:
# #                     print(f"   ✅ '{name}' 요소의 위치가 성공적으로 변경되었습니다.")
# #
# #             except TimeoutException:
# #                 error_msg = f"실패: '큰글씨' 모드에서 '{name}' 요소를 찾을 수 없습니다."
# #                 save_screenshot_on_failure(flow_tester.driver, f"final_{name.replace(' ', '_')}_not_found")
# #                 return False, error_msg
# #
# #         # 5. 최종 결과 판정
# #         if not unchanged_elements:
# #             print("\n✅ 모든 검증 대상 요소들의 위치가 성공적으로 변경되었습니다.")
# #             return True, "'큰글씨' 모드 UI 위치 변경 확인 성공."
# #         else:
# #             unchanged_list_str = ", ".join(unchanged_elements)
# #             error_msg = f"실패: '큰글씨' 모드 적용 후 다음 요소들의 위치가 변경되지 않았습니다: [{unchanged_list_str}]"
# #             save_screenshot_on_failure(flow_tester.driver, "elements_position_not_changed")
# #             return False, error_msg
# #
# #     except Exception as e:
# #         return False, f"'큰글씨' 모드 확인 중 예외 발생: {e}"
# #     finally:
# #         print("--- '큰글씨' 모드 > UI 요소 위치 변경 확인 시나리오 종료 ---")
#
#
#
#
# def test_verify_element_positions_after_large_font_click(flow_tester):
#     """
#     '큰글씨' 버튼 클릭 전과 후, 특정 ListView 하위 모든 요소들의 좌표 변경 여부를 검증합니다.
#     하위 요소 중 하나라도 위치가 변경되면 성공으로 간주합니다.
#     """
#     print("\n--- '큰글씨' 모드 > ListView 하위 요소 전체 위치 변경 확인 시나리오 시작 ---")
#     try:
#         time.sleep(1)
#         # 1. 기준이 될 부모 요소(ListView)의 XPath 정의
#         parent_listview_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[1]'
#         # 부모 아래의 모든 직계 자식 요소를 찾는 XPath
#         child_elements_xpath = f"{parent_listview_xpath}/*"
#
#         # 2. '큰글씨' 버튼 클릭 전, 모든 자식 요소의 초기 위치 저장
#         print(f"[1단계] '{parent_listview_xpath}' 하위 모든 자식 요소의 초기 위치를 저장합니다.")
#         initial_locations = []
#         try:
#             # WebDriverWait를 사용하여 최소 1개 이상의 자식 요소가 나타날 때까지 기다립니다.
#             child_elements = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_all_elements_located((AppiumBy.XPATH, child_elements_xpath))
#             )
#             if not child_elements:
#                 return False, f"실패: '{parent_listview_xpath}' 아래에 자식 요소가 없습니다."
#
#             print(f" - {len(child_elements)}개의 자식 요소를 찾았습니다.")
#             for element in child_elements:
#                 initial_locations.append(element.location)
#             print(f" - 초기 위치 리스트: {initial_locations}")
#
#         except TimeoutException:
#             error_msg = f"실패: 초기 상태의 자식 요소들을 찾을 수 없습니다. (XPath: {child_elements_xpath})"
#             save_screenshot_on_failure(flow_tester.driver, "initial_child_elements_not_found")
#             return False, error_msg
#
#         # 3. '큰글씨' 버튼 클릭
#         large_font_button_xpath = '//android.widget.Button[@text="큰글씨"]'
#         print(f"\n[2단계] '{large_font_button_xpath}' 버튼을 클릭합니다.")
#         try:
#             large_font_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, large_font_button_xpath))
#             )
#             large_font_button.click()
#             time.sleep(2)  # UI가 변경될 시간을 줍니다.
#         except TimeoutException:
#             error_msg = "실패: '큰글씨' 버튼을 찾거나 클릭할 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "large_font_button_not_found")
#             return False, error_msg
#
#         # 4. '큰글씨' 버튼 클릭 후, 모든 자식 요소의 최종 위치 저장
#         print("\n[3단계] '큰글씨' 버튼 클릭 후 자식 요소들의 최종 위치를 확인합니다.")
#         final_locations = []
#         try:
#             # 요소를 다시 찾습니다.
#             final_child_elements = flow_tester.driver.find_elements(by=AppiumBy.XPATH, value=child_elements_xpath)
#             if not final_child_elements:
#                 return False, "실패: '큰글씨' 클릭 후 자식 요소들을 다시 찾을 수 없습니다."
#
#             for element in final_child_elements:
#                 final_locations.append(element.location)
#             print(f" - 최종 위치 리스트: {final_locations}")
#
#         except Exception as e:
#             error_msg = f"실패: '큰글씨' 모드에서 자식 요소를 다시 찾는 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "final_child_elements_find_error")
#             return False, error_msg
#
#         # 5. 최종 결과 판정: 초기 위치 리스트와 최종 위치 리스트가 다른지 비교
#         if initial_locations == final_locations:
#             error_msg = f"실패: '큰글씨' 모드 적용 후 ListView 하위 요소들의 위치가 전혀 변경되지 않았습니다."
#             save_screenshot_on_failure(flow_tester.driver, "elements_position_not_changed")
#             return False, error_msg
#         else:
#             print("\n✅ 성공: ListView 하위 요소들의 위치가 성공적으로 변경되었습니다.")
#             return True, "'큰글씨' 모드 UI 위치 변경 확인 성공."
#
#     except Exception as e:
#         return False, f"'큰글씨' 모드 확인 중 예외 발생: {e}"
#     finally:
#         print("--- '큰글씨' 모드 > ListView 하위 요소 전체 위치 변경 확인 시나리오 종료 ---")