# -*- coding: utf-8 -*-

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Utils.screenshot_helper import save_screenshot_on_failure


def test_cody_matching_visibility(flow_tester):
    """Seller app checklist-65: 코디매칭 탭 이동 및 핵심 라벨 노출 확인"""
    print("\n--- 코디매칭 탭 이동 및 라벨 노출 시나리오 시작 (checklist-65) ---")

    wait = WebDriverWait(flow_tester.driver, 15)
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        # 1. '코디매칭' 탭 클릭 (좌표 기반)
        cody_matching_coords = (660, 310)
        print(f"'코디매칭' 탭 위치인 {cody_matching_coords} 좌표를 클릭합니다.")
        try:
            flow_tester.driver.tap([cody_matching_coords])
            time.sleep(2)  # 탭 전환 애니메이션 대기
        except Exception as e:
            error_msg = f"실패: '코디매칭' 탭 좌표 클릭 중 에러 발생: {e}"
            save_screenshot_on_failure(flow_tester.driver, "cody_matching_tap_failed")
            return False, error_msg

        # # --- Step 1: '코디매칭' 탭으로 이동 ---
        # cody_matching_tab_xpath = '//android.view.View[@text="코디매칭"]'
        # print(f"💡 '{cody_matching_tab_xpath}' 탭을 찾습니다...")
        # cody_matching_tab = wait.until(
        #     EC.element_to_be_clickable((AppiumBy.XPATH, cody_matching_tab_xpath))
        # )
        # print("✅ 탭을 찾았습니다. 클릭합니다.")
        # cody_matching_tab.click()
        # time.sleep(3)  # 페이지 로딩 대기

        # --- Step 2: '코디매칭 총주문' 라벨 확인 ---
        print("💡 '코디매칭 총주문' 라벨 확인...")
        total_order_label_xpath = '//android.widget.TextView[@text="코디매칭 총주문"]'
        wait.until(
            EC.visibility_of_element_located((AppiumBy.XPATH, total_order_label_xpath)),
            message="'코디매칭 총주문' 라벨을 찾지 못했습니다."
        )
        print("✅ '코디매칭 총주문' 라벨이 노출되었습니다.")

        # --- Step 3: '코디매칭 성공' 라벨 확인 ---
        print("💡 '코디매칭 성공' 라벨 확인...")
        success_order_label_xpath = '//android.widget.TextView[@text="코디매칭 성공"]'
        wait.until(
            EC.visibility_of_element_located((AppiumBy.XPATH, success_order_label_xpath)),
            message="'코디매칭 성공' 라벨을 찾지 못했습니다."
        )
        print("✅ '코디매칭 성공' 라벨이 노출되었습니다.")

        # --- 최종 성공 처리 ---
        scenario_passed = True
        result_message = "🎉 성공: 코디매칭 페이지의 핵심 라벨(총주문, 성공)이 모두 정상적으로 노출됩니다."

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "cody_matching_label_fail")
        result_message = f"❌ 실패: 요소를 찾지 못했거나 타임아웃 발생 - {e}"
        scenario_passed = False
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "cody_matching_error")
        result_message = f"❌ 실패: 테스트 실행 중 예상치 못한 오류 발생: {e}"
        scenario_passed = False
    finally:
        print(f"--- 코디매칭 탭 라벨 노출 시나리오 종료 ---\n")
        # 최종 결과를 튜플 형태로 반환
        return scenario_passed, result_message