import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Utils.screenshot_helper import save_screenshot_on_failure

def test_verify_recommended_questions_for_managed_customers(flow_tester):
    """
    '관리고객' 버튼 클릭 후, 추천 질문 텍스트가 노출되는지 검증합니다.
    """
    print("\n--- '관리고객' 추천 질문 노출 확인 시나리오 시작 ---")
    try:
        # 1. '관리고객' 버튼 클릭
        time.sleep(2)  # 화면이 로드될 시간을 기다립니다.
        managed_customer_button_xpath = '//android.widget.Button[@text="관리고객"]'
        print(f"'{managed_customer_button_xpath}' 버튼을 클릭합니다.")
        try:
            managed_customer_button = WebDriverWait(flow_tester.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, managed_customer_button_xpath))
            )
            managed_customer_button.click()
            time.sleep(2)  # 화면이 로드될 시간을 기다립니다.
        except TimeoutException:
            error_msg = "실패: '관리고객' 버튼을 찾거나 클릭할 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "managed_customer_button_not_found")
            return False, error_msg

        # 2. 추천 질문 텍스트 노출 확인
        recommendation_text_xpath = "//android.widget.TextView[@text=\"👍'관리 고객'에 대한 추천 질문 입니다.\"]"
        print(f"'{recommendation_text_xpath}' 텍스트가 노출되는지 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, recommendation_text_xpath))
            )
            print("✅ 추천 질문 텍스트가 성공적으로 노출되었습니다.")
            return True, "'관리고객' 추천 질문 확인 성공."
        except TimeoutException:
            error_msg = "실패: '관리고객' 버튼 클릭 후 추천 질문 텍스트를 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "recommended_question_text_not_found")
            return False, error_msg

    except Exception as e:
        return False, f"추천 질문 확인 중 예외 발생: {e}"
    finally:
        print("--- '관리고객' 추천 질문 노출 확인 시나리오 종료 ---");('ㅣ'
                                                     ' ㅜ ㅡ')