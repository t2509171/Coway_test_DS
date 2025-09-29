# PythonProject/Login/test_Login_failed.py

import sys
import os
import time

# 필요한 라이브러리 임포트
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy # AppiumBy
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Ensure the project root is in the path to import Base and Login modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from Login.test_login_view import AppiumLoginviewTest

def login_failed(flow_tester):
    """
    유효하지 않은 자격 증명으로 로그인 실패 시나리오를 실행합니다.
    """
    print("\n--- 유효하지 않은 자격 증명으로 로그인 실패 시나리오 시작 ---")

    # Read invalid credentials
    invalid_credentials_path = os.path.join(os.path.dirname(__file__), 'invalid_credentials.txt')
    try:
        with open(invalid_credentials_path, 'r', encoding='utf-8') as f:
            # 파일의 첫 번째 줄만 읽어와서 쉼표로 분리하고, 첫 두 값을 할당합니다.
            line = f.readline().strip()
            credentials = line.split(',')
            username = credentials[0]
            password = credentials[1]
    except FileNotFoundError:
        print(f"Error: {invalid_credentials_path} not found.")
        return False, "Invalid credentials file not found."
    except ValueError:
        print(f"Error: Invalid format in {invalid_credentials_path}. Expected 'username,password'.")
        return False, "Invalid invalid credentials format."

    failed_login_result = False
    ui_elements_ok = False

    try:
        print("앱이 성공적으로 실행되었습니다.")

        # 로그인 작업 수행
        print(f"유효하지 않은 계정으로 로그인 시도: ID='{username}', PW='{password}'")
        # 예상: 로그인 실패 (메인 페이지로 이동하지 않음)
        try:
            # 아이디 입력 필드 찾기 및 텍스트 입력
            id_field = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="id"]')))
            id_field.clear()
            id_field.send_keys(username)
            print(f"아이디 '{username}' 입력 완료.")

            # 비밀번호 입력 필드 찾기 및 텍스트 입력
            pwd_field = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="pwd"]')))
            pwd_field.clear()
            pwd_field.send_keys(password)
            print("비밀번호 입력 완료.")

            # 자동 로그인 영역 찾기
            try:
                auto_login_checkbox_locator = (AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="autoLogin"]')
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
                    # 현재 체크되어 있으면 해제
                    print("자동 로그인 체크박스가 현재 체크되어 있습니다. 해제합니다.")
                    auto_login_checkbox.click()  # 클릭하여 해제
                    print("자동 로그인 체크박스 해제 시도 완료.")
                    # 명시적 대기: 'checked' 속성이 'false'가 될 때까지 기다립니다.
                    target_checked_state = "false"
                    print("자동 로그인 체크박스 해제 완료.")
                else:  # is_checked == "false"
                    # 현재 해제되어 있으면 체크
                    print("자동 로그인 체크박스가 현재 해제되어 있습니다. 체크합니다.")
                    auto_login_checkbox.click()  # 클릭하여 체크
                    print("자동 로그인 체크박스 체크 시도 완료.")
                    # 명시적 대기: 'checked' 속성이 'true'가 될 때까지 기다립니다.
                    target_checked_state = "true"
                    print("자동 로그인 체크박스 체크 완료.")

                print(f"자동 로그인 체크박스 토글 시도 완료. 목표 상태: {target_checked_state}")
                time.sleep(3)

            except Exception as e:
                print(f"자동 로그인 체크박스 처리 중 오류 발생: {e}")
                flow_tester.driver.save_screenshot("auto_login_checkbox_error.png")
                raise  # 오류 발생 시 상위로 예외를 다시 발생시켜 로그인 프로세스 중단

            # 로그인 버튼 찾기 및 클릭
            login_button = flow_tester.wait.until(
                EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="로그인"]')))
            login_button.click()
            print("로그인 버튼 클릭.")
            time.sleep(3)  # 로그인 처리 시간을 위해 잠시 대기

            # 로그인 실패 확인 (예상 오류 메시지 또는 메인 페이지로 이동하지 않음)
            print("로그인 실패. 오류 메시지 확인 중...")
            error_message_xpath = '//android.widget.TextView[@text="업무포탈 통합계정 정보를 확인해 주세요."]'  # 실제 오류 메시지 XPath로 변경
            try:
                # 예상 오류 메시지가 나타날 때까지 명시적으로 대기
                error_message_element = flow_tester.wait.until(
                    EC.presence_of_element_located((AppiumBy.XPATH, error_message_xpath)),
                    message="예상 오류 메시지가 타임아웃 내에 나타나지 않았습니다."
                )
                if error_message_element:
                    print("✅ 유효하지 않은 자격 증명으로 로그인 실패 테스트 완료: 예상된 오류 메시지 확인.")
                    failed_login_result = True
                else:  # 이 경우는 발생하기 어려움 (TimeoutException으로 빠짐)
                    failed_login_result = False
            except TimeoutException:  # 오류 메시지가 나타나지 않고 타임아웃 된 경우 (즉, 로그인 성공으로 간주)
                print("❌ 오류 메시지 확인 타임아웃: 로그인 실패 메시지를 찾을 수 없습니다. 예상치 못하게 로그인 성공했거나 다른 오류 발생.")
                # 추가 확인: 예상치 못하게 메인 페이지로 이동했는지 확인 (실패 시나리오에서 성공한 경우)
                try:
                    main_page_element_locator_on_fail = (AppiumBy.XPATH, '//android.webkit.WebView[@content-desc="메인"]')
                    flow_tester.wait.until(EC.presence_of_element_located(main_page_element_locator_on_fail))
                    print("❌ 예상치 못하게 메인 페이지로 이동했습니다. 로그인 실패 테스트 실패 처리.")
                    failed_login_result = False
                except TimeoutException:
                    print("메인 페이지로도 이동하지 않았습니다. 예상치 못한 오류 또는 앱의 정지 상태.")
                    failed_login_result = False
                except Exception as ex:
                    print(f"로그인 실패 확인 중 추가 예외 발생: {ex}")
                    failed_login_result = False
            except NoSuchElementException:
                print("❌ 오류 메시지 요소를 DOM에서 찾지 못했습니다: 로그인 실패 테스트 실패.")
                failed_login_result = False
            except Exception as ex:
                print(f"오류 메시지 확인 중 예상치 못한 오류 발생: {ex}")
                failed_login_result = False
        except TimeoutException as e:
            print(f"로그인 입력/클릭 과정 중 타임아웃 발생: {e}")
            failed_login_result = False
        except NoSuchElementException as e:
            print(f"로그인 입력/클릭 과정 중 요소를 찾지 못했습니다: {e}")
            failed_login_result = False
        except Exception as e:
            print(f"로그인 과정 중 예상치 못한 오류 발생: {e}")
            failed_login_result = False
        if failed_login_result:  # 로그인 실패 시나리오에서 오류 메시지를 찾아 통과한 경우
            return True, "Failed login test passed: Expected error message found."
        else:
            return False, "Failed login test failed: Did not find expected error message or logged in unexpectedly."
    except Exception as e:
        print(f"🚨 유효하지 않은 자격 증명 로그인 시나리오 실행 중 오류 발생: {e}")
        # 특정 예외를 잡아서 실패로 처리 (예: NoSuchElementException for main page)
        return False, f"Error during failed login test: {e}"
    finally:
        # 드라이버 종료
        #loginview_tester.teardown_driver()
        print("--- 유효하지 않은 자격 증명으로 로그인 실패 시나리오 종료 ---\n")