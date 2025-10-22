# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
# def test_verify_commission_elements(flow_tester):
#     """
#     '수수료' 탭으로 이동하여 '수수료', '생산율', '수수료 상세' 텍스트 요소가 모두 노출되는지 검증합니다.
#     """
#     print("\n--- 마이페이지 > 수수료 탭 요소 노출 확인 시나리오 시작 ---")
#     try:
#         # 1. '수수료' 탭 클릭 (좌표 기반)
#         commission_coords = (950, 310)
#         print(f"'수수료' 탭 위치인 {commission_coords} 좌표를 클릭합니다.")
#         try:
#             flow_tester.driver.tap([commission_coords])
#             time.sleep(2)  # 탭 전환 애니메이션 대기
#         except Exception as e:
#             error_msg = f"실패: '수수료' 탭 좌표 클릭 중 에러 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "commission_tap_failed")
#             return False, error_msg
#
#         # # 1. '수수료' 탭 클릭
#         # commission_tab_xpath = '//android.view.View[@text="수수료"]'
#         # print(f"'{commission_tab_xpath}' (수수료 탭)을 클릭합니다.")
#         # try:
#         #     commission_tab = WebDriverWait(flow_tester.driver, 10).until(
#         #         EC.presence_of_element_located((AppiumBy.XPATH, commission_tab_xpath))
#         #     )
#         #     commission_tab.click()
#         #     time.sleep(2)  # 탭 전환 애니메이션 대기
#         # except TimeoutException:
#         #     error_msg = "실패: '수수료' 탭을 찾을 수 없습니다."
#         #     save_screenshot_on_failure(flow_tester.driver, "commission_tab_not_found")
#         #     return False, error_msg
#
#         # 2. 필수 텍스트 요소들이 모두 노출되는지 확인
#         print("수수료 화면의 필수 텍스트 요소들을 확인합니다.")
#
#         # 검증할 요소들을 딕셔너리 형태로 정의 (Key: 요소 설명, Value: XPath)
#         elements_to_verify = {
#             "수수료 제목": '//android.widget.TextView[@text="수수료"]',
#             "생산율 라벨": '//android.widget.TextView[@text="생산율"]',
#             "수수료 상세 라벨": '//android.widget.TextView[@text="수수료 상세"]'
#         }
#
#         missing_elements = []  # 미노출된 요소들의 이름을 저장할 리스트
#
#         # 정의된 각 요소에 대해 노출 여부를 순차적으로 확인
#         for element_name, element_xpath in elements_to_verify.items():
#             try:
#                 print(f" - '{element_name}' 요소 확인 중...")
#                 WebDriverWait(flow_tester.driver, 5).until(
#                     EC.presence_of_element_located((AppiumBy.XPATH, element_xpath))
#                 )
#                 print(f"   ✅ '{element_name}' 확인 완료.")
#             except TimeoutException:
#                 print(f"   ❌ '{element_name}' 미노출 확인.")
#                 missing_elements.append(element_name)  # 리스트에 미노출 요소 이름 추가
#
#         # 3. 최종 결과 판정
#         if not missing_elements:
#             # missing_elements 리스트가 비어있으면 모든 요소가 노출된 것이므로 성공
#             print("✅ 모든 필수 요소가 성공적으로 노출되었습니다.")
#             return True, "수수료 탭 요소 노출 확인 성공."
#         else:
#             # 리스트에 항목이 있으면 실패 처리하고, 어떤 요소가 없는지 정확히 알려줌
#             missing_list_str = ", ".join(missing_elements)
#             error_msg = f"실패: 다음 필수 요소가 화면에 노출되지 않았습니다: [{missing_list_str}]"
#             save_screenshot_on_failure(flow_tester.driver, "commission_elements_missing")
#             return False, error_msg
#
#     except Exception as e:
#         return False, f"수수료 탭 요소 확인 중 예외 발생: {e}"
#     finally:
#         print("--- 마이페이지 > 수수료 탭 요소 노출 확인 시나리오 종료 ---")


import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 MyPageKilLocators 임포트
from Xpath.xpath_repository import MyPageKilLocators


def test_verify_commission_elements(flow_tester):
    """
    '수수료' 탭으로 이동하여 '수수료', '생산율', '수수료 상세' 텍스트 요소가 모두 노출되는지 검증합니다.
    """
    print("\n--- 마이페이지 > 수수료 탭 요소 노출 확인 시나리오 시작 ---")

    # AOS 로케이터 세트 선택
    locators = MyPageKilLocators.AOS

    try:
        # 1. '수수료' 탭 클릭 (좌표 기반)
        commission_coords = (950, 310)
        print(f"'수수료' 탭 위치인 {commission_coords} 좌표를 클릭합니다.")
        try:
            flow_tester.driver.tap([commission_coords])
            time.sleep(2)  # 탭 전환 애니메이션 대기
        except Exception as e:
            error_msg = f"실패: '수수료' 탭 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "commission_tap_failed")
            return False, error_msg

        # 1-2. (대안) XPath로 '수수료' 탭 클릭 (좌표가 실패할 경우 대비)
        # commission_tab_xpath = locators.commission_tab_xpath # 수정됨
        # print(f"'{commission_tab_xpath}' (수수료 탭)을 클릭합니다.")
        # try:
        #     commission_tab = WebDriverWait(flow_tester.driver, 10).until(
        #         EC.presence_of_element_located((AppiumBy.XPATH, commission_tab_xpath))
        #     )
        #     commission_tab.click()
        #     time.sleep(2)
        # except TimeoutException:
        #     error_msg = "실패: '수수료' 탭을 찾을 수 없습니다."
        #     save_screenshot_on_failure(flow_tester.driver, "commission_tab_not_found")
        #     return False, error_msg

        # 2. 필수 텍스트 요소들이 모두 노출되는지 확인
        print("수수료 화면의 필수 텍스트 요소들을 확인합니다.")

        # 검증할 요소들을 딕셔너리 형태로 정의 (Key: 요소 설명, Value: XPath)
        elements_to_verify = {
            "수수료 제목": locators.commission_title_xpath,  # 수정됨
            "생산율 라벨": locators.production_rate_label_xpath,  # 수정됨
            "수수료 상세 라벨": locators.commission_detail_label_xpath  # 수정됨
        }

        missing_elements = []  # 미노출된 요소들의 이름을 저장할 리스트

        # 정의된 각 요소에 대해 노출 여부를 순차적으로 확인
        for element_name, element_xpath in elements_to_verify.items():
            try:
                print(f" - '{element_name}' 요소 확인 중...")
                WebDriverWait(flow_tester.driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, element_xpath))
                )
                print(f"   ✅ '{element_name}' 확인 완료.")
            except TimeoutException:
                print(f"   ❌ '{element_name}' 미노출 확인.")
                missing_elements.append(element_name)  # 리스트에 미노출 요소 이름 추가

        # 3. 최종 결과 판정
        if not missing_elements:
            # missing_elements 리스트가 비어있으면 모든 요소가 노출된 것이므로 성공
            print("✅ 모든 필수 요소가 성공적으로 노출되었습니다.")
            return True, "수수료 탭 요소 노출 확인 성공."
        else:
            # 리스트에 항목이 있으면 실패 처리하고, 어떤 요소가 없는지 정확히 알려줌
            missing_list_str = ", ".join(missing_elements)
            error_msg = f"실패: 다음 필수 요소가 화면에 노출되지 않았습니다: [{missing_list_str}]"
            save_screenshot_on_failure(flow_tester.driver, "commission_elements_missing")
            return False, error_msg

    except Exception as e:
        return False, f"수수료 탭 요소 확인 중 예외 발생: {e}"
    finally:
        print("--- 마이페이지 > 수수료 탭 요소 노출 확인 시나리오 종료 ---")