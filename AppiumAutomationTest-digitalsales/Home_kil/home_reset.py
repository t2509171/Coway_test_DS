import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def reset_to_home_and_refresh(flow_tester):
    """
    앱 화면을 초기 상태로 리셋합니다. (flow_tester를 인자로 받도록 수정)
    1. 홈 버튼을 클릭하여 홈 화면으로 이동합니다.
    2. 화면 최상단으로 스크롤합니다.
    3. PULL-DOWN 제스처로 화면을 새로고침합니다.
    """
    print("\n--- 화면 초기화 시작 ---")
    # flow_tester 객체에서 driver를 가져옵니다.
    driver = flow_tester.driver

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            print("경고: IOS 플랫폼의 home_reset 기능은 아직 완전히 구현되지 않았을 수 있습니다.")
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    try:
        # 1. 홈 버튼 클릭하여 홈 화면으로 이동
        print("홈 버튼을 클릭하여 홈 화면으로 이동합니다.")
        home_button_xpath = locators.home_button_xpath # 수정됨 (home_container_xpath -> home_button_xpath)
        try:
            driver.find_element(AppiumBy.XPATH, home_button_xpath).click()
            time.sleep(3)  # 홈 화면 로딩 대기
        except NoSuchElementException:
            print("경고: 홈 버튼을 찾을 수 없어 초기화의 일부를 건너뜁니다.")
            try:
                driver.back() # 뒤로가기 시도
                time.sleep(1)
                driver.find_element(AppiumBy.XPATH, home_button_xpath).click()
                time.sleep(3)
            except Exception as e:
                print(f"홈으로 이동 최종 실패: {e}")
                # 홈 이동 실패 시 스크롤 및 새로고침 의미 없으므로 종료
                print("❗️ 화면 초기화 실패 (홈 이동 불가).")
                return # 함수 종료

        # 2. 화면 최상단으로 스크롤 (위로 스와이프) - AOS/IOS 공통 로직
        print("화면 최상단으로 스크롤합니다.")
        size = driver.get_window_size()
        start_x = size['width'] / 2
        start_y = size['height'] * 0.4
        end_y = size['height'] * 0.8

        # 스크롤 횟수를 줄여 불필요한 대기 시간 감소
        driver.swipe(start_x, start_y, start_x, end_y, 400)
        time.sleep(1) # 스크롤 애니메이션 대기

        print("최상단 스크롤 완료.")

        # # 3. 화면 새로고침 (아래로 당기기 - Pull to Refresh) - 플랫폼별 구현 필요 시 추가
        # print("화면을 아래로 당겨 새로고침합니다.")
        # refresh_start_y = size['height'] * 0.2
        # refresh_end_y = size['height'] * 0.8
        # driver.swipe(start_x, refresh_start_y, start_x, refresh_end_y, 500)
        # time.sleep(4)  # 새로고침 및 데이터 로딩 대기

        print("✅ 화면 초기화 완료.")

    except Exception as e:
        print(f"❗️ 화면 초기화 중 오류 발생: {e}")


# import time
# from appium.webdriver.common.appiumby import AppiumBy

# from selenium.common.exceptions import NoSuchElementException
#
#
# def reset_to_home_and_refresh(flow_tester):
#     """
#     앱 화면을 초기 상태로 리셋합니다. (flow_tester를 인자로 받도록 수정)
#     1. 홈 버튼을 클릭하여 홈 화면으로 이동합니다.
#     2. 화면 최상단으로 스크롤합니다.
#     3. PULL-DOWN 제스처로 화면을 새로고침합니다.
#     """
#     print("\n--- 화면 초기화 시작 ---")
#     # flow_tester 객체에서 driver를 가져옵니다.
#     driver = flow_tester.driver
#
#     try:
#         # 1. 홈 버튼 클릭하여 홈 화면으로 이동
#         print("홈 버튼을 클릭하여 홈 화면으로 이동합니다.")
#         home_button_xpath = '//android.view.View[@content-desc="홈"]'
#         try:
#             driver.find_element(AppiumBy.XPATH, home_button_xpath).click()
#             time.sleep(3)  # 홈 화면 로딩 대기
#         except NoSuchElementException:
#             print("경고: 홈 버튼을 찾을 수 없어 초기화의 일부를 건너뜁니다.")
#             driver.back()
#             time.sleep(1)
#             try:
#                 driver.find_element(AppiumBy.XPATH, home_button_xpath).click()
#                 time.sleep(3)
#             except Exception as e:
#                 print(f"홈으로 이동 최종 실패: {e}")
#                 return
#
#         # 2. 화면 최상단으로 스크롤 (위로 스와이프)
#         print("화면 최상단으로 스크롤합니다.")
#         size = driver.get_window_size()
#         start_x = size['width'] / 2
#         start_y = size['height'] * 0.4
#         end_y = size['height'] * 0.8
#
#         for _ in range(1):
#             driver.swipe(start_x, start_y, start_x, end_y, 400)
#             time.sleep(0.5)
#
#         print("최상단 스크롤 완료.")
#         time.sleep(1)
#
#         # # 3. 화면 새로고침 (아래로 당기기 - Pull to Refresh)
#         # print("화면을 아래로 당겨 새로고침합니다.")
#         # refresh_start_y = size['height'] * 0.2
#         # refresh_end_y = size['height'] * 0.8
#         # driver.swipe(start_x, refresh_start_y, start_x, refresh_end_y, 500)
#         # time.sleep(4)  # 새로고침 및 데이터 로딩 대기
#
#         print("✅ 화면 초기화 완료.")
#
#     except Exception as e:
#         print(f"❗️ 화면 초기화 중 오류 발생: {e}")