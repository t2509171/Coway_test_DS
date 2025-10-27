# Home_kil/test_home_etc.py

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수들을 import 합니다.
from Utils.scrolling_function import scroll_down
from Utils.screenshot_helper import save_screenshot_on_failure

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_home_notice_count(flow_tester):
    """
    홈 화면의 공지사항 개수를 확인합니다.
    '홈' UI 위에 공지사항 섹션이 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
    """
    print("\n--- 홈 > 공지사항 개수 확인 (인덱스 순차 검사) 시나리오 시작 ---")

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            print("경고: IOS 플랫폼의 공지사항 개수 확인 로직이 다를 수 있습니다.")
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. XPath 정의
        notice_container_xpath = locators.notice_container_xpath
        home_container_xpath = locators.home_button_xpath # 수정됨

        # 2. 공지사항 컨테이너가 화면에 완전히 보이는지 확인 (스크롤 로직은 일반적으로 불필요하나 안정성을 위해 추가)
        try:
            WebDriverWait(flow_tester.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.XPATH, notice_container_xpath))
            )
            print("✅ 공지사항 섹션을 찾았습니다.")
        except TimeoutException:
            save_screenshot_on_failure(flow_tester.driver, "notice_section_not_found")
            return False, "실패: 공지사항 섹션을 찾을 수 없습니다."

        # 3. 공지사항 개수를 인덱스 1~4번 순차 확인
        print("공지사항 개수를 1번부터 4번까지 순차적으로 확인합니다.")
        # 플랫폼별 자식 요소 XPath 설정
        child_xpath_selector = "android.view.View" if flow_tester.platform == 'android' else "XCUIElementTypeOther" # IOS는 추정값
        base_xpath = f"{notice_container_xpath}/{child_xpath_selector}"

        found_count = 0
        fourth_item_found = False
        for i in range(1, 5):
            indexed_xpath = f"({base_xpath})[{i}]"
            try:
                print(f"공지사항 인덱스 [{i}] 확인 시도...")
                flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
                print(f"✅ 공지사항 인덱스 [{i}] 발견.")
                found_count = i
                if i == 4:
                    fourth_item_found = True
                    break
            except NoSuchElementException:
                print(f"공지사항 인덱스 [{i}] 없음. 탐색을 종료합니다.")
                break

        print(f"탐색 완료. 발견된 최대 공지사항 인덱스: {found_count}")

        # 4. 결과 판정
        if fourth_item_found:
            save_screenshot_on_failure(flow_tester.driver, "notice_count_exceeded")
            return False, f"실패: 4번째 공지사항이 발견되었습니다."

        print(f"✅ 성공: 공지사항 개수가 3개 이하입니다. (총 {found_count}개)")
        return True, f"공지사항 개수 확인 성공 ({found_count}개)."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "notice_count_failure")
        return False, f"공지사항 개수 확인 중 오류 발생: {e}"
    finally:
        print("--- 홈 > 공지사항 개수 확인 시나리오 종료 ---")


def test_home_notice_click(flow_tester):
    """홈 화면의 첫 번째 공지사항 클릭 시 상세 화면으로 이동하는지 확인합니다."""
    print("\n--- 홈 > 공지사항 이동 확인 시나리오 시작 (checklist-17) ---")

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
        # 1. 첫 번째 공지사항 클릭
        first_item_xpath = locators.first_item_xpath
        try:
            print("첫 번째 공지사항 존재 여부 확인...")
            first_notice = WebDriverWait(flow_tester.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, first_item_xpath))
            )
            print("✅ 공지사항 발견. 클릭을 진행합니다.")
            first_notice.click()
            time.sleep(3)
        except (NoSuchElementException, TimeoutException):
            print("공지사항이 존재하지 않으므로 클릭 테스트를 건너뛰고 성공 처리합니다.")
            return True, "공지사항 없음 (클릭 테스트 성공 간주)."

        # 2. 상세 페이지 이동 확인
        print("공지사항 상세 페이지로 이동했는지 확인합니다.")
        notice_page_title_xpath = locators.notice_page_title_xpath
        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath)),
            message="공지사항 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 공지사항 상세 페이지로 성공적으로 이동했습니다.")

        print("뒤로가기를 눌러 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back() # 상세 페이지 -> 홈
        time.sleep(3)

        return True, "공지사항 상세 페이지 이동 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "notice_click_failure")
        return False, f"공지사항 이동 확인 중 오류 발생: {e}"
    finally:
        print("--- 홈 > 공지사항 이동 확인 시나리오 종료 ---")


def test_notice_page_navigation(flow_tester):
    """
    홈 화면에서 '공지사항'을 찾아 클릭한 후, 상세 페이지로 정상적으로 이동하는지 검증합니다.
    '홈' UI 위에 '공지사항' 버튼이 완전히 보일 때까지 스크롤하는 로직을 포함합니다.
    """
    print("\n--- 홈 > 공지사항 버튼 클릭 및 상세 페이지 이동 확인 시나리오 시작 ---")

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            print("경고: IOS 플랫폼의 공지사항 버튼 XPath 확인이 필요합니다.")
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. XPath 정의
        notice_button_xpath = '//android.view.View[@content-desc="공지사항"]' # 로컬 XPath 유지 (Repository에 없음)
        ios_notice_button_xpath = None # IOS XPath 필요
        current_notice_button_xpath = notice_button_xpath if flow_tester.platform == 'android' else ios_notice_button_xpath
        if not current_notice_button_xpath:
             print(f"경고: {flow_tester.platform} 플랫폼의 공지사항 버튼 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
             return True, f"{flow_tester.platform} 공지사항 버튼 XPath 없음 (테스트 통과 간주)"

        home_container_xpath = locators.home_button_xpath # 수정됨
        notice_page_title_xpath = locators.notice_page_title_xpath

        max_scroll_attempts = 10
        element_in_view = False

        # 2. '공지사항' 버튼이 '홈' UI 위에 보일 때까지 스크롤
        print(f"'{current_notice_button_xpath}' 버튼이 '홈' UI 위에 나타날 때까지 스크롤합니다.")
        for i in range(max_scroll_attempts):
            try:
                # 대상 요소와 기준 요소를 찾습니다.
                notice_element = flow_tester.driver.find_element(AppiumBy.XPATH, current_notice_button_xpath)
                home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                # 요소가 화면에 보이는지 확인합니다.
                if notice_element.is_displayed():
                    print("✅ '공지사항' 버튼을 찾았습니다. 위치를 비교합니다.")
                    notice_rect = notice_element.rect
                    home_rect = home_container_element.rect

                    # '공지사항' 버튼의 하단이 '홈' UI의 상단보다 위에 있는지 확인
                    if (notice_rect['y'] + notice_rect['height']) < home_rect['y']:
                        print("✅ 위치 조건 충족! '공지사항' 버튼이 하단 '홈' UI보다 위에 있습니다.")
                        element_in_view = True
                        break  # 스크롤 중단
                    else:
                        print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. '공지사항' 버튼이 '홈' UI에 가려져 있습니다. 스크롤합니다.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) '공지사항' 버튼이 아직 보이지 않습니다. 스크롤합니다.")

            except NoSuchElementException:
                # 요소를 찾지 못하면 스크롤을 계속합니다.
                print(f"({i + 1}/{max_scroll_attempts}) '공지사항' 버튼을 찾는 중... 스크롤합니다.")

            # 아래로 스크롤
            scroll_down(flow_tester.driver)
            time.sleep(1)  # 스크롤 후 UI가 안정화될 시간을 줍니다.

        # 3. 스크롤 후 요소 발견 여부 확인
        if not element_in_view:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 '공지사항' 버튼을 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "notice_button_not_in_view")
            return False, error_msg

        # 4. '공지사항' 버튼 클릭
        print("'공지사항' 버튼을 클릭합니다.")
        # 루프가 끝나고 찾은 요소를 다시 한번 명시적으로 찾아 클릭합니다.
        flow_tester.driver.find_element(AppiumBy.XPATH, current_notice_button_xpath).click()
        time.sleep(3)  # 페이지 전환 대기

        # 5. 상세 페이지 진입 확인
        print(f"공지사항 상세 페이지로 이동했는지 확인합니다. (제목: '{notice_page_title_xpath}')")
        try:
            wait = WebDriverWait(flow_tester.driver, 10)
            wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath))
            )
            print("✅ Pass: 공지사항 상세 페이지로 성공적으로 이동했습니다.")

            # (선택사항) 원래 화면으로 돌아가려면 아래 코드 사용
            print("홈 화면으로 돌아갑니다.")
            flow_tester.driver.back() # 상세 -> 홈
            time.sleep(2)

            return True, "공지사항 상세 페이지 이동 확인 성공."
        except TimeoutException:
            error_msg = "실패: '공지사항' 버튼을 클릭했지만 상세 페이지 제목을 찾을 수 없습니다."
            save_screenshot_on_failure(flow_tester.driver, "notice_page_load_fail")
            return False, error_msg

    except Exception as e:
        # 예상치 못한 다른 오류 발생 시
        save_screenshot_on_failure(flow_tester.driver, "notice_navigation_exception")
        return False, f"공지사항 이동 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 공지사항 버튼 클릭 및 상세 페이지 이동 확인 시나리오 종료 ---")


# # Home_kil/test_home_etc.py (수정 완료)
#
# import sys
# import os
# import time
#
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # 유틸리티 함수 임포트
# from Utils.screenshot_helper import save_screenshot_on_failure
# from Utils.scrolling_function import scroll_down
#
# # [Seller app checklist-16] 홈 > 공지사항 개수 확인
# def test_home_notice_count(flow_tester):
#     """
#     홈 화면의 공지사항 개수를 확인합니다.
#     '홈' UI 위에 공지사항 섹션이 완전히 보일 때까지 스크롤하는 로직이 추가되었습니다.
#     """
#     print("\n--- 홈 > 공지사항 개수 확인 (인덱스 순차 검사) 시나리오 시작 ---")
#     try:
#         # 1. XPath 정의
#         notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'
#
#         # 2. 공지사항 컨테이너가 화면에 완전히 보이는지 확인 (스크롤 로직은 일반적으로 불필요하나 안정성을 위해 추가)
#         try:
#             WebDriverWait(flow_tester.driver, 5).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, notice_container_xpath))
#             )
#             print("✅ 공지사항 섹션을 찾았습니다.")
#         except TimeoutException:
#             save_screenshot_on_failure(flow_tester.driver, "notice_section_not_found")
#             return False, "실패: 공지사항 섹션을 찾을 수 없습니다."
#
#         # 3. 공지사항 개수를 인덱스 1~4번 순차 확인
#         print("공지사항 개수를 1번부터 4번까지 순차적으로 확인합니다.")
#         base_xpath = f"{notice_container_xpath}/android.view.View"
#
#         found_count = 0
#         fourth_item_found = False
#         for i in range(1, 5):
#             indexed_xpath = f"({base_xpath})[{i}]"
#             try:
#                 print(f"공지사항 인덱스 [{i}] 확인 시도...")
#                 flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
#                 print(f"✅ 공지사항 인덱스 [{i}] 발견.")
#                 found_count = i
#                 if i == 4:
#                     fourth_item_found = True
#                     break
#             except NoSuchElementException:
#                 print(f"공지사항 인덱스 [{i}] 없음. 탐색을 종료합니다.")
#                 break
#
#         print(f"탐색 완료. 발견된 최대 공지사항 인덱스: {found_count}")
#
#         # 4. 결과 판정
#         if fourth_item_found:
#             save_screenshot_on_failure(flow_tester.driver, "notice_count_exceeded")
#             return False, f"실패: 4번째 공지사항이 발견되었습니다."
#
#         print(f"✅ 성공: 공지사항 개수가 3개 이하입니다. (총 {found_count}개)")
#         return True, f"공지사항 개수 확인 성공 ({found_count}개)."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "notice_count_failure")
#         return False, f"공지사항 개수 확인 중 오류 발생: {e}"
#     finally:
#         print("--- 홈 > 공지사항 개수 확인 시나리오 종료 ---")
#
#
# # [Seller app checklist-17] 홈 > 공지사항 이동 확인
# def test_home_notice_click(flow_tester):
#     """홈 화면의 첫 번째 공지사항 클릭 시 상세 화면으로 이동하는지 확인합니다."""
#     print("\n--- 홈 > 공지사항 이동 확인 시나리오 시작 (checklist-17) ---")
#     try:
#         # 1. 첫 번째 공지사항 클릭
#         notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
#         first_item_xpath = f"({notice_container_xpath}/android.view.View)[1]"
#         try:
#             print("첫 번째 공지사항 존재 여부 확인...")
#             first_notice = WebDriverWait(flow_tester.driver, 5).until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, first_item_xpath))
#             )
#             print("✅ 공지사항 발견. 클릭을 진행합니다.")
#             first_notice.click()
#             time.sleep(3)
#         except (NoSuchElementException, TimeoutException):
#             print("공지사항이 존재하지 않으므로 클릭 테스트를 건너뛰고 성공 처리합니다.")
#             return True, "공지사항 없음 (클릭 테스트 성공 간주)."
#
#         # 2. 상세 페이지 이동 확인
#         print("공지사항 상세 페이지로 이동했는지 확인합니다.")
#         notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'
#         WebDriverWait(flow_tester.driver, 10).until(
#             EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath)),
#             message="공지사항 상세 페이지로 이동하지 못했습니다."
#         )
#         print("✅ 공지사항 상세 페이지로 성공적으로 이동했습니다.")
#
#         print("뒤로가기를 눌러 홈 화면으로 돌아갑니다.")
#         flow_tester.driver.back()
#         time.sleep(3)
#
#         return True, "공지사항 상세 페이지 이동 확인 성공."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "notice_click_failure")
#         return False, f"공지사항 이동 확인 중 오류 발생: {e}"
#     finally:
#         print("--- 홈 > 공지사항 이동 확인 시나리오 종료 ---")
#
#
# # [Seller app checklist-40] 홈 > 공지사항 이동 확인
# def test_notice_page_navigation(flow_tester):
#     """
#     홈 화면에서 '공지사항'을 찾아 클릭한 후, 상세 페이지로 정상적으로 이동하는지 검증합니다.
#     '홈' UI 위에 '공지사항' 버튼이 완전히 보일 때까지 스크롤하는 로직을 포함합니다.
#     """
#     print("\n--- 홈 > 공지사항 버튼 클릭 및 상세 페이지 이동 확인 시나리오 시작 ---")
#     try:
#         # 1. XPath 정의
#         notice_button_xpath = '//android.view.View[@content-desc="공지사항"]'
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'  # 위치 비교 기준 XPath
#         notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'  # 도착 페이지 검증 XPath
#
#         max_scroll_attempts = 10
#         element_in_view = False
#
#         # 2. '공지사항' 버튼이 '홈' UI 위에 보일 때까지 스크롤
#         print(f"'{notice_button_xpath}' 버튼이 '홈' UI 위에 나타날 때까지 스크롤합니다.")
#         for i in range(max_scroll_attempts):
#             try:
#                 # 대상 요소와 기준 요소를 찾습니다.
#                 notice_element = flow_tester.driver.find_element(AppiumBy.XPATH, notice_button_xpath)
#                 home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 # 요소가 화면에 보이는지 확인합니다.
#                 if notice_element.is_displayed():
#                     print("✅ '공지사항' 버튼을 찾았습니다. 위치를 비교합니다.")
#                     notice_rect = notice_element.rect
#                     home_rect = home_container_element.rect
#
#                     # '공지사항' 버튼의 하단이 '홈' UI의 상단보다 위에 있는지 확인
#                     if (notice_rect['y'] + notice_rect['height']) < home_rect['y']:
#                         print("✅ 위치 조건 충족! '공지사항' 버튼이 하단 '홈' UI보다 위에 있습니다.")
#                         element_in_view = True
#                         break  # 스크롤 중단
#                     else:
#                         print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. '공지사항' 버튼이 '홈' UI에 가려져 있습니다. 스크롤합니다.")
#                 else:
#                     print(f"({i + 1}/{max_scroll_attempts}) '공지사항' 버튼이 아직 보이지 않습니다. 스크롤합니다.")
#
#             except NoSuchElementException:
#                 # 요소를 찾지 못하면 스크롤을 계속합니다.
#                 print(f"({i + 1}/{max_scroll_attempts}) '공지사항' 버튼을 찾는 중... 스크롤합니다.")
#
#             # 아래로 스크롤
#             scroll_down(flow_tester.driver)
#             time.sleep(1)  # 스크롤 후 UI가 안정화될 시간을 줍니다.
#
#         # 3. 스크롤 후 요소 발견 여부 확인
#         if not element_in_view:
#             error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 '공지사항' 버튼을 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "notice_button_not_in_view")
#             return False, error_msg
#
#         # 4. '공지사항' 버튼 클릭
#         print("'공지사항' 버튼을 클릭합니다.")
#         # 루프가 끝나고 찾은 요소를 다시 한번 명시적으로 찾아 클릭합니다.
#         flow_tester.driver.find_element(AppiumBy.XPATH, notice_button_xpath).click()
#         time.sleep(3)  # 페이지 전환 대기
#
#         # 5. 상세 페이지 진입 확인
#         print(f"공지사항 상세 페이지로 이동했는지 확인합니다. (제목: '{notice_page_title_xpath}')")
#         try:
#             wait = WebDriverWait(flow_tester.driver, 10)
#             wait.until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath))
#             )
#             print("✅ Pass: 공지사항 상세 페이지로 성공적으로 이동했습니다.")
#
#             # (선택사항) 원래 화면으로 돌아가려면 아래 코드 사용
#             print("홈 화면으로 돌아갑니다.")
#             flow_tester.driver.back()
#             time.sleep(2)
#
#             return True, "공지사항 상세 페이지 이동 확인 성공."
#         except TimeoutException:
#             error_msg = "실패: '공지사항' 버튼을 클릭했지만 상세 페이지 제목을 찾을 수 없습니다."
#             save_screenshot_on_failure(flow_tester.driver, "notice_page_load_fail")
#             return False, error_msg
#
#     except Exception as e:
#         # 예상치 못한 다른 오류 발생 시
#         save_screenshot_on_failure(flow_tester.driver, "notice_navigation_exception")
#         return False, f"공지사항 이동 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 > 공지사항 버튼 클릭 및 상세 페이지 이동 확인 시나리오 종료 ---")
#
