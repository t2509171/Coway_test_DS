# Home_kil/test_item.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


# ----------------------------------------------------------------------------------
# 1. 실제 테스트 동작을 수행하는 내부 공통 함수
# ----------------------------------------------------------------------------------
def _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath):
    """
    (내부용 함수) 단일 항목 테스트의 공통 로직을 수행하고 결과를 True/False로 반환합니다.
    """
    print(f"--- {test_id} 테스트 실행 ---")
    wait = WebDriverWait(flow_tester.driver, 10)

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 클릭할 요소 확인 및 클릭
        print(f"[{test_id}] '{home_xpath}' 요소를 찾습니다...")
        home_element = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, home_xpath))) # 수정됨: presence -> clickable
        print(f"[{test_id}] 요소를 클릭합니다.")
        home_element.click()
        time.sleep(3) # 페이지 전환 대기 시간 증가

        # 상세 페이지 요소 확인
        print(f"[{test_id}] '{detail_xpath}' 요소가 나타나는지 확인합니다...")
        wait.until(EC.presence_of_element_located((AppiumBy.XPATH, detail_xpath)))
        print(f"[{test_id}] ✅ 확인 완료.")
        test_passed = True

    except (TimeoutException, NoSuchElementException) as e:
        print(f"[{test_id}] ❌ 실패: 요소를 찾지 못했거나 시간 초과. {e}")
        save_screenshot_on_failure(flow_tester.driver, f"failure_{test_id}")
        test_passed = False
    except Exception as e:
        print(f"[{test_id}] ❌ 실패: 예기치 않은 오류. {e}")
        save_screenshot_on_failure(flow_tester.driver, f"failure_{test_id}_exception")
        test_passed = False
    finally:
        print(f"[{test_id}] 홈 화면으로 복귀 시도...")
        try:
            # '전체메뉴' 버튼 클릭 후에는 사이드 네비게이션 닫기 버튼을 클릭해야 함
            if home_xpath == locators.menu_button_xpath: # 수정됨 (full_menu_button -> menu_button_xpath)
                back_xpath = locators.sidenav_button_xpath # 수정됨 (full_menu_sidenav -> sidenav_button_xpath)
                print(f"[{test_id}] 전체 메뉴 닫기 버튼 '{back_xpath}' 클릭...")
                back_element = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, back_xpath))) # 수정됨: presence -> clickable
                back_element.click()
            # 다른 경우는 일반적인 뒤로가기
            elif test_passed: # 성공했을 때만 뒤로가기 시도 (실패 시 현재 화면 유지하여 디버깅 용이)
                 print(f"[{test_id}] 뒤로가기 버튼 실행...")
                 flow_tester.driver.back()

            time.sleep(2) # 화면 전환 대기
            print(f"[{test_id}] 홈 화면 복귀 완료 (추정).")
        except Exception as e:
             print(f"[{test_id}] 홈 화면 복귀 중 오류 발생 (무시): {e}")

    return test_passed # 수정됨: boolean 값만 반환하도록 변경


# ----------------------------------------------------------------------------------
# 2. 각 체크리스트 항목별 개별 테스트 함수 (총 6개)
# ----------------------------------------------------------------------------------

def test_full_menu(flow_tester):
    """Seller app checklist-41 테스트"""
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    test_id = "전체메뉴"
    home_xpath = locators.menu_button_xpath # 수정됨 (full_menu_button -> menu_button_xpath)
    detail_xpath = locators.sidenav_button_xpath # 수정됨 (full_menu_sidenav -> sidenav_button_xpath)
    test_passed = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
    return test_passed, f"{test_id} 확인 {'성공' if test_passed else '실패'}" # 수정됨: 결과 메시지 동적 생성


def test_checklist_42(flow_tester):
    """Seller app checklist-42 테스트 (보류)"""
    # 이 함수는 실제 테스트를 수행하지 않고, 'Block' 상태를 반환하도록 runner에서 처리합니다.
    # runner와의 일관성을 위해 True를 반환하지만, runner에서는 이 함수의 결과를 사용하지 않습니다.
    return True, "테스트 보류 (Block 처리 필요)" # 수정됨: 메시지 명확화


def test_management_customer(flow_tester):
    """Seller app checklist-43 테스트"""
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    test_id = "관리고객"
    home_xpath = locators.management_customer_xpath
    detail_xpath = locators.management_customer_title_xpath
    test_passed = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
    return test_passed, f"{test_id} 확인 {'성공' if test_passed else '실패'}"


def test_home(flow_tester):
    """Seller app checklist-44 테스트"""
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    test_id = "홈"
    home_xpath = locators.home_button_xpath # 수정됨 (home_container_xpath -> home_button_xpath)
    detail_xpath = locators.digital_sales_title_xpath # 수정됨 (banner_xpath -> digital_sales_title_xpath)
    test_passed = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
    return test_passed, f"{test_id} 확인 {'성공' if test_passed else '실패'}"


def test_mobile_order(flow_tester):
    """Seller app checklist-45 테스트"""
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    test_id = "모바일 주문"
    home_xpath = locators.mobile_order_button_xpath # 수정됨 (mobile_order_xpath -> mobile_order_button_xpath)
    detail_xpath = locators.mobile_order_title_xpath
    test_passed = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
    return test_passed, f"{test_id} 확인 {'성공' if test_passed else '실패'}"


def test_my_page(flow_tester):
    """Seller app checklist-46 테스트"""
    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---
    test_id = '마이페이지'
    home_xpath = locators.mypage_icon_xpath # 수정됨 (my_page_xpath -> mypage_icon_xpath)
    detail_xpath = locators.mypage_title_xpath
    test_passed = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
    return test_passed, f"{test_id} 확인 {'성공' if test_passed else '실패'}"





# # Home_kil/test_item.py
#
# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# from Utils.screenshot_helper import save_screenshot_on_failure
#
#
# # ----------------------------------------------------------------------------------
# # 1. 실제 테스트 동작을 수행하는 내부 공통 함수
# # ----------------------------------------------------------------------------------
# def _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath):
#     """
#     (내부용 함수) 단일 항목 테스트의 공통 로직을 수행하고 결과를 True/False로 반환합니다.
#     """
#     print(f"--- {test_id} 테스트 실행 ---")
#     wait = WebDriverWait(flow_tester.driver, 10)
#
#     try:
#         home_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, home_xpath)))
#         home_element.click()
#         time.sleep(2)
#
#         wait.until(EC.presence_of_element_located((AppiumBy.XPATH, detail_xpath)))
#         print(f"[{test_id}] ✅ 확인 완료.")
#         return True
#
#     except (TimeoutException, NoSuchElementException) as e:
#         print(f"[{test_id}] ❌ 실패: 요소를 찾지 못했습니다. {e}")
#         save_screenshot_on_failure(flow_tester.driver, f"failure_{test_id}")
#         return False
#     except Exception as e:
#         print(f"[{test_id}] ❌ 실패: 예기치 않은 오류. {e}")
#         save_screenshot_on_failure(flow_tester.driver, f"failure_{test_id}_exception")
#         return False
#     finally:
#         print(f"[{test_id}] 홈 화면으로 복귀.")
#         if home_xpath != '//android.view.View[@content-desc="전체메뉴"]' :
#             flow_tester.driver.back()
#             time.sleep(2)
#         else:
#             back = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
#             back_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, back)))
#             back_element.click()
#             time.sleep(2)
#
# # ----------------------------------------------------------------------------------
# # 2. 각 체크리스트 항목별 개별 테스트 함수 (총 6개)
# # ----------------------------------------------------------------------------------
#
# def test_full_menu(flow_tester):
#     """Seller app checklist-41 테스트"""
#     test_id = "전체메뉴"
#     home_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#     detail_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
#     test = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
#     return test, f"{test_id} 확인 성공"
#
#
# def test_checklist_42(flow_tester):
#     """Seller app checklist-42 테스트 (보류)"""
#     # 이 함수는 실제 테스트를 수행하지 않고, 'Block' 상태를 반환하도록 runner에서 처리합니다.
#     # runner와의 일관성을 위해 True를 반환하지만, runner에서는 이 함수의 결과를 사용하지 않습니다.
#     return True
#
#
# def test_management_customer(flow_tester):
#     """Seller app checklist-43 테스트"""
#     test_id = "관리고객"
#     home_xpath = '//android.view.View[@content-desc="관리고객"]'
#     detail_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
#     test = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
#     return test, f"{test_id} 확인 성공"
#
#
# def test_home(flow_tester):
#     """Seller app checklist-44 테스트"""
#     test_id = "홈"
#     home_xpath = '//android.view.View[@content-desc="홈"]'
#     detail_xpath = '//android.widget.TextView[@text="디지털세일즈"]'
#     test = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
#
#     return test, f"{test_id} 확인 성공"
#
#
# def test_mobile_order(flow_tester):
#     """Seller app checklist-45 테스트"""
#     test_id = "모바일 주문"
#     home_xpath = '//android.view.View[@content-desc="모바일 주문"]'
#     detail_xpath = '(//android.widget.TextView[@text="모바일 주문"])[1]'
#     test = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
#
#     return test, f"{test_id} 확인 성공"
#
#
# def test_my_page(flow_tester):
#     """Seller app checklist-46 테스트"""
#     test_id = '마이페이지'
#     home_xpath = '//android.view.View[@content-desc="마이페이지"]'
#     detail_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
#     test = _perform_single_item_test(flow_tester, test_id, home_xpath, detail_xpath)
#     return test, f"{test_id} 확인 성공"