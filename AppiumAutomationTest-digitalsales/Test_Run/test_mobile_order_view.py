import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

from Mobile_Order.test_mobile_order import (test_mobile_order_view,test_general_order_acceptance_order_view,test_pre_ordering_view,test_general_order_status_view,
                                            test_pre_contract_order_status_view)

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet


def test_mobile_order_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   프로모션 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 프로모션 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
    test_no_counter = 66

    try:
        # --- 모바일주문 Hub 집계 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  모바일주문 Hub 집계 확인 ---")
            my_page_view_passed, my_page_view_message = test_mobile_order_view(flow_tester)
            overall_results["전체주문, 인증입력 , 인증완료 , 서명입력 , 주문확정 영역이 노출된다."] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"모바일주문 Hub 집계 확인 실패: {e}"

        # --- 모바일주문 일반주문하기 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  모바일주문 일반주문하기 확인 ---")
            my_page_view_passed, my_page_view_message = test_general_order_acceptance_order_view(flow_tester)
            overall_results["Tap시 '주문접수'' 화면으로 이동된다"] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"모바일주문 일반주문하기 확인 실패: {e}"

        # --- 모바일주문 사전계약 주문하기 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  모바일주문 사전계약 주문하기 확인 ---")
            my_page_view_passed, my_page_view_message = test_pre_ordering_view(flow_tester)
            overall_results["Tap시 '사전계약 고객(재렌탈 사전계약)' 화면으로 이동된다."] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"모바일주문 사전계약 주문하기 확인 실패: {e}"

        # --- 모바일주문 일반주문 이어하기 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  모바일주문 일반주문 이어하기 확인 ---")
            my_page_view_passed, my_page_view_message = test_general_order_status_view(flow_tester)
            overall_results["Tap시 일반 탭 주문현황 페이지로 이동된다."] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"모바일주문 일반주문 이어하기 확인 실패: {e}"

        # --- 모바일주문 사전계약 이어하기 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  모바일주문 사전계약 이어하기 확인 ---")
            my_page_view_passed, my_page_view_message = test_pre_contract_order_status_view(flow_tester)
            overall_results["Tap시 사전계약 탭 주문현황 페이지로 이동된다."] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"모바일주문 사전계약 이어하기 확인 실패: {e}"

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