import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

# def scroll_down(driver, start_x=None, start_y=None, end_x=None, end_y=None, duration_ms=200):
#     """
#     W3C Actions를 사용하여 화면을 아래로 스크롤합니다.
#     좌표가 주어지지 않으면 화면 중앙을 기준으로 스크롤합니다.
#
#     :param driver: Appium 드라이버 객체
#     :param start_x: 스크롤 시작 x 좌표
#     :param start_y: 스크롤 시작 y 좌표
#     :param end_x: 스크롤 끝 x 좌표
#     :param end_y: 스크롤 끝 y 좌표
#     :param duration_ms: 스크롤 동작 시간 (밀리초)
#     """
#     try:
#         if start_x is None or start_y is None or end_x is None or end_y is None:
#             screen_size = driver.get_window_size()
#             start_x = screen_size['width'] // 2
#             start_y = screen_size['height'] * 0.8
#             end_x = screen_size['width'] // 2
#             end_y = screen_size['height'] * 0.2
#
#         actions = ActionChains(driver)
#         actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#         actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
#         actions.w3c_actions.pointer_action.pointer_down()
#         actions.w3c_actions.pointer_action.pause(duration_ms / 1000)
#         actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
#         actions.w3c_actions.pointer_action.release()
#         actions.perform()
#         time.sleep(1)
#         print(f"스크롤 다운 수행 완료: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
#     except Exception as e:
#         print(f"스크롤 다운 중 오류 발생: {e}")
#
#
# def scroll_to_element(flow_tester, element_xpath, max_scrolls=5, start_x=550, start_y=1800, end_x=550, end_y=1100):
#     """
#     지정된 XPath를 가진 요소를 찾을 때까지 스크롤합니다.
#
#     :param flow_tester: 테스트 플로우 객체
#     :param element_xpath: 찾고자 하는 요소의 XPath
#     :param max_scrolls: 최대 스크롤 횟수
#     :param start_x: 스크롤 시작 x 좌표
#     :param start_y: 스크롤 시작 y 좌표
#     :param end_x: 스크롤 끝 x 좌표
#     :param end_y: 스크롤 끝 y 좌표
#     :return: (bool, str) 성공 여부와 메시지
#     """
#     for i in range(max_scrolls):
#         print(f"스크롤 시도 {i + 1}/{max_scrolls}")
#         try:
#             element = flow_tester.driver.find_element(AppiumBy.XPATH, element_xpath)
#             if element.is_displayed():
#                 print(f"✅ '{element_xpath}' 요소가 성공적으로 노출되었습니다.")
#                 return True, f"'{element_xpath}' 요소까지 W3C 스크롤 성공."
#         except NoSuchElementException:
#             print(f"'{element_xpath}' 요소를 찾을 수 없습니다. W3C 스크롤을 시도합니다.")
#             scroll_down(flow_tester.driver, start_x, start_y, end_x, end_y)
#
#     return False, f"최대 스크롤 횟수({max_scrolls}) 내에 '{element_xpath}' 요소를 찾지 못했습니다."
#
# # 동적 스크롤
# # def scroll_down(driver, duration_ms=500):
# #     """
# #     W3C Actions를 사용하여 화면을 아래로 스크롤합니다.
# #     화면 중앙을 기준으로 동적으로 좌표를 계산하여 스크롤합니다.
# #     """
# #     try:
# #         # 현재 디바이스의 화면 크기를 가져옵니다.
# #         screen_size = driver.get_window_size()
# #         start_x = screen_size['width'] // 2
# #         start_y = screen_size['height'] * 0.8  # 화면의 80% 지점에서 스크롤 시작
# #         end_y = screen_size['height'] * 0.2    # 화면의 20% 지점까지 스크롤
# #
# #         actions = ActionChains(driver)
# #         actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
# #         actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
# #         actions.w3c_actions.pointer_action.pointer_down()
# #         actions.w3c_actions.pointer_action.pause(duration_ms / 1000)
# #         actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
# #         actions.w3c_actions.pointer_action.release()
# #         actions.perform()
# #         time.sleep(1.5) # 스크롤 후 UI가 안정화될 때까지 대기
# #         print(f"스크롤 다운 수행 완료: ({start_x}, {start_y}) -> ({start_x}, {end_y})")
# #     except Exception as e:
# #         print(f"스크롤 다운 중 오류 발생: {e}")
#
# # def scroll_to_element(flow_tester, element_xpath, max_scrolls=5):
# #     """
# #     지정된 XPath를 가진 요소를 '실제 화면에 노출될 때까지' 아래로 스크롤합니다.
# #     요소의 좌표를 직접 계산하여 정확한 가시성을 확인합니다.
# #     """
# #     # 화면의 높이를 가져옵니다.
# #     screen_size = flow_tester.driver.get_window_size()
# #     screen_height = screen_size['height']
# #
# #     for i in range(max_scrolls):
# #         print(f"스크롤 시도 {i + 1}/{max_scrolls}")
# #         try:
# #             # 1. 앱의 전체 UI 구조에서 요소를 찾습니다.
# #             element = flow_tester.driver.find_element(AppiumBy.XPATH, element_xpath)
# #
# #             # --- 👇 신뢰도 높은 가시성 확인 로직 👇 ---
# #             # 2. 요소의 y 좌표와 높이를 가져옵니다.
# #             element_location_y = element.location['y']
# #             element_height = element.size['height']
# #
# #             # 3. 요소의 상단과 하단이 모두 화면 경계 내에 있는지 직접 계산합니다.
# #             is_truly_visible = (element_location_y >= 0) and ((element_location_y + element_height) <= screen_height)
# #
# #             if is_truly_visible:
# #                 print(f"✅ '{element_xpath}' 요소가 '실제 화면에' 성공적으로 노출되었습니다.")
# #                 return True, f"'{element_xpath}' 요소까지 스크롤 성공."
# #             else:
# #                 # 요소는 존재하지만 화면 밖에 있는 경우
# #                 print(f"'{element_xpath}' 요소를 찾았지만 화면 밖에 있습니다. 스크롤을 계속합니다.")
# #                 scroll_down(flow_tester.driver)
# #             # --- 👆 신뢰도 높은 가시성 확인 로직 👆 ---
# #
# #         except NoSuchElementException:
# #             # 요소를 아예 찾지 못한 경우
# #             print(f"'{element_xpath}' 요소를 찾을 수 없습니다. 스크롤을 시도합니다.")
# #             scroll_down(flow_tester.driver)
# #
# #     return False, f"최대 스크롤 횟수({max_scrolls}) 내에 '{element_xpath}' 요소를 화면에 노출시키지 못했습니다."

# scroll_down 함수는 동적 좌표 계산을 위해 그대로 둡니다.
def scroll_down(driver, duration_ms=500):
    try:
        screen_size = driver.get_window_size()
        start_x = screen_size['width'] // 2
        start_y = screen_size['height'] * 0.8
        end_y = screen_size['height'] * 0.4

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_ms / 1000)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        time.sleep(1.5)
        print(f"스크롤 다운 수행 완료: ({start_x}, {start_y}) -> ({start_x}, {end_y})")
    except Exception as e:
        print(f"스크롤 다운 중 오류 발생: {e}")

# scroll_up 함수는 동적 좌표 계산을 위해 그대로 둡니다.
def scroll_up(driver, duration_ms=500):
    try:
        screen_size = driver.get_window_size()
        start_x = screen_size['width'] // 2
        # 시작점을 화면 상단(20%)으로 설정 (scroll_down과 반대)
        start_y = screen_size['height'] * 0.2
        # 끝점을 화면 하단(80%)으로 설정 (scroll_down과 반대)
        end_y = screen_size['height'] * 0.8

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_ms / 1000)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        time.sleep(1.5)
        print(f"스크롤 업 수행 완료: ({start_x}, {start_y}) -> ({start_x}, {end_y})")
    except Exception as e:
        print(f"스크롤 업 중 오류 발생: {e}")



# --- 👇 [핵심 수정 부분] 👇 ---
def scroll_to_element(flow_tester, element_xpath, max_scrolls=5):
    """
    지정된 XPath를 가진 요소를 '실제 화면에 노출될 때까지' 아래로 스크롤합니다.
    요소의 좌표를 직접 계산하여 정확한 가시성을 확인합니다.
    """
    # 현재 화면의 높이를 가져옵니다.
    screen_size = flow_tester.driver.get_window_size()
    screen_height = screen_size['height']

    for i in range(max_scrolls):
        print(f"스크롤 시도 {i + 1}/{max_scrolls}")
        try:
            # 1. 앱의 전체 UI 구조에서 요소를 먼저 찾습니다.
            element = flow_tester.driver.find_element(AppiumBy.XPATH, element_xpath)

            # 2. 요소의 y 좌표와 높이를 가져옵니다.
            element_location_y = element.location['y']
            element_height = element.size['height']

            # 3. 요소의 상단과 하단이 모두 화면 경계 내에 있는지 직접 계산합니다.
            # 요소의 y 좌표가 0보다 크거나 같고, y좌표+높이가 화면 높이보다 작거나 같아야 합니다.
            is_truly_visible = (element_location_y >= 0) and ((element_location_y + element_height) <= screen_height)

            if is_truly_visible:
                print(f"✅ '{element_xpath}' 요소가 '실제 화면 안에서' 성공적으로 노출되었습니다.")
                return True, f"'{element_xpath}' 요소까지 스크롤 성공."
            else:
                # 요소는 찾았지만, 계산 결과 화면 밖에 있는 경우
                print(f"'{element_xpath}' 요소를 찾았지만 화면 밖에 있습니다. 스크롤을 계속합니다.")
                scroll_down(flow_tester.driver)

        except NoSuchElementException:
            # 요소를 아예 찾지 못한 경우(앱 구조에 없는 경우)
            print(f"'{element_xpath}' 요소를 찾을 수 없습니다. 스크롤을 시도합니다.")
            scroll_down(flow_tester.driver)

    return False, f"최대 스크롤 횟수({max_scrolls}) 내에 '{element_xpath}' 요소를 화면에 노출시키지 못했습니다."



