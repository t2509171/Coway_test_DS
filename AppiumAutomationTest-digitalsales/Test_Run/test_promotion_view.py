# PythonProject/Appuim_Test.py
import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

from Promotion.test_customer_promotion import (test_customer_promotion_view,test_customer_promotion_click,test_customer_promotion_bulletin_view,
                                               test_customer_promotion_detailed_post_click,test_customer_promotion_detailed_post_view,
                                               test_customer_promotion_detailed_post_list_click)
from Promotion.test_salesperson_promotion import (test_salesperson_promotion_view,test_salesperson_promotion_click,test_salesperson_promotion_bulletin_view,
                                                  test_salesperson_promotion_detailed_post_click,test_salesperson_promotion_detailed_post_view,
                                                  test_salesperson_promotion_detailed_post_list_click)

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

def test_promotion_view(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   프로모션 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True
    overall_test_message = "모든 프로모션 확인 테스트 시나리오가 성공적으로 완료되었습니다."

    # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
    test_no_counter = 92

    try:
        # 고객 프로모션 테스트 실행
        try:
            # --- 고객 프로모션 항목 노출 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_view(flow_tester)
                overall_results["전체 메뉴 > 고객 프로모션 항목이 노출된다."] = {
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
                overall_test_message = f"고객 프로모션 노출 확인 실패: {e}"

            # --- 고객 프로모션 목록 화면 이동 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 목록 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_click(flow_tester)
                overall_results["고객 프로모션 항목 터치 시, 고객 프로모션 목록 화면으로 이동된다."] = {
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
                overall_test_message = f"고객 프로모션 목록 화면 이동 확인 실패: {e}"

            # --- 고객 프로모션 게시글 노출 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 게시글 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_bulletin_view(flow_tester)
                overall_results["수정 시간 순서로 고객 프로모션 게시물이 노출된다."] = {
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
                overall_test_message = f"고객 프로모션 게시글 노출 확인 실패: {e}"

            # --- 고객 프로모션 상세 게시글 클릭 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 상세 게시글 클릭 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_detailed_post_click(flow_tester)
                overall_results["게시물 터치 시, 상세 게시물 프로모션 화면으로 이동된다."] = {
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
                overall_test_message = f"고객 프로모션 상세 게시글 클릭 확인 실패: {e}"

            # --- 고객 프로모션 상세 게시글 노출 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 상세 게시글 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_detailed_post_view(flow_tester)
                overall_results["페이지 표시: 제목, 상태, 이벤트 시간, 이미지, 목록 버튼(이전, 다음, 목록)"] = {
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
                overall_test_message = f"고객 프로모션 상세 게시글 노출 확인 실패: {e}"

            # --- 고객 프로모션 목록 버튼 클릭 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 목록 버튼 클릭 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_detailed_post_list_click(flow_tester)
                overall_results["[목록] 버튼 tap 시, 프로모션 화면으로 이동된다."] = {
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
                overall_test_message = f"고객 프로모션 목록 버튼 클릭 확인 실패: {e}"
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"고객 프로모션 테스트 시나리오 확인 실패: {e}"

        # 판매인 프로모션 테스트 실행
        try:
            # --- 판매인 프로모션 항목 노출 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion_view(flow_tester)
                overall_results["전체 메뉴 > 판매인 프로모션 항목이 노출된다."] = {
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
                overall_test_message = f"판매인 프로모션 노출 확인 실패: {e}"

            # --- 판매인 프로모션 목록 화면 이동 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 목록 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion_click(flow_tester)
                overall_results["판매인 프로모션 항목 터치 시, 판매인 프로모션 목록 화면으로 이동된다."] = {
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
                overall_test_message = f"판매인 프로모션 목록 화면 이동 확인 실패: {e}"

            # --- 판매인 프로모션 게시글 노출 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 게시글 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion_bulletin_view(flow_tester)
                overall_results["수정 시간 순서로 판매인 프로모션 게시물이 노출된다."] = {
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
                overall_test_message = f"판매인 프로모션 게시글 노출 확인 실패: {e}"

            # --- 판매인 프로모션 상세 게시글 클릭 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 상세 게시글 클릭 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion_detailed_post_click(flow_tester)
                overall_results["게시물 터치 시, 상세 게시물 프로모션 화면으로 이동된다."] = {
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
                overall_test_message = f"판매인 프로모션 상세 게시글 클릭 확인 실패: {e}"

            # --- 판매인 프로모션 상세 게시글 노출 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 상세 게시글 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion_detailed_post_view(flow_tester)
                overall_results["페이지 표시: 제목, 상태, 이벤트 시간, 이미지, 목록 버튼(이전, 다음, 목록)"] = {
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
                overall_test_message = f"판매인 프로모션 상세 게시글 노출 확인 실패: {e}"

            # --- 판매인 프로모션 목록 버튼 클릭 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 목록 버튼 클릭 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion_detailed_post_list_click(
                    flow_tester)
                overall_results["[목록] 버튼 tap 시, 프로모션 화면으로 이동된다."] = {
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
                overall_test_message = f"판매인 프로모션 목록 버튼 클릭 확인 실패: {e}"

        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"판매인 프로모션 테스트 시나리오 확인 실패: {e}"

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