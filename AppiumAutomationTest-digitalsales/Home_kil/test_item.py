# Home_kil/test_item.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


# ----------------------------------------------------------------------------------
# 1. 실제 테스트 동작을 수행하는 내부 공통 함수
# ----------------------------------------------------------------------------------
def _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath):
    """
    (내부용 함수) 단일 항목 테스트의 공통 로직을 수행하고 결과를 True/False로 반환합니다.
    """
    print(f"--- {test_id} 테스트 실행 ---")
    wait = WebDriverWait(flow_tester.driver, 10)

    try:
        home_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, home_xpath)))
        home_element.click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((AppiumBy.XPATH, detail_xpath)))
        print(f"[{test_id}] ✅ 확인 완료.")
        return True

    except (TimeoutException, NoSuchElementException) as e:
        print(f"[{test_id}] ❌ 실패: 요소를 찾지 못했습니다. {e}")
        save_screenshot_on_failure(flow_tester.driver, f"failure_{test_id}")
        return False
    except Exception as e:
        print(f"[{test_id}] ❌ 실패: 예기치 않은 오류. {e}")
        save_screenshot_on_failure(flow_tester.driver, f"failure_{test_id}_exception")
        return False
    finally:
        print(f"[{test_id}] 홈 화면으로 복귀.")
        if home_xpath != '//android.view.View[@content-desc="전체메뉴"]' :
            flow_tester.driver.back()
            time.sleep(2)
        else:
            back = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
            back_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, back)))
            back_element.click()
            time.sleep(2)

# ----------------------------------------------------------------------------------
# 2. 각 체크리스트 항목별 개별 테스트 함수 (총 6개)
# ----------------------------------------------------------------------------------

def test_full_menu(flow_tester):
    """Seller app checklist-41 테스트"""
    test_id = 'Seller app checklist-41'
    home_xpath = '//android.view.View[@content-desc="전체메뉴"]'
    detail_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
    test = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
    return test


def test_checklist_42(flow_tester):
    """Seller app checklist-42 테스트 (보류)"""
    # 이 함수는 실제 테스트를 수행하지 않고, 'Block' 상태를 반환하도록 runner에서 처리합니다.
    # runner와의 일관성을 위해 True를 반환하지만, runner에서는 이 함수의 결과를 사용하지 않습니다.
    return True


def test_management_customer(flow_tester):
    """Seller app checklist-43 테스트"""
    test_id = 'Seller app checklist-43'
    home_xpath = '//android.view.View[@content-desc="관리고객"]'
    detail_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
    return _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)


def test_home(flow_tester):
    """Seller app checklist-44 테스트"""
    test_id = 'Seller app checklist-44'
    home_xpath = '//android.view.View[@content-desc="홈"]'
    detail_xpath = '//android.widget.TextView[@text="디지털세일즈"]'
    return _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)


def test_mobile_order(flow_tester):
    """Seller app checklist-45 테스트"""
    test_id = 'Seller app checklist-45'
    home_xpath = '//android.view.View[@content-desc="모바일 주문"]'
    detail_xpath = '(//android.widget.TextView[@text="모바일 주문"])[1]'
    return _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)


def test_my_page(flow_tester):
    """Seller app checklist-46 테스트"""
    test_id = 'Seller app checklist-46'
    home_xpath = '//android.view.View[@content-desc="마이페이지"]'
    detail_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
    return _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)