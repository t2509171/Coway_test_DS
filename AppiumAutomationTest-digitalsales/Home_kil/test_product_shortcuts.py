import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 유틸리티 함수들을 import 합니다.
from Utils.screenshot_helper import save_screenshot_on_failure
from Utils.scrolling_function import scroll_down

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_verify_product_shortcuts_exist(flow_tester):
    """
    홈 화면에서 '제품 바로가기' 섹션과 '정수기' 아이콘(ID)이 '홈' UI(ID) 위에 보일 때까지 스크롤합니다.
    [수정] 확인 후 '정수기' 아이콘(ID)을 클릭하고, '정수기' 버튼(ID)이 나타나는지 검증합니다.
    [추가] 검증 완료 후 '뒤로가기' 버튼을 클릭하여 홈 화면으로 복귀합니다.
    """
    print("\n--- 홈 > 제품 바로가기 > '정수기' (ID) 클릭 및 뒤로가기 확인 시나리오 시작 ---")

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
        # 1. XPath 및 Accessibility ID 정의
        target_text_xpath = locators.target_text_xpath

        # --- [수정]: XPath 대신 Accessibility ID 사용 ---
        water_purifier_aid = '정수기'
        home_container_aid = '홈'
        # --- [수정 완료] ---

        max_scroll_attempts = 10
        element_in_view = False  # 최종 성공 여부 플래그

        print(f"'{target_text_xpath}'와 '{water_purifier_aid}'(ID)가 '{home_container_aid}'(ID) UI 위에 나타날 때까지 스크롤합니다.")
        for i in range(max_scroll_attempts):
            try:
                # --- [수정]: find_element 방식을 ID로 변경 ---
                target_element = flow_tester.driver.find_element(AppiumBy.XPATH, target_text_xpath)
                icon_element = flow_tester.driver.find_element(AppiumBy.ACCESSIBILITY_ID, water_purifier_aid)
                home_element = flow_tester.driver.find_element(AppiumBy.ACCESSIBILITY_ID, home_container_aid)
                # --- [수정 완료] ---

                # '제품 바로가기'와 '정수기' 아이콘이 모두 화면에 보이는지 확인
                if target_element.is_displayed() and icon_element.is_displayed():
                    print("✅ '제품 바로가기'와 '정수기' 아이콘을 찾았습니다. 위치를 비교합니다.")
                    target_rect = target_element.rect
                    icon_rect = icon_element.rect
                    home_rect = home_element.rect

                    if (target_rect['y'] + target_rect['height']) < home_rect['y'] and \
                            (icon_rect['y'] + icon_rect['height']) < home_rect['y']:
                        print("✅ 위치 조건 충족! '정수기' 아이콘을 클릭합니다.")

                        try:
                            # 1. '정수기' 아이콘 클릭
                            icon_element.click()
                            print("🖱️ '정수기' 아이콘 클릭 완료.")

                            wait = WebDriverWait(flow_tester.driver, 10)

                            # --- [로직 수정]: 새 버튼을 기다리기 전, 기존 아이콘이 사라질 때까지 대기 (Staleness) ---
                            # 동일한 ID('정수기')를 사용하므로, 페이지 전환을 명확히 인지하기 위해 추가
                            try:
                                print("페이지 전환 대기 중 (기존 아이콘 사라짐 확인)...")
                                wait.until(EC.staleness_of(icon_element))
                                print("✅ 페이지 전환 확인됨.")
                            except TimeoutException:
                                print("⚠️ 경고: 기존 '정수기' 아이콘이 10초 내에 사라지지 않았습니다. 다음 단계로 계속 진행합니다.")

                            # 2. '정수기' 버튼(새 페이지)이 나타나는지 명시적 대기 (10초)
                            new_button_aid = '//android.widget.Button[@text="정수기"]'  # 새 페이지의 버튼 ID

                            print(f"'{new_button_aid}'(ID) 버튼이 나타나는지 확인합니다.")
                            wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, new_button_aid)))

                            print("✅ '정수기' 버튼(페이지) 확인 성공.")
                            # --- [로직 수정 완료] ---

                            try:
                                # 페이지 복귀를 위한 '뒤로가기' 버튼 (10초 대기)
                                back_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View[1]/android.widget.Button[1]'
                                print(f"페이지 복귀를 위해 뒤로가기 버튼({back_button_xpath})을 클릭합니다.")

                                back_button = wait.until(
                                    EC.element_to_be_clickable((AppiumBy.XPATH, back_button_xpath))
                                )
                                back_button.click()
                                print("🖱️ 뒤로가기 버튼 클릭 완료. 홈 화면으로 복귀합니다.")
                                time.sleep(1)

                            except Exception as back_e:
                                print(f"⚠️ 경고: 뒤로가기 버튼 클릭 중 오류 발생: {back_e}")
                                save_screenshot_on_failure(flow_tester.driver, "water_purifier_back_button_fail")

                            element_in_view = True
                            break  # 모든 시나리오를 완료했으므로 스크롤 루프 종료

                        except TimeoutException:
                            print(f"❌ 실패: '정수기' 아이콘 클릭 후 10초 내에 새 '{new_button_aid}'(ID) 버튼을 찾지 못했습니다.")
                            save_screenshot_on_failure(flow_tester.driver, "water_purifier_button_not_found")
                            break
                        except Exception as click_e:
                            print(f"❌ '정수기' 아이콘 클릭 또는 대기 중 예외 발생: {click_e}")
                            save_screenshot_on_failure(flow_tester.driver, "water_purifier_click_exception")
                            break

                    else:
                        print(f"({i + 1}/{max_scroll_attempts}) 위치 조건 불충족. 요소가 '홈' UI에 가려져 있습니다. 스크롤합니다.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) 두 요소 중 하나 이상이 아직 보이지 않습니다. 스크롤합니다.")

            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾는 중... 스크롤합니다.")

            scroll_down(flow_tester.driver)
            time.sleep(1)

        if not element_in_view:
            error_msg = f"실패: {max_scroll_attempts}번 스크롤 시도 후 '제품 바로가기' 및 '정수기' 버튼 확인에 실패했습니다."
            return False, error_msg

        return True, "제품 바로가기 섹션 및 정수기 아이콘(ID) 클릭, '정수기' 버튼(ID) 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "verify_product_shortcut_failure")
        return False, f"제품 바로가기 존재 확인 테스트 중 예외 발생: {e}"
    finally:
        print("--- 홈 > 제품 바로가기 > '정수기' (ID) 클릭 및 뒤로가기 확인 시나리오 종료 ---")