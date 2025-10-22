# Test_Run/conftest.py

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="function")
def driver():
    # Desired Capabilities 설정 (안정성 옵션 추가)
    capabilities = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:platformVersion": "15",
        "appium:deviceName": "R3CT70V2T5H",
        "appium:appPackage": "com.coway.catalog.seller.stg",
        "appium:appActivity": "kr.coway.catalog.activity.webMain.WebMainActivity",
        "appium:noReset": True,
        "appium:newCommandTimeout": 300, # 명령 대기 시간 연장
        # --- 안정성을 위한 추천 옵션 ---
        "appium:skipServerInstallation": True, # 매번 서버 재설치 건너뛰기
        "appium:disableWindowAnimation": True # UI 애니메이션 비활성화로 테스트 속도 및 안정성 향상
    }

    appium_server_url = 'http://localhost:4723'

    # 드라이버 인스턴스 생성
    driver_instance = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    # 생성된 드라이버를 테스트 함수로 전달
    yield driver_instance

    # 테스트 함수 종료 후 드라이버 종료 (항상 실행됨)
    if driver_instance:
        driver_instance.quit()