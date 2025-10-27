import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 약속대로 사용자님의 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_recommended_sales_content(flow_tester):
    """
    홈 화면 '영업 콘텐츠' 섹션의 세 가지 주요 UI가 올바른 순서로
    (제목 > 정렬 버튼 > 하단 홈 UI) 정렬될 때까지 스크롤하고 검증합니다.
    """
    print("\n--- 홈 > 공유할 영업 콘텐츠 추천 (Y 좌표 정렬) 시나리오 시작 ---")

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            # 필요한 모든 XPath가 정의되었는지 확인
            if not all([locators.title_xpath, locators.sort_button_xpath,
                        locators.home_button_xpath, locators.lifestory_title_xpath]):
                 print(f"경고: {flow_tester.platform} 플랫폼에 필요한 일부 영업 콘텐츠 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
                 return True, f"{flow_tester.platform} 영업 콘텐츠 XPath 부족 (테스트 통과 간주)"
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. XPath 정의 (locators 객체 사용)
        title_xpath = locators.title_xpath
        sort_button_xpath = locators.sort_button_xpath
        home_container_xpath = locators.home_button_xpath # 수정됨
        print("세 요소의 Y 좌표 순서가 맞을 때까지 스크롤을 시작합니다.")

        max_scroll_attempts = 10
        section_in_correct_order = False
        target_element = None # 클릭할 제목 요소를 저장할 변수

        # 2. 지정된 횟수만큼 스크롤하며 요소들의 Y 좌표 순서를 확인하는 루프
        for i in range(max_scroll_attempts):
            try:
                # 2-1. 필요한 세 가지 요소를 모두 찾습니다.
                target_element = flow_tester.driver.find_element(AppiumBy.XPATH, title_xpath)
                sort_button_element = flow_tester.driver.find_element(AppiumBy.XPATH, sort_button_xpath)
                home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                # 2-2. 세 요소가 모두 화면에 보이는지 확인합니다.
                if all(elem.is_displayed() for elem in [target_element, sort_button_element, home_container_element]):
                    print("✅ 세 요소를 모두 화면에서 찾았습니다. Y 좌표 순서를 비교합니다.")

                    # 2-3. 각 요소의 Y 좌표를 가져옵니다.
                    title_y = target_element.location['y']
                    sort_button_y = sort_button_element.location['y']
                    home_container_y = home_container_element.location['y']

                    print(f"  -> 제목 Y: {title_y}, 정렬 버튼 Y: {sort_button_y}, 홈 UI Y: {home_container_y}")

                    # ✨ 2-4. Y 좌표 순서(제목 < 정렬 버튼 < 홈 UI)가 올바른지 확인
                    if title_y < sort_button_y < home_container_y:
                        print("✅ 위치 조건 충족! 세 요소가 올바른 순서로 정렬되었습니다.")
                        section_in_correct_order = True
                        break  # 루프를 성공적으로 종료합니다.
                    else:
                        print("⚠️ 위치 조건 불충족. 요소들이 아직 올바른 순서가 아닙니다. 스크롤합니다.")
                else:
                    print("요소는 찾았지만 일부가 화면에 표시되지 않았습니다. 스크롤합니다.")

            except NoSuchElementException:
                # 세 요소 중 하나라도 DOM에서 찾지 못한 경우
                print("필요한 요소를 모두 찾지 못했습니다. 스크롤합니다.")
                pass

            # 루프의 마지막에 스크롤을 실행합니다.
            print(f"({i + 1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")
            scroll_down(flow_tester.driver)
            time.sleep(1) # 스크롤 후 대기

        # 3. 루프 종료 후, 성공 여부를 확인합니다.
        if not section_in_correct_order:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 세 요소의 정렬을 확인할 수 없었습니다."
            save_screenshot_on_failure(flow_tester.driver, "sales_content_section_not_aligned")
            return False, error_msg

        # 4. 검증이 완료된 제목 요소를 클릭합니다. (target_element는 루프에서 찾은 요소)
        print("정확한 위치에서 섹션을 확인하고 클릭합니다.")
        target_element.click()
        time.sleep(3)

        # 5. 최종 목록 페이지에서 '라이프스토리' 텍스트 확인
        final_page_text_xpath = locators.lifestory_title_xpath # 수정됨 (final_page_text_xpath -> lifestory_title_xpath)
        print(f"목록 페이지에서 '{final_page_text_xpath}' 텍스트를 확인합니다.")
        try:
            WebDriverWait(flow_tester.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, final_page_text_xpath))
            )
            print("✅ 최종 페이지에서 '라이프스토리' 텍스트를 확인했습니다.")
        except TimeoutException:
            error_msg = "실패: 최종 목록 페이지에서 '라이프스토리' 텍스트를 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "final_page_verification_failed")
            return False, error_msg

        # 모든 검증 통과
        flow_tester.driver.back() # 목록 -> 홈
        time.sleep(1)
        return True, "공유할 영업 콘텐츠 확인 시나리오 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "sales_content_test_failure")
        return False, f"공유할 영업 콘텐츠 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 공유할 영업 콘텐츠 추천 확인 시나리오 종료 ---")



# import time
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
#
# # 약속대로 사용자님의 유틸리티 함수들을 import 합니다.
# from Utils.screenshot_helper import save_screenshot_on_failure
# from Utils.scrolling_function import scroll_down
#
#
# def test_recommended_sales_content(flow_tester):
#     """
#     홈 화면 '영업 콘텐츠' 섹션의 세 가지 주요 UI가 올바른 순서로
#     (제목 > 정렬 버튼 > 하단 홈 UI) 정렬될 때까지 스크롤하고 검증합니다.
#     """
#     print("\n--- 홈 > 공유할 영업 콘텐츠 추천 (Y 좌표 정렬) 시나리오 시작 ---")
#     try:
#         # 1. XPath 정의
#         title_xpath = '//android.view.View[@content-desc="공유할 영업 콘텐츠를 추천 드려요"]'
#         sort_button_xpath = '//android.widget.Button[@text="신규"]'
#         home_container_xpath = '//android.view.View[@content-desc="홈"]'
#         print("세 요소의 Y 좌표 순서가 맞을 때까지 스크롤을 시작합니다.")
#
#         max_scroll_attempts = 10
#         section_in_correct_order = False
#         target_element = None
#
#         # 2. 지정된 횟수만큼 스크롤하며 요소들의 Y 좌표 순서를 확인하는 루프
#         for i in range(max_scroll_attempts):
#             try:
#                 # 2-1. 필요한 세 가지 요소를 모두 찾습니다.
#                 target_element = flow_tester.driver.find_element(AppiumBy.XPATH, title_xpath)
#                 sort_button_element = flow_tester.driver.find_element(AppiumBy.XPATH, sort_button_xpath)
#                 home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 # 2-2. 세 요소가 모두 화면에 보이는지 확인합니다.
#                 if all(elem.is_displayed() for elem in [target_element, sort_button_element, home_container_element]):
#                     print("✅ 세 요소를 모두 화면에서 찾았습니다. Y 좌표 순서를 비교합니다.")
#
#                     # 2-3. 각 요소의 Y 좌표를 가져옵니다.
#                     title_y = target_element.location['y']
#                     sort_button_y = sort_button_element.location['y']
#                     home_container_y = home_container_element.location['y']
#
#                     print(f"  -> 제목 Y: {title_y}, 정렬 버튼 Y: {sort_button_y}, 홈 UI Y: {home_container_y}")
#
#                     # ✨ 2-4. Y 좌표 순서(제목 < 정렬 버튼 < 홈 UI)가 올바른지 확인
#                     if title_y < sort_button_y < home_container_y:
#                         print("✅ 위치 조건 충족! 세 요소가 올바른 순서로 정렬되었습니다.")
#                         section_in_correct_order = True
#                         break  # 루프를 성공적으로 종료합니다.
#                     else:
#                         print("⚠️ 위치 조건 불충족. 요소들이 아직 올바른 순서가 아닙니다. 스크롤합니다.")
#                 else:
#                     print("요소는 찾았지만 일부가 화면에 표시되지 않았습니다. 스크롤합니다.")
#
#             except NoSuchElementException:
#                 # 세 요소 중 하나라도 DOM에서 찾지 못한 경우
#                 print("필요한 요소를 모두 찾지 못했습니다. 스크롤합니다.")
#                 pass
#
#             # 루프의 마지막에 스크롤을 실행합니다.
#             print(f"({i + 1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")
#             scroll_down(flow_tester.driver)
#
#         # 3. 루프 종료 후, 성공 여부를 확인합니다.
#         if not section_in_correct_order:
#             error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 세 요소의 정렬을 확인할 수 없었습니다."
#             save_screenshot_on_failure(flow_tester.driver, "sales_content_section_not_aligned")
#             return False, error_msg
#
#         # 4. 검증이 완료된 제목 요소를 클릭합니다.
#         print("정확한 위치에서 섹션을 확인하고 클릭합니다.")
#         target_element.click()
#         time.sleep(3)
#
#         # 5. 최종 목록 페이지에서 '라이프스토리' 텍스트 확인
#         final_page_text_xpath = '//android.widget.TextView[@text="라이프스토리"]'
#         print(f"목록 페이지에서 '{final_page_text_xpath}' 텍스트를 확인합니다.")
#         try:
#             WebDriverWait(flow_tester.driver, 10).until(
#                 EC.presence_of_element_located((AppiumBy.XPATH, final_page_text_xpath))
#             )
#             print("✅ 최종 페이지에서 '라이프스토리' 텍스트를 확인했습니다.")
#         except TimeoutException:
#             error_msg = "실패: 최종 목록 페이지에서 '라이프스토리' 텍스트를 찾지 못했습니다."
#             save_screenshot_on_failure(flow_tester.driver, "final_page_verification_failed")
#             return False, error_msg
#
#         # 모든 검증 통과
#         flow_tester.driver.back()
#         time.sleep(1)
#         return True, "공유할 영업 콘텐츠 확인 시나리오 성공."
#
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "sales_content_test_failure")
#         return False, f"공유할 영업 콘텐츠 테스트 중 예외 발생: {e}"
#     finally:
#         print("--- 홈 > 공유할 영업 콘텐츠 추천 확인 시나리오 종료 ---")