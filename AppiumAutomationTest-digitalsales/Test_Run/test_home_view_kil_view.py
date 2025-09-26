import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

from Home_View_kil.test_webview_navigation import test_navigate_to_webview_from_home
from Home_View_kil.test_greeting_message import test_verify_greeting_message_in_menu
from Home_View_kil.test_home_button_visibility import test_verify_home_button_visibility
from Home_View_kil.test_large_font_mode import test_verify_element_positions_after_large_font_click

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet


# AppiumLoginTest 클래스를 임포트합니다.


def test_home_view_kil_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   검색 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 검색 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message


    test_no_counter = 136


    # """Seller app checklist-137 : AI 코디 비서 노출 확인 테스트 실행"""
    # try:
    #     test_no_counter += 1
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     print(f"\n--- {test_no}: AI 코디 비서 노출 확인---")
    #
    #     content_unit_passed, content_unit_message = test_verify_greeting_message_in_menu(flow_tester)
    #
    #     overall_results["AI 코디 비서 노출 확인"] = {
    #         "test_no": test_no,
    #         "passed": content_unit_passed,
    #         "message": content_unit_message
    #     }
    #     if not content_unit_passed:
    #         overall_test_passed = False
    #         overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."
    #
    #     status = "Pass" if content_unit_passed else "Fail"
    #     update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
    #     # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
    #     print(f"{test_no}테스트 케이스 완료.")
    #     print("-" * 50)
    # except Exception as e:
    #     print(f"🚨 AI 코디 비서 노출 확인 테스트 중 오류 발생: {e}")
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     overall_results["AI 코디 비서 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
    #     update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)
    #
    # """Seller app checklist-138 : AI 코디 비서 노출 확인 테스트 실행"""
    # try:
    #     test_no_counter += 1
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     print(f"\n--- {test_no}: AI 코디 비서 노출 확인---")
    #
    #     content_unit_passed, content_unit_message = test_verify_home_button_visibility(flow_tester)
    #
    #     overall_results["AI 코디 비서 노출 확인"] = {
    #         "test_no": test_no,
    #         "passed": content_unit_passed,
    #         "message": content_unit_message
    #     }
    #     if not content_unit_passed:
    #         overall_test_passed = False
    #         overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."
    #
    #     status = "Pass" if content_unit_passed else "Fail"
    #     update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
    #     # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
    #     print(f"{test_no}테스트 케이스 완료.")
    #     print("-" * 50)
    # except Exception as e:
    #     print(f"🚨 AI 코디 비서 노출 확인 테스트 중 오류 발생: {e}")
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     overall_results["AI 코디 비서 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
    #     update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)
    #
    #
    # test_no_counter = 136
    #
    # """Seller app checklist-136 : AI 코디 비서 노출 확인 테스트 실행"""
    # try:
    #     test_no_counter += 1
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     print(f"\n--- {test_no}: AI 코디 비서 노출 확인---")
    #
    #     content_unit_passed, content_unit_message = test_navigate_to_webview_from_home(flow_tester)
    #
    #     overall_results["AI 코디 비서 노출 확인"] = {
    #         "test_no": test_no,
    #         "passed": content_unit_passed,
    #         "message": content_unit_message
    #     }
    #     if not content_unit_passed:
    #         overall_test_passed = False
    #         overall_test_message = "일부 검색 확인 테스트에서 실패가 발생했습니다."
    #
    #     status = "Pass" if content_unit_passed else "Fail"
    #     update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
    #     # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
    #     print(f"{test_no}테스트 케이스 완료.")
    #     print("-" * 50)
    # except Exception as e:
    #     print(f"🚨 AI 코디 비서 노출 확인 테스트 중 오류 발생: {e}")
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     overall_results["AI 코디 비서 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
    #     update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    """Seller app checklist-139 : AI 코디 비서 큰글씨 모드 확인 테스트 실행"""
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: AI 코디 비서 노출 확인---")

        content_unit_passed, content_unit_message = test_verify_element_positions_after_large_font_click(flow_tester)

        overall_results["AI 코디 비서 노출 확인"] = {
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
        print(f"🚨 AI 코디 비서 노출 확인 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["AI 코디 비서 노출 확인 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
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

    return overall_test_passed, overall_test_message


if __name__ == "__main__":
    print("\n--- 테스트 완료 ---")