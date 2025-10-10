# PythonProject/Menu/test_Menu_view.py

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

# Base 드라이버와 로그인 뷰 클래스 임포트
from Base.base_driver import BaseAppiumDriver

# 마이 페이지 화면 확인
def test_my_page_view(flow_tester):
    """
    전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '마이페이지' 버튼 클릭 (전체메뉴 내)
        print(" '마이페이지' 버튼을 찾고 클릭합니다.")
        # [cite_start][ITQA] 디지털세일즈앱 UI 요소 파일 참조: 전체메뉴 하위 마이페이지의 accessibility id가 '마이페이지' [cite: 30]
        mypage_button_xpath = '//android.view.View[@content-desc="마이페이지"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print(" '마이페이지' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            print(f" '마이페이지' 버튼 클릭 중 오류 발생: {e}")
            return False, f"마이페이지 버튼 클릭 실패: {e}"

        # '마이페이지' 타이틀 노출 확인
        print(" '마이페이지' 타이틀 노출을 확인합니다.")
        # [cite_start][ITQA] 디지털세일즈앱 UI 요소 파일 참조: 마이페이지 타이틀의 XPath가 '(//android.widget.TextView[@text="마이페이지"])[1]' [cite: 30]
        mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '마이페이지' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" '마이페이지' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 홈 페이지로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 전체메뉴 > 마이페이지 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        return scenario_passed, f"시나리오 실행 중 예상치 못한 오류: {e}"

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 최근 본 제품 화면 확인
def test_recent_main_product_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(1)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"전체메뉴 버튼 클릭 실패: {e}"
            return False, result_message

        # '최근 본 제품' 버튼 클릭 (전체메뉴 내)
        print("'최근 본 제품' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.view.View[@content-desc="최근 본 제품"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'최근 본 제품' 버튼 클릭 완료.")
        except Exception as e:
            print(f" '최근 본 제품' 버튼 클릭 중 오류 발생: {e}")
            result_message = f"최근 본 제품 버튼 클릭 실패: {e}"
            return False, result_message

        # '최근 본 제품' 타이틀 노출 확인
        print("'최근 본 제품' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '최근 본 제품' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "최근 본 제품 진입 및 타이틀 확인 성공."
        except Exception as e:
            print(f" '최근 본 제품' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False
            result_message = f"최근 본 제품 타이틀 노출 확인 실패: {e}"
            time.sleep(2)

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        return scenario_passed, result_message  # 결과 반환


    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# 정수기 화면 확인
def test_water_purifier_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # '정수기' 버튼 클릭 (전체메뉴 내)
        print("'정수기' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.view.View[@content-desc="정수기"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'정수기' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '정수기' 버튼 클릭 중 오류 발생: {e}")
            return False, f"정수기 버튼 클릭 실패: {e}"

        # '정수기' 타이틀 노출 확인
        print("'정수기' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="정수기"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '정수기' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" '정수기' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# 청정기 화면 확인
def test_cleaner_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # '청정기' 버튼 클릭 (전체메뉴 내)
        print("'청정기' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.view.View[@content-desc="청정기"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'청정기' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '청정기' 버튼 클릭 중 오류 발생: {e}")
            return False, f"청정기 버튼 클릭 실패: {e}"

        # '청정기' 타이틀 노출 확인
        print("'청정기' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="청정기"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '청정기' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" '청정기' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# 룰루비데/연수기 화면 확인
def test_bide_salter_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # '룰루비데/연수기' 버튼 클릭 (전체메뉴 내)
        print("'룰루비데/연수기' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.view.View[@content-desc="룰루비데/연수기"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'룰루비데/연수기' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '룰루비데/연수기' 버튼 클릭 중 오류 발생: {e}")
            return False, f"룰루비데/연수기 버튼 클릭 실패: {e}"

        # '룰루비데/연수기' 타이틀 노출 확인
        print("'룰루비데/연수기' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="룰루비데/연수기"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '룰루비데/연수기' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" '룰루비데/연수기' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# BEREX 침대 화면 확인
def test_berex_bed_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # 'BEREX 침대' 버튼 클릭 (전체메뉴 내)
        print("'BEREX 침대' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.widget.TextView[@text="BEREX 침대"]' # 오타 수정
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'BEREX 침대' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" 'BEREX 침대' 버튼 클릭 중 오류 발생: {e}")
            return False, f"BEREX 침대 버튼 클릭 실패: {e}"

        # 'BEREX 침대' 타이틀 노출 확인
        print("'BEREX 침대' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="BEREX 침대"]'  #xpath 수정
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ 'BEREX 침대' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" 'BEREX 침대' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# BEREX 안마의자 화면 확인
def test_berex_massage_chair_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # 'BEREX 안마의자' 버튼 클릭 (전체메뉴 내)
        print("'BEREX 안마의자' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.widget.TextView[@text="BEREX 안마의자"]' #xpath 수정
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'BEREX 안마의자' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" 'BEREX 안마의자' 버튼 클릭 중 오류 발생: {e}")
            return False, f"BEREX 안마의자 버튼 클릭 실패: {e}"

        # 'BEREX 안마의자' 타이틀 노출 확인
        print("'BEREX 안마의자' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="BEREX 안마의자"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ 'BEREX 안마의자' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" 'BEREX 안마의자' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# 주방/생활가전 화면 확인
def test_kitchen_home_appliances_menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # '주방/생활가전' 버튼 클릭 (전체메뉴 내)
        print("'주방/생활가전' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.view.View[@content-desc="주방/생활가전"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'주방/생활가전' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '주방/생활가전' 버튼 클릭 중 오류 발생: {e}")
            return False, f"주방/생활가전 버튼 클릭 실패: {e}"

        # '주방/생활가전' 타이틀 노출 확인
        print("'주방/생활가전' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="주방/생활가전"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '주방/생활가전' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" '주방/생활가전' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

# 리퍼브 기획전 화면 확인
def test_refurbished_exhibition_Menu_view(flow_tester):
    """
       전체메뉴 화면에서 마이페이지 버튼 클릭 후, 마이페이지 타이틀이 정상적으로 노출되는지 확인합니다.
       """
    print("\n--- 전체메뉴 > 마이페이지 진입 및 타이틀 확인 시나리오 시작 ---")
    scenario_passed = False
    home_menu_element_xpath = '//android.view.View[@content-desc="전체메뉴"]'  # 메인 화면 로딩을 나타내는 요소

    try:
        flow_tester.wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, home_menu_element_xpath)),
            message="메인 화면의 '전체메뉴' 요소를 20초 내에 찾지 못했습니다. 로딩 실패."
        )
        print("✅ 메인 화면 로딩 완료 확인.")

        # '전체메뉴' 버튼 클릭
        print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        try:
            all_menu_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
                message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            all_menu_button.click()
            print(" '전체메뉴' 버튼 클릭 완료.")
            time.sleep(2)  # 메뉴 열림 대기
        except Exception as e:
            print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")

        # '리퍼브 기획전' 버튼 클릭 (전체메뉴 내)
        print("'리퍼브 기획전' 버튼을 찾고 클릭합니다.")
        mypage_button_xpath = '//android.view.View[@content-desc="리퍼브 기획전"]'
        try:
            mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath)),
                message=f"'{mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            mypage_button.click()
            print("'리퍼브 기획전' 버튼 클릭 완료.")
            time.sleep(2)  # 페이지 전환 대기
        except Exception as e:
            print(f" '리퍼브 기획전' 버튼 클릭 중 오류 발생: {e}")
            return False, f"리퍼브 기획전 버튼 클릭 실패: {e}"

        # '리퍼브 기획전' 타이틀 노출 확인
        print("'리퍼브 기획전' 타이틀 노출을 확인합니다.")
        mypage_title_xpath = '//android.widget.Button[@text="리퍼브 기획전"]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)),
                message=f"'{mypage_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '리퍼브 기획전' 타이틀이 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" '리퍼브 기획전' 타이틀 노출 확인 실패: {e}")
            scenario_passed = False

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(2)  # 홈 페이지로 돌아오는 시간 대기

        if scenario_passed:
            return True, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 성공."
        else:
            return False, "전체메뉴에서 마이페이지 진입 및 타이틀 확인 실패."

    except Exception as e:
        print(f"🚨 최근 본 제품 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"  # 전역 예외 메시지 업데이트
        return scenario_passed, result_message

    finally:
        # 드라이버 종료 호출 제거
        print("--- 전체메뉴 > 최근 본 제품 진입 및 타이틀 확인 시나리오 종료 ---\n")

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, test_Scenario_01.py에서 호출됩니다.")