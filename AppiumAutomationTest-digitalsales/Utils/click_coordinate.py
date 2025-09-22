from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time

# W3C Actions를 위한 추가 임포트
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder


def w3c_click_coordinate(driver, x, y):
    """
    W3C Actions를 사용하여 주어진 좌표(x, y)를 클릭하는 함수입니다.

    Args:
        driver: Appium 드라이버 객체
        x (int): 클릭할 x 좌표
        y (int): 클릭할 y 좌표
    """
    try:
        # 카테고리 '상품브리핑' 노출 및 클릭 확인
        print("\n--- 배너 클릭 시도 ---")

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver,
                                            mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(x,y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(x,y)
        actions.w3c_actions.pointer_action.release()

        print(f"W3C Actions로 좌표 ({x}, {y})를 탭합니다.")
        time.sleep(3)  # 클릭 후 페이지 로딩 대기

        # 정의된 모든 액션을 실행합니다.
        actions.perform()
        time.sleep(2)  # 클릭 후 안정적인 다음 동작을 위해 잠시 대기
        print("✅ 좌표 클릭 성공.")

    except Exception as e:
        print(f"❌ 좌표 클릭 중 오류 발생: {e}")

