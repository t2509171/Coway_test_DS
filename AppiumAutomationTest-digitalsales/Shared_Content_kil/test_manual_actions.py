# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 SharedContentKilLocators 임포트
from Xpath.xpath_repository import SharedContentKilLocators


def test_manual_search_and_share(flow_tester):
    """공유 콘텐츠 > 매뉴얼: 검색 및 카카오톡 공유 기능 확인"""
    print("\n--- 공유 콘텐츠 > 매뉴얼 검색 및 카카오톡 공유 시나리오 시작 ---")

    # --- ✨ [수정] 플랫폼에 맞는 로케이터 동적 선택 (분기만) ---
    if flow_tester.platform == 'android':
        locators = SharedContentKilLocators.AOS
    else: # iOS 또는 기본값
        locators = SharedContentKilLocators.IOS
    # --- --- --- --- --- --- --- --- --- ---

    wait = WebDriverWait(flow_tester.driver, 10)

    try:
        # 1. '매뉴얼' 탭 클릭
        print(f"'{locators.manual_tab_xpath}' 탭을 클릭합니다.")
        manual_tab = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.manual_tab_xpath)))
        manual_tab.click()
        time.sleep(2)  # 탭 콘텐츠 로딩 대기

        # 2. 검색 아이콘 클릭
        print(f"'{locators.search_icon_xpath}' 검색 아이콘을 클릭합니다.")
        search_icon = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.search_icon_xpath)))
        search_icon.click()

        # 3. 검색어 입력
        search_term = "매뉴얼"
        print(f"'{locators.search_input_field_xpath}' 검색창에 '{search_term}'을 입력합니다.")
        search_field = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, locators.search_input_field_xpath)))
        # iOS에서는 clear() 전에 클릭 필요할 수 있음
        if flow_tester.platform != 'android':
            search_field.click()
        search_field.clear()
        search_field.send_keys(search_term)

        # 4. 검색 실행 (키보드 '검색' 또는 '엔터' 버튼)
        print("키보드 '검색' 버튼(엔터)을 누릅니다.")
        try:
            if flow_tester.platform == 'android':
                flow_tester.driver.press_keycode(66)
                print("Android: press_keycode(66) 'Enter' 액션 수행")
            else: # iOS
                # iOS 키보드의 'Search' 버튼 클릭 (XPath나 ID 필요 - 예시)
                # xpath_repository.py에 iOS용 'search_keyboard_button_xpath' 추가 필요
                # 예시: ios_search_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.search_keyboard_button_xpath)))
                #       ios_search_button.click()
                flow_tester.driver.execute_script("mobile: performEditorAction", {"action": "search"})
                print("iOS: execute_script 'search' 액션 수행 (임시)")
        except Exception as e:
            print(f"검색 실행 중 오류: {e}. 다른 방법 시도...")
            # 대체 방법
            if flow_tester.platform == 'android':
                 flow_tester.driver.execute_script("mobile: performEditorAction", {"action": "search"})
                 print("Android 대체: execute_script 'search' 액션 수행")
            else: # iOS
                 # flow_tester.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Search").click() # ID 예시
                 print("iOS 대체: 키보드 검색 버튼 클릭 로직 추가 필요")
                 # 우선 재시도
                 flow_tester.driver.execute_script("mobile: performEditorAction", {"action": "search"})

        time.sleep(3) # 검색 결과 로딩 대기

        # 5. 첫 번째 검색 결과의 공유 버튼 클릭
        print(f"첫 번째 검색 결과의 공유 버튼({locators.first_item_share_button_xpath})을 클릭합니다.")
        # [수정] iOS 경우 스크롤 필요 가능성 있음
        share_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.first_item_share_button_xpath)))
        share_button.click()
        time.sleep(2)

        # 6. '카카오톡' 공유 옵션 클릭
        print(f"'{locators.kakaotalk_share_option_xpath}' (카카오톡) 옵션을 클릭합니다.")
        kakao_option = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.kakaotalk_share_option_xpath)))
        kakao_option.click()
        time.sleep(2)

        # 7. '광고성 정보' 동의 팝업 확인
        # [주의] iOS에서는 이 팝업의 XPath가 다를 수 있음
        print(f"'{locators.ad_consent_popup_agree_xpath}' (동의) 버튼을 클릭합니다.")
        agree_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.ad_consent_popup_agree_xpath)))
        agree_button.click()
        time.sleep(3)  # 카카오톡 앱 전환 대기

        # 8. 카카오톡 화면(공유 대상 선택) 노출 확인
        print(f"'{locators.kakaotalk_friend_list_title_xpath}' (카카오톡 친구 목록) 화면을 확인합니다.")
        wait.until(EC.presence_of_element_located((AppiumBy.XPATH, locators.kakaotalk_friend_list_title_xpath)))

        print("✅ 성공: 카카오톡 공유 화면으로 정상적으로 이동했습니다.")

        # [수정] 앱 복귀 로직 플랫폼 분기
        print("앱으로 복귀 시도...")
        if flow_tester.platform == 'android':
            flow_tester.driver.back()
            print("Android: driver.back() 실행")
        else:
            # iOS 복귀 로직 필요
            # flow_tester.driver.activate_app(flow_tester.config.BUNDLE_ID)
            print("iOS: 앱 복귀 로직 필요 (현재는 아무 작업 안 함)")
            # 임시로 back 시도
            try: flow_tester.driver.back()
            except: pass
        time.sleep(2)

        # 9. 앱으로 복귀 후 'X' 버튼(검색 종료) 클릭
        print(f"'{locators.search_close_button_xpath}' (검색 닫기) 버튼을 클릭합니다.")
        close_button = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locators.search_close_button_xpath)))
        close_button.click()
        time.sleep(2)

        return True, "매뉴얼 검색 및 카카오톡 공유 기능 확인 성공"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "manual_search_share_fail")
        return False, f"실패: 매뉴얼 테스트 중 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "manual_search_share_error")
        return False, f"실패: 매뉴얼 테스트 중 예상치 못한 오류 발생: {e}"
    finally:
        print("--- 공유 콘텐츠 > 매뉴얼 검색 및 카카오톡 공유 시나리오 종료 ---")









# import time
# from appium.webdriver.common.appiumby import AppiumBy
#
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException,NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions import interaction
# from selenium.webdriver.common.actions.pointer_input import PointerInput
#
# # 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
# from Utils.scrolling_function import scroll_down  # 스크롤 함수 추가
#
# def test_share_manual_to_kakaotalk(flow_tester):
#     """
#     제품 사용설명서를 카카오톡으로 공유하는 기능을 검증합니다.
#     공유 버튼 선택 > 채널 선택 > 카카오톡 선택 > 광고성 정보 동의 > 카카오톡 앱 호출 확인
#     """
#     print("\n--- 제품 사용설명서 카카오톡 공유 시나리오 시작 ---")
#     try:
#         menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
#         manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
#         home_item_xpath = '//android.view.View[@content-desc="홈"]'
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
#
#         # ※ 사전 조건: 제품 사용설명서 상세 화면에 진입한 상태라고 가정합니다.
#
#         # 0. 좌표 클릭
#         # 0 '공유하기' 버튼 활성화를 위해 좌표 클릭 (driver.tap 방식)
#         print("'공유하기' 버튼 활성화를 위해 (880, 857) 좌표를 클릭합니다.")
#         try:
#             # driver.tap은 [(x, y)] 형태의 리스트를 인자로 받습니다.
#             flow_tester.driver.tap([(880, 857)])
#             print("✅ driver.tap 동작이 실행되었습니다.")
#             time.sleep(3)  # UI 반응 시간을 넉넉하게 3초로 줍니다.
#             flow_tester.driver.back()
#             time.sleep(2)
#         except Exception as e:
#             error_msg = f"실패: driver.tap을 이용한 좌표 클릭 중 에러 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "driver_tap_error")
#             return False, error_msg
#
#         # UI가 반응할 시간을 넉넉하게 줍니다.
#         print("UI 반응 대기 중... (5초)")
#
#         # 1. '공유하기' 버튼 클릭
#         share_button_xpath = '//android.widget.Button[@text="공유하기"]' # 실제 앱의 XPath로 수정 필요
#         print(f"'{share_button_xpath}' (공유하기) 버튼을 클릭합니다.")
#         try:
#             share_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, share_button_xpath))
#             )
#             share_button.click()
#         except TimeoutException:
#             error_msg = "실패: '공유하기' 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "manual_share_button_not_found")
#             return False, error_msg
#
#         # 2. '채널 선택' 팝업에서 '카카오톡' 아이콘 클릭
#         kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]' # 실제 앱의 XPath로 수정 필요
#         print(f"'{kakaotalk_xpath}' (카카오톡) 아이콘을 클릭합니다.")
#         try:
#             kakaotalk_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, kakaotalk_xpath))
#             )
#             kakaotalk_button.click()
#         except TimeoutException:
#             error_msg = "실패: 공유 채널 팝업에서 '카카오톡' 아이콘을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "kakaotalk_icon_not_found")
#             return False, error_msg
#
#         # 3. '광고성 정보 전송에 따른 의무사항' 팝업창 노출 확인
#         legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]' #
#         print(f"'{legal_notice_xpath}' 팝업이 노출되는지 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, legal_notice_xpath))
#             )
#             print("✅ '광고성 정보' 팝업이 성공적으로 확인되었습니다.")
#         except TimeoutException:
#             error_msg = "실패: '광고성 정보' 팝업을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "manual_legal_notice_popup_not_found")
#             return False, error_msg
#
#         # 4. '동의' 버튼 클릭
#         agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
#         print(f"'{agree_button_xpath}' (동의) 버튼을 클릭합니다.")
#         try:
#             agree_button = flow_tester.driver.find_element(AppiumBy.XPATH, agree_button_xpath)
#             agree_button.click()
#         except Exception as e:
#             error_msg = f"실패: '동의' 버튼 클릭 중 오류 발생: {e}"
#             save_screenshot_on_failure(flow_tester.driver, "manual_agree_button_click_failed")
#             return False, error_msg
#
#         # 5. 카카오톡 앱이 호출되었는지 확인 (Activity/Package 확인)
#         print("카카오톡 앱이 실행되었는지 확인합니다.")
#         time.sleep(5) # 앱 전환 대기
#         current_package = flow_tester.driver.current_package
#         print(f"현재 활성화된 패키지: {current_package}")
#
#         # 카카오톡 패키지명: 'com.kakao.talk'
#         if 'com.kakao.talk' in current_package:
#             print("✅ 카카오톡 앱이 성공적으로 호출되었습니다.")
#         else:
#             error_msg = f"실패: 카카오톡 앱이 호출되지 않았습니다. (현재 패키지: {current_package})"
#             save_screenshot_on_failure(flow_tester.driver, "kakaotalk_app_not_launched")
#             return False, error_msg
#
#         # 테스트 종료를 위해 원래 앱으로 돌아갑니다.
#         flow_tester.driver.back()
#         time.sleep(2)
#
#         return True, "제품 사용설명서 카카오톡 공유 기능 검증 성공."
#
#     except Exception as e:
#         return False, f"제품 사용설명서 공유 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 제품 사용설명서 카카오톡 공유 시나리오 종료 ---")
#
#
# def test_download_manual(flow_tester):
#     """
#     제품 사용설명서 다운로드 기능을 검증합니다. (AOS 기준)
#     다운로드 버튼 선택 > 다운로드 Confirm창 노출 > 확인 버튼 선택
#     """
#     print("\n--- 제품 사용설명서 다운로드 시나리오 시작 ---")
#     try:
#         # ※ 사전 조건: 제품 사용설명서 상세 화면에 진입한 상태라고 가정합니다.
#
#         # 1. '다운로드' 버튼 클릭
#         download_button_xpath = '//android.widget.Button[@text="다운로드"]' # 실제 앱의 XPath로 수정 필요
#         print(f"'{download_button_xpath}' (다운로드) 버튼을 클릭합니다.")
#         try:
#             download_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, download_button_xpath))
#             )
#             download_button.click()
#         except TimeoutException:
#             error_msg = "실패: '다운로드' 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "manual_download_button_not_found")
#             return False, error_msg
#
#         # 2. '다운로드 Confirm' 팝업창에서 '확인' 버튼 노출 확인 및 클릭
#         confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]' # 실제 앱의 XPath로 수정 필요
#         print(f"다운로드 확인 팝업에서 '{confirm_button_xpath}' (확인) 버튼을 찾아 클릭합니다.")
#         try:
#             confirm_button = WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, confirm_button_xpath))
#             )
#             print("✅ 다운로드 확인 팝업이 성공적으로 노출되었습니다.")
#             confirm_button.click()
#             print("다운로드를 시작했습니다.")
#             flow_tester.driver.back()
#             time.sleep(2)
#             flow_tester.driver.back()
#             time.sleep(3)
#         except TimeoutException:
#             error_msg = "실패: 다운로드 확인 팝업 또는 '확인' 버튼을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "manual_download_confirm_popup_not_found")
#             return False, error_msg
#
#         return True, "제품 사용설명서 다운로드 기능 검증 성공."
#
#     except Exception as e:
#         return False, f"제품 사용설명서 다운로드 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 제품 사용설명서 다운로드 시나리오 종료 ---")