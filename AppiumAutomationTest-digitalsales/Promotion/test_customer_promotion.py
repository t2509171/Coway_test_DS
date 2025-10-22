import sys
import os
import time

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

# 스크롤 기능을 위한 임포트
from Utils.scrolling_function import scroll_to_element

# Xpath 저장소에서 PromotionLocators 임포트
from Xpath.xpath_repository import PromotionLocators


def _navigate_to_full_menu(flow_tester):
    """
    홈 화면에서 전체메뉴 버튼을 클릭하여 전체 메뉴 화면으로 진입합니다.
    """
    print(" '전체메뉴' 버튼을 찾고 클릭합니다.")

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS
    all_menu_button_xpath = locators.all_menu_button_xpath  # 수정됨

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


# 고객 프로모션 항목 노출 확인
def test_customer_promotion_view(flow_tester, start_x=None, start_y=None):
    """
    전체 메뉴에서 고객 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 고객 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '고객 프로모션' 항목 노출 확인
        print(" '고객 프로모션' 항목 노출 확인")
        customer_promotion_button_xpath = locators.customer_promotion_button_xpath  # 수정됨

        # scroll_to_element 함수 호출 시 스크롤 좌표 전달
        scenario_passed, result_message = scroll_to_element(
            flow_tester,
            customer_promotion_button_xpath,
            start_x=550,
            start_y=1800,
            end_x=550,
            end_y=1100
        )
        if not scenario_passed:
            return False, result_message

    except Exception as e:
        print(f"🚨 고객 프로모션 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 고객 프로모션 항목 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 고객 프로모션 목록 화면 이동 확인
def test_customer_promotion_click(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 2. '고객 프로모션' 버튼 클릭
    print(" '고객 프로모션' 버튼을 찾고 클릭합니다.")
    customer_promotion_button_xpath = locators.customer_promotion_button_xpath  # 수정됨

    try:
        customer_promotion_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_button_xpath)),
            message=f"'{customer_promotion_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        customer_promotion_button.click()
        print(" '고객 프로모션' 버튼 클릭 완료.")
        time.sleep(1)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"고객 프로모션 버튼 클릭 실패: {e}"
        return False, result_message

        # 3. '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
    print(" '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출을 확인합니다.")
    promotion_title_xpath = locators.promotion_title_xpath  # 수정됨
    promotion_tab_xpath = locators.promotion_tab_xpath  # 수정됨
    promotion_view_xpath = locators.promotion_view_xpath  # 수정됨

    try:
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_title_xpath)))
        print("✅ '프로모션 타이틀'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_tab_xpath)))
        print("✅ '프로모션 탭'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_view_xpath)))
        print("✅ '프로모션 뷰'가 성공적으로 노출되었습니다.")
        scenario_passed = True
        result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(1)
        return False, result_message

    finally:
        print("--- 고객 프로모션 목록 화면 이동 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 고객 프로모션 게시글 노출 확인
def test_customer_promotion_bulletin_view(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 3. '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
    print(" '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출을 확인합니다.")
    promotion_title_xpath = locators.promotion_title_xpath  # 수정됨
    promotion_tab_xpath = locators.promotion_tab_xpath  # 수정됨
    promotion_view_xpath = locators.promotion_view_xpath  # 수정됨

    try:
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_title_xpath)))
        print("✅ '프로모션 타이틀'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_tab_xpath)))
        print("✅ '프로모션 탭'이 성공적으로 노출되었습니다.")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_view_xpath)))
        print("✅ '프로모션 뷰'가 성공적으로 노출되었습니다.")
        scenario_passed = True
        result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(1)
        return False, result_message

    finally:
        print("--- 고객 프로모션 게시글 노출 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 고객 프로모션 상세 게시물 클릭 확인
def test_customer_promotion_detailed_post_click(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 2. '고객 프로모션 상세 게시물' 클릭
    print(" '고객 프로모션 상세 게시물' 을 찾고 클릭합니다.")
    customer_promotion_detailed_post_button_xpath = locators.customer_promotion_detailed_post_button_xpath  # 수정됨

    try:
        customer_promotion_detailed_post_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_detailed_post_button_xpath)),
            message=f"'{customer_promotion_detailed_post_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        customer_promotion_detailed_post_button.click()
        print(" '고객 프로모션 상세 게시물' 클릭 완료.")
        time.sleep(5)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"고객 프로모션 상세 게시물 클릭 실패: {e}"
        return False, result_message

    # 3. '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
    print(" '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
    promotion_list_xpath = locators.promotion_list_xpath  # 수정됨
    promotion_sharing_xpath = locators.promotion_sharing_xpath  # 수정됨

    elements_to_check = [
        (promotion_list_xpath, "✅ '고객 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
        (promotion_sharing_xpath, "✅ '고객 프로모션 상세 게시물 공유하기' 버튼이 성공적으로 노출되었습니다."),
    ]

    try:
        for xpath, success_message in elements_to_check:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            print(success_message)
            time.sleep(1)  # 각 요소 확인 후 1초 대기

        scenario_passed = True
        result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

    finally:
        print("--- 고객 프로모션 상세 게시물 클릭 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 고객 프로모션 상세 게시물 노출 확인
def test_customer_promotion_detailed_post_view(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 3. '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
    print(" '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
    """
    promotion_title1_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
    promotion_title2_xpath = '//android.widget.TextView[@text="Test11"]'
    promotion_state_xpath = '//android.widget.TextView[@text="진행중2024.06.30 ~ 2025.07.31"]'
    promotion_earlier_article_xpath = '//android.widget.Button[@text="이전글"]'
    """
    promotion_list_xpath = locators.promotion_list_xpath  # 수정됨
    promotion_sharing_xpath = locators.promotion_sharing_xpath  # 수정됨

    elements_to_check = [
        # (promotion_title1_xpath, "✅ '고객 프로모션 상세 게시물 타이틀1'이 성공적으로 노출되었습니다."),
        # (promotion_title2_xpath, "✅ '고객 프로모션 상세 게시물 타이틀2'가 성공적으로 노출되었습니다."),
        # (promotion_state_xpath, "✅ '고객 프로모션 상세 게시물 상태'가 성공적으로 노출되었습니다."),
        # (promotion_earlier_article_xpath, "✅ '고객 프로모션 상세 게시물 이전글' 버튼이 성공적으로 노출되었습니다."),
        (promotion_list_xpath, "✅ '고객 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
        (promotion_sharing_xpath, "✅ '고객 프로모션 상세 게시물 공유하기' 버튼이 성공적으로 노출되었습니다."),
    ]

    try:
        for xpath, success_message in elements_to_check:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            print(success_message)
            time.sleep(1)  # 각 요소 확인 후 1초 대기

        scenario_passed = True
        result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

    finally:
        print("--- 고객 프로모션 상세 게시물 노출 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 상세 게시물 목록 버튼 클릭 확인
def test_customer_promotion_detailed_post_list_click(flow_tester):
    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 2. '상세 게시물'의 목록 버튼 클릭
    print(" '상세 게시물'의 목록 버튼을 찾고 클릭합니다.")
    customer_promotion_detailed_post_button_xpath = locators.promotion_list_xpath  # 수정됨

    try:
        customer_promotion_detailed_post_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_detailed_post_button_xpath)),
            message=f"'{customer_promotion_detailed_post_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        customer_promotion_detailed_post_button.click()
        print(" '상세 게시물'의 목록 버튼 클릭 완료.")
        time.sleep(1)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"상세 게시물 목록 버튼 클릭 실패: {e}"
        return False, result_message

    # 3. '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
    print(" '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출을 확인합니다.")
    promotion_title_xpath = locators.promotion_title_xpath  # 수정됨
    promotion_tab_xpath = locators.promotion_tab_xpath  # 수정됨
    promotion_view_xpath = locators.promotion_view_xpath  # 수정됨

    elements_to_check = [
        (promotion_title_xpath, "✅ ''프로모션 타이틀'이 성공적으로 노출되었습니다."),
        (promotion_tab_xpath, "✅ '프로모션 탭'이 성공적으로 노출되었습니다."),
        (promotion_view_xpath, "✅ '프로모션 뷰'가 성공적으로 노출되었습니다."),

    ]

    try:
        for xpath, success_message in elements_to_check:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            print(success_message)
            time.sleep(1)  # 각 요소 확인 후 1초 대기

        scenario_passed = True
        result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        return False, result_message

    finally:
        print("--- 상세 게시물 목록 버튼 클릭 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")











# import sys
# import os
# import time
#
# # 필요한 라이브러리 임포트
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # W3C Actions를 위한 추가 임포트
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions.pointer_input import PointerInput
# from selenium.webdriver.common.actions import interaction
# from selenium.webdriver.common.actions.action_builder import ActionBuilder
#
# # 스크롤 기능을 위한 임포트
# from Utils.scrolling_function import scroll_to_element
#
# def _navigate_to_full_menu(flow_tester):
#     """
#     홈 화면에서 전체메뉴 버튼을 클릭하여 전체 메뉴 화면으로 진입합니다.
#     """
#     print(" '전체메뉴' 버튼을 찾고 클릭합니다.")
#     all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#     try:
#         all_menu_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, all_menu_button_xpath)),
#             message=f"'{all_menu_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         all_menu_button.click()
#         print(" '전체메뉴' 버튼 클릭 완료.")
#         time.sleep(5)  # 메뉴 열림 대기
#         return True, ""
#     except Exception as e:
#         print(f" '전체메뉴' 버튼 클릭 중 오류 발생: {e}")
#         return False, f"전체메뉴 버튼 클릭 실패: {e}"
#
# # 고객 프로모션 항목 노출 확인
# def test_customer_promotion_view(flow_tester, start_x=None, start_y=None):
#     """
#     전체 메뉴에서 고객 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
#     """
#     print("\n--- 전체메뉴 > 고객 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     try:
#         # 1. 전체메뉴 진입
#         nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
#         if not nav_success:
#             return False, nav_msg
#
#         # 2. '고객 프로모션' 항목 노출 확인
#         print(" '고객 프로모션' 항목 노출 확인")
#         customer_promotion_button_xpath = '//android.view.View[@content-desc="고객 프로모션"]'
#
#         # scroll_to_element 함수 호출 시 스크롤 좌표 전달
#         scenario_passed, result_message = scroll_to_element(
#             flow_tester,
#             customer_promotion_button_xpath,
#             start_x=550,
#             start_y=1800,
#             end_x=550,
#             end_y=1100
#         )
#         if not scenario_passed:
#             return False, result_message
#
#     except Exception as e:
#         print(f"🚨 고객 프로모션 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 고객 프로모션 항목 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 고객 프로모션 목록 화면 이동 확인
# def test_customer_promotion_click(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 2. '고객 프로모션' 버튼 클릭
#     print(" '고객 프로모션' 버튼을 찾고 클릭합니다.")
#     customer_promotion_button_xpath = '//android.view.View[@content-desc="고객 프로모션"]'  # [cite: 6]
#
#     try:
#         customer_promotion_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_button_xpath)),
#             message=f"'{customer_promotion_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         customer_promotion_button.click()
#         print(" '고객 프로모션' 버튼 클릭 완료.")
#         time.sleep(1)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"고객 프로모션 버튼 클릭 실패: {e}"
#         return False, result_message
#
#         # 3. '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
#     print(" '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출을 확인합니다.")
#     promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'  # [cite: 6]
#     promotion_tab_xpath = '//android.widget.ListView'  # [cite: 6]
#     promotion_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'  # [cite: 6]
#
#     try:
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_title_xpath)))
#         print("✅ '프로모션 타이틀'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_tab_xpath)))
#         print("✅ '프로모션 탭'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_view_xpath)))
#         print("✅ '프로모션 뷰'가 성공적으로 노출되었습니다.")
#         scenario_passed = True
#         result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(1)
#         return False, result_message
#
#     finally:
#         print("--- 고객 프로모션 목록 화면 이동 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 고객 프로모션 게시글 노출 확인
# def test_customer_promotion_bulletin_view(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 3. '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
#     print(" '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출을 확인합니다.")
#     promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'  # [cite: 6]
#     promotion_tab_xpath = '//android.widget.ListView'  # [cite: 6]
#     promotion_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'  # [cite: 6]
#
#     try:
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_title_xpath)))
#         print("✅ '프로모션 타이틀'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_tab_xpath)))
#         print("✅ '프로모션 탭'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, promotion_view_xpath)))
#         print("✅ '프로모션 뷰'가 성공적으로 노출되었습니다.")
#         scenario_passed = True
#         result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(1)
#         return False, result_message
#
#     finally:
#         print("--- 고객 프로모션 게시글 노출 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 고객 프로모션 상세 게시물 클릭 확인
# def test_customer_promotion_detailed_post_click(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 2. '고객 프로모션 상세 게시물' 클릭
#     print(" '고객 프로모션 상세 게시물' 을 찾고 클릭합니다.")
#     customer_promotion_detailed_post_button_xpath = '(//android.view.View[@content-desc="#"])'  # [cite: 6]
#
#     try:
#         customer_promotion_detailed_post_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_detailed_post_button_xpath)),
#             message=f"'{customer_promotion_detailed_post_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         customer_promotion_detailed_post_button.click()
#         print(" '고객 프로모션 상세 게시물' 클릭 완료.")
#         time.sleep(5)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"고객 프로모션 상세 게시물 클릭 실패: {e}"
#         return False, result_message
#
#     # 3. '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
#     print(" '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
#     promotion_list_xpath = '//android.widget.Button[@text="목록"]'
#     promotion_sharing_xpath = '//android.widget.Button[@text="공유하기"]'
#
#     elements_to_check = [
#         (promotion_list_xpath, "✅ '고객 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
#         (promotion_sharing_xpath, "✅ '고객 프로모션 상세 게시물 공유하기' 버튼이 성공적으로 노출되었습니다."),
#     ]
#
#     try:
#         for xpath, success_message in elements_to_check:
#             flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#             print(success_message)
#             time.sleep(1)  # 각 요소 확인 후 1초 대기
#
#         scenario_passed = True
#         result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     finally:
#         print("--- 고객 프로모션 상세 게시물 클릭 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 고객 프로모션 상세 게시물 노출 확인
# def test_customer_promotion_detailed_post_view(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 3. '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
#     print(" '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
#     """
#     promotion_title1_xpath = '//android.widget.TextView[@text="고객 프로모션"]'
#     promotion_title2_xpath = '//android.widget.TextView[@text="Test11"]'
#     promotion_state_xpath = '//android.widget.TextView[@text="진행중2024.06.30 ~ 2025.07.31"]'
#     promotion_earlier_article_xpath = '//android.widget.Button[@text="이전글"]'
#     """
#     promotion_list_xpath = '//android.widget.Button[@text="목록"]'
#     promotion_sharing_xpath = '//android.widget.Button[@text="공유하기"]'
#
#     elements_to_check = [
#         #(promotion_title1_xpath, "✅ '고객 프로모션 상세 게시물 타이틀1'이 성공적으로 노출되었습니다."),
#         #(promotion_title2_xpath, "✅ '고객 프로모션 상세 게시물 타이틀2'가 성공적으로 노출되었습니다."),
#         #(promotion_state_xpath, "✅ '고객 프로모션 상세 게시물 상태'가 성공적으로 노출되었습니다."),
#         #(promotion_earlier_article_xpath, "✅ '고객 프로모션 상세 게시물 이전글' 버튼이 성공적으로 노출되었습니다."),
#         (promotion_list_xpath, "✅ '고객 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
#         (promotion_sharing_xpath, "✅ '고객 프로모션 상세 게시물 공유하기' 버튼이 성공적으로 노출되었습니다."),
#     ]
#
#     try:
#         for xpath, success_message in elements_to_check:
#             flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#             print(success_message)
#             time.sleep(1)  # 각 요소 확인 후 1초 대기
#
#         scenario_passed = True
#         result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     finally:
#         print("--- 고객 프로모션 상세 게시물 노출 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 상세 게시물 목록 버튼 클릭 확인
# def test_customer_promotion_detailed_post_list_click(flow_tester):
#     # 2. '상세 게시물'의 목록 버튼 클릭
#     print(" '상세 게시물'의 목록 버튼을 찾고 클릭합니다.")
#     customer_promotion_detailed_post_button_xpath = '//android.widget.Button[@text="목록"]'
#
#     try:
#         customer_promotion_detailed_post_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_detailed_post_button_xpath)),
#             message=f"'{customer_promotion_detailed_post_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         customer_promotion_detailed_post_button.click()
#         print(" '상세 게시물'의 목록 버튼 클릭 완료.")
#         time.sleep(1)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"상세 게시물 목록 버튼 클릭 실패: {e}"
#         return False, result_message
#
#     # 3. '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
#     print(" '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출을 확인합니다.")
#     promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'  # [cite: 6]
#     promotion_tab_xpath = '//android.widget.ListView'  # [cite: 6]
#     promotion_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'  # [cite: 6]
#
#     elements_to_check = [
#         (promotion_title_xpath, "✅ ''프로모션 타이틀'이 성공적으로 노출되었습니다."),
#         (promotion_tab_xpath, "✅ '프로모션 탭'이 성공적으로 노출되었습니다."),
#         (promotion_view_xpath, "✅ '프로모션 뷰'가 성공적으로 노출되었습니다."),
#
#     ]
#
#     try:
#         for xpath, success_message in elements_to_check:
#             flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#             print(success_message)
#             time.sleep(1)  # 각 요소 확인 후 1초 대기
#
#         scenario_passed = True
#         result_message = "고객 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         return False, result_message
#
#     finally:
#         print("--- 상세 게시물 목록 버튼 클릭 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# if __name__ == "__main__":
#     print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")