# PythonProject/Login/run_successful_login_test.py

import sys
import os
import time

# Ensure the project root is in the path to import Base and Login modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy # AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Xpath 저장소에서 LoginLocators 임포트
from Xpath.xpath_repository import LoginLocators

def login_successful(flow_tester):

    print("\n--- 유효한 자격 증명으로 로그인 성공 시나리오 시작 ---")
    scenario_passed = False
    result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."

    try:
        if flow_tester.platform == 'android':  # 'AOS' -> 'android'
            locators = LoginLocators.AOS
        elif flow_tester.platform == 'ios':  # 'IOS' -> 'ios'
            locators = LoginLocators.IOS
        else:
            raise ValueError(f"지원하지 않는 플랫폼입니다: {flow_tester.platform}")
    except AttributeError:
        print("경고: flow_tester에 'platform' 속성이 없습니다. Android로 기본 설정합니다.")  # AOS -> Android
        locators = LoginLocators.AOS

    # --- [수정 완료] ---
    # Read valid credentials
    valid_credentials_path = os.path.join(os.path.dirname(__file__), 'valid_credentials.txt')
    try:
        with open(valid_credentials_path, 'r', encoding='utf-8') as f:
            # 파일의 첫 번째 줄만 읽어와서 쉼표로 분리하고, 첫 두 값을 할당합니다.
            line = f.readline().strip()
            credentials = line.split(',')
            username = credentials[0]
            password = credentials[1]
    except FileNotFoundError:
        print(f"Error: {valid_credentials_path} not found.")
        return False, "Valid credentials file not found."
    except ValueError:
        print(f"Error: Invalid format in {valid_credentials_path}. Expected 'username,password'.")
        return False, "Invalid valid credentials format."

    try:
        print("앱이 성공적으로 실행되었습니다.")

        # 로그인 여부 확인: 메인 페이지 요소가 이미 존재하는지 확인
        main_page_element_locator = (AppiumBy.XPATH, locators.main_page_element_locator) # 수정됨
        try:
            # 일정 시간 동안 기다려 요소가 로드되는지 확인
            flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator))
            print("✅ 메인 페이지 요소가 이미 존재합니다. 로그인 상태로 판단하고 로그인 과정을 스킵")
            return True, "Already logged in, skipped login process."
        except TimeoutException:
            print("로그인 상태가 아닙니다. 로그인 과정을 진행합니다.")
            # 요소를 찾지 못하면 로그인 페이지에 있다고 가정하고 계속 진행

        # 로그인 작업 수행
        print(f"유효한 계정으로 로그인 시도: ID='{username}', PW='{password}'")
        try:
            # 아이디 입력 필드 찾기 및 텍스트 입력
            id_field = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, locators.id_field))) # 수정됨
            id_field.clear()
            id_field.send_keys(username)
            print(f"아이디 '{username}' 입력 완료.")

            # 비밀번호 입력 필드 찾기 및 텍스트 입력
            pwd_field = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, locators.pwd_field))) # 수정됨
            pwd_field.clear()
            pwd_field.send_keys(password)
            print(f"비밀번호 '{password}' 입력 완료.")

            # 자동 로그인 영역 찾기
            try:
                auto_login_checkbox_locator = (AppiumBy.XPATH, locators.auto_login_checkbox_locator) # 수정됨
                # 자동 로그인 체크박스 요소를 찾습니다. (클릭 가능할 때까지 대기)
                print(f"자동 로그인 체크박스 {auto_login_checkbox_locator}를 기다리는 중...")
                auto_login_checkbox = flow_tester.wait.until(
                    EC.element_to_be_clickable(auto_login_checkbox_locator),
                    message=f"자동 로그인 체크박스 {auto_login_checkbox_locator}를 20초 내에 찾지 못했습니다."
                )
                time.sleep(2)
                print("자동 로그인 체크박스를 성공적으로 찾았습니다.")

                # 체크박스의 'checked' 속성을 확인하여 현재 상태를 파악합니다.
                is_checked = auto_login_checkbox.get_attribute("checked")
                if is_checked == "true":
                    # 현재 해제되어 있으면 체크
                    print("자동 로그인 체크박스가 현재 체크되어 있습니다. 해제합니다.")
                    auto_login_checkbox.click()  # 클릭하여 체크
                    print("자동 로그인 체크박스 해제 시도 완료.")
                    time.sleep(3)
                else:
                    # 현재 체크되어 있으면 아무것도 하지 않음
                    print("자동 로그인 체크박스가 현재 해제되어 있습니다. 변경하지 않습니다.")
                    time.sleep(3)

                print(f"자동 로그인 체크박스 처리 완료. 현재 상태: {auto_login_checkbox.get_attribute('checked')}")

            except Exception as e:
                    print(f"자동 로그인 체크박스 처리 중 오류 발생: {e}")
                    flow_tester.driver.save_screenshot("auto_login_checkbox_error.png")
                    raise  # 오류 발생 시 상위로 예외를 다시 발생시켜 로그인 프로세스 중단

            # 로그인 버튼 찾기 및 클릭
            login_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, locators.login_button))) # 수정됨
            login_button.click()
            print("로그인 버튼 클릭.")
            time.sleep(5)  # 로그인 처리 시간을 위해 잠시 대기 (네트워크 환경에 따라 조절 필요)

            # 로그인 성공 여부 확인 (예: 메인 페이지의 특정 요소 확인)
            try:
                # 로그인 성공 시 나타날 것으로 예상되는 요소의 XPath 또는 ID
                main_page_element_locator = (AppiumBy.XPATH, locators.main_page_element_locator) # 수정됨
                flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator))
                print("메인 페이지 요소 확인: 로그인 성공.")
                successful_login_result = True
                time.sleep(3)
            except TimeoutException:
                print("❌ 메인 페이지 요소 확인 타임아웃: 로그인 성공 후 예상되는 메인 페이지 요소를 찾을 수 없습니다.")
                flow_tester.driver.save_screenshot("main_page_element_not_found_timeout.png")
                successful_login_result = False
            except NoSuchElementException:
                print("❌ 메인 페이지 요소 확인 실패: 예상되는 메인 페이지 요소를 찾을 수 없습니다. XPath 확인 필요.")
                flow_tester.driver.save_screenshot("main_page_element_not_found_no_such_element.png")
                successful_login_result = False
            except Exception as ex:
                print(f"메인 페이지 요소 확인 중 예상치 못한 오류 발생: {ex}")
                successful_login_result = False
        except Exception as e:
            print(f"로그인 과정 중 예상치 못한 오류 발생: {e}")
            successful_login_result = False

        if successful_login_result:
            print("✅ 유효한 자격 증명으로 로그인 성공 테스트 완료.")
            return True, "Successful login test passed."
        else:
            print("❌ 유효한 자격 증명으로 로그인 실패 (예상치 못한 결과).")
            return False, "Successful login test failed unexpectedly."

    except Exception as e:
        print(f"🚨 유효한 자격 증명 로그인 시나리오 실행 중 오류 발생: {e}")
        return False, f"Error during successful login test: {e}"

    finally:
        print("--- 로그인 화면 UI 요소 노출 확인 시나리오 종료 ---\n")
    # 마지막 줄 수정: scenario_passed와 result_message를 반환하도록 함
    return scenario_passed, result_message
# # PythonProject/Login/run_successful_login_test.py
#
# import sys
# import os
# import time
#
# # Ensure the project root is in the path to import Base and Login modules
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# # 필요한 라이브러리 임포트
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.appiumby import AppiumBy # AppiumBy
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
#
# def login_successful(flow_tester):
#
#     print("\n--- 유효한 자격 증명으로 로그인 성공 시나리오 시작 ---")
#     scenario_passed = False
#     result_message = "알 수 없는 이유로 시나리오가 완료되지 않았습니다."
#
#     # Read valid credentials
#     valid_credentials_path = os.path.join(os.path.dirname(__file__), 'valid_credentials.txt')
#     try:
#         with open(valid_credentials_path, 'r', encoding='utf-8') as f:
#             # 파일의 첫 번째 줄만 읽어와서 쉼표로 분리하고, 첫 두 값을 할당합니다.
#             line = f.readline().strip()
#             credentials = line.split(',')
#             username = credentials[0]
#             password = credentials[1]
#     except FileNotFoundError:
#         print(f"Error: {valid_credentials_path} not found.")
#         return False, "Valid credentials file not found."
#     except ValueError:
#         print(f"Error: Invalid format in {valid_credentials_path}. Expected 'username,password'.")
#         return False, "Invalid valid credentials format."
#
#     try:
#         print("앱이 성공적으로 실행되었습니다.")
#
#         # 로그인 여부 확인: 메인 페이지 요소가 이미 존재하는지 확인
#         # 이 예시에서는 'android.webkit.WebView[@content-desc="메인"]' 이라고 가정합니다.
#         # 실제 앱의 메인 화면에 있는 고유한 요소를 Appium Inspector로 확인 후 정확히 변경해주세요.
#         main_page_element_locator = (AppiumBy.XPATH,
#                                      '//android.widget.TextView[@text="디지털세일즈"]')
#         try:
#             # 일정 시간 동안 기다려 요소가 로드되는지 확인
#             flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator))
#             print("✅ 메인 페이지 요소가 이미 존재합니다. 로그인 상태로 판단하고 로그인 과정을 스킵")
#             return True, "Already logged in, skipped login process."
#         except TimeoutException:
#             print("로그인 상태가 아닙니다. 로그인 과정을 진행합니다.")
#             # 요소를 찾지 못하면 로그인 페이지에 있다고 가정하고 계속 진행
#
#         # 로그인 작업 수행
#         print(f"유효한 계정으로 로그인 시도: ID='{username}', PW='{password}'")
#         try:
#             # 아이디 입력 필드 찾기 및 텍스트 입력
#             id_field = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="id"]')))
#             id_field.clear()
#             id_field.send_keys(username)
#             print(f"아이디 '{username}' 입력 완료.")
#
#             # 비밀번호 입력 필드 찾기 및 텍스트 입력
#             pwd_field = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="pwd"]')))
#             pwd_field.clear()
#             pwd_field.send_keys(password)
#             print(f"비밀번호 '{password}' 입력 완료.")
#
#             # 자동 로그인 영역 찾기
#             try:
#                 auto_login_checkbox_locator = (AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="autoLogin"]')
#                 # 자동 로그인 체크박스 요소를 찾습니다. (클릭 가능할 때까지 대기)
#                 print(f"자동 로그인 체크박스 {auto_login_checkbox_locator}를 기다리는 중...")
#                 auto_login_checkbox = flow_tester.wait.until(
#                     EC.element_to_be_clickable(auto_login_checkbox_locator),
#                     message=f"자동 로그인 체크박스 {auto_login_checkbox_locator}를 20초 내에 찾지 못했습니다."
#                 )
#                 time.sleep(2)
#                 print("자동 로그인 체크박스를 성공적으로 찾았습니다.")
#
#                 # 체크박스의 'checked' 속성을 확인하여 현재 상태를 파악합니다.
#                 is_checked = auto_login_checkbox.get_attribute("checked")
#                 if is_checked == "true":
#                     # 현재 해제되어 있으면 체크
#                     print("자동 로그인 체크박스가 현재 체크되어 있습니다. 해제합니다.")
#                     auto_login_checkbox.click()  # 클릭하여 체크
#                     print("자동 로그인 체크박스 해제 시도 완료.")
#                     time.sleep(3)
#                 else:
#                     # 현재 체크되어 있으면 아무것도 하지 않음
#                     print("자동 로그인 체크박스가 현재 해제되어 있습니다. 변경하지 않습니다.")
#                     time.sleep(3)
#
#                 print(f"자동 로그인 체크박스 처리 완료. 현재 상태: {auto_login_checkbox.get_attribute('checked')}")
#
#             except Exception as e:
#                     print(f"자동 로그인 체크박스 처리 중 오류 발생: {e}")
#                     flow_tester.driver.save_screenshot("auto_login_checkbox_error.png")
#                     raise  # 오류 발생 시 상위로 예외를 다시 발생시켜 로그인 프로세스 중단
#
#             # 로그인 버튼 찾기 및 클릭
#             login_button = flow_tester.wait.until(
#                 EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="로그인"]')))
#             login_button.click()
#             print("로그인 버튼 클릭.")
#             time.sleep(5)  # 로그인 처리 시간을 위해 잠시 대기 (네트워크 환경에 따라 조절 필요)
#
#             # 로그인 성공 여부 확인 (예: 메인 페이지의 특정 요소 확인)
#             # 이 부분은 실제 앱의 메인 페이지에 있는 고유한 요소를 찾아야 합니다.
#             # 예시: 메인 페이지에 '메인 화면 타이틀' 또는 특정 아이콘이 나타나는 경우
#             try:
#                 # 로그인 성공 시 나타날 것으로 예상되는 요소의 XPath 또는 ID
#                 # 이 예시에서는 'android.webkit.WebView[@content-desc="메인"]' 이라고 가정합니다.
#                 # 실제 앱의 메인 화면에 있는 고유한 요소를 Appium Inspector로 확인 후 정확히 변경해주세요.
#                 main_page_element_locator = (AppiumBy.XPATH,
#                                              '//android.widget.TextView[@text="디지털세일즈"]')  # 실제 메인 페이지의 요소로 변경 필수
#                 flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator))
#                 print("메인 페이지 요소 확인: 로그인 성공.")
#                 successful_login_result = True
#                 time.sleep(3)
#             except TimeoutException:
#                 print("❌ 메인 페이지 요소 확인 타임아웃: 로그인 성공 후 예상되는 메인 페이지 요소를 찾을 수 없습니다.")
#                 flow_tester.driver.save_screenshot("main_page_element_not_found_timeout.png")
#                 successful_login_result = False
#             except NoSuchElementException:
#                 print("❌ 메인 페이지 요소 확인 실패: 예상되는 메인 페이지 요소를 찾을 수 없습니다. XPath 확인 필요.")
#                 flow_tester.driver.save_screenshot("main_page_element_not_found_no_such_element.png")
#                 successful_login_result = False
#             except Exception as ex:
#                 print(f"메인 페이지 요소 확인 중 예상치 못한 오류 발생: {ex}")
#                 successful_login_result = False
#         except Exception as e:
#             print(f"로그인 과정 중 예상치 못한 오류 발생: {e}")
#             successful_login_result = False
#
#         if successful_login_result:
#             print("✅ 유효한 자격 증명으로 로그인 성공 테스트 완료.")
#             return True, "Successful login test passed."
#         else:
#             print("❌ 유효한 자격 증명으로 로그인 실패 (예상치 못한 결과).")
#             return False, "Successful login test failed unexpectedly."
#
#     except Exception as e:
#         print(f"🚨 유효한 자격 증명 로그인 시나리오 실행 중 오류 발생: {e}")
#         return False, f"Error during successful login test: {e}"
#
#     finally:
#         print("--- 로그인 화면 UI 요소 노출 확인 시나리오 종료 ---\n")
#     return scenario_passed, result_message