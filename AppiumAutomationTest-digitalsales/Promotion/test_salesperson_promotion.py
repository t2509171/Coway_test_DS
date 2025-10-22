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


# 판매인 프로모션 항목 노출 확인
def test_salesperson_promotion_view(flow_tester):
    """
    전체 메뉴에서 판매인 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 판매인 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    try:
        # 1. 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 2. '판매인 프로모션' 버튼 클릭
        print(" '판매인 프로모션' 버튼을 찾고 클릭합니다.")
        customer_promotion_button_xpath = locators.salesperson_promotion_button_xpath  # 수정됨
        max_scrolls = 5  # 최대 스크롤 횟수 설정

        for i in range(max_scrolls):
            print(f"스크롤 시도 {i + 1}/{max_scrolls}")
            try:
                # '판매인 프로모션' 요소가 보이는지 확인
                customer_promotion_element = flow_tester.driver.find_element(AppiumBy.XPATH,
                                                                             customer_promotion_button_xpath)
                if customer_promotion_element.is_displayed():
                    print("✅ '판매인 프로모션' 요소가 성공적으로 노출되었습니다.")
                    scenario_passed = True
                    result_message = "'판매인 프로모션' 요소까지 W3C 스크롤 성공."
                    # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
                    break
            except NoSuchElementException:
                # 요소가 현재 화면에 없으면 스크롤 수행
                print("'판매인 프로모션' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")

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
            result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '판매인 프로모션' 요소를 찾지 못했습니다."
            return False, result_message

    except Exception as e:
        print(f"🚨 판매인 프로모션 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > 판매인 프로모션 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 판매인 프로모션 목록 화면 이동 확인
def test_salesperson_promotion_click(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 2. '판매인 프로모션' 버튼 클릭
    print(" '판매인 프로모션' 버튼을 찾고 클릭합니다.")
    customer_promotion_button_xpath = locators.salesperson_promotion_button_xpath  # 수정됨

    try:
        customer_promotion_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_button_xpath)),
            message=f"'{customer_promotion_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        customer_promotion_button.click()
        print(" '판매인 프로모션' 버튼 클릭 완료.")
        time.sleep(5)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"판매인 프로모션 버튼 클릭 실패: {e}"
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
        result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

    return scenario_passed, result_message


# 판매인 프로모션 게시글 노출 확인
def test_salesperson_promotion_bulletin_view(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
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
        result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

    finally:
        print("--- 판매인 프로모션 게시글 노출 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message


# 판매인 프로모션 상세 게시물 클릭 확인
def test_salesperson_promotion_detailed_post_click(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 2. '판매인 프로모션 상세 게시물' 클릭
    print(" '판매인 프로모션 상세 게시물' 을 찾고 클릭합니다.")
    customer_promotion_detailed_post_button_xpath = locators.customer_promotion_detailed_post_button_xpath  # 수정됨

    try:
        customer_promotion_detailed_post_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_detailed_post_button_xpath)),
            message=f"'{customer_promotion_detailed_post_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        customer_promotion_detailed_post_button.click()
        print(" '판매인 프로모션 상세 게시물' 클릭 완료.")
        time.sleep(5)  # 페이지 전환 대기
    except Exception as e:
        result_message = f"판매인 프로모션 상세 게시물 클릭 실패: {e}"
        return False, result_message

    # 3. '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
    print(" '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
    promotion_title1_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'  # [유지] 저장소에 없음
    # promotion_title2_xpath = '//android.widget.TextView[@text="7월 동시구매 할인요금제"]'
    # promotion_state_xpath = '//android.widget.TextView[@text="진행중2025.04.09 ~ 2025.07.31"]'
    # promotion_earlier_article_xpath = '//android.widget.Button[@text="이전글"]'
    promotion_list_xpath = locators.promotion_list_xpath  # 수정됨

    elements_to_check = [
        (promotion_title1_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀1'이 성공적으로 노출되었습니다."),
        # (promotion_title2_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀2'가 성공적으로 노출되었습니다."),
        # (promotion_state_xpath, "✅ '판매인 프로모션 상세 게시물 상태'가 성공적으로 노출되었습니다."),
        # (promotion_earlier_article_xpath, "✅ '판매인 프로모션 상세 게시물 이전글' 버튼이 성공적으로 노출되었습니다."),
        (promotion_list_xpath, "✅ '판매인 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
    ]

    try:
        for xpath, success_message in elements_to_check:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            print(success_message)
            time.sleep(1)  # 각 요소 확인 후 1초 대기

        scenario_passed = True
        result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

    return scenario_passed, result_message


# 판매인 프로모션 상세 게시물 노출 확인
def test_salesperson_promotion_detailed_post_view(flow_tester):
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    # AOS 로케이터 세트 선택
    locators = PromotionLocators.AOS

    # 3. '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
    print(" '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
    promotion_title1_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'  # [유지] 저장소에 없음
    # promotion_title2_xpath = '//android.widget.TextView[@text="7월 동시구매 할인요금제"]'
    # promotion_state_xpath = '//android.widget.TextView[@text="진행중2025.04.09 ~ 2025.07.31"]'
    # promotion_earlier_article_xpath = '//android.widget.Button[@text="이전글"]'
    promotion_list_xpath = locators.promotion_list_xpath  # 수정됨

    elements_to_check = [
        (promotion_title1_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀1'이 성공적으로 노출되었습니다."),
        # (promotion_title2_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀2'가 성공적으로 노출되었습니다."),
        # (promotion_state_xpath, "✅ '판매인 프로모션 상세 게시물 상태'가 성공적으로 노출되었습니다."),
        # (promotion_earlier_article_xpath, "✅ '판매인 프로모션 상세 게시물 이전글' 버튼이 성공적으로 노출되었습니다."),
        (promotion_list_xpath, "✅ '판매인 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
    ]

    try:
        for xpath, success_message in elements_to_check:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            print(success_message)
            time.sleep(1)  # 각 요소 확인 후 1초 대기

        scenario_passed = True
        result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

    return scenario_passed, result_message


# 상세 게시물 목록 버튼 클릭 확인
def test_salesperson_promotion_detailed_post_list_click(flow_tester):
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
        time.sleep(5)  # 페이지 전환 대기
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
            time.sleep(2)  # 각 요소 확인 후 1초 대기

        scenario_passed = True
        result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
    except Exception as e:
        result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
        time.sleep(3)
        return False, result_message

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
# # 판매인 프로모션 항목 노출 확인
# def test_salesperson_promotion_view(flow_tester):
#     """
#     전체 메뉴에서 판매인 프로모션을 클릭 후, 프로모션 타이틀/탭/뷰가 노출되는지 확인합니다.
#     """
#     print("\n--- 전체메뉴 > 판매인 프로모션 진입 및 UI 요소 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     try:
#         # 1. 전체메뉴 진입
#         nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
#         if not nav_success:
#             return False, nav_msg
#
#         # 2. '판매인 프로모션' 버튼 클릭
#         print(" '판매인 프로모션' 버튼을 찾고 클릭합니다.")
#         customer_promotion_button_xpath = '//android.view.View[@content-desc="판매인 프로모션"]' # [cite: 6]
#         max_scrolls = 5  # 최대 스크롤 횟수 설정
#
#         for i in range(max_scrolls):
#             print(f"스크롤 시도 {i + 1}/{max_scrolls}")
#             try:
#                 # '판매인 프로모션' 요소가 보이는지 확인
#                 customer_promotion_element = flow_tester.driver.find_element(AppiumBy.XPATH, customer_promotion_button_xpath)
#                 if customer_promotion_element.is_displayed():
#                     print("✅ '판매인 프로모션' 요소가 성공적으로 노출되었습니다.")
#                     scenario_passed = True
#                     result_message = "'판매인 프로모션' 요소까지 W3C 스크롤 성공."
#                     # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
#                     break
#             except NoSuchElementException:
#                 # 요소가 현재 화면에 없으면 스크롤 수행
#                 print("'판매인 프로모션' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")
#
#                 # W3C Actions를 이용한 스크롤 동작
#                 actions = ActionChains(flow_tester.driver)
#                 actions.w3c_actions = ActionBuilder(flow_tester.driver,
#                                                                 mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#                 actions.w3c_actions.pointer_action.move_to_location(550, 1800)
#                 actions.w3c_actions.pointer_action.pointer_down()
#                 actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
#                 actions.w3c_actions.pointer_action.move_to_location(550, 1100)
#                 actions.w3c_actions.pointer_action.release()
#                 actions.perform()
#                 time.sleep(3)  # 스크롤 후 페이지 로딩 대기
#
#         if not scenario_passed:
#             result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '판매인 프로모션' 요소를 찾지 못했습니다."
#             return False, result_message
#
#     except Exception as e:
#         print(f"🚨 판매인 프로모션 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#     finally:
#         print("--- 전체메뉴 > 판매인 프로모션 진입 및 UI 요소 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 판매인 프로모션 목록 화면 이동 확인
# def test_salesperson_promotion_click(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 2. '판매인 프로모션' 버튼 클릭
#     print(" '판매인 프로모션' 버튼을 찾고 클릭합니다.")
#     customer_promotion_button_xpath = '//android.view.View[@content-desc="판매인 프로모션"]'  # [cite: 6]
#
#     try:
#         customer_promotion_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_button_xpath)),
#             message=f"'{customer_promotion_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         customer_promotion_button.click()
#         print(" '판매인 프로모션' 버튼 클릭 완료.")
#         time.sleep(5)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"판매인 프로모션 버튼 클릭 실패: {e}"
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
#         result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     return scenario_passed, result_message
#
# # 판매인 프로모션 게시글 노출 확인
# def test_salesperson_promotion_bulletin_view(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # '프로모션 타이틀', '프로모션 탭', '프로모션 뷰' 노출 확인
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
#         result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     finally:
#         print("--- 판매인 프로모션 게시글 노출 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 판매인 프로모션 상세 게시물 클릭 확인
# def test_salesperson_promotion_detailed_post_click(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 2. '판매인 프로모션 상세 게시물' 클릭
#     print(" '판매인 프로모션 상세 게시물' 을 찾고 클릭합니다.")
#     customer_promotion_detailed_post_button_xpath = '(//android.view.View[@content-desc="#"])[1]'  # [cite: 6]
#
#     try:
#         customer_promotion_detailed_post_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, customer_promotion_detailed_post_button_xpath)),
#             message=f"'{customer_promotion_detailed_post_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         customer_promotion_detailed_post_button.click()
#         print(" '판매인 프로모션 상세 게시물' 클릭 완료.")
#         time.sleep(5)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"판매인 프로모션 상세 게시물 클릭 실패: {e}"
#         return False, result_message
#
#     # 3. '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
#     print(" '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
#     promotion_title1_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'
#     #promotion_title2_xpath = '//android.widget.TextView[@text="7월 동시구매 할인요금제"]'
#     #promotion_state_xpath = '//android.widget.TextView[@text="진행중2025.04.09 ~ 2025.07.31"]'
#     #promotion_earlier_article_xpath = '//android.widget.Button[@text="이전글"]'
#     promotion_list_xpath = '//android.widget.Button[@text="목록"]'
#
#     elements_to_check = [
#         (promotion_title1_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀1'이 성공적으로 노출되었습니다."),
#         #(promotion_title2_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀2'가 성공적으로 노출되었습니다."),
#         #(promotion_state_xpath, "✅ '판매인 프로모션 상세 게시물 상태'가 성공적으로 노출되었습니다."),
#         #(promotion_earlier_article_xpath, "✅ '판매인 프로모션 상세 게시물 이전글' 버튼이 성공적으로 노출되었습니다."),
#         (promotion_list_xpath, "✅ '판매인 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
#     ]
#
#     try:
#         for xpath, success_message in elements_to_check:
#             flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#             print(success_message)
#             time.sleep(1)  # 각 요소 확인 후 1초 대기
#
#         scenario_passed = True
#         result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     return scenario_passed, result_message
#
# # 판매인 프로모션 상세 게시물 노출 확인
# def test_salesperson_promotion_detailed_post_view(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 3. '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출 확인
#     print(" '상세 게시물 타이틀', '상세 게시물 제목', '상세 게시물 상태', '상세 게시물 이전글', '상세 게시물 목록', '상세 게시물 공유하기' 노출을 확인합니다.")
#     promotion_title1_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'
#     #promotion_title2_xpath = '//android.widget.TextView[@text="7월 동시구매 할인요금제"]'
#     #promotion_state_xpath = '//android.widget.TextView[@text="진행중2025.04.09 ~ 2025.07.31"]'
#     #promotion_earlier_article_xpath = '//android.widget.Button[@text="이전글"]'
#     promotion_list_xpath = '//android.widget.Button[@text="목록"]'
#
#     elements_to_check = [
#         (promotion_title1_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀1'이 성공적으로 노출되었습니다."),
#         #(promotion_title2_xpath, "✅ '판매인 프로모션 상세 게시물 타이틀2'가 성공적으로 노출되었습니다."),
#         #(promotion_state_xpath, "✅ '판매인 프로모션 상세 게시물 상태'가 성공적으로 노출되었습니다."),
#         #(promotion_earlier_article_xpath, "✅ '판매인 프로모션 상세 게시물 이전글' 버튼이 성공적으로 노출되었습니다."),
#         (promotion_list_xpath, "✅ '판매인 프로모션 상세 게시물 목록' 버튼이 성공적으로 노출되었습니다."),
#     ]
#
#     try:
#         for xpath, success_message in elements_to_check:
#             flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#             print(success_message)
#             time.sleep(1)  # 각 요소 확인 후 1초 대기
#
#         scenario_passed = True
#         result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     return scenario_passed, result_message
#
# # 상세 게시물 목록 버튼 클릭 확인
# def test_salesperson_promotion_detailed_post_list_click(flow_tester):
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
#         time.sleep(5)  # 페이지 전환 대기
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
#     ]
#
#     try:
#         for xpath, success_message in elements_to_check:
#             flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
#             print(success_message)
#             time.sleep(2)  # 각 요소 확인 후 1초 대기
#
#         scenario_passed = True
#         result_message = "판매인 프로모션 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"프로모션 UI 요소 노출 확인 실패: {e}"
#         time.sleep(3)
#         return False, result_message
#
#     return scenario_passed, result_message
#
# if __name__ == "__main__":
#     print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")