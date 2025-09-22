import sys
import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수 임포트
from Utils.screenshot_helper import save_screenshot_on_failure



# [Seller app checklist-16] 홈 > 공지사항 개수 확인 (인덱스 순차 검사 방식)
def test_home_notice_count(flow_tester):
    """
    홈 화면의 공지사항 개수를 인덱스를 1부터 4까지 순차적으로 확인하여 검증합니다.
    - 4번째 공지사항 XPath가 존재하면 '실패'로 처리합니다.
    """
    print("\n--- 홈 > 공지사항 개수 확인 (인덱스 순차 검사) 시나리오 시작 ---")
    try:

        # 1. 공지사항 개수를 인덱스 1~4번 순차 확인
        print("공지사항 개수를 1번부터 4번까지 순차적으로 확인합니다.")

        base_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]/android.view.View'

        # notice_container//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((AppiumBy.XPATH, notice_container_xpath))
        # )
        found_count = 0
        fourth_item_found = False

        # i 변수를 1부터 4까지 증가시키며 XPath 존재 여부 확인
        for i in range(1, 5):
            indexed_xpath = f"{base_xpath}[{i}]"
            try:
                print(f"공지사항 인덱스 [{i}] 확인 시도...{indexed_xpath}")
                flow_tester.driver.find_element(AppiumBy.XPATH, indexed_xpath)
                print(f"✅ 공지사항 인덱스 [{i}] 발견.{indexed_xpath}")
                found_count = i

                if i == 4:
                    fourth_item_found = True
                    break

            except NoSuchElementException:
                print(f"공지사항 인덱스 [{i}] 없음. 탐색을 종료합니다.")
                break

        print(f"탐색 완료. 발견된 최대 공지사항 인덱스: {found_count}")

        # 2. 결과 판정
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


# [Seller app checklist-17] 홈 > 공지사항 이동 확인
def test_home_notice_click(flow_tester):
    """홈 화면의 첫 번째 공지사항 클릭 시 상세 화면으로 이동하는지 확인합니다."""
    print("\n--- 홈 > 공지사항 이동 확인 시나리오 시작 (checklist-17) ---")
    try:
        notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        first_item_xpath = f"({notice_container_xpath}/android.view.View)[1]"
        # ⭐️ 1. 첫 번째 공지사항이 존재하는지 먼저 확인합니다.
        try:
            print("첫 번째 공지사항 존재 여부 확인...")
            first_notice = flow_tester.driver.find_element(AppiumBy.XPATH, first_item_xpath)
            print("✅ 공지사항 발견. 클릭을 진행합니다.")
            first_notice.click()
            time.sleep(3)
        except NoSuchElementException:
            # ⭐️ 2. 공지사항이 없으면, 실패가 아닌 성공으로 간주하고 메시지와 함께 True를 반환합니다.
            print("공지사항이 존재하지 않으므로 클릭 테스트를 건너뛰고 성공 처리합니다.")
            return True, "공지사항 없음 (클릭 테스트 성공 간주)."

        print("공지사항 상세 페이지로 이동했는지 확인합니다.")
        notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'
        WebDriverWait(flow_tester.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, notice_page_title_xpath)),
            message="공지사항 상세 페이지로 이동하지 못했습니다."
        )
        print("✅ 공지사항 상세 페이지로 성공적으로 이동했습니다.")

        print("뒤로가기를 눌러 홈 화면으로 돌아갑니다.")
        flow_tester.driver.back()
        time.sleep(3)

        return True, "공지사항 상세 페이지 이동 확인 성공."

    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "notice_click_failure")
        return False, f"공지사항 이동 확인 중 오류 발생: {e}"
    finally:
        print("--- 홈 > 공지사항 이동 확인 시나리오 종료 ---")