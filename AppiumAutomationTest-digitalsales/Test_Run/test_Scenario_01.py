# PythonProject/Appuim_Test.py
import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

# AppiumLoginTest 클래스를 임포트합니다.
from Login.test_Login_passed import login_successful

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet




# sheets_service와 tester_name 인자를 추가
def test_login(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   Appium 로그인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 로그인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    try:
        """
        #[Seller app checklist-6] 로그인 화면 UI 요소 확인 테스트 실행
        print("\n--- Seller app checklist-6 : 로그인 화면 UI 요소 확인 ---")
        login_view_test_passed = False
        login_view_message = ""
        login_view_tester = None
        try:
            login_view_tester = AppiumLoginviewTest()
            login_view_tester.setup_driver()  # 드라이버 설정
            login_view_test_passed = login_view_tester.verify_login_ui_elements(flow_tester)  # UI 요소 확인
            if login_view_test_passed:
                login_view_message = "모든 로그인 화면 UI 요소가 정상적으로 노출되었습니다."
            else:
                login_view_message = "일부 로그인 화면 UI 요소 노출에 문제가 있습니다. 상세 로그 확인 필요."
        except Exception as e:
            login_view_message = f"로그인 화면 UI 요소 확인 중 예외 발생: {e}"
            login_view_test_passed = False
        finally:
            if login_view_tester:
                login_view_tester.teardown_driver()  # 드라이버 종료

        overall_results["로그인 화면 UI 요소 확인"] = {
            "test_no": "Seller app checklist-6",
            "passed": login_view_test_passed,
            "message": login_view_message
        }
        print("테스트 케이스 0 완료.")
        print("-" * 50)  # Separator
        
        # [Seller app checklist-8] 유효하지 않은 자격 증명으로 로그인 실패 테스트 실행
        print("\n--- Seller app checklist-8 : 유효하지 않은 자격 증명으로 로그인 실패 ---")
        failure_test_passed, failure_test_message = run_failed_login_scenario(flow_tester)
        overall_results["잘못된 계정 및 비밀번호 입력시 로그인이 실패한다."] = {
            "test_no": "Seller app checklist-8",
            "passed": failure_test_passed,
            "message": failure_test_message
        }
        # 스프레드시트에 테스트 결과 기록
        status = "PASS" if failure_test_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-8", status, tester_name)
        print("Seller app checklist-8 테스트 케이스 완료.")
        print("-" * 50)  # Separator

        # --- 비밀번호 변경 후 뒤로가기 테스트 실행 ---
        print("\n--- Seller app checklist-11: 비밀번호 변경 후 뒤로가기 ---")
        password_change_back_passed, password_change_back_message = run_password_change_button_back_scenario(flow_tester)
        overall_results["[비밀번호 변경] 버튼 터치 시, 비밀번호 변경 페이지로 이동된다."] = {
            "test_no": "Seller app checklist-11",
            "passed": password_change_back_passed,
            "message": password_change_back_message
        }
        # 스프레드시트에 테스트 결과 기록
        status = "PASS" if password_change_back_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-11", status, tester_name)
        print("Seller app checklist-11 테스트 케이스 완료.")
        print("-" * 50)  # Separator

        # --- 비밀번호 초기화 후 뒤로가기 테스트 실행 ---
        print("\n--- Seller app checklist-10 : 비밀번호 초기화 후 뒤로가기 ---")
        password_reset_back_passed, password_reset_back_message = run_password_reset_button_back_scenario(flow_tester)
        overall_results["[비밀번호 초기화] 버튼 터치 시, 비밀번호 초기화 페이지로 이동된다."] = {
            "test_no": "Seller app checklist-10",
            "passed": password_reset_back_passed,
            "message": password_reset_back_message
        }
        # 스프레드시트에 테스트 결과 기록
        status = "PASS" if password_reset_back_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-10", status, tester_name)
        print("Seller app checklist-10 테스트 케이스 완료.")
        print("-" * 50)  # Separator
        """
        # [Seller app checklist-7/9] --- 유효한 자격 증명으로 로그인 성공 테스트 실행 ---
        print("\n--- Seller app checklist-7/9 : 유효한 자격 증명으로 로그인 성공 ---")
        success_test_passed, success_test_message = login_successful(flow_tester)
        overall_results["정상적으로 로그인 진행시 메인페이지가 노출된다."] = {
            "test_no": "Seller app checklist-7/Seller app checklist-9",
            "passed": success_test_passed,
            "message": success_test_message
        }
        # 스프레드시트에 테스트 결과 기록 (7)
        status = "PASS" if success_test_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-7", status, tester_name)
        print("Seller app checklist-7 테스트 케이스 완료.")
        print("-" * 50)  # Separator

        # 스프레드시트에 테스트 결과 기록 (9)
        status = "PASS" if success_test_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-9", status, tester_name)
        print("Seller app checklist-9 테스트 케이스 완료.")
        print("-" * 50)  # Separator
        """
        #[Seller app checklist-12/13] --- 홈 > 검색 / 공지사항 테스트 실행 ---
        print("\n--- Seller app checklist-12/13 : 홈 화면 내비게이션 (검색 아이콘, 공지사항) ---")
        home_navigation_passed, home_navigation_message = run_home_navigation_scenario(flow_tester)
        overall_results["검색 화면으로 이동한다/등록/수정 날짜 내림차순으로 최대 3개의 공지를 표시한다"] = {
            "test_no": "Seller app checklist-12/Seller app checklist-13",  # You can assign a specific checklist number
            "passed": home_navigation_passed,
            "message": home_navigation_message
        }
        # 스프레드시트에 테스트 결과 기록 (12)
        status = "PASS" if home_navigation_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-12", status, tester_name)
        print("Seller app checklist-12 테스트 케이스 완료.")
        print("-" * 50)  # Separator

        # 스프레드시트에 테스트 결과 기록 (13)
        status = "PASS" if home_navigation_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-13", status, tester_name)
        print("Seller app checklist-13 테스트 케이스 완료.")
        print("-" * 50)  # Separator

        #[Seller app checklist-16] --- 홈 > 배너 스와이프, 클릭
        print("\n--- Seller app checklist-16: 배너 스와이프, 클릭 ---")
        home_navigation_passed, home_navigation_message = perform_home_banner_swipe(flow_tester)
        overall_results["좌우로 스와이프가 가능하며, 터치 시 해당 제품의 상세 정보 페이지로 이동한다."] = {
            "test_no": "Seller app checklist-16",  # You can assign a specific checklist number
            "passed": home_navigation_passed,
            "message": home_navigation_message
        }
        # 스프레드시트에 테스트 결과 기록
        status = "PASS" if home_navigation_passed else "FAIL"
        update_test_result_in_sheet(sheets_service, "Seller app checklist-16", status, tester_name)
        print("Seller app checklist-16 테스트 케이스 완료.")
        print("-" * 50)  # Separator
        """
    except Exception as e:
        print(f"🚨 전체 테스트 스위트 실행 중 치명적인 오류 발생: {e}")
        overall_results["전체 스위트 초기화 오류"] = {
            "test_no": "N/A",
            "passed": False,
            "message": f"초기 드라이버 설정 또는 테스트 실행 중 오류 발생: {e}"
        }

    finally:
        # --- 최종 테스트 결과 종합 ---
        print("\n=========================================")
        print("   Appium 로그인 테스트 최종 종합 결과")
        print("=========================================")

        all_passed = True
        for test_name, result in overall_results.items():
            status = "✅ 성공" if result["passed"] else "❌ 실패"
            print(f"테스트 번호: {result['test_no']}")
            print(f"테스트명: {test_name}")
            print(f"결과: {status}")
            print(f"메시지: {result["message"]}")
            print("-" * 30)
            if not result["passed"]:
                all_passed = False

        if overall_test_passed:
            print("\n🎉 모든 로그인 테스트 시나리오가 성공적으로 완료되었습니다!")
        else:
            print("\n⚠️ 일부 로그인 테스트 시나리오에서 실패가 발생했습니다. 로그를 확인하세요.")

        print("\n=========================================")
        print("   Appium 로그인 테스트 스위트 종료")
        print("=========================================\n")

    return overall_test_passed, overall_test_message

if __name__ == "__main__":
    print("\n--- 테스트 완료 ---")