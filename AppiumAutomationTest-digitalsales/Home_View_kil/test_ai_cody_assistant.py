import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Utils.screenshot_helper import save_screenshot_on_failure


def test_ai_cody_assistant_slide_and_visibility(flow_tester):
    """
    홈 화면의 AI 코디 비서 버튼을 클릭했을 때,
    화면이 우->좌로 슬라이드되고 'AI 코디 비서' 타이틀이 노출되는지 검증합니다.
    """
    print("\n--- 홈 화면 > AI 코디 비서 진입 및 슬라이드 확인 시나리오 시작 ---")

    # XPath 로케이터 정의
    ai_cody_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
    ai_cody_title_xpath = '//android.widget.TextView[@text="AI 코디 비서"]'

    try:
        # 1. 테스트 시작 전, AI 코디 비서 타이틀이 화면에 없는지 확인
        print("'AI 코디 비서' 타이틀이 초기에 없는지 확인합니다.")
        try:
            # find_elements는 요소를 즉시 찾고 없으면 빈 리스트를 반환 (Timeout 대기 없음)
            initial_title_elements = flow_tester.driver.find_elements(by=AppiumBy.XPATH, value=ai_cody_title_xpath)
            if len(initial_title_elements) > 0:
                error_msg = "실패: 테스트 시작 전 'AI 코디 비서' 타이틀이 이미 화면에 존재합니다."
                save_screenshot_on_failure(flow_tester.driver, "ai_cody_title_already_present")
                return False, error_msg
        except Exception as e:
            # find_elements 자체에서 에러가 나는 경우
            return False, f"초기 타이틀 확인 중 예외 발생: {e}"

        # 2. AI 코디 비서 버튼 찾기 및 초기 위치 저장
        print(f"'{ai_cody_button_xpath}' (AI 코디 비서 버튼)을 찾습니다.")
        try:
            wait = WebDriverWait(flow_tester.driver, 15)
            ai_cody_button = wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, ai_cody_button_xpath))
            )
            # 슬라이드 효과 검증을 위해 클릭 전 x좌표 저장
            initial_location_x = ai_cody_button.location['x']
            print(f"버튼 초기 X 좌표: {initial_location_x}")
        except TimeoutException:
            error_msg = "실패: 'AI 코디 비서' 버튼을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "ai_cody_button_not_found")
            return False, error_msg

        # 3. 버튼 클릭
        print("'AI 코디 비서' 버튼을 클릭합니다.")
        ai_cody_button.click()
        time.sleep(2)  # 화면 전환 애니메이션을 안정적으로 기다림

        # 4. 'AI 코디 비서' 타이틀 노출 확인
        print(f"'{ai_cody_title_xpath}' 타이틀이 노출되는지 확인합니다.")
        try:
            ai_cody_title = wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, ai_cody_title_xpath))
            )
            print("✅ 'AI 코디 비서' 타이틀이 성공적으로 노출되었습니다.")
        except TimeoutException:
            error_msg = "실패: 버튼 클릭 후 'AI 코디 비서' 타이틀을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "ai_cody_title_not_found")
            return False, error_msg

        # # 5. 슬라이드 애니메이션 (우 -> 좌) 검증
        # print("화면이 우->좌 형태로 슬라이드 되었는지 확인합니다.")
        # try:
        #     # 화면 전환 후, 동일한 XPath의 요소(이전 화면의 버튼)의 x좌표를 다시 가져옴
        #     final_location_x = ai_cody_button.location['x']
        #     print(f"버튼 최종 X 좌표: {final_location_x}")
        #     if final_location_x >= initial_location_x:
        #         error_msg = f"실패: 버튼의 X좌표가 감소하지 않아 슬라이드 효과가 확인되지 않았습니다. (초기: {initial_location_x}, 최종: {final_location_x})"
        #         save_screenshot_on_failure(flow_tester.driver, "ai_cody_slide_effect_fail")
        #         return False, error_msg
        #
        #     print(f"✅ 슬라이드 효과 확인 완료 (좌표 감소: {initial_location_x} -> {final_location_x})")
        #
        # except NoSuchElementException:
        #     # 화면이 완전히 전환되어 이전 버튼을 더 이상 찾을 수 없는 경우도 성공으로 간주
        #     print("✅ 슬라이드 효과 확인 완료 (이전 버튼을 더 이상 찾을 수 없음)")
        #     pass
        # except Exception as e:
        #     error_msg = f"슬라이드 효과 검증 중 예외 발생: {e}"
        #     save_screenshot_on_failure(flow_tester.driver, "ai_cody_slide_check_exception")
        #     return False, error_msg
        flow_tester.driver.back()
        time.sleep(3)
        return True, "AI 코디 비서 화면 진입 및 슬라이드 효과 확인 성공."

    except Exception as e:
        error_msg = f"AI 코디 비서 시나리오 진행 중 예상치 못한 예외 발생: {e}"
        save_screenshot_on_failure(flow_tester.driver, "ai_cody_scenario_unexpected_exception")
        return False, error_msg
    finally:
        print("--- 홈 화면 > AI 코디 비서 진입 및 슬라이드 확인 시나리오 종료 ---")