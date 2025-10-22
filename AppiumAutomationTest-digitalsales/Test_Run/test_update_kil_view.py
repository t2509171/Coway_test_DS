# 라이브러리 임포트
import os
import sys


from Update_kil.test_update_alert import test_verify_update_alert, test_perform_app_update
from Update_kil.test_app_permissions import test_verify_permission_guide_title, test_verify_required_permissions,test_verify_optional_permissions_with_scroll, test_confirm_permissions_and_navigate_to_login, test_login_after_relaunch_and_verify_version, test_verify_no_permission_guide_after_relaunch
# Google Sheets API 연동을 위해 필요한 함수를 임포트
from My_Page_kil.test_mypage_navigation import test_verify_mypage_icon_in_menu, test_navigate_to_mypage
from My_Page_kil.test_commission_visibility import test_verify_commission_elements


from Utils.test_result_input import update_test_result_in_sheet

def test_update_kil_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 앱 업데이트 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   앱 업데이트 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 앱 업데이트 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    test_no_counter = 0 # 앱 업데이트 화면 시작 Seller app checklist-51



    """Seller app checklist-1 : 업데이트 얼럿 노출 확인 테스트 실행"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 업데이트 얼럿 노출 확인---")

        content_unit_passed, content_unit_message = test_verify_update_alert(flow_tester)

        overall_results["업데이트 얼럿 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 업데이트 얼럿 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["업데이트 얼럿 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    """Seller app checklist-2 : 업데이트  확인 테스트 실행"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 업데이트 얼럿 노출 확인---")

        content_unit_passed, content_unit_message = test_perform_app_update(flow_tester)

        overall_results["업데이트 얼럿 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 업데이트 얼럿 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["업데이트 얼럿 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


    """Seller app checklist-4 : 접근권한 안내 팝업 노출 확인 테스트 실행"""
    try:
        test_no_counter += 2
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 접근권한 안내 팝업 노출 노출 확인---")

        content_unit_passed, content_unit_message = test_verify_permission_guide_title(flow_tester)

        overall_results["접근권한 안내 팝업 노출 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 접근권한 안내 팝업 노출 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["접근권한 안내 팝업 노출 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    """Seller app checklist-6 : 필수적 접근권한 확인 테스트 실행"""
    try:
        test_no_counter += 2
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 필수적 접근권한 노출 확인---")

        content_unit_passed, content_unit_message = test_verify_required_permissions(flow_tester)

        overall_results["필수적 접근권한 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 필수적 접근권한 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["필수적 접근권한 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


    """Seller app checklist-7 : 선택적 접근권한 확인 테스트 실행"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 선택적 접근권한 노출 확인---")

        content_unit_passed, content_unit_message = test_verify_optional_permissions_with_scroll(flow_tester)

        overall_results["선택적 접근권한 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 선택적 접근권한 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["선택적 접근권한 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


    """Seller app checklist-8 : 팝업종료 확인 테스트 실행"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 팝업종료 확인---")

        content_unit_passed, content_unit_message = test_confirm_permissions_and_navigate_to_login(flow_tester)

        overall_results["팝업종료 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 팝업종료 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["팝업종료 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    """Seller app checklist-3 : 재실행 업데이트 노출 확인 테스트 실행"""
    try:
        test_no_counter = 3
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 재실행 업데이트 노출 확인---")

        content_unit_passed, content_unit_message = test_login_after_relaunch_and_verify_version(flow_tester)

        overall_results["재실행 업데이트 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 재실행 업데이트 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["재실행 업데이트 노출 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    """Seller app checklist- : 재실행 접근권한 노출 확인 테스트 실행"""
    try:
        test_no_counter = 5
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 재실행 접근권한 노출 확인---")

        content_unit_passed, content_unit_message = test_verify_no_permission_guide_after_relaunch(flow_tester)

        overall_results["재실행 접근권한 노출 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, "No Run", tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)

    except Exception as e:
        print(f"🚨 재실행 접근권한 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["재실행 접근권한 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)




    finally:
    # --- 최종 테스트 결과 종합 ---
        print("\n=========================================")
        print("   Appium 메뉴 클릭 테스트 최종 종합 결과")
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
            print(f"\n🎉 {overall_test_message}")
        else:
            print(f"\n⚠️ {overall_test_message}")

        print("\n=========================================")
        print("   Appium 로그인 테스트 스위트 종료")
        print("=========================================\n")
        #print(f"마지막 테스트 케이스 번호: {test_no_counter}")

    return overall_test_passed, overall_test_message