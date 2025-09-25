# 라이브러리 임포트
import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))
# 새로 추가한 콘텐츠 유닛 테스트 함수 import
from Managed_Customers_kil.test_customized_sharing import test_find_customized_sharing_menu, test_navigate_to_customized_sharing_view
# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

def test_managed_customers_kil_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   홈 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 홈 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    test_no_counter = 79 # 홈화면 시작 Seller app checklist-15

    """Seller app checklist-80 관리고객 노출 확인"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 관리고객 노출 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_find_customized_sharing_menu(flow_tester)

        overall_results["관리고객 노출 확인"] = {
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
        print(f"🚨 관리고객 노출 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["관리고객 노출 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


    """Seller app checklist-81 관리고객 이동 확인"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 관리고객 이동 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_navigate_to_customized_sharing_view(flow_tester)

        overall_results["관리고객 이동 기능 확인"] = {
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
        print(f"🚨 관리고객 이동 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["관리고객 이동 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
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