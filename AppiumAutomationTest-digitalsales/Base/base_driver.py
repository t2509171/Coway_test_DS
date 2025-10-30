# PythonProject/Base/base_driver.py

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException # 예외 처리를 위해 추가
from Base.base_config import AndroidConfig,IOSConfig,AppiumConfig

class BaseAppiumDriver:
    """
    Appium 드라이버의 기본 설정 및 공통 기능을 제공하는 베이스 클래스입니다.
    """
    def __init__(self):
        """
        플랫폼 인수를 받지 않도록 생성자를 수정합니다.
        """
        self.driver = None
        self.wait = None
        self.platform = None # 감지된 플랫폼을 저장할 변수
        self.config = None   # 감지된 플랫폼의 설정을 저장할 변수

    def setup_driver(self):
        """
        연결된 디바이스의 플랫폼을 자동으로 감지하여 드라이버를 설정합니다.
        Android 연결을 먼저 시도하고, 실패하면 iOS 연결을 시도합니다.
        """
        # 1. Android 드라이버 설정 시도
        try:
            print("--- Android 플랫폼 연결 시도... ---")
            self.config = AndroidConfig
            options = UiAutomator2Options()
            options.platform_name = self.config.PLATFORM_NAME
            options.platform_version = self.config.PLATFORM_VERSION
            options.device_name = self.config.DEVICE_NAME
            options.app_package = self.config.APP_PACKAGE
            options.app_activity = self.config.APP_ACTIVITY
            options.automation_name = self.config.AUTOMATION_NAME
            options.no_reset = AppiumConfig.NO_RESET
            options.new_command_timeout = AppiumConfig.NEW_COMMAND_TIMEOUT

            options.chromedriver_executable = "C:\\chromedriver-win64\\chromedriver.exe"

            self.driver = webdriver.Remote(AppiumConfig.APPIUM_SERVER_URL, options=options)
            self.platform = 'android'
            print("✅ Android 드라이버 초기화 성공 및 앱 실행.")

        except WebDriverException as android_error:
            print(f"⚠️ Android 연결 실패: {android_error}")
            print("\n--- iOS 플랫폼 연결 시도... ---")

            # 2. Android 실패 시 iOS 드라이버 설정 시도
            try:
                self.config = IOSConfig
                options = XCUITestOptions()
                options.platform_name = self.config.PLATFORM_NAME
                options.platform_version = self.config.PLATFORM_VERSION
                options.device_name = self.config.DEVICE_NAME
                options.bundle_id = self.config.BUNDLE_ID
                options.automation_name = self.config.AUTOMATION_NAME
                options.no_reset = AppiumConfig.NO_RESET
                options.new_command_timeout = AppiumConfig.NEW_COMMAND_TIMEOUT

                self.driver = webdriver.Remote(AppiumConfig.APPIUM_SERVER_URL, options=options)
                self.platform = 'ios'
                print("✅ iOS 드라이버 초기화 성공 및 앱 실행.")

            except WebDriverException as ios_error:
                print(f"❌ iOS 연결 실패: {ios_error}")
                raise Exception("Android와 iOS 플랫폼 모두에 연결할 수 없습니다. Appium 서버와 디바이스 연결 상태를 확인해주세요.")

        # 공통 설정
        self.driver.implicitly_wait(AppiumConfig.IMPLICIT_WAIT_TIME)
        self.wait = WebDriverWait(self.driver, AppiumConfig.EXPLICIT_WAIT_TIME)
        print(f"--- 최종 연결된 플랫폼: {self.platform.upper()} ---")
        return self.driver

    def teardown_driver(self):
        """Appium 드라이버 세션을 종료합니다."""
        if self.driver:
            print("드라이버를 종료합니다.")
            self.driver.quit()
            self.driver = None
            self.wait = None
            print("드라이버 종료 완료.")