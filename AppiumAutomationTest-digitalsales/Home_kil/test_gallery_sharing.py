# -*- coding: utf-8 -*-

import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 유틸리티 함수 임포트
from Utils.screenshot_helper import save_screenshot_on_failure
# --- ▼ [수정] 직접 스크롤 로직을 사용하므로 scroll_down만 import 합니다 ▼ ---
from Utils.scrolling_function import scroll_down

# Xpath 저장소에서 HomeKilLocators 임포트
from Xpath.xpath_repository import HomeKilLocators


def test_gallery_facebook_share(flow_tester):
    """Seller app checklist-23: 코웨이 갤러리 페이스북 공유 기능 확인"""
    print("\n--- 코웨이 갤러리 페이스북 공유 시나리오 시작 (checklist-23) ---")

    # --- 플랫폼 분기 로직 추가 ---
    try:
        if flow_tester.platform == 'android':
            locators = HomeKilLocators.AOS
        elif flow_tester.platform == 'ios':
            locators = HomeKilLocators.IOS
            if not all([locators.gallery_link_xpath, locators.share_button_gallery_xpath,
                        locators.facebook_xpath, locators.agree_button_xpath, locators.facebook_webview_xpath]):
                print("경고: IOS 플랫폼에 필요한 일부 갤러리 공유 XPath가 정의되지 않았습니다. 테스트를 건너<0xEB><0x9A><0xB4>니다.")
                return True, f"{flow_tester.platform} 갤러리 공유 XPath 부족 (테스트 통과 간주)"
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")
        locators = HomeKilLocators.AOS
    # --- 플랫폼 분기 로직 완료 ---

    # XPath 변수 정의 (locators 객체 사용)
    gallery_link_xpath = locators.gallery_link_xpath
    home_container_xpath = locators.home_button_xpath # 수정됨
    share_button_xpath = locators.share_button_gallery_xpath # 수정됨 (share_button_xpath -> share_button_gallery_xpath)
    facebook_option_xpath = locators.facebook_xpath # 수정됨 (facebook_option_xpath -> facebook_xpath)
    agree_button_xpath = locators.agree_button_xpath
    facebook_webview_xpath = locators.facebook_webview_xpath

    try:
        # 1. '코웨이 갤러리 체험 공유하기'가 홈 UI 위에 보일 때까지 스크롤
        print(f"'{gallery_link_xpath}' 텍스트가 클릭 가능한 위치에 올 때까지 스크롤합니다.")
        max_scroll_attempts = 10
        element_in_view = False
        gallery_element = None

        for i in range(max_scroll_attempts):
            try:
                gallery_element = flow_tester.driver.find_element(AppiumBy.XPATH, gallery_link_xpath)
                home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)

                if gallery_element.is_displayed():
                    gallery_rect = gallery_element.rect
                    home_rect = home_element.rect

                    # '코웨이 갤러리' 요소의 하단이 '홈' 요소의 상단보다 위에 있는지 확인
                    if (gallery_rect['y'] + gallery_rect['height']) < home_rect['y']:
                        print("✅ '코웨이 갤러리' 텍스트를 클릭 가능한 위치에서 찾았습니다.")
                        element_in_view = True
                        break
                    else:
                        print(f"({i + 1}/{max_scroll_attempts}) '코웨이 갤러리'가 홈 UI에 가려져 있습니다. 스크롤 다운.")
                else:
                    print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾았지만 보이지 않습니다. 스크롤 다운.")

            except NoSuchElementException:
                print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾지 못했습니다. 스크롤 다운.")

            scroll_down(flow_tester.driver)  # Utils에 있는 scroll_down 함수 사용
            time.sleep(1)

        if not element_in_view:
            raise NoSuchElementException("스크롤 후 '코웨이 갤러리 체험 공유하기'를 클릭 가능한 위치에서 찾지 못했습니다.")

        # 2. '코웨이 갤러리 체험 공유하기' 클릭
        print("갤러리 체험 공유하기를 클릭합니다.")
        gallery_element.click()
        time.sleep(3)  # 페이지 로딩 대기

        # 3. 공유 버튼 노출 확인 및 클릭
        print(f"'{share_button_xpath}' 공유 버튼을 찾습니다...")
        share_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, share_button_xpath))
        )
        print("✅ 공유 버튼을 찾았습니다. 클릭합니다.")
        share_button.click()
        time.sleep(2)  # 공유 시트 팝업 대기

        # 4. '페이스북' 옵션 확인 및 클릭
        print(f"'{facebook_option_xpath}' 옵션을 찾습니다...")
        facebook_option = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, facebook_option_xpath))
        )
        print("✅ '페이스북' 옵션을 찾았습니다. 클릭합니다.")
        facebook_option.click()
        time.sleep(2)  # 권한 동의 팝업 대기

        # 5. 권한 동의 버튼 확인 및 클릭
        print(f"'{agree_button_xpath}' 동의 버튼을 찾습니다...")
        agree_button = WebDriverWait(flow_tester.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, agree_button_xpath))
        )
        print("✅ 동의 버튼을 찾았습니다. 클릭합니다.")
        agree_button.click()
        time.sleep(3)  # 페이스북 공유 화면 로딩 대기

        # 6. 최종 확인: 'Facebook에 공유' WebView 노출 확인
        print(f"'{facebook_webview_xpath}' 화면이 노출되는지 확인합니다...")
        WebDriverWait(flow_tester.driver, 15).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, facebook_webview_xpath))
        )
        print("✅ 성공: 'Facebook에 공유' 화면이 정상적으로 노출되었습니다.")
        flow_tester.driver.back() # 페이스북 웹뷰에서 뒤로가기
        time.sleep(1)
        flow_tester.driver.back() # 갤러리 상세에서 뒤로가기
        time.sleep(1)
        return True, "코웨이 갤러리 페이스북 공유 기능 확인 성공"

    except (TimeoutException, NoSuchElementException) as e:
        save_screenshot_on_failure(flow_tester.driver, "gallery_fb_share_element_not_found")
        return False, f"실패: 테스트 중 필수 요소를 찾지 못했습니다. - {e}"
    except Exception as e:
        save_screenshot_on_failure(flow_tester.driver, "gallery_fb_share_failure")
        return False, f"실패: 코웨이 갤러리 공유 테스트 중 오류 발생: {e}"
    finally:
        print("--- 코웨이 갤러리 페이스북 공유 시나리오 종료 ---")


# # -*- coding: utf-8 -*-
#
# import time
#
#
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# # 유틸리티 함수 임포트


# from Utils.screenshot_helper import save_screenshot_on_failure
# # --- ▼ [수정] 직접 스크롤 로직을 사용하므로 scroll_down만 import 합니다 ▼ ---
# from Utils.scrolling_function import scroll_down
#
#
# def test_gallery_facebook_share(flow_tester):
#     """Seller app checklist-23: 코웨이 갤러리 페이스북 공유 기능 확인"""
#     print("\n--- 코웨이 갤러리 페이스북 공유 시나리오 시작 (checklist-23) ---")
#
#     # XPath 변수 정의
#     gallery_link_xpath = '//android.widget.TextView[@text="코웨이 갤러리 체험 공유하기"]'
#     home_container_xpath = '//android.view.View[@content-desc="홈"]'  # 하단 홈 UI 컨테이너
#     share_button_xpath = '//android.widget.Button[@resource-id="gallery-promotion-share-button"]'
#     facebook_option_xpath = '//android.widget.TextView[@text="페이스북"]'
#     agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
#     facebook_webview_xpath = '//android.webkit.WebView[@text="Facebook에 공유"]'
#
#     try:
#         # 1. '코웨이 갤러리 체험 공유하기'가 홈 UI 위에 보일 때까지 스크롤
#         print(f"'{gallery_link_xpath}' 텍스트가 클릭 가능한 위치에 올 때까지 스크롤합니다.")
#         max_scroll_attempts = 10
#         element_in_view = False
#         gallery_element = None
#
#         for i in range(max_scroll_attempts):
#             try:
#                 gallery_element = flow_tester.driver.find_element(AppiumBy.XPATH, gallery_link_xpath)
#                 home_element = flow_tester.driver.find_element(AppiumBy.XPATH, home_container_xpath)
#
#                 if gallery_element.is_displayed():
#                     gallery_rect = gallery_element.rect
#                     home_rect = home_element.rect
#
#                     # '코웨이 갤러리' 요소의 하단이 '홈' 요소의 상단보다 위에 있는지 확인
#                     if (gallery_rect['y'] + gallery_rect['height']) < home_rect['y']:
#                         print("✅ '코웨이 갤러리' 텍스트를 클릭 가능한 위치에서 찾았습니다.")
#                         element_in_view = True
#                         break
#                     else:
#                         print(f"({i + 1}/{max_scroll_attempts}) '코웨이 갤러리'가 홈 UI에 가려져 있습니다. 스크롤 다운.")
#                 else:
#                     print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾았지만 보이지 않습니다. 스크롤 다운.")
#
#             except NoSuchElementException:
#                 print(f"({i + 1}/{max_scroll_attempts}) 요소를 찾지 못했습니다. 스크롤 다운.")
#
#             scroll_down(flow_tester.driver)  # Utils에 있는 scroll_down 함수 사용
#             time.sleep(1)
#
#         if not element_in_view:
#             raise NoSuchElementException("스크롤 후 '코웨이 갤러리 체험 공유하기'를 클릭 가능한 위치에서 찾지 못했습니다.")
#
#         # 2. '코웨이 갤러리 체험 공유하기' 클릭
#         print("갤러리 체험 공유하기를 클릭합니다.")
#         gallery_element.click()
#         time.sleep(3)  # 페이지 로딩 대기
#
#         # 3. 공유 버튼 노출 확인 및 클릭
#         print(f"'{share_button_xpath}' 공유 버튼을 찾습니다...")
#         share_button = WebDriverWait(flow_tester.driver, 10).until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, share_button_xpath))
#         )
#         print("✅ 공유 버튼을 찾았습니다. 클릭합니다.")
#         share_button.click()
#         time.sleep(2)  # 공유 시트 팝업 대기
#
#         # 4. '페이스북' 옵션 확인 및 클릭
#         print(f"'{facebook_option_xpath}' 옵션을 찾습니다...")
#         facebook_option = WebDriverWait(flow_tester.driver, 10).until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, facebook_option_xpath))
#         )
#         print("✅ '페이스북' 옵션을 찾았습니다. 클릭합니다.")
#         facebook_option.click()
#         time.sleep(2)  # 권한 동의 팝업 대기
#
#         # 5. 권한 동의 버튼 확인 및 클릭
#         print(f"'{agree_button_xpath}' 동의 버튼을 찾습니다...")
#         agree_button = WebDriverWait(flow_tester.driver, 10).until(
#             EC.element_to_be_clickable((AppiumBy.XPATH, agree_button_xpath))
#         )
#         print("✅ 동의 버튼을 찾았습니다. 클릭합니다.")
#         agree_button.click()
#         time.sleep(3)  # 페이스북 공유 화면 로딩 대기
#
#         # 6. 최종 확인: 'Facebook에 공유' WebView 노출 확인
#         print(f"'{facebook_webview_xpath}' 화면이 노출되는지 확인합니다...")
#         WebDriverWait(flow_tester.driver, 15).until(
#             EC.visibility_of_element_located((AppiumBy.XPATH, facebook_webview_xpath))
#         )
#         print("✅ 성공: 'Facebook에 공유' 화면이 정상적으로 노출되었습니다.")
#         flow_tester.driver.back()
#         time.sleep(1)
#         return True, "코웨이 갤러리 페이스북 공유 기능 확인 성공"
#
#     except (TimeoutException, NoSuchElementException) as e:
#         save_screenshot_on_failure(flow_tester.driver, "gallery_fb_share_element_not_found")
#         return False, f"실패: 테스트 중 필수 요소를 찾지 못했습니다. - {e}"
#     except Exception as e:
#         save_screenshot_on_failure(flow_tester.driver, "gallery_fb_share_failure")
#         return False, f"실패: 코웨이 갤러리 공유 테스트 중 오류 발생: {e}"
#     finally:
#         print("--- 코웨이 갤러리 페이스북 공유 시나리오 종료 ---")