import os
from datetime import datetime

def save_screenshot_on_failure(driver, test_name):
    """
    테스트 실패 시 스크린샷을 저장하는 함수

    :param driver: Appium 드라이버 객체
    :param test_name: 파일 이름에 포함될 테스트 시나리오 이름
    """
    # 스크린샷을 저장할 디렉토리 경로 설정
    screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')

    # 'screenshots' 디렉토리가 없으면 생성
    os.makedirs(screenshots_dir, exist_ok=True)

    # 타임스탬프를 포함한 고유한 파일 이름 생성 (덮어쓰기 방지)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"failure_{test_name}_{timestamp}.png"
    file_path = os.path.join(screenshots_dir, file_name)

    try:
        # 스크린샷 캡처 및 저장
        driver.save_screenshot(file_path)
        print(f"📸 스크린샷이 저장되었습니다: {file_path}")
    except Exception as e:
        print(f"🚨 스크린샷 저장 중 오류 발생: {e}")