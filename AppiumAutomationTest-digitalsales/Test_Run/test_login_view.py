import os
import sys
import time
import logging

# 대상 테스트 함수들 임포트
from Login.test_login_view import test_login_main_view
from Login.test_Login_failed import login_failed
from Login.test_Login_passed import login_successful
from Login.test_pw_change import run_password_change_button_back_scenario, run_password_reset_button_back_scenario
from Home.test_etc import test_etc_setting_sign_out
from Update_kil.test_app_permissions import test_verify_no_permission_guide_after_relaunch  # 자동로그인 확인용

# Google Sheets API 연동
from Utils.test_result_input import update_test_result_in_sheet

# 로거 설정
log = logging.getLogger(__name__)


def test_login(flow_tester, sheets_service, tester_name):
    """
    (리팩터링) 모든 로그인 테스트 시나리오를 리스트 기반으로 실행합니다.
    """
    print("=========================================")
    print("   Appium 로그인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True
    overall_test_message = "모든 로그인 테스트 시나리오가 성공적으로 완료되었습니다."

    try:
        # --- 테스트 사전 준비: 로그아웃 및 앱 재시작 ---
        print("--- 테스트 사전 준비 시작 ---")
        test_etc_setting_sign_out(flow_tester)

        print("테스트를 위해 teardown_driver()를 호출하여 드라이버 세션을 종료합니다.")
        if flow_tester.driver:
            flow_tester.teardown_driver()
        time.sleep(3)

        print("setup_driver()를 호출하여 새로운 드라이버 세션을 시작하고 앱을 실행합니다.")
        flow_tester.setup_driver()
        print("✅ 앱이 성공적으로 재실행되었습니다.")
        time.sleep(3)
        print("--- 테스트 사전 준비 완료 ---")
        # --- 사전 준비 완료 ---

    except Exception as setup_e:
        print(f"🚨 테스트 사전 준비(앱 재시작) 중 치명적 오류 발생: {setup_e}")
        return False, "로그인 테스트 사전 준비(앱 재시작) 실패"

    # --- 로그인 테스트 케이스 정의 ---
    # (테스트명, 테스트 함수, Checklist ID)
    test_scenarios = [
        ("로그인 화면 노출 확인", test_login_main_view, 9),
        ("정상 로그인 및 메인 페이지 노출", login_successful, 10),
        ("로그인 실패 팝업 확인", login_failed, 11),
        ("자동 로그인 확인", test_verify_no_permission_guide_after_relaunch, 12),  # 기존 'No Run' 항목
        ("비밀번호 초기화 페이지 이동 확인", run_password_reset_button_back_scenario, 13),
        ("비밀번호 변경 페이지 이동 확인", run_password_change_button_back_scenario, 14),
    ]

    # --- 테스트 실행 루프 ---
    for test_name, test_function, checklist_id in test_scenarios:
        test_no = f"Seller app checklist-{checklist_id}"
        test_passed = False
        test_message = ""

        try:
            print(f"\n--- {test_no}: {test_name} ---")

            # ID 12 (자동로그인)은 기존 로직대로 'No Run' 처리
            if checklist_id == 12:
                status = "No Run"
                test_passed = True  # 스위트 실패로 간주하지 않음
                test_message = "자동화 테스트 임시 제외"
            else:
                test_passed, test_message = test_function(flow_tester)
                status = "Pass" if test_passed else "Fail"

            if not test_passed:
                overall_test_passed = False
                overall_test_message = "일부 로그인 테스트에서 실패가 발생했습니다."

        except Exception as e:
            test_passed = False
            test_message = f"🚨 테스트 실행 중 예외 발생: {e}"
            log.error(test_message)
            overall_test_passed = False
            overall_test_message = "일부 로그인 테스트에서 심각한 오류가 발생했습니다."
            status = "Fail"

        # --- 결과 저장 및 시트 업데이트 ---
        overall_results[test_name] = {
            "test_no": test_no,
            "passed": test_passed,
            "message": test_message
        }
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)

        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)

    # --- 최종 테스트 결과 종합 ---
    print("\n=========================================")
    print("   Appium 로그인 테스트 최종 종합 결과")
    print("=========================================")

    for test_name, result in overall_results.items():
        status = "✅ 성공" if result["passed"] else "❌ 실패"
        print(f"테스트 번호: {result['test_no']}")
        print(f"테스트명: {test_name}")
        print(f"결과: {status}")
        print(f"메시지: {result['message']}")
        print("-" * 30)

    if overall_test_passed:
        print(f"\n🎉 {overall_test_message}")
    else:
        print(f"\n⚠️ {overall_test_message}")

    print("\n=========================================")
    print("   Appium 로그인 테스트 스위트 종료")
    print("=========================================\n")

    return overall_test_passed, overall_test_message


if __name__ == "__main__":
    print("\n--- 테스트 완료 ---")
    pass




# # PythonProject/Appuim_Test.py
# import os
# import sys
# import time
#
# # Ensure the Login directory is in the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))
#
# from Login.test_login_view import test_login_main_view
# from Login.test_Login_failed import login_failed
# from Login.test_Login_passed import login_successful
# from Login.test_pw_change import run_password_change_button_back_scenario, run_password_reset_button_back_scenario
# from Home.test_etc import test_etc_setting_view, test_etc_setting_set_notifications, test_etc_setting_sign_out # 로그아웃을 위해
# # Google Sheets API 연동을 위해 필요한 함수를 임포트
# from Utils.test_result_input import update_test_result_in_sheet
# # from Update_kil.test_app_permissions import test_verify_no_permission_guide_after_relaunch
#
# # sheets_service와 tester_name 인자를 추가
# def test_login(flow_tester, sheets_service, tester_name):
#     """
#     모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
#     """
#     print("=========================================")
#     print("   Appium 로그인 테스트 스위트 시작")
#     print("=========================================\n")
#
#     overall_results = {}
#     overall_test_passed = True  # Initialize for the overall test result
#     overall_test_message = "모든 로그인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message
#
#
#     test_etc_setting_sign_out(flow_tester)
#
#     # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
#
#     print("테스트를 위해 teardown_driver()를 호출하여 드라이버 세션을 종료합니다.")
#     if flow_tester.driver:
#         flow_tester.teardown_driver()
#     time.sleep(3)
#
#     print("setup_driver()를 호출하여 새로운 드라이버 세션을 시작하고 앱을 실행합니다.")
#     flow_tester.setup_driver()
#     print("✅ 앱이 성공적으로 재실행되었습니다.")
#     print("앱 안정화를 위해 8초간 대기합니다...")
#     time.sleep(3)
#     try:
#         # --- Seller app checklist-  자동 로그인 확인 테스트 실행 --- 5번 케이스 앱 재실행 테스트와 결과 같게 처리
#         try:
#             test_no_counter =12
#             test_no = f"Seller app checklist-{test_no_counter}"
#             # print(f"\n--- {test_no}:  자동 로그인 확인 ---")
#             # login_main_view_passed, login_main_view_message = test_verify_no_permission_guide_after_relaunch(flow_tester)
#             # overall_results["자동로그인 체크 후 로그인 진행하면 App 종료후 재실행시 자동로그인이 되어 메인 페이지가 노출된다."] = {
#             #     "test_no": test_no,  # 동적 번호 할당
#             #     "passed": login_main_view_passed,
#             #     "message": login_main_view_message
#             # }
#             # if not login_main_view_passed:
#             #     overall_test_passed = False  # Mark overall test as failed
#             #     overall_test_message = "로그인 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
#             # # 스프레드시트에 테스트 결과 기록
#             # status = "Pass" if login_main_view_passed else "Fail"
#             update_test_result_in_sheet(sheets_service, test_no, "No Run", tester_name)
#             # update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
#             print(f"{test_no} 테스트 케이스 완료.")
#             print("-" * 50)  # Separator
#         except Exception as e:
#             overall_test_passed = False
#             overall_test_message = f"로그인 화면 노출 확인 실패: {e}"
#
#         test_no_counter = 8
#
#         # --- 로그인 화면 노출 확인 테스트 실행 ---
#         try:
#             test_no_counter += 1
#             test_no = f"Seller app checklist-{test_no_counter}"
#             print(f"\n--- {test_no}:  로그인 화면 노출 확인 ---")
#             login_main_view_passed, login_main_view_message = test_login_main_view(flow_tester)
#             overall_results["App 실행시 로그인 창이 노출된다."] = {
#                 "test_no": test_no,  # 동적 번호 할당
#                 "passed": login_main_view_passed,
#                 "message": login_main_view_message
#             }
#             if not login_main_view_passed:
#                 overall_test_passed = False  # Mark overall test as failed
#                 overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
#             # 스프레드시트에 테스트 결과 기록
#             status = "Pass" if login_main_view_passed else "Fail"
#             update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
#             print(f"{test_no} 테스트 케이스 완료.")
#             print("-" * 50)  # Separator
#         except Exception as e:
#             overall_test_passed = False
#             overall_test_message = f"로그인 화면 노출 확인 실패: {e}"
#
#         test_no_counter = 10
#         # --- Seller app checklist-11 로그인 실패 확인 테스트 실행 ---
#         try:
#             test_no_counter += 1
#             test_no = f"Seller app checklist-{test_no_counter}"
#             print(f"\n--- {test_no}:  정상적인 로그인 진행 후, 메인 페이지 노출 확인 ---")
#             login_failed_passed, login_failed_message = login_failed(flow_tester)
#             overall_results["정상적으로 로그인 진행시 메인페이지가 노출된다."] = {
#                 "test_no": test_no,  # 동적 번호 할당
#                 "passed": login_failed_passed,
#                 "message": login_failed_message
#             }
#             if not login_failed_passed:
#                 overall_test_passed = False  # Mark overall test as failed
#                 overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
#             # 스프레드시트에 테스트 결과 기록
#             status = "Pass" if login_failed_passed else "Fail"
#             update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
#             print(f"{test_no} 테스트 케이스 완료.")
#             print("-" * 50)  # Separator
#         except Exception as e:
#             overall_test_passed = False
#             overall_test_message = f"정상적인 로그인 진행 후, 메인 페이지 노출 확인 실패: {e}"
#
#         # --- Seller app checklist-13 비밀번호 초기화 페이지 이동 확인 테스트 실행 ---
#         try:
#             test_no_counter = 12
#             test_no_counter += 1
#             test_no = f"Seller app checklist-{test_no_counter}"
#             print(f"\n--- {test_no}:  비밀번호 초기화 페이지 이동 확인 ---")
#             login_successful_passed, login_successful_message = run_password_reset_button_back_scenario(flow_tester)
#             overall_results["비밀번호 초기화 페이지로 이동된다."] = {
#                 "test_no": test_no,  # 동적 번호 할당
#                 "passed": login_successful_passed,
#                 "message": login_successful_message
#             }
#             if not login_successful_passed:
#                 overall_test_passed = False  # Mark overall test as failed
#                 overall_test_message = "일부 로그인 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
#             # 스프레드시트에 테스트 결과 기록
#             status = "Pass" if login_successful_passed else "Fail"
#             update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
#             print(f"{test_no} 테스트 케이스 완료.")
#             print("-" * 50)  # Separator
#         except Exception as e:
#             overall_test_passed = False
#             overall_test_message = f"비밀번호 초기화 페이지 이동 확인 실패: {e}"
#
#         # --- Seller app checklist-14 비밀번호 변경 페이지 이동 확인 테스트 실행 ---
#         try:
#             test_no_counter = 13
#             test_no_counter += 1
#             test_no = f"Seller app checklist-{test_no_counter}"
#             print(f"\n--- {test_no}:  비밀번호 변경 페이지 이동 확인 ---")
#             login_successful_passed, login_successful_message = run_password_change_button_back_scenario(flow_tester)
#             overall_results["비밀번호 변경 페이지로 이동된다."] = {
#                 "test_no": test_no,  # 동적 번호 할당
#                 "passed": login_successful_passed,
#                 "message": login_successful_message
#             }
#             if not login_successful_passed:
#                 overall_test_passed = False  # Mark overall test as failed
#                 overall_test_message = "일부 로그인 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
#             # 스프레드시트에 테스트 결과 기록
#             status = "Pass" if login_successful_passed else "Fail"
#             update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
#             print(f"{test_no} 테스트 케이스 완료.")
#             print("-" * 50)  # Separator
#         except Exception as e:
#             overall_test_passed = False
#             overall_test_message = f"비밀번호 변경 페이지 이동 확인 실패: {e}"
#
#
#
#         # --- Seller app checklist-10 정상적인 로그인 진행 후, 메인 페이지 노출 확인 테스트 실행 ---
#         try:
#             test_no_counter = 9
#             test_no_counter += 1
#             test_no = f"Seller app checklist-{test_no_counter}"
#             print(f"\n--- {test_no}:  정상적인 로그인 진행 후, 메인 페이지 노출 확인 ---")
#             login_successful_passed, login_successful_message = login_successful(flow_tester)
#             overall_results["정상적으로 로그인 진행시 메인페이지가 노출된다."] = {
#                 "test_no": test_no,  # 동적 번호 할당
#                 "passed": login_successful_passed,
#                 "message": login_successful_message
#             }
#             if not login_successful_passed:
#                 overall_test_passed = False  # Mark overall test as failed
#                 overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
#             # 스프레드시트에 테스트 결과 기록
#             status = "Pass" if login_successful_passed else "Fail"
#             update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
#             print(f"{test_no} 테스트 케이스 완료.")
#             print("-" * 50)  # Separator
#         except Exception as e:
#             overall_test_passed = False
#             overall_test_message = f"정상적인 로그인 진행 후, 메인 페이지 노출 확인 실패: {e}"
#
#
#
#
#
#
#
#
#
#
#
#         """
#
#         # [Seller app checklist-8] 유효하지 않은 자격 증명으로 로그인 실패 테스트 실행
#         print("\n--- Seller app checklist-8 : 유효하지 않은 자격 증명으로 로그인 실패 ---")
#         failure_test_passed, failure_test_message = run_failed_login_scenario(flow_tester)
#         overall_results["잘못된 계정 및 비밀번호 입력시 로그인이 실패한다."] = {
#             "test_no": "Seller app checklist-8",
#             "passed": failure_test_passed,
#             "message": failure_test_message
#         }
#         # 스프레드시트에 테스트 결과 기록
#         status = "PASS" if failure_test_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-8", status, tester_name)
#         print("Seller app checklist-8 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         # --- 비밀번호 변경 후 뒤로가기 테스트 실행 ---
#         print("\n--- Seller app checklist-11: 비밀번호 변경 후 뒤로가기 ---")
#         password_change_back_passed, password_change_back_message = run_password_change_button_back_scenario(flow_tester)
#         overall_results["[비밀번호 변경] 버튼 터치 시, 비밀번호 변경 페이지로 이동된다."] = {
#             "test_no": "Seller app checklist-11",
#             "passed": password_change_back_passed,
#             "message": password_change_back_message
#         }
#         # 스프레드시트에 테스트 결과 기록
#         status = "PASS" if password_change_back_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-11", status, tester_name)
#         print("Seller app checklist-11 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         # --- 비밀번호 초기화 후 뒤로가기 테스트 실행 ---
#         print("\n--- Seller app checklist-10 : 비밀번호 초기화 후 뒤로가기 ---")
#         password_reset_back_passed, password_reset_back_message = run_password_reset_button_back_scenario(flow_tester)
#         overall_results["[비밀번호 초기화] 버튼 터치 시, 비밀번호 초기화 페이지로 이동된다."] = {
#             "test_no": "Seller app checklist-10",
#             "passed": password_reset_back_passed,
#             "message": password_reset_back_message
#         }
#         # 스프레드시트에 테스트 결과 기록
#         status = "PASS" if password_reset_back_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-10", status, tester_name)
#         print("Seller app checklist-10 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         # [Seller app checklist-7/9] --- 유효한 자격 증명으로 로그인 성공 테스트 실행 ---
#         print("\n--- Seller app checklist-7/9 : 유효한 자격 증명으로 로그인 성공 ---")
#         success_test_passed, success_test_message = run_successful_login_scenario(flow_tester)
#         overall_results["정상적으로 로그인 진행시 메인페이지가 노출된다."] = {
#             "test_no": "Seller app checklist-7/Seller app checklist-9",
#             "passed": success_test_passed,
#             "message": success_test_message
#         }
#         # 스프레드시트에 테스트 결과 기록 (7)
#         status = "PASS" if success_test_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-7", status, tester_name)
#         print("Seller app checklist-7 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         # 스프레드시트에 테스트 결과 기록 (9)
#         status = "PASS" if success_test_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-9", status, tester_name)
#         print("Seller app checklist-9 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         #[Seller app checklist-12/13] --- 홈 > 검색 / 공지사항 테스트 실행 ---
#         print("\n--- Seller app checklist-12/13 : 홈 화면 내비게이션 (검색 아이콘, 공지사항) ---")
#         home_navigation_passed, home_navigation_message = run_home_navigation_scenario(flow_tester)
#         overall_results["검색 화면으로 이동한다/등록/수정 날짜 내림차순으로 최대 3개의 공지를 표시한다"] = {
#             "test_no": "Seller app checklist-12/Seller app checklist-13",  # You can assign a specific checklist number
#             "passed": home_navigation_passed,
#             "message": home_navigation_message
#         }
#         # 스프레드시트에 테스트 결과 기록 (12)
#         status = "PASS" if home_navigation_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-12", status, tester_name)
#         print("Seller app checklist-12 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         # 스프레드시트에 테스트 결과 기록 (13)
#         status = "PASS" if home_navigation_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-13", status, tester_name)
#         print("Seller app checklist-13 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#
#         #[Seller app checklist-16] --- 홈 > 배너 스와이프, 클릭
#         print("\n--- Seller app checklist-16: 배너 스와이프, 클릭 ---")
#         home_navigation_passed, home_navigation_message = perform_home_banner_swipe(flow_tester)
#         overall_results["좌우로 스와이프가 가능하며, 터치 시 해당 제품의 상세 정보 페이지로 이동한다."] = {
#             "test_no": "Seller app checklist-16",  # You can assign a specific checklist number
#             "passed": home_navigation_passed,
#             "message": home_navigation_message
#         }
#         # 스프레드시트에 테스트 결과 기록
#         status = "PASS" if home_navigation_passed else "FAIL"
#         update_test_result_in_sheet(sheets_service, "Seller app checklist-16", status, tester_name)
#         print("Seller app checklist-16 테스트 케이스 완료.")
#         print("-" * 50)  # Separator
#     """
#
#     except Exception as e:
#         print(f"🚨 전체 테스트 스위트 실행 중 치명적인 오류 발생: {e}")
#         overall_results["전체 스위트 초기화 오류"] = {
#             "test_no": "N/A",
#             "passed": False,
#             "message": f"초기 드라이버 설정 또는 테스트 실행 중 오류 발생: {e}"
#         }
#
#     finally:
#         # --- 최종 테스트 결과 종합 ---
#         print("\n=========================================")
#         print("   Appium 로그인 테스트 최종 종합 결과")
#         print("=========================================")
#
#         all_passed = True
#         for test_name, result in overall_results.items():
#             status = "✅ 성공" if result["passed"] else "❌ 실패"
#             print(f"테스트 번호: {result['test_no']}")
#             print(f"테스트명: {test_name}")
#             print(f"결과: {status}")
#             print(f"메시지: {result["message"]}")
#             print("-" * 30)
#             if not result["passed"]:
#                 all_passed = False
#
#         if overall_test_passed:
#             print("\n🎉 모든 로그인 테스트 시나리오가 성공적으로 완료되었습니다!")
#         else:
#             print("\n⚠️ 일부 로그인 테스트 시나리오에서 실패가 발생했습니다. 로그를 확인하세요.")
#
#         print("\n=========================================")
#         print("   Appium 로그인 테스트 스위트 종료")
#         print("=========================================\n")
#
#     return overall_test_passed, overall_test_message
#
# if __name__ == "__main__":
#     print("\n--- 테스트 완료 ---")
#     pass