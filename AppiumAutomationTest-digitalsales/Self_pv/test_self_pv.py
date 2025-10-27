# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 SharedContentKilLocators 임포트
from Xpath.xpath_repository import SharedContentKilLocators


# PythonProject/Self_pv/test_self_pv.py
# ... (import 부분 동일) ...
from Xpath.xpath_repository import SelfPvLocators

def _navigate_to_full_menu(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    all_menu_button_xpath = locators.menu_button_xpath
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일) ...

def test_etc_self_promotional_video_view(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일, self_promotional_video_button_xpath 변수 설정 시 locators 사용) ...

def test_etc_self_promotional_video_button_click(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일, xpath 변수 설정 시 locators 사용) ...

def test_etc_self_promotional_video_detail_view(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일, xpath 변수 설정 시 locators 사용) ...

def test_etc_self_promotional_video_bulletin_click(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일, xpath 변수 설정 시 locators 사용) ...

def test_etc_self_promotional_video_bulletin_view(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일, xpath 변수 설정 시 locators 사용) ...

def test_etc_self_promotional_video_bulletin_list_button_click(flow_tester):
    # ... (시작 로그 동일) ...
    # --- [수정됨] ---
    # 플랫폼 분기 로직 수정 ('android', 'ios')
    try:
        if flow_tester.platform == 'android': # 'AOS' -> 'android'
            locators = SelfPvLocators.AOS
        elif flow_tester.platform == 'ios': # 'IOS' -> 'ios'
            locators = SelfPvLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.") # AOS -> Android
        locators = SelfPvLocators.AOS
    # --- [수정 완료] ---
    # ... (나머지 함수 로직 동일, xpath 변수 설정 시 locators 사용) ...

# ... (if __name__ == "__main__": 부분 동일) ...

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
# # 전체메뉴 진입 확인
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
# # 셀프홍보영상 버튼 노출 확인
# def test_etc_self_promotional_video_view(flow_tester):
#     """
#     전체 메뉴에서 셀프홍보영상 클릭 후, 셀프홍보영상 타이틀이 노출되는지 확인합니다.
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
#         # 2. '셀프홍보영상' 버튼 노출 확인
#         self_promotional_video_button_xpath = '//android.view.View[@content-desc="셀프 홍보영상"]'  # [cite: 6]
#         max_scrolls = 5  # 최대 스크롤 횟수 설정
#
#         for i in range(max_scrolls):
#             print(f"스크롤 시도 {i + 1}/{max_scrolls}")
#             try:
#                 # '셀프홍보영상' 요소가 보이는지 확인
#                 self_promotional_video_element = flow_tester.driver.find_element(AppiumBy.XPATH,
#                                                                              self_promotional_video_button_xpath)
#                 if self_promotional_video_element.is_displayed():
#                     print("✅ '셀프홍보영상' 요소가 성공적으로 노출되었습니다.")
#                     scenario_passed = True
#                     result_message = "'셀프홍보영상' 요소까지 W3C 스크롤 성공."
#                     # 요소가 보이면 테스트 성공으로 간주하고 루프 종료
#                     break
#             except NoSuchElementException:
#                 # 요소가 현재 화면에 없으면 스크롤 수행
#                 print("'셀프홍보영상' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")
#
#                 # W3C Actions를 이용한 스크롤 동작
#                 actions = ActionChains(flow_tester.driver)
#                 actions.w3c_actions = ActionBuilder(flow_tester.driver,
#                                                     mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#                 actions.w3c_actions.pointer_action.move_to_location(550, 1800)
#                 actions.w3c_actions.pointer_action.pointer_down()
#                 actions.w3c_actions.pointer_action.pause(0.1)  # 짧은 일시정지 (선택 사항)
#                 actions.w3c_actions.pointer_action.move_to_location(550, 1100)
#                 actions.w3c_actions.pointer_action.release()
#                 actions.perform()
#                 time.sleep(0.5)  # 스크롤 후 페이지 로딩 대기
#
#         if not scenario_passed:
#             result_message = f"최대 스크롤 횟수({max_scrolls}) 내에 '셀프홍보영상' 요소를 찾지 못했습니다."
#             return False, result_message
#
#     except Exception as e:
#         print(f"🚨 셀프홍보영상 확인 시나리오 실행 중 오류 발생: {e}")
#         scenario_passed = False
#         result_message = f"시나리오 실행 중 예상치 못한 오류: {e}"
#
#     finally:
#         print("--- 전체메뉴 > 셀프홍보영상 진입 및 UI 요소 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 셀프홍보영상 상세 페이지 확인
# def test_etc_self_promotional_video_button_click(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     print(" '셀프홍보영상' 버튼을 찾고 클릭합니다.")
#     self_promotional_video_button_xpath = '//android.view.View[@content-desc="셀프 홍보영상"]' # [cite: 6]
#     try:
#         self_promotional_video_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, self_promotional_video_button_xpath)),
#             message=f"'{self_promotional_video_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         self_promotional_video_button.click()
#         print(" '셀프홍보영상' 버튼 클릭 완료.")
#
#         # 셀프 홍보영상 페이지의 고유 요소(타이틀)가 노출되는지 확인합니다.
#         self_promotional_video_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]'
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_title_xpath)))
#         print("✅ '셀프 홍보영상' 페이지로 성공적으로 이동했습니다.")
#         scenario_passed = True
#         result_message = "셀프 홍보영상 페이지로 성공적으로 이동했습니다."
#
#     except Exception as e:
#         result_message = f"셀프홍보영상 버튼 클릭 실패: {e}"
#         return False, result_message
#
#     finally:
#         print("--- 셀프홍보영상 상세 페이지 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 셀프홍보영상 검색영역, 게시글 영역 확인
# def test_etc_self_promotional_video_detail_view(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # '셀프홍보영상 타이틀','검색영역','게시글영역' 노출 확인
#     print(" '셀프홍보영상 타이틀','검색영역','게시글영역' 노출을 확인합니다.")
#     #self_promotional_video_title_xpath = '//android.widget.ListView' # [cite: 6]
#     self_promotional_video_search_xpath = '//android.widget.EditText'  # [cite: 6]
#     self_promotional_video_bulletin_xpath = '(//android.view.View[@content-desc])[1]'  # [cite: 6]
#
#     try:
#     #    flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_title_xpath)))
#     #    print("✅ '셀프홍보영상 타이틀'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_search_xpath)))
#         print("✅ '셀프홍보영상 검색영역'이 성공적으로 노출되었습니다.")
#         #게시글영역은 특정 게시글의 정보로 하드코팅 되어있음
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_bulletin_xpath)))
#         print("✅ '셀프홍보영상 게시글영역'이 성공적으로 노출되었습니다.")
#         scenario_passed = True
#         result_message = "셀프홍보영상 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"셀프홍보영상 UI 요소 노출 확인 실패: {e}"
#         time.sleep(1)
#         return False, result_message
#
#     finally:
#         print("--- 셀프홍보영상 검색영역, 게시글 영역 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 셀프홍보영상 게시글 상세 페이지 이동 확인
# def test_etc_self_promotional_video_bulletin_click(flow_tester):
#     """
#         셀프홍보영상 리스트에서 게시글 클릭 후, 셀프홍보영상 상세 페이지가 노출되는지 확인합니다.
#         """
#     print("\n--- 셀프홍보영상 상세 페이지 진입 및 UI 요소 확인 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     #셀프홍보영상 게시글 클릭
#     print(" '셀프홍보영상 게시글'을 찾고 클릭합니다.")
#     #게시글영역의 특정 게시글의 정보를 하드코팅 되어있음
#     self_promotional_video_details_button_xpath = '//android.view.View[contains(@content-desc, "Test")]'  # [cite: 6]
#     try:
#         self_promotional_video_details_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, self_promotional_video_details_button_xpath)),
#             message=f"'{self_promotional_video_details_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         self_promotional_video_details_button.click()
#         print(" '셀프홍보영상 게시글' 클릭 완료.")
#
#         # 셀프 홍보영상 페이지의 고유 요소(타이틀)가 노출되는지 확인합니다.
#         self_promotional_video_details_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]'  # [cite: 6]
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_details_title_xpath)))
#         print("✅ '셀프 홍보영상' 페이지로 성공적으로 이동했습니다.")
#         scenario_passed = True
#         result_message = "셀프 홍보영상 페이지로 성공적으로 이동했습니다."
#
#         time.sleep(1)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"셀프홍보영상 게시글 클릭 실패: {e}"
#         return False, result_message
#
#     finally:
#         print("--- 전체메뉴 > 셀프홍보영상 진입 및 UI 요소 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 셀프홍보영상 게시글 상세 페이지 노출 확인
# def test_etc_self_promotional_video_bulletin_view(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 3. '게시글 상세화면 타이틀','글제목','등록일','조회수','파일링크','본문','이전글','목록' 노출 확인
#     print(" '셀프홍보영상 타이틀','글제목','등록일','조회수','파일링크','본문','이전글','목록' 노출을 확인합니다.")
#     self_promotional_video_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]'  # [cite: 6]
#     #self_promotional_video_texttitle_xpath = '//android.widget.TextView[@text="셀프 홍보영상 등록 - Sotatek test"]'  # [cite: 6]
#     self_promotional_video_dateregistration_xpath = '//android.widget.TextView[@text="등록일"]'  # [cite: 6]
#     self_promotional_video_viewers_xpath = '//android.widget.TextView[@text="조회수"]'  # [cite: 6]
#     #게시글 상세 페이지 파일링크는 특정 게시글로 하드코딩 되어있음
#     #self_promotional_video_fileLink_xpath = '//android.view.View[@content-desc="https://cowaysctest.page.link/1G3f8WeFiTnDTUQd6"]'  # [cite: 6]
#     #게시글 상세 페이지 본문은 xpath 존재하지 않아, 미처리
#     #self_promotional_video_text_xpath = ''  # [cite: 6]
#     self_promotional_video_earlierarticle_xpath = '//android.view.View[@content-desc="이전글"]'  # [cite: 6]
#     self_promotional_video_list_xpath = '//android.view.View[@content-desc="목록"]'  # [cite: 6]
#
#     try:
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_title_xpath)))
#         print("✅ '셀프홍보영상 타이틀'이 성공적으로 노출되었습니다.")
#         #flow_tester.wait.until(
#         #    EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_texttitle_xpath)))
#         #print("✅ '셀프홍보영상 글제목'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_dateregistration_xpath)))
#         print("✅ '셀프홍보영상 등록일'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_viewers_xpath)))
#         print("✅ '셀프홍보영상 조회수'가 성공적으로 노출되었습니다.")
#         # 게시글 상세 페이지 파일링크는 특정 게시글로 하드코딩 되어있음
#         #flow_tester.wait.until(
#         #    EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_fileLink_xpath)))
#         #print("✅ '셀프홍보영상 파일링크'가 성공적으로 노출되었습니다.")
#         #flow_tester.wait.until(
#         #    EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_text_xpath)))
#         #print("✅ '셀프홍보영상 본문'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_earlierarticle_xpath)))
#         print("✅ '셀프홍보영상 이전글'이 성공적으로 노출되었습니다.")
#         flow_tester.wait.until(
#             EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_list_xpath)))
#         print("✅ '셀프홍보영상 목록'이 성공적으로 노출되었습니다.")
#         scenario_passed = True
#         result_message = "셀프홍보영상 진입 및 UI 요소 확인 성공."
#     except Exception as e:
#         result_message = f"셀프홍보영상 UI 요소 노출 확인 실패: {e}"
#         time.sleep(1)
#         return False, result_message
#
#     finally:
#         print("--- 전체메뉴 > 셀프홍보영상 진입 및 UI 요소 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# # 셀프홍보영상 게시글 목록 버튼 클릭 확인
# def test_etc_self_promotional_video_bulletin_list_button_click(flow_tester):
#
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # 셀프홍보영상 게시글 목록 버튼 클릭
#     print(" 목록 버튼을 찾고 클릭합니다.")
#     self_promotional_video_bulletin_list_button_xpath = '//android.view.View[@content-desc="목록"]'
#     try:
#         self_promotional_video_bulletin_list_button = flow_tester.wait.until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, self_promotional_video_bulletin_list_button_xpath)),
#             message=f"'{self_promotional_video_bulletin_list_button_xpath}' 버튼을 20초 내에 찾지 못했습니다."
#         )
#         self_promotional_video_bulletin_list_button.click()
#         print(" '목록 버튼 클릭 완료.")
#
#         # 셀프 홍보영상 페이지의 고유 요소(타이틀)가 노출되는지 확인합니다.
#         self_promotional_video_texttitle_xpath = '//android.widget.TextView[@text="셀프 홍보영상 등록 - Sotatek test"]'  # [cite: 6]
#         flow_tester.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self_promotional_video_texttitle_xpath)))
#         print("✅ '셀프 홍보영상' 페이지로 성공적으로 이동했습니다.")
#         scenario_passed = True
#         result_message = "셀프 홍보영상 페이지로 성공적으로 이동했습니다."
#
#         time.sleep(1)  # 페이지 전환 대기
#     except Exception as e:
#         result_message = f"셀프홍보영상 게시글 클릭 실패: {e}"
#         return False, result_message
#
#     finally:
#         print("--- 전체메뉴 > 셀프홍보영상 진입 및 UI 요소 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message
#
# if __name__ == "__main__":
#     print("이 파일은 이제 개별 함수를 포함하며, 다른 테스트 스위트에서 호출됩니다.")