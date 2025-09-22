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

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# Base 드라이버 클래스 임포트 (BaseAppiumDriver)
from Base.base_driver import BaseAppiumDriver

def _navigate_to_full_menu(flow_tester):
    """
    홈 화면에서 전체메뉴 버튼을 클릭하여 전체 메뉴 화면으로 진입합니다.
    """
    print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
    all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
    try:
        all_menu_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
            message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        all_menu_button.click()
        print(" '전체메뉴' 버튼 클릭 완료.")
        time.sleep(5)  # 메뉴 열림 대기
        return True, ""
    except Exception as e:
        print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")
        return False, f"전체메뉴 버튼 클릭 실패: {e}"

# 라이프스토리 확인
def test_shared_content_lifestory(flow_tester):
    """
    전체 메뉴에서 고객 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 고객 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '라이프스토리' 버튼 클릭
        print(" '라이프스토리' 버튼을 찾고 클릭합니다.")
        lifestory_button_xpath = '//android.view.View[@content-desc="라이프스토리"]' # [cite: 6]
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # '라이프스토리' 요소가 보이는지 확인
                lifestory_element = flow_tester.driver.find_element(AppiumBy.XPATH, lifestory_button_xpath)
                if lifestory_element.is_displayed():
                    print("✅ '라이프스토리' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'라이프스토리' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'라이프스토리' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

                # W3C Actions를 이용한 스크롤 동작
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                                mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(550, 1800)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
                actions.w3c_actions.pointer_action.move_to_location(550, 1100)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                time.sleep(3)  # 스크롤 후 페이지 로딩 대기

        if not scenario_passed:
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '라이프스토리' 요소를 찾지 못했습니다."
            return False, result_message

        try:
            lifestory_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, lifestory_button_xpath)),
                message=f"'{lifestory_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            lifestory_button.click()
            print(" '라이프스토리' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"라이프스토리 버튼 클릭 실패: {e}"
            return False, result_message

        # 3. '라이프스토리 타이틀', '라이프스토리 탭', '라이프스토리 뷰' 노출 확인
        print(" '라이프스토리 타이틀', '라이프스토리 탭', '라이프스토리 뷰' 노출을 확인합니다.")
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]' # [cite: 6]
        lifestory_tab_xpath = '//android.widget.ListView' # [cite: 6]
        lifestory_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]' # [cite: 6]

        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, lifestory_title_xpath)))
            print("✅ '라이프스토리 타이틀'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, lifestory_tab_xpath)))
            print("✅ '라이프스토리 탭'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, lifestory_view_xpath)))
            print("✅ '라이프스토리 뷰'가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "라이프스토리 진입 및 UI 요소 확인 성공."
        except Exception as e:
            result_message = f"라이프스토리 UI 요소 노출 확인 실패: {e}"
            time.sleep(3)
            return False, result_message

        # 4. 뒤로가기 (Back) 액션 수행 (라이프스토리 상세 -> 전체메뉴)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 라이프스토리 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > 라이프스토리 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# e카탈로그 확인
def test_shared_content_ecatalog(flow_tester):
    """
    전체 메뉴에서 판매인 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 판매인 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. 'e카탈로그' 버튼 클릭

        ecatalog_button_xpath = '//android.view.View[@content-desc="e카탈로그"]'  # [cite: 6]
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # 'e카탈로그' 요소가 보이는지 확인
                ecatalog_element = flow_tester.driver.find_element(AppiumBy.XPATH,
                                                                             ecatalog_button_xpath)
                if ecatalog_element.is_displayed():
                    print("✅ 'e카탈로그' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'e카탈로그' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'e카탈로그' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

                # W3C Actions를 이용한 스크롤 동작
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(550, 1800)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
                actions.w3c_actions.pointer_action.move_to_location(550, 1100)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                time.sleep(3)  # 스크롤 후 페이지 로딩 대기

        if not scenario_passed:
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 'e카탈로그' 요소를 찾지 못했습니다."
            return False, result_message

        print(" 'e카탈로그' 버튼을 찾고 클릭합니다.")
        ecatalog_button_xpath = '//android.view.View[@content-desc="e카탈로그"]' # [cite: 6]
        try:
            ecatalog_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, ecatalog_button_xpath)),
                message=f"'{ecatalog_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            ecatalog_button.click()
            print(" 'e카탈로그' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"e카탈로그 버튼 클릭 실패: {e}"
            return False, result_message

        # 3. 'e카탈로그 타이틀', 'e카탈로그 탭', 'e카탈로그 뷰' 노출 확인
        print(" 'e카탈로그 타이틀', 'e카탈로그 탭', 'e카탈로그 뷰' 노출을 확인합니다.")
        ecatalog_title_xpath = '//android.widget.TextView[@text="라이브러리"]' # [cite: 6]
        ecatalog_tab_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView' # [cite: 6]
        ecatalog_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.widget.ListView' # [cite: 6]

        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ecatalog_title_xpath)))
            print("✅ 'e카탈로그 타이틀'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ecatalog_tab_xpath)))
            print("✅ 'e카탈로그 탭'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ecatalog_view_xpath)))
            print("✅ 'e카탈로그 뷰'가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "e카탈로그 진입 및 UI 요소 확인 성공."
        except Exception as e:
            result_message = f"e카탈로그 UI 요소 노출 확인 실패: {e}"
            time.sleep(3)
            return False, result_message

        # 4. 뒤로가기 (Back) 액션 수행 (e카탈로그 상세 -> 전체메뉴)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 e카탈로그 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > e카탈로그 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 제품사용설명서 확인
def test_shared_content_productguide(flow_tester):
    """
    전체 메뉴에서 제품사용설명서 클릭 후, 제품사용설명서 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 제품사용설명서 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '제품사용설명서' 버튼 클릭

        productguide_button_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'  # [cite: 6]
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # '고객 프로모션' 요소가 보이는지 확인
                productguide_element = flow_tester.driver.find_element(AppiumBy.XPATH,
                                                                             productguide_button_xpath)
                if productguide_element.is_displayed():
                    print("✅ '제품사용설명서' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'제품사용설명서' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'제품사용설명서' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

                # W3C Actions를 이용한 스크롤 동작
                actions = ActionChains(flow_tester.driver)
                actions.w3c_actions = ActionBuilder(flow_tester.driver,
                                                    mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
                actions.w3c_actions.pointer_action.move_to_location(550, 1800)
                actions.w3c_actions.pointer_action.pointer_down()
                actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
                actions.w3c_actions.pointer_action.move_to_location(550, 1100)
                actions.w3c_actions.pointer_action.release()
                actions.perform()
                time.sleep(3)  # 스크롤 후 페이지 로딩 대기

        if not scenario_passed:
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '제품사용설명서' 요소를 찾지 못했습니다."
            return False, result_message

        print(" '제품사용설명서' 버튼을 찾고 클릭합니다.")
        productguide_button_xpath = '//android.view.View[@content-desc="제품 사용설명서"]' # [cite: 6]
        try:
            productguide_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, productguide_button_xpath)),
                message=f"'{productguide_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            productguide_button.click()
            print(" '제품사용설명서' 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"제품사용설명서 버튼 클릭 실패: {e}"
            return False, result_message

        # 3. '제품사용설명서 타이틀', '제품사용설명서 탭', '제품사용설명서 뷰' 노출 확인
        print(" '제품사용설명서 타이틀', '제품사용설명서 탭', '제품사용설명서 뷰' 노출을 확인합니다.")
        productguide_title_xpath = '//android.widget.TextView[@text="라이브러리"]' # [cite: 6]
        productguide_tab_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView' # [cite: 6]
        productguide_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.widget.ListView' # [cite: 6]

        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, productguide_title_xpath)))
            print("✅ '제품사용설명서 타이틀'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, productguide_tab_xpath)))
            print("✅ '제품사용설명서 탭'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, productguide_view_xpath)))
            print("✅ '제품사용설명서 뷰'가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "제품사용설명서 진입 및 UI 요소 확인 성공."
        except Exception as e:
            result_message = f"제품사용설명서 UI 요소 노출 확인 실패: {e}"
            time.sleep(3)
            return False, result_message

        # 4. 뒤로가기 (Back) 액션 수행 (제품사용설명서 상세 -> 전체메뉴)
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(3)  # 전체메뉴로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 제품사용설명서 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > 제품사용설명서 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")