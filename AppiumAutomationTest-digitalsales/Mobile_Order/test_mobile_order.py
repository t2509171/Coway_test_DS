import sys
import os
import time

# Ensure the project root and Base directory are in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Xpath 저장소에서 MobileOrderLocators 임포트
from Xpath.xpath_repository import MobileOrderLocators

# 모바일 주문 확인
def test_mobile_order_view(flow_tester):
    """
    주문 > 모바일 주문 버튼 클릭 후, 주문 시작하기 타이틀이 정상적으로 노출되는지 확인합니다.
    [Seller app checklist-119]
    """
    print("\n--- 주문 > 모바일 주문 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = MobileOrderLocators.AOS

    # 홈 화면 로딩을 나타내는 요소
    home_main_element_xpath = locators.home_main_element_xpath # 수정됨

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_main_element_xpath)),
            message="홈 화면의 '홈' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 홈 화면 로딩 완료 확인.")
        # '모바일 주문' 버튼 클릭
        print(" '모바일 주문' 버튼을 찾고 클릭합니다.")
        mobile_order_button_xpath = locators.mobile_order_button_xpath # 수정됨
        try:
            mobile_order_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mobile_order_button_xpath)),
                message=f"'{mobile_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mobile_order_button.click()
            print(" '모바일 주문' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '모바일 주문' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"모바일 주문 버튼 클릭 실패: {e}"
            return False, result_message

        # '주문 시작하기' 타이틀 노출 확인
        print(" '주문 시작하기' 타이틀 노출을 확인합니다.")
        order_start_title_xpath = locators.order_start_title_xpath # 수정됨
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, order_start_title_xpath)),
                message=f"'{order_start_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '주문 시작하기' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "모바일 주문 진입 및 타이틀 확인 성공."
        except Exception as e:
            print(f" '주문 시작하기' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False
            result_message = f"주문 시작하기 타이틀 노출 확인 실패: {e}"
    except Exception as e:
        print(f"🚨 주문 > 모바일 주문 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 주문 > 모바일 주문 진입 및 타이틀 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 일반 주문하기 확인
def test_general_order_acceptance_order_view(flow_tester):
    """
    모바일 주문 > 일반주문 버튼 클릭 후, 일반 탭 타이틀이 정상적으로 노출되는지 확인합니다.
    [Seller app checklist-122]
    """
    print("\n--- 홈 > 모바일 일반 주문하기 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = MobileOrderLocators.AOS

    try:
        # '일반 주문하기' 버튼 클릭
        print(" '일반 주문하기' 버튼을 찾고 클릭합니다.")
        general_order_button_xpath = locators.general_order_button_xpath # 수정됨
        time.sleep(2) # 홈 화면 로딩 대기
        try:
            general_order_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, general_order_button_xpath)),
                message=f"'{general_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            general_order_button.click()
            print(" '일반 주문하기' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '일반 주문하기' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"일반 주문하기 버튼 클릭 실패: {e}"
            # 선행 클릭으로 진입한 모바일 주문 페이지에서 뒤로가기
            flow_tester.driver.back()
            return False, result_message

        # '주문접수' 타이틀 노출 확인
        print(" '주문접수' 타이틀 노출을 확인합니다.")
        order_receipt_title_xpath = locators.order_receipt_title_xpath # 수정됨
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, order_receipt_title_xpath)),
                message=f"'{order_receipt_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '주문접수' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "일반 주문하기 진입 및 타이틀 확인 성공."
        except Exception as e:
            print(f" '주문접수' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False
            result_message = f"주문접수 타이틀 노출 확인 실패: {e}"

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        # 종료 팝업 '확인' 버튼 클릭
        print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
        confirm_button_xpath = locators.confirm_button_xpath # 수정됨
        try:
            confirm_button = flow_tester.wait.until( # 변수명 수정
                EC.element_to_be_clickable((AppiumBy.XPATH, confirm_button_xpath)), # 변수명 수정
                message=f"'{confirm_button_xpath}' 버튼을 20초 내에 찾지 못했습니다." # 변수명 수정
            )
            confirm_button.click() # 변수명 수정
            print(" 종료 팝업 '확인' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
            # 선행 클릭으로 진입한 모바일 주문 페이지에서 뒤로가기
            return False, result_message

    except Exception as e:
        print(f"🚨 모바일 주문 > 일반 주문하기 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 모바일 주문 > 일반 주문하기 진입 및 타이틀 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 사전계약 주문하기 확인
def test_pre_ordering_view(flow_tester):
    """
    모바일 주문 > 사전계약 주문하기 버튼 클릭 후, 재렌탈 사전계약 타이틀이 정상적으로 노출되는지 확인합니다.
    [Seller app checklist-121]
    """
    print("\n--- 모바일 주문 > 사전계약 주문하기 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    time.sleep(2)  # 홈 화면 로딩 대기

    # AOS 로케이터 세트 선택
    locators = MobileOrderLocators.AOS

    try:
        # '사전계약 주문하기' 버튼 클릭
        print(" '사전계약 주문하기' 버튼을 찾고 클릭합니다.")
        pre_contract_order_button_xpath = locators.pre_contract_order_button_xpath # 수정됨
        try:
            pre_contract_order_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, pre_contract_order_button_xpath)),
                message=f"'{pre_contract_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            pre_contract_order_button.click()
            print(" '사전계약 주문하기' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '사전계약 주문하기' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"사전계약 주문하기 버튼 클릭 실패: {e}"
            return False, result_message

        # '재렌탈 사전계약' 타이틀 노출 확인
        print(" '재렌탈 사전계약' 타이틀 노출을 확인합니다.")
        re_rental_pre_contract_title_xpath = locators.re_rental_pre_contract_title_xpath # 수정됨
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, re_rental_pre_contract_title_xpath)),
                message=f"'{re_rental_pre_contract_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '재렌탈 사전계약' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "사전계약 주문하기 진입 및 타이틀 확인 성공."
        except Exception as e:
            print(f" '재렌탈 사전계약' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False
            result_message = f"재렌탈 사전계약 타이틀 노출 확인 실패: {e}"

        time.sleep(2)  # 페이지로 돌아오는 시간 대기
        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        # 종료 팝업 '확인' 버튼 클릭
        print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
        confirm_button_xpath = locators.confirm_button_xpath # 수정됨
        try:
            confirm_button = flow_tester.wait.until( # 변수명 수정
                EC.element_to_be_clickable((AppiumBy.XPATH, confirm_button_xpath)), # 변수명 수정
                message=f"'{confirm_button_xpath}' 버튼을 20초 내에 찾지 못했습니다." # 변수명 수정
            )
            confirm_button.click() # 변수명 수정
            print(" 종료 팝업 '확인' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
            return False, result_message

    except Exception as e:
        print(f"🚨 모바일 주문 > 사전계약 주문하기 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 모바일 주문 > 사전계약 주문하기 진입 및 타이틀 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 일반 주문현황 확인
def test_general_order_status_view(flow_tester):
    """
    모바일 주문 > 일반주문 버튼 클릭 후, 일반 탭 타이틀이 정상적으로 노출되는지 확인합니다.
    [Seller app checklist-122]
    """
    print("\n--- 모바일 주문 > 일반 주문이어하기 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = MobileOrderLocators.AOS

    try:
        # # '일반 주문' 버튼 클릭
        # print(" '일반 주문' 버튼을 찾고 클릭합니다.")
        # general_order_tab_button_xpath = '(//android.widget.Button[@text="0건"])[1]'
        # try:
        #     general_order_tab_button = flow_tester.wait.until(
        #         EC.element_to_be_clickable((AppiumBy.XPATH, general_order_tab_button_xpath)),
        #         message=f"'{general_order_tab_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        #     )
        #     general_order_tab_button.click()
        #     print(" '일반 주문' 버튼 클릭 완료.")
        #     time.sleep(3)
        # except Exception as e:
        #     print(f" '일반 주문' 버튼 클릭 중 오류 발생: {e}")
        #     time.sleep(2)
        #     result_message = f"일반 주문 버튼 클릭 실패: {e}"
        #     return False, result_message

        # --- ✨ 로직 수정 시작 ✨ ---
        # 1. '일반주문' 텍스트 요소를 찾아 Y 좌표를 가져온 후 클릭
        print(" '일반주문' 텍스트의 좌표를 기반으로 버튼을 클릭합니다.")
        general_order_text_xpath = locators.general_order_text_xpath # 수정됨
        target_x_coordinate = 950  # 클릭할 고정 X 좌표
        try:
            # '일반주문' 텍스트 요소를 찾습니다.
            general_order_text_element = flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, general_order_text_xpath)),
                message=f"'{general_order_text_xpath}' 텍스트를 20초 내에 찾지 못했습니다."
            )

            # 요소의 Y 좌표(세로 위치)를 가져옵니다.
            element_location = general_order_text_element.location
            element_size = general_order_text_element.size
            # 요소의 세로 중앙 좌표를 계산하여 더 정확한 클릭을 유도합니다.
            target_y_coordinate = element_location['y'] + (element_size['height'] / 2)

            print(f" - 대상 요소 Y 좌표(중앙): {target_y_coordinate}")
            print(f" - 최종 클릭할 좌표: ({target_x_coordinate}, {target_y_coordinate})")

            # 계산된 좌표를 tap(클릭)합니다.
            flow_tester.driver.tap([(target_x_coordinate, target_y_coordinate)])
            print(" 좌표 기반 클릭 완료.")
            time.sleep(3)
        except Exception as e:
            print(f" '일반주문' 좌표 기반 클릭 중 오류 발생: {e}")
            return False, f"일반 주문 버튼 좌표 클릭 실패: {e}"
        # --- ✨ 로직 수정 종료 ✨ ---



        # '일반' 탭 타이틀 노출 확인
        print(" '일반' 탭 타이틀 노출을 확인합니다.")
        general_tab_title_xpath = locators.general_tab_title_xpath # 수정됨
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, general_tab_title_xpath)),
                message=f"'{general_tab_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '일반' 탭 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "일반주문 탭 진입 및 타이틀 확인 성공."
        except Exception as e:
            print(f" '일반' 탭 타이틀 노출 확인 실패: {e}")
            scenario_passed = False
            result_message = f"일반 탭 타이틀 노출 확인 실패: {e}"

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        # 종료 팝업 '확인' 버튼 클릭
        print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
        confirm_button_xpath = locators.confirm_button_xpath # 수정됨
        try:
            confirm_button = flow_tester.wait.until( # 변수명 수정
                EC.element_to_be_clickable((AppiumBy.XPATH, confirm_button_xpath)), # 변수명 수정
                message=f"'{confirm_button_xpath}' 버튼을 20초 내에 찾지 못했습니다." # 변수명 수정
            )
            confirm_button.click() # 변수명 수정
            print(" 종료 팝업 '확인' 버튼 클릭 완료.")
            time.sleep(3)  # 페이지 전환 대기
        except Exception as e:
            print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
            return False, result_message

    except Exception as e:
        print(f"🚨 모바일 주문 > 일반주문 탭 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 모바일 주문 > 일반주문 탭 진입 및 타이틀 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 사전계약 주문현황 확인
def test_pre_contract_order_status_view(flow_tester):
    """
    모바일 주문 > 일반주문 버튼 클릭 후, 일반 탭 타이틀이 정상적으로 노출되는지 확인합니다.
    [Seller app checklist-122]
    """
    print("\n--- 모바일 주문 > 사전계약 주문 이어하기 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    time.sleep(2)  # 홈 화면 로딩 대기

    # AOS 로케이터 세트 선택
    locators = MobileOrderLocators.AOS

    try:
        # # '일반 주문' 버튼 클릭
        # print(" '일반 주문' 버튼을 찾고 클릭합니다.")
        # general_order_tab_button_xpath = '(//android.widget.Button[@text="0건"])[1]'
        #
        # try:
        #     general_order_tab_button = flow_tester.wait.until(
        #         EC.element_to_be_clickable((AppiumBy.XPATH, general_order_tab_button_xpath)),
        #         message=f"'{general_order_tab_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        #     )
        #     general_order_tab_button.click()
        #     print(" '일반 주문' 버튼 클릭 완료.")
        #     time.sleep(3)
        # except Exception as e:
        #     print(f" '일반 주문' 버튼 클릭 중 오류 발생: {e}")
        #     time.sleep(2)
        #     result_message = f"일반 주문 버튼 클릭 실패: {e}"
        #     return False, result_message

        # --- ✨ 로직 수정 시작 ✨ ---
        # 1. '사전계약 주문'' 텍스트 요소를 찾아 Y 좌표를 가져온 후 클릭
        print(" '사전계약 주문'' 텍스트의 좌표를 기반으로 버튼을 클릭합니다.")
        pre_contract_text_xpath = locators.pre_contract_text_xpath # 수정됨
        target_x_coordinate = 965  # 클릭할 고정 X 좌표
        try:
            # '사전계약 주문'' 텍스트 요소를 찾습니다.
            general_order_text_element = flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, pre_contract_text_xpath)),
                message=f"'{pre_contract_text_xpath}' 텍스트를 20초 내에 찾지 못했습니다."
            )
            # 요소의 Y 좌표(세로 위치)를 가져옵니다.
            element_location = general_order_text_element.location
            element_size = general_order_text_element.size
            # 요소의 세로 중앙 좌표를 계산하여 더 정확한 클릭을 유도합니다.
            target_y_coordinate = element_location['y'] + (element_size['height'] / 1.5)

            print(f" - 대상 요소 Y 좌표(중앙): {target_y_coordinate}")
            print(f" - 최종 클릭할 좌표: ({target_x_coordinate}, {target_y_coordinate})")
            # 계산된 좌표를 tap(클릭)합니다.
            flow_tester.driver.tap([(target_x_coordinate, target_y_coordinate)])
            print(" 좌표 기반 클릭 완료.")
            time.sleep(3)
        except Exception as e:
            print(f" '사전계약 주문'' 좌표 기반 클릭 중 오류 발생: {e}")
            return False, f"사전계약 주문' 버튼 좌표 클릭 실패: {e}"
        # --- ✨ 로직 수정 종료 ✨ ---

        # '사전계약' 탭 타이틀 노출 확인
        print(" '사전계약' 탭 타이틀 노출을 확인합니다.")
        pre_contract_tab_title_xpath = locators.pre_contract_tab_title_xpath # 수정됨
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, pre_contract_tab_title_xpath)),
                message=f"'{pre_contract_tab_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '사전계약' 탭 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "사전계약 주문 탭 진입 및 타이틀 확인 성공."
        except Exception as e:
            print(f" '사전계약' 탭 타이틀 노출 확인 실패: {e}")
            scenario_passed = False
            result_message = f"사전계약 탭 타이틀 노출 확인 실패: {e}"

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        # 종료 팝업 '확인' 버튼 클릭
        print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
        confirm_button_xpath = locators.confirm_button_xpath # 수정됨
        try:
            confirm_button = flow_tester.wait.until( # 변수명 수정
                EC.element_to_be_clickable((AppiumBy.XPATH, confirm_button_xpath)), # 변수명 수정
                message=f"'{confirm_button_xpath}' 버튼을 20초 내에 찾지 못했습니다." # 변수명 수정
            )
            confirm_button.click() # 변수명 수정
            print(" 종료 팝업 '확인' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
            return False, result_message

        # --- ✨ 로직 추가 시작 ✨ ---
        # 4. 홈 화면으로 복귀
        print("\n테스트 완료 후 홈 화면으로 복귀합니다.")
        home_button_xpath = locators.home_button_xpath # 수정됨
        try:
            home_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
            )
            home_button.click()
            print("✅ 홈 버튼을 클릭하여 홈 화면으로 성공적으로 복귀했습니다.")
            time.sleep(3)  # 홈 화면 로딩 대기
            scenario_passed = True
            result_message = "사전계약 주문 테스트 및 홈 화면 복귀 성공."
        except Exception as e:
            result_message = f"홈 버튼 클릭 실패: {e}"
            raise  # 홈으로 못가면 실패처리
        # --- ✨ 로직 추가 종료 ✨ ---
    except Exception as e:
        print(f"🚨 모바일 주문 > 사전계약 탭 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 모바일 주문 > 사전계약 탭 진입 및 타이틀 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")

# import sys
# import os
# import time
#
# # Ensure the project root and Base directory are in the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# # 필요한 라이브러리 임포트
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # 모바일 주문 확인
# def test_mobile_order_view(flow_tester):
#     """
#     주문 > 모바일 주문 버튼 클릭 후, 주문 시작하기 타이틀이 정상적으로 노출되는지 확인합니다.
#     [Seller app checklist-119]
#     """
#     print("\n--- 주문 > 모바일 주문 진입 및 타이틀 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 홈 화면 로딩을 나타내는 요소
#     home_main_element_xpath = '//android.view.View[@content-desc="홈"]'
#
#     try:
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, home_main_element_xpath)),
#             message="홈 화면의 '홈' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
#         )
#         print("✅ 홈 화면 로딩 완료 확인.")
#         # '모바일 주문' 버튼 클릭
#         print(" '모바일 주문' 버튼을 찾고 클릭합니다.")
#         mobile_order_button_xpath = '//android.view.View[@content-desc="모바일 주문"]'
#         try:
#             mobile_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, mobile_order_button_xpath)),
#                 message=f"'{mobile_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             mobile_order_button.click()
#             print(" '모바일 주문' 버튼 클릭 완료.")
#             time.sleep(2)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" '모바일 주문' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"모바일 주문 버튼 클릭 실패: {e}"
#             return False, result_message
#
#         # '주문 시작하기' 타이틀 노출 확인
#         print(" '주문 시작하기' 타이틀 노출을 확인합니다.")
#         order_start_title_xpath = '//android.widget.TextView[@text="주문 시작하기"]'
#         try:
#             flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, order_start_title_xpath)),
#                 message=f"'{order_start_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
#             )
#             print("✅ '주문 시작하기' 타이틀이 성공적으로 노출되었습니다.")
#             scenario_passed = True
#             result_message = "모바일 주문 진입 및 타이틀 확인 성공."
#         except Exception as e:
#             print(f" '주문 시작하기' 타이틀 노출 확인 실패: {e}")
#             scenario_passed = False
#             result_message = f"주문 시작하기 타이틀 노출 확인 실패: {e}"
#     except Exception as e:
#         print(f"🚨 주문 > 모바일 주문 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 주문 > 모바일 주문 진입 및 타이틀 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 일반 주문하기 확인
# def test_general_order_acceptance_order_view(flow_tester):
#     """
#     모바일 주문 > 일반주문 버튼 클릭 후, 일반 탭 타이틀이 정상적으로 노출되는지 확인합니다.
#     [Seller app checklist-122]
#     """
#     print("\n--- 홈 > 모바일 일반 주문하기 UI 요소 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     try:
#         # '일반 주문하기' 버튼 클릭
#         print(" '일반 주문하기' 버튼을 찾고 클릭합니다.")
#         general_order_button_xpath = '//android.widget.Button[@text="일반 주문하기"]'
#         time.sleep(2) # 홈 화면 로딩 대기
#         try:
#             general_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, general_order_button_xpath)),
#                 message=f"'{general_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             general_order_button.click()
#             print(" '일반 주문하기' 버튼 클릭 완료.")
#             time.sleep(2)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" '일반 주문하기' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"일반 주문하기 버튼 클릭 실패: {e}"
#             # 선행 클릭으로 진입한 모바일 주문 페이지에서 뒤로가기
#             flow_tester.driver.back()
#             return False, result_message
#
#         # '주문접수' 타이틀 노출 확인
#         print(" '주문접수' 타이틀 노출을 확인합니다.")
#         order_receipt_title_xpath = '//android.widget.TextView[@text="주문접수"]'
#         try:
#             flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, order_receipt_title_xpath)),
#                 message=f"'{order_receipt_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
#             )
#             print("✅ '주문접수' 타이틀이 성공적으로 노출되었습니다.")
#             scenario_passed = True
#             result_message = "일반 주문하기 진입 및 타이틀 확인 성공."
#         except Exception as e:
#             print(f" '주문접수' 타이틀 노출 확인 실패: {e}")
#             scenario_passed = False
#             result_message = f"주문접수 타이틀 노출 확인 실패: {e}"
#
#         # 뒤로가기 (Back) 액션 수행
#         print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
#         flow_tester.driver.back()
#         print("뒤로가기 액션 수행 완료.")
#         time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기
#
#         # 종료 팝업 '확인' 버튼 클릭
#         print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
#         general_order_button_xpath = '//android.widget.Button[@text="확인"]'
#         try:
#             general_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, general_order_button_xpath)),
#                 message=f"'{general_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             general_order_button.click()
#             print(" 종료 팝업 '확인' 버튼 클릭 완료.")
#             time.sleep(2)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
#             # 선행 클릭으로 진입한 모바일 주문 페이지에서 뒤로가기
#             return False, result_message
#
#     except Exception as e:
#         print(f"🚨 모바일 주문 > 일반 주문하기 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 모바일 주문 > 일반 주문하기 진입 및 타이틀 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 사전계약 주문하기 확인
# def test_pre_ordering_view(flow_tester):
#     """
#     모바일 주문 > 사전계약 주문하기 버튼 클릭 후, 재렌탈 사전계약 타이틀이 정상적으로 노출되는지 확인합니다.
#     [Seller app checklist-121]
#     """
#     print("\n--- 모바일 주문 > 사전계약 주문하기 진입 및 타이틀 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#     time.sleep(2)  # 홈 화면 로딩 대기
#
#     try:
#         # '사전계약 주문하기' 버튼 클릭
#         print(" '사전계약 주문하기' 버튼을 찾고 클릭합니다.")
#         pre_contract_order_button_xpath = '//android.widget.Button[@text="사전계약 주문하기"]'
#         try:
#             pre_contract_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, pre_contract_order_button_xpath)),
#                 message=f"'{pre_contract_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             pre_contract_order_button.click()
#             print(" '사전계약 주문하기' 버튼 클릭 완료.")
#             time.sleep(2)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" '사전계약 주문하기' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"사전계약 주문하기 버튼 클릭 실패: {e}"
#             return False, result_message
#
#         # '재렌탈 사전계약' 타이틀 노출 확인
#         print(" '재렌탈 사전계약' 타이틀 노출을 확인합니다.")
#         re_rental_pre_contract_title_xpath = '//android.widget.TextView[@text="재렌탈 사전계약"]'
#         try:
#             flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, re_rental_pre_contract_title_xpath)),
#                 message=f"'{re_rental_pre_contract_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
#             )
#             print("✅ '재렌탈 사전계약' 타이틀이 성공적으로 노출되었습니다.")
#             scenario_passed = True
#             result_message = "사전계약 주문하기 진입 및 타이틀 확인 성공."
#         except Exception as e:
#             print(f" '재렌탈 사전계약' 타이틀 노출 확인 실패: {e}")
#             scenario_passed = False
#             result_message = f"재렌탈 사전계약 타이틀 노출 확인 실패: {e}"
#
#         time.sleep(2)  # 페이지로 돌아오는 시간 대기
#         # 뒤로가기 (Back) 액션 수행
#         print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
#         flow_tester.driver.back()
#         print("뒤로가기 액션 수행 완료.")
#         time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기
#
#         # 종료 팝업 '확인' 버튼 클릭
#         print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
#         general_order_button_xpath = '//android.widget.Button[@text="확인"]'
#         try:
#             general_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, general_order_button_xpath)),
#                 message=f"'{general_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             general_order_button.click()
#             print(" 종료 팝업 '확인' 버튼 클릭 완료.")
#             time.sleep(2)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
#             return False, result_message
#
#     except Exception as e:
#         print(f"🚨 모바일 주문 > 사전계약 주문하기 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 모바일 주문 > 사전계약 주문하기 진입 및 타이틀 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 일반 주문현황 확인
# def test_general_order_status_view(flow_tester):
#     """
#     모바일 주문 > 일반주문 버튼 클릭 후, 일반 탭 타이틀이 정상적으로 노출되는지 확인합니다.
#     [Seller app checklist-122]
#     """
#     print("\n--- 모바일 주문 > 일반 주문이어하기 진입 및 타이틀 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     try:
#         # # '일반 주문' 버튼 클릭
#         # print(" '일반 주문' 버튼을 찾고 클릭합니다.")
#         # general_order_tab_button_xpath = '(//android.widget.Button[@text="0건"])[1]'
#         # try:
#         #     general_order_tab_button = flow_tester.wait.until(
#         #         EC.element_to_be_clickable((AppiumBy.XPATH, general_order_tab_button_xpath)),
#         #         message=f"'{general_order_tab_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         #     )
#         #     general_order_tab_button.click()
#         #     print(" '일반 주문' 버튼 클릭 완료.")
#         #     time.sleep(3)
#         # except Exception as e:
#         #     print(f" '일반 주문' 버튼 클릭 중 오류 발생: {e}")
#         #     time.sleep(2)
#         #     result_message = f"일반 주문 버튼 클릭 실패: {e}"
#         #     return False, result_message
#
#         # --- ✨ 로직 수정 시작 ✨ ---
#         # 1. '일반주문' 텍스트 요소를 찾아 Y 좌표를 가져온 후 클릭
#         print(" '일반주문' 텍스트의 좌표를 기반으로 버튼을 클릭합니다.")
#         general_order_text_xpath = '//android.widget.TextView[@text="일반주문"]'
#         target_x_coordinate = 950  # 클릭할 고정 X 좌표
#         try:
#             # '일반주문' 텍스트 요소를 찾습니다.
#             general_order_text_element = flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, general_order_text_xpath)),
#                 message=f"'{general_order_text_xpath}' 텍스트를 20초 내에 찾지 못했습니다."
#             )
#
#             # 요소의 Y 좌표(세로 위치)를 가져옵니다.
#             element_location = general_order_text_element.location
#             element_size = general_order_text_element.size
#             # 요소의 세로 중앙 좌표를 계산하여 더 정확한 클릭을 유도합니다.
#             target_y_coordinate = element_location['y'] + (element_size['height'] / 2)
#
#             print(f" - 대상 요소 Y 좌표(중앙): {target_y_coordinate}")
#             print(f" - 최종 클릭할 좌표: ({target_x_coordinate}, {target_y_coordinate})")
#
#             # 계산된 좌표를 tap(클릭)합니다.
#             flow_tester.driver.tap([(target_x_coordinate, target_y_coordinate)])
#             print(" 좌표 기반 클릭 완료.")
#             time.sleep(3)
#         except Exception as e:
#             print(f" '일반주문' 좌표 기반 클릭 중 오류 발생: {e}")
#             return False, f"일반 주문 버튼 좌표 클릭 실패: {e}"
#         # --- ✨ 로직 수정 종료 ✨ ---
#
#
#
#         # '일반' 탭 타이틀 노출 확인
#         print(" '일반' 탭 타이틀 노출을 확인합니다.")
#         general_tab_title_xpath = '//android.view.View[@text="일반"]'
#         try:
#             flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, general_tab_title_xpath)),
#                 message=f"'{general_tab_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
#             )
#             print("✅ '일반' 탭 타이틀이 성공적으로 노출되었습니다.")
#             scenario_passed = True
#             result_message = "일반주문 탭 진입 및 타이틀 확인 성공."
#         except Exception as e:
#             print(f" '일반' 탭 타이틀 노출 확인 실패: {e}")
#             scenario_passed = False
#             result_message = f"일반 탭 타이틀 노출 확인 실패: {e}"
#
#         # 뒤로가기 (Back) 액션 수행
#         print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
#         flow_tester.driver.back()
#         print("뒤로가기 액션 수행 완료.")
#         time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기
#
#         # 종료 팝업 '확인' 버튼 클릭
#         print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
#         general_order_button_xpath = '//android.widget.Button[@text="확인"]'
#         try:
#             general_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, general_order_button_xpath)),
#                 message=f"'{general_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             general_order_button.click()
#             print(" 종료 팝업 '확인' 버튼 클릭 완료.")
#             time.sleep(3)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
#             return False, result_message
#
#     except Exception as e:
#         print(f"🚨 모바일 주문 > 일반주문 탭 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 모바일 주문 > 일반주문 탭 진입 및 타이틀 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 사전계약 주문현황 확인
# def test_pre_contract_order_status_view(flow_tester):
#     """
#     모바일 주문 > 일반주문 버튼 클릭 후, 일반 탭 타이틀이 정상적으로 노출되는지 확인합니다.
#     [Seller app checklist-122]
#     """
#     print("\n--- 모바일 주문 > 사전계약 주문 이어하기 진입 및 타이틀 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#     time.sleep(2)  # 홈 화면 로딩 대기
#     try:
#         # # '일반 주문' 버튼 클릭
#         # print(" '일반 주문' 버튼을 찾고 클릭합니다.")
#         # general_order_tab_button_xpath = '(//android.widget.Button[@text="0건"])[1]'
#         #
#         # try:
#         #     general_order_tab_button = flow_tester.wait.until(
#         #         EC.element_to_be_clickable((AppiumBy.XPATH, general_order_tab_button_xpath)),
#         #         message=f"'{general_order_tab_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         #     )
#         #     general_order_tab_button.click()
#         #     print(" '일반 주문' 버튼 클릭 완료.")
#         #     time.sleep(3)
#         # except Exception as e:
#         #     print(f" '일반 주문' 버튼 클릭 중 오류 발생: {e}")
#         #     time.sleep(2)
#         #     result_message = f"일반 주문 버튼 클릭 실패: {e}"
#         #     return False, result_message
#
#         # --- ✨ 로직 수정 시작 ✨ ---
#         # 1. '사전계약 주문'' 텍스트 요소를 찾아 Y 좌표를 가져온 후 클릭
#         print(" '사전계약 주문'' 텍스트의 좌표를 기반으로 버튼을 클릭합니다.")
#         pre_contract_text_xpath = '//android.widget.TextView[@text="사전계약 주문"]'
#         target_x_coordinate = 965  # 클릭할 고정 X 좌표
#         try:
#             # '사전계약 주문'' 텍스트 요소를 찾습니다.
#             general_order_text_element = flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, pre_contract_text_xpath)),
#                 message=f"'{pre_contract_text_xpath}' 텍스트를 20초 내에 찾지 못했습니다."
#             )
#             # 요소의 Y 좌표(세로 위치)를 가져옵니다.
#             element_location = general_order_text_element.location
#             element_size = general_order_text_element.size
#             # 요소의 세로 중앙 좌표를 계산하여 더 정확한 클릭을 유도합니다.
#             target_y_coordinate = element_location['y'] + (element_size['height'] / 1.5)
#
#             print(f" - 대상 요소 Y 좌표(중앙): {target_y_coordinate}")
#             print(f" - 최종 클릭할 좌표: ({target_x_coordinate}, {target_y_coordinate})")
#             # 계산된 좌표를 tap(클릭)합니다.
#             flow_tester.driver.tap([(target_x_coordinate, target_y_coordinate)])
#             print(" 좌표 기반 클릭 완료.")
#             time.sleep(3)
#         except Exception as e:
#             print(f" '사전계약 주문'' 좌표 기반 클릭 중 오류 발생: {e}")
#             return False, f"사전계약 주문' 버튼 좌표 클릭 실패: {e}"
#         # --- ✨ 로직 수정 종료 ✨ ---
#
#         # '사전계약' 탭 타이틀 노출 확인
#         print(" '사전계약' 탭 타이틀 노출을 확인합니다.")
#         pre_contract_tab_title_xpath = '//android.view.View[@text="사전계약"]'
#         try:
#             flow_tester.wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, pre_contract_tab_title_xpath)),
#                 message=f"'{pre_contract_tab_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
#             )
#             print("✅ '사전계약' 탭 타이틀이 성공적으로 노출되었습니다.")
#             scenario_passed = True
#             result_message = "사전계약 주문 탭 진입 및 타이틀 확인 성공."
#         except Exception as e:
#             print(f" '사전계약' 탭 타이틀 노출 확인 실패: {e}")
#             scenario_passed = False
#             result_message = f"사전계약 탭 타이틀 노출 확인 실패: {e}"
#
#         # 뒤로가기 (Back) 액션 수행
#         print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
#         flow_tester.driver.back()
#         print("뒤로가기 액션 수행 완료.")
#         time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기
#
#         # 종료 팝업 '확인' 버튼 클릭
#         print(" 종료 팝업 '확인' 버튼을 찾고 클릭합니다.")
#         general_order_button_xpath = '//android.widget.Button[@text="확인"]'
#         try:
#             general_order_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, general_order_button_xpath)),
#                 message=f"'{general_order_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#             )
#             general_order_button.click()
#             print(" 종료 팝업 '확인' 버튼 클릭 완료.")
#             time.sleep(2)  # 페이지 전환 대기
#         except Exception as e:
#             print(f" 종료 팝업 '확인' 버튼 클릭 중 오류 발생: {e}")
#             result_message = f"종료 팝업 '확인' 버튼 클릭 실패: {e}"
#             return False, result_message
#
#         # --- ✨ 로직 추가 시작 ✨ ---
#         # 4. 홈 화면으로 복귀
#         print("\n테스트 완료 후 홈 화면으로 복귀합니다.")
#         home_button_xpath = '//android.view.View[@content-desc="홈"]'
#         try:
#             home_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, home_button_xpath))
#             )
#             home_button.click()
#             print("✅ 홈 버튼을 클릭하여 홈 화면으로 성공적으로 복귀했습니다.")
#             time.sleep(3)  # 홈 화면 로딩 대기
#             scenario_passed = True
#             result_message = "사전계약 주문 테스트 및 홈 화면 복귀 성공."
#         except Exception as e:
#             result_message = f"홈 버튼 클릭 실패: {e}"
#             raise  # 홈으로 못가면 실패처리
#         # --- ✨ 로직 추가 종료 ✨ ---
#     except Exception as e:
#         print(f"🚨 모바일 주문 > 사전계약 탭 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 모바일 주문 > 사전계약 탭 진입 및 타이틀 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# if __name__ == "__main__":
#     print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")

