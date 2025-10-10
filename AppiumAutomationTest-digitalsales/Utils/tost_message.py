import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def watch_for_any_toast(flow_tester, max_wait_seconds=30):
    """
    지정된 시간 동안 1초마다 반복적으로 토스트 메시지가 나타나는지 감시합니다.
    텍스트 내용과 상관없이 토스트가 발견되면 즉시 True를 반환합니다.
    """
    print(f"\n--- 최대 {max_wait_seconds}초 동안 토스트 메시지 출현 감시 시작 ---")

    toast_message_xpath = '//android.widget.Toast'
    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        try:
            # 1초의 짧은 대기시간으로 토스트 메시지를 즉시 확인
            WebDriverWait(flow_tester.driver, 1).until(
                EC.presence_of_element_located((AppiumBy.XPATH, toast_message_xpath))
            )

            # 위의 코드가 성공하면 토스트가 나타난 것이므로 바로 성공 처리
            success_message = "✅ 성공: 토스트 메시지가 화면에 노출되었습니다."
            print(success_message)
            return True, success_message

        except TimeoutException:
            # 1초 안에 토스트가 안 보이면 통과하고 루프 계속
            print(f"감시 중... (경과 시간: {int(time.time() - start_time)}초)")
            time.sleep(1)  # CPU 부하를 줄이기 위해 잠시 대기
            continue

    failure_message = f"❌ 실패: {max_wait_seconds}초 내에 토스트 메시지가 나타나지 않았습니다."
    print(failure_message)
    save_screenshot_on_failure(flow_tester.driver, "toast_watch_timeout")
    return False, failure_message