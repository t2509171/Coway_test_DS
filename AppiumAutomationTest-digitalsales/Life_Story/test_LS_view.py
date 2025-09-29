# 라이브러리 임포트
import re
import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# 좌표 클릭을 위한 임포트
from Utils.click_coordinate import w3c_click_coordinate

from Base.base_driver import BaseAppiumDriver
from Login.test_Login_passed import login_successful

# 스크린샷 헬퍼 함수
from Utils.screenshot_helper import save_screenshot_on_failure

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
def test_lifestory_view(flow_tester):
    """
    전체 메뉴에서 라이프스토리 타이틀/탭/뷰가 노출되는지 확인합니다.
    """
    print("\n--- 전체메뉴 > 라이프스토리 진입 및 UI 요소 확인 시나리오 시작 ---")
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
                time.sleep(1)  # 스크롤 후 페이지 로딩 대기

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
            time.sleep(1)  # 페이지 전환 대기
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
            time.sleep(1)
            # ===== 스크린샷 함수 호출 추가 =====
            save_screenshot_on_failure(flow_tester.driver, "home_search_icon_click")
            # =================================
            return False, result_message

    except Exception as e:
        print(f"🚨 라이프스토리 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 전체메뉴 > 라이프스토리 진입 및 UI 요소 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 라이프스토리 카테고리 글목록 노출 확인
def test_lifestory_details_list_view(flow_tester):

    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 카테고리 '상품브리핑' 노출 및 클릭 확인
        # 상품브리핑 탭 좌표 정의 및 클릭
        first_x = 400
        first_y = 520
        print("\n=== 상품브리핑 탭 좌표 클릭 시작 ===")
        w3c_click_coordinate(flow_tester.driver, first_x, first_y)
        print("\n=== 상품브리핑 탭 좌표 클릭 종료 ===")
        time.sleep(1)  # 클릭 후 페이지 로딩 대기

        # '상품브리핑' 카테고리 리스트 노출 확인
        print("'상품브리핑' 카테고리 리스트 노출을 확인합니다.")
        ls_dv_1_title_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_1_title_xpath)),
                message=f"'{ls_dv_1_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            scenario_passed = True
            result_message = "'상품브리핑' 카테고리 리스트 노출 확인 성공."
        except Exception as e:
            result_message = f"'상품브리핑' 카테고리 리스트 노출 확인 실패: {e}"
            scenario_passed = False
            return False, result_message

    except Exception as e:
        print(f"🚨 라이프스토리 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"라이프스토리 시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 라이프스토리 항목 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 라이프스토리 카테고리 클릭 확인
def test_lifestory_details_list_click(flow_tester):

    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 카테고리 '상품브리핑' 게시글 클릭 확인
        print("'상품브리핑' 카테고리 게시글을 찾고 클릭합니다.")
        ls_dv_tab1_details_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.view.View[2]'
        try:
            ls_dv_tab1_details_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab1_details_button_xpath)),
                message=f"'{ls_dv_tab1_details_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            ls_dv_tab1_details_button.click()
            print("'상품브리핑' 카테고리 탭 게시글 클릭 완료.")
            time.sleep(1)  # 페이지 전환 대기
        except Exception as e:
            print(f"'상품브리핑' 카테고리 탭 게시글 클릭 중 오류 발생: {e}")
            return False, f"'상품브리핑' 카테고리 탭 게시글 클릭 실패: {e}"

        # '상품브리핑' 카테고리 게시글 타이틀, 뷰 노출 확인
        print("'상품브리핑' 카테고리 리스트 노출을 확인합니다.")
        ls_dv_tab1_details_title_xpath = '//android.widget.TextView[@text="라이프 스토리"]'
        ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab1_details_title_xpath)))
            print("✅ '상세글 타이틀'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab1_details_view_xpath)))
            print("✅ '상세글 뷰'가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "'상품브리핑' 카테고리 게시글 타이틀, 뷰 노출 확인 성공."
        except Exception as e:
            result_message = f"'상품브리핑' 카테고리 게시글 타이틀, 뷰 노출 확인 실패: {e}"
            return False, result_message

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(1)  # 전체메뉴로 돌아오는 시간 대기

        # 카테고리 '라이프팁' 노출 및 클릭 확인
        # 라이프팁 탭 좌표 정의 및 클릭
        first_x = 680
        first_y = 520
        print("\n=== 라이프팁 탭 좌표 클릭 시작 ===")
        w3c_click_coordinate(flow_tester.driver, first_x, first_y)
        print("\n=== 라이프팁 탭 좌표 클릭 종료 ===")
        time.sleep(1)  # 클릭 후 페이지 로딩 대기

        # '라이프팁' 카테고리 리스트 노출 확인
        print("'라이프팁' 카테고리 리스트 노출을 확인합니다.")
        ls_dv_tab2_title_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        try:
            flow_tester.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab2_title_xpath)),
                message=f"'{ls_dv_tab2_title_xpath}' 타이틀을 20초 내에 찾지 못했습니다."
            )
            print("✅ '라이프팁' 카테고리 리스트가 성공적으로 노출되었습니다.")
            scenario_passed = True
        except Exception as e:
            print(f" 라이프팁' 카테고리 리스트 노출 확인 실패: {e}")
            scenario_passed = False
        
        # 카테고리 '라이프팁' 게시글 클릭 확인
        print("'라이프팁' 카테고리 게시글을 찾고 클릭합니다.")
        ls_dv_tab2_details_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.view.View[2]'
        try:
            ls_dv_tab2_details_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_details_button_xpath)),
                message=f"'{ls_dv_tab2_details_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            ls_dv_tab2_details_button.click()
            print("'라이프팁' 카테고리 탭 게시글 클릭 완료.")
            time.sleep(1)  # 페이지 전환 대기
        except Exception as e:
            print(f"'라이프팁' 카테고리 탭 게시글 클릭 중 오류 발생: {e}")
            return False, f"'라이프팁' 카테고리 탭 게시글 클릭 실패: {e}"

        # '라이프팁' 카테고리 게시글 타이틀, 뷰 노출 확인
        print("'라이프팁' 카테고리 리스트 노출을 확인합니다.")
        ls_dv_tab2_details_title_xpath = '//android.widget.TextView[@text="라이프 스토리"]'
        ls_dv_tab2_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        try:
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab2_details_title_xpath)))
            print("✅ '상세글 타이틀'이 성공적으로 노출되었습니다.")
            flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, ls_dv_tab2_details_view_xpath)))
            print("✅ '상세글 뷰'가 성공적으로 노출되었습니다.")
            scenario_passed = True
            result_message = "'라이프팁' 카테고리 게시글 타이틀, 뷰 노출 확인 성공."
        except Exception as e:
            result_message = f"'라이프팁' 카테고리 게시글 타이틀, 뷰 노출 확인 실패: {e}"
            return False, result_message

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(1)  # 전체메뉴로 돌아오는 시간 대기

        # 뒤로가기 (Back) 액션 수행
        print("뒤로가기 버튼(디바이스 백 버튼)을 클릭합니다.")
        flow_tester.driver.back()
        print("뒤로가기 액션 수행 완료.")
        time.sleep(1)  # 전체메뉴로 돌아오는 시간 대기

    except Exception as e:
        print(f"🚨 라이프스토리 카테고리 클릭 확인 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
    finally:
        print("--- 라이프스토리 카테고리 클릭 확인 시나리오 종료 ---\n")
    return scenario_passed, result_message

# 라이프스토리 공유하기 > 카카오톡 공유하기 (74)
def test_lifestory_sharing_kakao(flow_tester):
    appium_driver = None
    # 마이페이지 버튼 클릭 확인
    print("마이페이지 버튼을 찾고 클릭합니다.")
    home_mypage_button_xpath = '//android.view.View[@content-desc="마이페이지"]'
    try:
        home_mypage_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, home_mypage_button_xpath)),
            message=f"'{home_mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        home_mypage_button.click()
        print("마이페이지 버튼 클릭 완료.")
        time.sleep(1)  # 페이지 전환 대기
        return True, "마이페이지 버튼 클릭 성공"
    except Exception as e:
        result_message = f"마이페이지 버튼 클릭 중 오류 발생: {e}"
        time.sleep(1)
        return False, result_message

# 카카오톡 공유하기 수행 함수
def test_lifestory_perform_kakao_share(flow_tester):
    """
    라이프스토리 게시글을 카카오톡으로 공유하는 액션만 수행합니다.
    """
    print("\n--- 라이프스토리 카카오톡 공유 액션 시작 ---")
    try:
        # 1. 라이프스토리 페이지로 이동
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        lifestory_button_xpath = '//android.view.View[@content-desc="라이프스토리"]'
        lifestory_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, lifestory_button_xpath)),
            message=f"'{lifestory_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        lifestory_button.click()
        time.sleep(5)

        # 2. 공유하기 버튼 클릭
        print("카테고리 게시글 공유하기 버튼을 찾고 클릭합니다.")
        ls_dv_tab2_Sharing_button_xpath = '(//android.widget.Button[@text="공유하기"])[1]'
        ls_dv_tab2_Sharing_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_Sharing_button_xpath)),
            message=f"'{ls_dv_tab2_Sharing_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        ls_dv_tab2_Sharing_button.click()
        time.sleep(5)

        # 3. 공유하기 팝업 > 카카오톡 버튼 클릭
        print("공유하기 팝업 > 카카오톡 버튼을 찾고 클릭합니다.")
        ls_dv_tab2_Sharing_kakao_button_xpath = '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.coway.catalog.seller.stg:id/layout_kakao"]/android.widget.ImageView[2]'
        ls_dv_tab2_Sharing_kakao_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_Sharing_kakao_button_xpath)),
            message=f"'{ls_dv_tab2_Sharing_kakao_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        ls_dv_tab2_Sharing_kakao_button.click()
        time.sleep(5)

        # 4. '광고성 정보 전송에 따른 의무사항' 팝업 '동의합니다' 버튼 클릭
        print("'광고성 정보 전송에 따른 의무사항' 팝업 '동의합니다' 버튼을 클릭합니다.")
        ls_dv_tab2_Sharing_popup_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        ls_dv_tab2_Sharing_popup_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_Sharing_popup_button_xpath)),
            message=f"'{ls_dv_tab2_Sharing_popup_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        ls_dv_tab2_Sharing_popup_button.click()
        time.sleep(3)

        # 5. 카카오톡 친구하기 탭 클릭
        ls_dv_tab2_Sharing_kakao_tab_button_xpath = '//android.widget.TextView[@resource-id="com.kakao.talk:id/txt_title" and @text="친구"]'
        ls_dv_tab2_Sharing_kakao_tab_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_Sharing_kakao_tab_button_xpath)),
            message=f"'{ls_dv_tab2_Sharing_kakao_tab_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
        )
        ls_dv_tab2_Sharing_kakao_tab_button.click()
        time.sleep(3)

        # 카카오톡 프로필 클릭 후, 확인 버튼 클릭 확인
        ls_dv_tab2_Sharing_kakao_profile_button_xpath = '(//android.widget.CheckBox[@resource-id="com.kakao.talk:id/check"])[1]'
        ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath = '//android.widget.Button[@resource-id="com.kakao.talk:id/button"]'
        try:
            ls_dv_tab2_Sharing_kakao_profile_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_Sharing_kakao_profile_button_xpath)),
                message=f"'{ls_dv_tab2_Sharing_kakao_profile_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            ls_dv_tab2_Sharing_kakao_profile_button.click()
            print(f"✅ 카카오톡 친구하기 탭 클릭 완료")
            time.sleep(2)  # 클릭 후 페이지 로딩 대기

            ls_dv_tab2_Sharing_kakao_profile_ok_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath)),
                message=f"'{ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            ls_dv_tab2_Sharing_kakao_profile_ok_button.click()
            print(f"✅ 카카오톡 친구하기 탭 클릭 완료")
            time.sleep(2)  # 클릭 후 페이지 로딩 대기
        except Exception as e:
            result_message = f"카카오톡 친구하기 탭 클릭 중 오류 발생: {e}"
            time.sleep(3)
            return False, result_message

        print("✅ 카카오톡 공유 액션 완료.")
        return True, ""
    except Exception as e:
        print(f"🚨 카카오톡 공유 액션 중 오류 발생: {e}")
        return False, f"카카오톡 공유 액션 실패: {e}"

# 공유하기 건수 카운트를 찾아 숫자를 추출하는 함수
def get_share_count(driver):
    """
    공유하기 카운트 텍스트를 찾아 숫자를 추출하는 함수
    """
    try:
        # Step 1: WebDriverWait를 사용하여 요소가 나타날 때까지 명시적 대기
        element_xpath = '(//android.widget.TextView[contains(@text, "건")])'

        wait = WebDriverWait(driver, 10)
        share_count_element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, element_xpath))
        )

        # Step 2: 찾은 요소의 실제 텍스트를 가져옴
        full_text = share_count_element.text
        logging.info(f"요소에서 추출된 전체 텍스트: {full_text}")

        # Step 3: 정규 표현식을 사용하여 숫자 추출
        match = re.search(r'(\d+)\s*건', full_text)

        if match:
            # 매칭에 성공한 경우
            share_count = int(match.group(1))
            logging.info(f"공유 건수 추출 성공: {share_count}")
            # 성공 시 튜플로 반환
            return share_count, ""
        else:
            # 정규 표현식 매칭에 실패한 경우
            error_message = "정규 표현식으로 '건' 앞의 숫자를 찾을 수 없습니다."
            logging.error(error_message)
            return -1, error_message

    except Exception as e:
        # 요소 자체를 찾지 못하거나 다른 예외 발생 시
        error_message = f"공유 건수 요소를 찾는 중 오류 발생: {e}"
        logging.error(error_message)
        # 실패 시 튜플로 반환
        return -1, error_message

# 공유하기 카운트 증가 확인 (75)
def test_lifestory_share_count_increase(flow_tester):
    """
    마이페이지의 공유하기 카운트가 1 증가하는지 확인하는 테스트 스크립트.
    """
    print("\n--- 마이페이지 내가 공유한 방법 '카카오톡' 공유하기 카운트 증가 확인 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    try:
        # 1. 초기 공유하기 카운트 확인
        print("💡 1단계: 초기 마이페이지 공유하기 카운트 획득")
        # 전체메뉴 진입
        nav_success, nav_msg = _navigate_to_full_menu(flow_tester)
        if not nav_success:
            return False, nav_msg

        # 마이페이지로 이동
        mypage_button_xpath = '//android.view.View[@content-desc="마이페이지"]'
        mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        mypage_button = flow_tester.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, mypage_button_xpath))
        )
        mypage_button.click()
        print("마이페이지 로딩 대기...")
        flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, mypage_title_xpath)))
        print("✅ 마이페이지 로딩 완료.")
        time.sleep(3)  # 추가적인 안정성 확보를 위한 대기

        # 이 부분이 마이페이지 로딩 완료 후에 실행됩니다.
        print("\n💡초기 카운트 확인을 시작합니다.")
        initial_count, count_msg = get_share_count(flow_tester.driver)
        if initial_count == -1:
            return False, f"초기 카운트 획득 실패: {count_msg}"
        print(f"✅ 초기 공유하기 카운트: {initial_count}")

        # 2. 공유하기 시나리오 실행
        print("\n💡 2단계: 라이프스토리 카카오톡 공유 액션 실행")
        # 뒤로가기
        flow_tester.driver.back()
        time.sleep(3)
        share_action_passed, share_action_msg = test_lifestory_perform_kakao_share(flow_tester)
        if not share_action_passed:
            return False, f"공유하기 시나리오 실패: {share_action_msg}"
        print(f"✅ 공유하기 액션 완료: {share_action_msg}")

        # --- 💡추가된 앱 재시작 및 로그인 단계 시작 ---
        print("\n💡 2.5단계: 최종 카운트 확인을 위해 앱 재시작 및 로그인 수행")
        relaunch_success, relaunch_msg = test_lifestory_mypage_count(flow_tester)
        if not relaunch_success:
            return False, f"앱 재시작 및 로그인 실패: {relaunch_msg}"
        print("✅ 앱 재시작 및 로그인 완료.")

        # UI가 완전히 로드될 시간을 충분히 확보합니다. (추가된 부분)
        print("UI 로딩을 위해 5초 대기...")
        time.sleep(5)

        final_count, count_msg = get_share_count(flow_tester.driver)
        if final_count == -1:
            return False, f"최종 카운트 획득 실패: {count_msg}"
        print(f"✅ 최종 공유하기 카운트: {final_count}")

        time.sleep(3)
        # --- 💡추가된 앱 재시작 및 로그인 단계 종료 ---

        # 4. 결과 검증
        print("\n💡 4단계: 카운트 증가 여부 검증")
        if final_count == initial_count + 1:
            print("🎉 성공: 공유하기 카운트가 1 증가했습니다!")
            scenario_passed = True
            result_message = "공유하기 카운트 증가 확인 성공."
        else:
            print("❌ 실패: 공유하기 카운트가 예상과 다릅니다.")
            result_message = f"카운트 증가 실패: 예상({initial_count + 1}), 실제({final_count})"
            scenario_passed = False

    except Exception as e:
        print(f"🚨 공유하기 카운트 증가 확인 시나리오 실행 중 오류 발생: {e}")
        scenario_passed = False
        result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"

    finally:
        print("--- 마이페이지 내가 공유한 방법 '카카오톡' 공유하기 카운트 증가 확인 시나리오 종료 ---\n")

    # 이 부분이 누락되었기 때문에 None이 반환되었습니다.
    return scenario_passed, result_message

# 앱 재실핼 후, 로그인 / 마이페이지 진입하는 함수
def test_lifestory_mypage_count(flow_tester):
    print("\n--- 앱 강제 종료 및 재실행, 로그인 재수행 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
    try:
        # 현재 드라이버 세션 종료
        if flow_tester.driver:
            print("기존 드라이버 세션을 종료합니다...")
            flow_tester.driver.quit()
            flow_tester.driver = None
            print("기존 드라이버 세션 종료 완료.")

        # 새로운 드라이버 세션 생성 (앱 재실행 효과)
        print("새로운 Appium 드라이버 세션을 생성하여 앱을 다시 시작합니다...")
        flow_tester.setup_driver()
        print("드라이버 세션 재설정 완료.")

        # 로그인 시나리오 재실행
        login_success, login_msg = login_successful(flow_tester)
        if not login_success:
            return False, f"앱 재실행 후 로그인 실패: {login_msg}"

        # 3. 마이페이지를 실행합니다.
        print("마이페이지 버튼을 찾고 클릭합니다.")
        home_mypage_button_xpath = '//android.view.View[@content-desc="마이페이지"]'
        try:
            home_mypage_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, home_mypage_button_xpath)),
                message=f"'{home_mypage_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
            )
            home_mypage_button.click()
            print("마이페이지 버튼 클릭 완료.")
            time.sleep(5)  # 페이지 전환 대기
        except Exception as e:
            result_message = f"마이페이지 버튼 클릭 중 오류 발생: {e}"
            time.sleep(3)
            return False, result_message

        return True, "앱 재시작 및 로그인 완료."
    except Exception as e:
        print(f"🚨 시나리오 실행 중 치명적인 오류 발생: {e}")
        return False, f"시나리오 실행 중 실패: {e}"

if __name__ == "__main__":
    print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")