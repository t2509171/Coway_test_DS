# PythonProject/Config/config.py

class AndroidConfig:
    APPIUM_SERVER_URL = 'http://127.0.0.1:4723'
    PLATFORM_NAME = 'Android'
    PLATFORM_VERSION = '15'
    #DEVICE_NAME = ('10.131.62.168:44603')
    DEVICE_NAME = ('R3CT70V2T5H')
    APP_PACKAGE = 'com.coway.catalog.seller.stg'
    APP_ACTIVITY = 'kr.coway.catalog.activity.webMain.WebMainActivity'
    AUTOMATION_NAME = 'UiAutomator2'
    NO_RESET = True
    NEW_COMMAND_TIMEOUT = 120
    IMPLICIT_WAIT_TIME = 5
    EXPLICIT_WAIT_TIME = 20

class IOSConfig:
    """iOS 테스트 환경 설정"""
    PLATFORM_NAME = 'iOS'
    PLATFORM_VERSION = '16.0'  # 실제 iOS 버전
    DEVICE_NAME = 'iPhone 14 Pro'  # 실제 iOS 기기/시뮬레이터 이름
    BUNDLE_ID = 'com.coway.ios.app.bundle.id'  # iOS 앱의 Bundle ID
    AUTOMATION_NAME = 'XCUITest'
    # ... 기타 iOS 설정 ...

class AppiumConfig:
    APPIUM_SERVER_URL = 'http://127.0.0.1:4723'
    NO_RESET = True
    NEW_COMMAND_TIMEOUT = 60
    IMPLICIT_WAIT_TIME = 5
    EXPLICIT_WAIT_TIME = 20