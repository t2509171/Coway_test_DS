import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 약속대로 사용자님의 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down


def test_recommended_sales_content(flow_tester):
    """
    홈 화면의 '공유할 영업 콘텐츠' 섹션을 테스트합니다.
    1. 섹션과 '유입순' 버튼이 하단 '홈' UI보다 위에 보일 때까지 스크롤하여 섹션을 클릭
    2. 상세 페이지에서 '라이프 스토리' 확인
    3. '목록' 버튼 클릭
    4. 목록 페이지에서 '라이프스토리' 확인
    """
    print("\n--- 홈 > 공유할 영업 콘텐츠 추천 확인 시나리오 시작 ---")
    try:
        # ⭐️ 1. XPath 정의 (하단 '홈' UI 포함)
        title_xpath = '//android.view.View[@content-desc="공유할 영업 콘텐츠를 추천 드려요"]/android.widget.TextView[2]'
        sort_button_xpath = '//android.widget.Button[@text="유입순"]'
        home_container_xpath = '//android.view.View[@content-desc="홈"]'  # 위치 비교 기준이 될 하단 고정 UI
        print(f"'{title_xpath}'와 '{sort_button_xpath}'를 찾고, '{home_container_xpath}'보다 위에 있는지 확인합니다.")

        max_scroll_attempts = 10
        section_found_and_clickable = False
        target_element = None

        # ⭐️ 2. 지정된 횟수만큼 스크롤하며 요소의 위치를 확인하는 루프
        for i in range(max_scroll_attempts):
            try:
                # 2-1. 필요한 세 가지 요소를 모두 찾습니다.
                target_element = flow_tester.driver.find_element(AppiumBy.XPATH, title_xpath)
                sort_button_element = flow_tester.driver.find_element(AppiumBy.XPATH, sort_button_xpath)
                home_container_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                # 2-2. 대상 요소들이 화면에 보이는지 먼저 확인합니다.
                if target_element.is_displayed() and sort_button_element.is_displayed():
                    print("✅ '공유할 영업 콘텐츠'와 '유입순' 버튼을 화면에서 찾았습니다. 이제 위치를 비교합니다.")

                    # ⭐️ 2-3. 위치 정보(.rect)를 가져와 Y 좌표를 비교합니다.
                    target_rect = target_element.rect
                    home_rect = home_container_element.rect

                    # 대상 UI의 가장 아래쪽 Y 좌표
                    target_bottom_y = target_rect['y'] + target_rect['height']
                    # '홈' UI의 가장 위쪽 Y 좌표
                    home_top_y = home_rect['y']

                    print(f"  -> 대상 UI 하단 Y: {target_bottom_y}, 홈 컨테이너 상단 Y: {home_top_y}")

                    # ⭐️ 2-4. 대상 UI가 '홈' UI보다 완전히 위에 있는지 확인
                    if target_bottom_y < home_top_y:
                        print("✅ 위치 조건 충족! 대상 UI가 하단 '홈' UI보다 위에 있습니다.")
                        section_found_and_clickable = True
                        break  # 루프를 성공적으로 종료합니다.
                    else:
                        print("⚠️ 위치 조건 불충족. 대상이 '홈' UI에 가려져 있습니다. 스크롤합니다.")
                else:
                    # 요소는 찾았으나 화면에 아직 표시되지 않은 경우
                    print("요소는 찾았지만 화면에 완전히 표시되지 않았습니다. 스크롤합니다.")

            except NoSuchElementException:
                # 세 요소 중 하나라도 DOM에서 찾지 못한 경우
                print("필요한 요소를 찾지 못했습니다. 스크롤합니다.")
                pass

            # 루프의 마지막에 스크롤을 실행합니다.
            print(f"({i + 1}/{max_scroll_attempts}) 스크롤 다운을 시도합니다.")
            scroll_down(flow_tester.driver)

        # 3. 루프 종료 후, 성공 여부를 확인합니다.
        if not section_found_and_clickable:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 했지만 클릭 가능한 위치에서 섹션을 찾지 못했습니다."
            save_screenshot_on_failure(flow_tester.driver, "sales_content_section_not_found")
            return False, error_msg

        # 4. 검증이 완료된 요소를 클릭합니다.
        print("정확한 위치에서 섹션을 확인하고 클릭합니다.")
        target_element.click()
        time.sleep(3)

        # 5. 최종 목록 페이지에서 '라이프스토리' 텍스트 확인 (기존 코드 유지)
        final_page_text_xpath = '//android.widget.TextView[@text="라이프스토리"]'
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
        return True, "공유할 영업 콘텐츠 확인 시나리오 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "sales_content_test_failure")
        return False, f"공유할 영업 콘텐츠 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 공유할 영업 콘텐츠 추천 확인 시나리오 종료 ---")