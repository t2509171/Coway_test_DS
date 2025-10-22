import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re # 숫자 추출을 위해 정규식(re) 모듈을 import 합니다.

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from xml.etree import ElementTree


def find_element_by_coordinate(driver, x, y):
    """
    주어진 좌표(x, y)에 위치한 가장 작은 UI 요소의 속성을 찾아 반환합니다.
    """
    try:
        # 현재 화면의 UI 구조를 XML 형태로 가져옵니다.
        page_source = driver.page_source
        root = ElementTree.fromstring(page_source)

        found_element = None
        smallest_area = float('inf')

        # 모든 노드(UI 요소)를 순회합니다.
        for element in root.iter():
            bounds_str = element.get('bounds')
            if not bounds_str:
                continue

            # bounds 속성값 "[x1,y1][x2,y2]" 에서 숫자만 추출합니다.
            coords = [int(n) for n in re.findall(r'\d+', bounds_str)]
            x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]

            # 주어진 좌표가 요소의 범위 안에 있는지 확인합니다.
            if x1 <= x <= x2 and y1 <= y <= y2:
                # 좌표를 포함하는 요소들 중 가장 작은 영역을 가진 요소를 찾습니다.
                area = (x2 - x1) * (y2 - y1)
                if area < smallest_area:
                    smallest_area = area
                    found_element = element

        if found_element is not None:
            print(f"✅ ({x}, {y}) 좌표에서 요소를 찾았습니다.")
            # 찾은 요소의 주요 속성들을 딕셔너리로 반환합니다.
            attributes = found_element.attrib

            # 이 속성들을 조합하여 XPath를 만들 수 있습니다.
            # 예: //tag[@resource-id='...']
            return attributes
        else:
            print(f"❌ ({x}, {y}) 좌표에서 어떠한 요소도 찾지 못했습니다.")
            return None

    except Exception as e:
        print(f"좌표로 요소 찾기 중 오류 발생: {e}")
        return None





def test_verify_customer_list_elements(flow_tester):
    """
    '관리고객 맞춤 공유하기' 화면의 주요 UI 요소들이 모두 노출되는지 검증합니다.
    """
    print("\n--- '관리고객 맞춤 공유하기' 화면 > 주요 UI 요소 노출 확인 시나리오 시작 ---")
    try:
        # ※ 사전 조건: '관리고객 맞춤 공유하기' 화면에 진입한 상태

        # 1. 검증할 모든 요소들을 딕셔너리 형태로 정의 (작은따옴표로 수정)
        # TODO: 아래 각 요소의 xpath 값을 실제 값으로 채워주세요.
        elements_to_verify = {
            '표시 필터': '//android.view.View[@text="빠른 필터"]',
            '고객 목록': '//android.view.View[@resource-id="root"]/android.widget.ListView[4]',
            '정렬 유형': '//android.view.View[@resource-id="root"]/android.widget.ListView[3]',
            '세부 검색 버튼': '//android.widget.Button[@text="상세 조회"]',
            '토글 버튼': '//android.widget.CheckBox[@resource-id="switch"]',
            '체크박스 선택 모두': '//android.widget.CheckBox[@resource-id="checkAll"]',
            # '하나 선택 체크박스': '',
            # '다음 버튼 [>]': ''
        }

        missing_elements = []  # 미노출된 요소들의 이름을 저장할 리스트

        print("화면에 노출되어야 할 UI 요소들을 순차적으로 확인합니다.")
        # 2. 정의된 각 요소에 대해 노출 여부를 순차적으로 확인
        for element_name, element_xpath in elements_to_verify.items():
            if not element_xpath:
                print(f"⚠️ '{element_name}' 요소의 XPath가 비어있어 검증을 건너뜁니다.")
                continue

            try:
                print(f" - '{element_name}' 요소 확인 중...")
                WebDriverWait(flow_tester.driver, 5).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, element_xpath))
                )
                print(f"   ✅ '{element_name}' 확인 완료.")
            except TimeoutException:
                print(f"   ❌ '{element_name}' 미노출 확인.")
                missing_elements.append(element_name)

        # 3. 최종 결과 판정
        if not missing_elements:
            print("✅ 모든 필수 UI 요소가 성공적으로 노출되었습니다.")
            return True, "관리고객 화면 UI 요소 노출 확인 성공."
        else:
            missing_list_str = ", ".join(missing_elements)
            error_msg = f"실패: 다음 필수 요소가 화면에 노출되지 않았습니다: [{missing_list_str}]"
            save_screenshot_on_failure(flow_tester.driver, "customer_list_elements_missing")
            return False, error_msg

    except Exception as e:
        return False, f"관리고객 화면 UI 요소 확인 중 예외 발생: {e}"
    finally:
        print("--- '관리고객 맞춤 공유하기' 화면 > 주요 UI 요소 노출 확인 시나리오 종료 ---")


def test_verify_filter_result_count_sequentially(flow_tester):
    """
    각 필터 버튼을 개별적으로 클릭하며 조회 결과 건수가 달라지는지 순차적으로 검증합니다.
    """
    print("\n--- '관리고객' 필터별 결과 건수 순차 변경 확인 시나리오 시작 ---")
    try:
        # --- 1단계: '이번주 점검 고객' 필터 적용 및 결과 확인 ---
        print("\n[1단계] '이번주 점검 고객' 필터를 적용합니다.")
        try:
            filter1_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[1]'
            filter1_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, filter1_xpath))
            )
            filter1_element.click()
            time.sleep(2)

            result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
            result1_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, result_count_xpath))
            )
            result1_text = result1_element.text
            print(f" - 1번 필터 결과: '{result1_text}'")

        except TimeoutException as e:
            error_msg = f"실패: 1단계('이번주 점검 고객') 처리 중 요소를 찾을 수 없습니다: {e}"
            save_screenshot_on_failure(flow_tester.driver, "filter1_step_failed")
            return False, error_msg

        # --- 2단계: '사전계약 대상고객' 필터 적용 및 결과 확인 ---
        print("\n[2단계] '사전계약 대상고객' 필터를 적용합니다.")
        try:
            filter2_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[2]'
            filter2_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, filter2_xpath))
            )
            filter2_element.click()
            time.sleep(2)

            result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
            result2_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, result_count_xpath))
            )
            result2_text = result2_element.text
            print(f" - 2번 필터 결과: '{result2_text}'")

        except TimeoutException as e:
            error_msg = f"실패: 2단계('사전계약 대상고객') 처리 중 요소를 찾을 수 없습니다: {e}"
            save_screenshot_on_failure(flow_tester.driver, "filter2_step_failed")
            return False, error_msg

        # --- 3단계: '전체 관리고객' 필터 적용 및 결과 확인 ---
        print("\n[3단계] '전체 관리고객' 필터를 적용합니다.")
        try:
            filter3_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[3]'
            filter3_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, filter3_xpath))
            )
            filter3_element.click()
            time.sleep(2)

            result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
            result3_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, result_count_xpath))
            )
            result3_text = result3_element.text
            print(f" - 3번 필터 결과: '{result3_text}'")

        except TimeoutException as e:
            error_msg = f"실패: 3단계('전체 관리고객') 처리 중 요소를 찾을 수 없습니다: {e}"
            save_screenshot_on_failure(flow_tester.driver, "filter3_step_failed")
            return False, error_msg

        # --- 최종 비교 ---
        print("\n[최종 비교] 3개 필터의 결과가 모두 다른지 확인합니다.")
        if result1_text == result2_text or result2_text == result3_text or result1_text == result3_text:
            error_msg = f"실패: 필터 적용 후 결과가 동일한 항목이 있습니다. (결과: '{result1_text}', '{result2_text}', '{result3_text}')"
            save_screenshot_on_failure(flow_tester.driver, "filter_results_are_the_same")
            return False, error_msg

        print(f"✅ 3개 필터의 결과('{result1_text}', '{result2_text}', '{result3_text}')가 모두 다릅니다.")
        return True, "모든 필터 적용 시 결과 건수가 정상적으로 변경되었습니다."

    except Exception as e:
        return False, f"필터별 결과 건수 순차 확인 중 예외 발생: {e}"
    finally:
        print("--- '관리고객' 필터별 결과 건수 순차 변경 확인 시나리오 종료 ---")



def test_verify_filter_results_sequentially(flow_tester):
    """
    각 필터 위치를 좌표로 클릭하며 조회 결과가 다른지 순차적으로 검증합니다.
    """
    print("\n--- '관리고객' 필터별 결과 순차 변경 확인 시나리오 시작 ---")
    try:
        # --- 1단계: '이번 주 점검 고객' 필터 적용 및 결과 확인 ---
        print("\n[1단계] '이번 주 점검 고객' 필터를 적용합니다.")
        try:
            # --- 여기를 수정했습니다 ---
            coords_filter1 = (230, 650)
            print(f" - 좌표 {coords_filter1}를 클릭합니다.")
            flow_tester.driver.tap([coords_filter1])
            time.sleep(2)
            # --- 여기까지 수정했습니다 ---

            result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
            result1_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, result_count_xpath))
            )
            result1_text = result1_element.text
            print(f" - 1번 필터 결과: '{result1_text}'")

        except Exception as e:
            error_msg = f"실패: 1단계('이번 주 점검 고객') 처리 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "filter1_step_failed")
            return False, error_msg

        # --- 2단계: '사전계약 대상고객' 필터 적용 및 결과 확인 ---
        print("\n[2단계] '사전계약 대상고객' 필터를 적용합니다.")
        try:
            # --- 여기를 수정했습니다 ---
            coords_filter2 = (550, 650)
            print(f" - 좌표 {coords_filter2}를 클릭합니다.")
            flow_tester.driver.tap([coords_filter2])
            time.sleep(2)
            # --- 여기까지 수정했습니다 ---

            result2_xpath = '//android.widget.TextView[contains(@text, "조회결과")]' # 예시 XPath
            result2_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, result2_xpath))
            )
            result2_text = result2_element.text
            print(f" - 2번 필터 결과: '{result2_text}'")

        except Exception as e:
            error_msg = f"실패: 2단계('사전계약 대상고객') 처리 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "filter2_step_failed")
            return False, error_msg

        # --- 3단계: '전체 관리고객' 필터 적용 및 결과 확인 ---
        print("\n[3단계] '전체 관리고객' 필터를 적용합니다.")
        try:
            # --- 여기를 수정했습니다 ---
            coords_filter3 = (860, 650)
            print(f" - 좌표 {coords_filter3}를 클릭합니다.")
            flow_tester.driver.tap([coords_filter3])
            time.sleep(7)
            # --- 여기까지 수정했습니다 ---

            result3_xpath = '//android.widget.TextView[contains(@text, "조회결과")]' # 예시 XPath
            result3_element = WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, result3_xpath))
            )
            result3_text = result3_element.text
            print(f" - 3번 필터 결과: '{result3_text}'")

        except Exception as e:
            error_msg = f"실패: 3단계('전체 관리고객') 처리 중 오류 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "filter3_step_failed")
            return False, error_msg

        # --- 최종 비교 ---
        print("\n[최종 비교] 3개 필터의 결과가 모두 다른지 확인합니다.")
        if result1_text != result2_text and result2_text != result3_text and result1_text != result3_text :
            if result1_text < result3_text and result2_text < result3_text:
                print(f"✅ 3개 필터의 결과('{result1_text}', '{result2_text}', '{result3_text}')가 모두 다릅니다.")
                return True, "모든 필터 적용 시 결과 건수가 정상적으로 변경되었습니다."
        else:
            error_msg = f"실패: 필터 적용 후 결과가 동일한 항목이 있습니다. (결과: '{result1_text}', '{result2_text}', '{result3_text}')"
            save_screenshot_on_failure(flow_tester.driver, "filter_results_are_the_same")
            return False, error_msg

    except Exception as e:
        return False, f"필터별 결과 건수 순차 확인 중 예외 발생: {e}"
    finally:
        print("--- '관리고객' 필터별 결과 건수 순차 변경 확인 시나리오 종료 ---")