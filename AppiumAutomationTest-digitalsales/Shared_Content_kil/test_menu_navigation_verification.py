# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# W3C Actions 임포트 (스크롤)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 SharedContentKilLocators 임포트
from Xpath.xpath_repository import SharedContentKilLocators


def scroll_to_element(flow_tester, element_xpath, max_attempts=5):
    """
    지정된 XPath의 요소가 화면에 나타날 때까지 스크롤합니다.
    (이 파일 내에서만 사용하는 로컬 스크롤 함수)
    """
    print(f"'{element_xpath}' 요소를 찾기 위해 스크롤을 시작합니다.")
    driver = flow_tester.driver
    for attempt in range(max_attempts):
        try:
            element = driver.find_element(AppiumBy.XPATH, element_xpath)
            # [수정] is_displayed() 대신 presence 확인으로 변경 (스크롤 중 요소가 순간적으로 안 보일 수 있음)
            # if element.is_displayed():
            print(f"✅ 요소를 찾았습니다. (시도 {attempt + 1})")
            return element  # 요소를 찾았으면 반환
        except NoSuchElementException:
            pass  # 요소를 못 찾으면 스크롤 계속

        print(f"({attempt + 1}/{max_attempts}) 요소를 찾지 못해 스크롤합니다.")
        # W3C Actions를 이용한 스크롤 동작
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        size = driver.get_window_size()
        start_x = size['width'] * 0.75 # 전체 메뉴 영역 고려
        end_x = start_x
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2

        # [수정] iOS 스크롤은 swipe 또는 mobile:scroll 사용 가능
        if flow_tester.platform == 'android':
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            print("Android: W3C 스크롤 수행")
        else: # iOS
             # driver.swipe(start_x, start_y, end_x, end_y, 400) # swipe 사용 예시
             driver.execute_script("mobile: scroll", {'direction': 'down'}) # mobile:scroll 사용 예시
             print("iOS: mobile:scroll 'down' 수행")
        time.sleep(1.5)  # 스크롤 후 UI 안정화 대기

    # 최대 시도 후에도 못 찾으면 예외 발생
    raise NoSuchElementException(f"'{element_xpath}' 요소를 {max_attempts}번 스크롤 후에도 찾지 못했습니다.")


def test_navigate_to_shared_content(flow_tester):
    """전체 메뉴 > '공유 콘텐츠' 이동 및 타이틀 확인"""
    print("\n--- 전체 메뉴 > '공유 콘텐츠' 이동 및 타이틀 확인 시나리오 시작 ---")

    # --- ✨ [수정] 플랫폼에 맞는 로케이터 동적 선택 (분기만) ---
    if flow_tester.platform == 'android':
        locators = SharedContentKilLocators.AOS
    else: # iOS 또는 기본값
        locators = SharedContentKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    wait = WebDriverWait(flow_tester.driver, 10)

    try:
        # 1. '전체메뉴' 버튼 클릭
        print(f"'{locators.menu_button_xpath}' (전체메뉴) 버튼을 클릭합니다.")
        menu_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.menu_button_xpath)))
        menu_button.click()
        time.sleep(2)  # 메뉴 애니메이션 대기

        # 2. '공유 콘텐츠' 메뉴가 보일 때까지 스크롤
        shared_content_menu = scroll_to_element(flow_tester, locators.shared_content_menu_xpath)

        # 3. '공유 콘텐츠' 메뉴 클릭
        print(f"'{locators.shared_content_menu_xpath}' 메뉴를 클릭합니다.")
        shared_content_menu.click()
        time.sleep(3)  # 페이지 전환 대기

        # 4. '공유 콘텐츠' 페이지 타이틀 확인
        print(f"'{locators.page_title_xpath}' (페이지 타이틀)을 확인합니다.")
        wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, locators.page_title_xpath)))

        print("✅ 성공: '공유 콘텐츠' 페이지로 정상적으로 이동했습니다.")
        return True, "공유 콘텐츠 페이지 이동 및 타이틀 확인 성공"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "shared_content_nav_fail")
        return False, f"실패: '공유 콘텐츠' 이동 중 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "shared_content_nav_error")
        return False, f"실패: '공유 콘텐츠' 이동 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 전체 메뉴 > '공유 콘텐츠' 이동 및 타이틀 확인 시나리오 종료 ---")


def test_verify_tab_elements(flow_tester):
    """공유 콘텐츠: 탭 요소(라이프스토리, 카탈로그, 매뉴얼) 노출 확인"""
    print("\n--- 공유 콘텐츠 > 탭 요소(라이프스토리, 카탈로그, 매뉴얼) 노출 확인 시나리오 시작 ---")

    # --- ✨ [수정] 플랫폼에 맞는 로케이터 동적 선택 (분기만) ---
    if flow_tester.platform == 'android':
        locators = SharedContentKilLocators.AOS
    else: # iOS 또는 기본값
        locators = SharedContentKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    wait = WebDriverWait(flow_tester.driver, 10)
    missing_tabs = []

    # 검증할 탭 목록
    tabs_to_check = {
        "라이프스토리": locators.life_story_tab_xpath,
        "카탈로그": locators.catalog_tab_xpath,
        "매뉴얼": locators.manual_tab_xpath
    }

    try:
        # 1. 각 탭이 존재하는지 순차적으로 확인
        for tab_name, tab_xpath in tabs_to_check.items():
            print(f"'{tab_name}' 탭 확인 중...")
            try:
                wait.until(EC.presence_of_element_located((AppiumBy.XPATH, tab_xpath)))
                print(f"✅ '{tab_name}' 탭이 노출되었습니다.")
            except TimeoutException:
                print(f"❌ '{tab_name}' 탭을 찾지 못했습니다.")
                missing_tabs.append(tab_name)

        # 2. 결과 판정
        if not missing_tabs:
            print("✅ 성공: 모든 탭(라이프스토리, 카탈로그, 매뉴얼)이 정상적으로 노출되었습니다.")
            return True, "공유 콘텐츠 탭 요소 노출 확인 성공"
        else:
            error_msg = f"실패: 다음 탭이 노출되지 않았습니다 - {', '.join(missing_tabs)}"
            save_screenshot_on_failure(flow_tester.driver, "shared_content_tabs_missing")
            return False, error_msg

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "shared_content_tabs_error")
        return False, f"실패: 탭 요소 확인 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 공유 콘텐츠 > 탭 요소 노출 확인 시나리오 종료 ---")









# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
# from Utils.scrolling_function import scroll_down  # 스크롤 함수 추가
#
#
# def test_menu_navigation_and_verification(flow_tester):
#     """
#     전체 메뉴에서 e카탈로그, 제품 사용설명서를 스크롤하여 찾고, 위치를 확인한 후 각 화면으로 정상 이동하는지 검증합니다.
#     """
#     print("\n--- 전체 메뉴 > e카탈로그/제품 사용설명서 네비게이션 및 화면 검증 시나리오 시작 ---")
#     try:
#         # =================================================================
#         # 1. 'e카탈로그' 메뉴 검증
#         # =================================================================
#         print("\n[1단계: 'e카탈로그' 검증 시작]")
#
#         # 1-1. XPath 정의
#         menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#         ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
#         home_item_xpath = '//android.view.View[@content-desc="홈"]'
#         library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
#
#         # 1-2. 전체 메뉴 버튼 클릭
#         print("전체 메뉴 버튼을 클릭합니다.")
#         try:
#             menu_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
#             )
#             menu_button.click()
#             time.sleep(2)
#         except TimeoutException:
#             error_msg = "실패: '전체메뉴' 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_ecatalog")
#             return False, error_msg
#
#         # 1-3. 스크롤하며 'e카탈로그' 메뉴 찾기
#         print("'e카탈로그' 메뉴를 찾기 위해 스크롤을 시작합니다.")
#         ecatalog_item = None
#         for i in range(5):  # 최대 5번 스크롤
#             try:
#                 ecatalog_item = flow_tester.driver.find_element(AppiumBy.XPATH, ecatalog_item_xpath)
#                 if ecatalog_item.is_displayed():
#                     print(f"✅ 'e카탈로그' 메뉴를 찾았습니다. (시도: {i + 1}번)")
#                     break
#             except NoSuchElementException:
#                 print(f"({i + 1}/5) 'e카탈로그' 메뉴를 찾지 못했습니다. 아래로 스크롤합니다.")
#                 scroll_down(flow_tester.driver)
#                 time.sleep(1)
#
#         if not ecatalog_item or not ecatalog_item.is_displayed():
#             error_msg = "실패: 5번 스크롤 했지만 'e카탈로그' 메뉴를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "ecatalog_not_found_after_scroll")
#             return False, error_msg
#
#         # 1-4. 'e카탈로그' 메뉴 위치 확인 및 클릭
#         print("'e카탈로그' 메뉴가 '홈' 메뉴보다 위에 있는지 확인합니다.")
#         try:
#             home_item = flow_tester.driver.find_element(AppiumBy.XPATH, home_item_xpath)
#             ecatalog_y = ecatalog_item.location['y']
#             home_y = home_item.location['y']
#             print(f"'e카탈로그' 위치: {ecatalog_y}, '홈' 위치: {home_y}")
#
#             if ecatalog_y >= home_y:
#                 raise Exception("'e카탈로그' 메뉴가 '홈' 메뉴보다 아래에 위치합니다.")
#
#             print("✅ 위치 확인 완료. 'e카탈로그' 메뉴를 클릭합니다.")
#             ecatalog_item.click()
#
#         except (NoSuchElementException, Exception) as e:
#             error_msg = f"실패: 'e카탈로그' 메뉴 위치 검증 또는 클릭 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "ecatalog_verification_failed")
#             return False, error_msg
#
#         # 1-5. '라이브러리' 화면으로 이동했는지 확인
#         print("'라이브러리' 화면으로 이동했는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, library_text_xpath))
#             )
#             print("✅ '라이브러리' 텍스트가 성공적으로 확인되었습니다.")
#             print("[1단계: 'e카탈로그' 검증 성공]")
#         except TimeoutException:
#             error_msg = "실패: 'e카탈로그' 클릭 후 '라이브러리' 화면을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "library_view_not_found_for_ecatalog")
#             return False, error_msg
#
#         # =================================================================
#         # 2. '제품 사용설명서' 메뉴 검증
#         # =================================================================
#         print("\n[2단계: '제품 사용설명서' 검증 시작]")
#         manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
#
#         # 2-1. 전체 메뉴 버튼 다시 클릭
#         print("전체 메뉴 버튼을 다시 클릭합니다.")
#         try:
#             menu_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, menu_button_xpath))
#             )
#             menu_button.click()
#             time.sleep(2)
#         except TimeoutException:
#             error_msg = "실패: '제품 사용설명서' 검증을 위해 '전체메뉴' 버튼을 다시 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "menu_button_not_found_manual")
#             return False, error_msg
#
#         # 2-2. 스크롤하며 '제품 사용설명서' 메뉴 찾기
#         print("'제품 사용설명서' 메뉴를 찾기 위해 스크롤을 시작합니다.")
#         manual_item = None
#         for i in range(5):
#             try:
#                 manual_item = flow_tester.driver.find_element(AppiumBy.XPATH, manual_item_xpath)
#                 if manual_item.is_displayed():
#                     print(f"✅ '제품 사용설명서' 메뉴를 찾았습니다. (시도: {i + 1}번)")
#                     break
#             except NoSuchElementException:
#                 print(f"({i + 1}/5) '제품 사용설명서' 메뉴를 찾지 못했습니다. 아래로 스크롤합니다.")
#                 scroll_down(flow_tester.driver)
#                 time.sleep(1)
#
#         if not manual_item or not manual_item.is_displayed():
#             error_msg = "실패: 5번 스크롤 했지만 '제품 사용설명서' 메뉴를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "manual_not_found_after_scroll")
#             return False, error_msg
#
#         # 2-3. '제품 사용설명서' 메뉴 위치 확인 및 클릭
#         print("'제품 사용설명서' 메뉴가 '홈' 메뉴보다 위에 있는지 확인합니다.")
#         try:
#             home_item = flow_tester.driver.find_element(AppiumBy.XPATH, home_item_xpath)
#             manual_y = manual_item.location['y']
#             home_y = home_item.location['y']
#             print(f"'제품 사용설명서' 위치: {manual_y}, '홈' 위치: {home_y}")
#
#             if manual_y >= home_y:
#                 raise Exception("'제품 사용설명서' 메뉴가 '홈' 메뉴보다 아래에 위치합니다.")
#
#             print("✅ 위치 확인 완료. '제품 사용설명서' 메뉴를 클릭합니다.")
#             manual_item.click()
#
#         except (NoSuchElementException, Exception) as e:
#             error_msg = f"실패: '제품 사용설명서' 메뉴 위치 검증 또는 클릭 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "manual_verification_failed")
#             return False, error_msg
#
#         # 2-4. '라이브러리' 화면으로 이동했는지 확인
#         print("'라이브러리' 화면으로 이동했는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, library_text_xpath))
#             )
#             print("✅ '라이브러리' 텍스트가 성공적으로 확인되었습니다.")
#             print("[2단계: '제품 사용설명서' 검증 성공]")
#         except TimeoutException:
#             error_msg = "실패: '제품 사용설명서' 클릭 후 '라이브러리' 화면을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "library_view_not_found_for_manual")
#             return False, error_msg
#
#         return True, "전체 메뉴 네비게이션 및 화면 검증 성공."
#
#     except Exception as e:
#         return False, f"전체 메뉴 검증 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 전체 메뉴 > e카탈로그/제품 사용설명서 네비게이션 및 화면 검증 시나리오 종료 ---")