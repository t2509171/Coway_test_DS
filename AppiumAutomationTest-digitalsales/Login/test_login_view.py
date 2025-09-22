# PythonProject/Login/test_login.py

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.options.android import UiAutomator2Options
import unittest
import time

# 새로 생성된 base_driver 모듈에서 BaseAppiumDriver 클래스를 임포트합니다.
from Base.base_driver import BaseAppiumDriver

class AppiumLoginviewTest(BaseAppiumDriver):
    """
    def __init__(self, platform_version='13', device_name='10.131.62.168:38915',
                 app_package='com.coway.catalog.seller.stg',
                 app_activity='kr.coway.catalog.activity.webMain.WebMainActivity',
                 appium_server_url='http://127.0.0.1:4723/wd/hub'):
        # 부모 클래스(BaseAppiumDriver)의 생성자를 호출하여 기본 드라이버 설정을 초기화합니다.
        super().__init__(platform_version, device_name, app_package, app_activity, appium_server_url)
        self._login_ui_elements_ok = False  # 로그인 UI 요소 확인 결과 저장
        self.element_verification_results = {}  # 개별 UI 요소 확인 결과 저장
    """
    def __init__(self):
        # 부모 클래스(BaseAppiumDriver)의 생성자를 platform 인자와 함께 호출합니다.
        super().__init__()
        self._login_ui_elements_ok = False
        self.element_verification_results = {}

    # setup_driver와 teardown_driver 메소드는 이제 BaseAppiumDriver에서 상속받아 사용합니다.
    # 따라서 이 클래스에서는 별도로 정의할 필요가 없습니다. (오버라이드할 경우에만 재정의)
    """
    def setup_driver(self):
        print("Appium 드라이버를 초기화합니다...")
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': self.platform_version,
            'deviceName': self.device_name,
            'appPackage': self.app_package,
            'appActivity': self.app_activity,
            'automationName': 'UiAutomator2',
            'noReset': True,
            'newCommandTimeout': 20
        }

        options = UiAutomator2Options()
        options.load_capabilities(desired_caps)

        try:
            self.driver = webdriver.Remote(self.appium_server_url, options=options)
            self.driver.implicitly_wait(5)  # 요소를 찾을 때 최대 10초까지 기다립니다.
            self.wait = WebDriverWait(self.driver, 20) # 명시적 대기를 위한 WebDriverWait 객체 생성 (기본 20초)
            print("Appium 드라이버 초기화 성공 및 앱 실행.")
            return self.driver
        except Exception as e:
            print(f"Appium 드라이버 초기화 실패: {e}")
            raise
    """

    def verify_login_ui_elements(self):
        """로그인 화면의 모든 UI 요소가 정상적으로 노출되는지 확인합니다."""
        # ... (기존 verify_login_ui_elements 메소드 내용은 그대로 유지) ...
        print("\n--- 로그인 화면 UI 요소 확인 시작 ---")
        ui_elements = [
            ("타이틀", '//android.widget.TextView[@text="디지털 세일즈"]'),
            ("안내 문구1", '//android.widget.TextView[@text="판매인 분들은 아이디에 업무등록번호를 입력 부탁드립니다."]'),
            ("안내 문구2", '//android.widget.TextView[@text="비밀번호는 런웨이의 로그인 정보와 동일합니다."]'),
            ("아이디 타이틀", '//android.widget.TextView[@text="아이디"]'),
            ("아이디 입력", '//android.widget.EditText[@resource-id="id"]'),
            ("패스워드 타이틀", '//android.widget.TextView[@text="비밀번호"]'),
            ("패스워드 입력", '//android.widget.EditText[@resource-id="pwd"]'),
            ("자동 로그인 체크박스", '//android.widget.CheckBox[@resource-id="autoLogin"]'),
            ("로그인 버튼", '//android.widget.Button[@text="로그인"]'),
            ("비밀번호 변경 버튼", '//android.widget.Button[@text="비밀번호 변경"]'),
            ("비밀번호 초기화 버튼", '//android.widget.Button[@text="비밀번호 초기화"]')
        ]

        self._login_ui_elements_ok = True
        self.element_verification_results = {}

        all_elements_present = True
        for name, xpath in ui_elements:
            try:
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
                print(f"✅ '{name}' 요소가 성공적으로 노출되었습니다.")
                self.element_verification_results[name] = True
            except Exception as e:
                print(f"❌ '{name}' 요소 노출 확인 실패: {e}")
                self.element_verification_results[name] = False
                self._login_ui_elements_ok = False

        if self._login_ui_elements_ok:
            print("--- 모든 로그인 화면 UI 요소가 정상적으로 노출되었습니다. ---")
        else:
            print("--- 일부 로그인 화면 UI 요소 노출에 문제가 있습니다. ---")
        print("--- 로그인 화면 UI 요소 확인 종료 ---\n")
        return self._login_ui_elements_ok
    """
    def verify_login_ui_elements(self):
        print("\n--- 로그인 화면 UI 요소 확인 시작 ---")
        ui_elements = [
            ("타이틀", '//android.widget.TextView[@text="디지털 세일즈"]'),
            ("안내 문구1", '//android.widget.TextView[@text="판매인 분들은 아이디에 업무등록번호를 입력 부탁드립니다."]'),
            ("안내 문구2", '//android.widget.TextView[@text="비밀번호는 런웨이의 로그인 정보와 동일합니다."]'),
            ("아이디 타이틀", '//android.widget.TextView[@text="아이디"]'),
            ("아이디 입력", '//android.widget.EditText[@resource-id="id"]'),
            ("패스워드 타이틀", '//android.widget.TextView[@text="비밀번호"]'),
            ("패스워드 입력", '//android.widget.EditText[@resource-id="pwd"]'),
            ("자동 로그인 체크박스", '//android.widget.CheckBox[@resource-id="autoLogin"]'),
            ("로그인 버튼", '//android.widget.Button[@text="로그인"]'),
            ("비밀번호 변경 버튼", '//android.widget.Button[@text="비밀번호 변경"]'),
            ("비밀번호 초기화 버튼", '//android.widget.Button[@text="비밀번호 초기화"]')
        ]

        self._login_ui_elements_ok = True  # Initialize overall status to True
        self.element_verification_results = {}  # Reset for each verification run

        all_elements_present = True
        for name, xpath in ui_elements:
            try:
                self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
                print(f"✅ '{name}' 요소가 성공적으로 노출되었습니다.")
                self.element_verification_results[name] = True
            except Exception as e:
                print(f"❌ '{name}' 요소 노출 확인 실패: {e}")
                self.element_verification_results[name] = False
                self._login_ui_elements_ok = False  # Set overall status to False if any element fails

        if self._login_ui_elements_ok:
            print("--- 모든 로그인 화면 UI 요소가 정상적으로 노출되었습니다. ---")
        else:
            print("--- 일부 로그인 화면 UI 요소 노출에 문제가 있습니다. ---")
        print("--- 로그인 화면 UI 요소 확인 종료 ---\n")
        return self._login_ui_elements_ok
    """
    """
    def teardown_driver(self):
            if self.driver:
                print("드라이버를 종료합니다.")
                self.driver.quit()
                self.driver = None  # 드라이버 객체를 None으로 설정하여 재사용 방지
                print("드라이버 종료 완료.")
            pass
    """