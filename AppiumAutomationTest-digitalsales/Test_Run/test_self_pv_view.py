# PythonProject/Appuim_Test.py
import os
import sys

from Self_pv.test_self_pv import (test_etc_self_promotional_video_view,test_etc_self_promotional_video_button_click,test_etc_self_promotional_video_detail_view,
                                  test_etc_self_promotional_video_bulletin_click,
                                  test_etc_self_promotional_video_bulletin_view,test_etc_self_promotional_video_bulletin_list_button_click)
# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

def test_self_pv_view(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   셀프홍보영상 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 셀프홍보영상 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
    test_no_counter = 104

    try:
        # --- 셀프홍보영상 항목 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 항목 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_view(flow_tester)
            overall_results["전체메뉴에 셀프 홍보영상 항목이  노출된다."] = {
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
            overall_test_message = f"마이페이지 버튼 노출 확인 실패: {e}"

        # --- 셀프홍보영상 상세 페이지 이동 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 상세 페이지 이동 확인 ---")
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_button_click(flow_tester)
            overall_results["항목 선택시 셀프 홍보영상 상세 페이지로 이동된다."] = {
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
            overall_test_message = f"마이페이지 버튼 노출 확인 실패: {e}"

        # --- 셀프홍보영상 검색영역, 게시글영역 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 검색영역, 게시글영역 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_detail_view(flow_tester)
            overall_results["검색영역과 게시글영역으로 구성되어 노출된다."] = {
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
            overall_test_message = f"마이페이지 버튼 노출 확인 실패: {e}"

        # --- 셀프홍보영상 페이지 구성 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 페이지 구성 확인 ---")
            """
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_detail_view(flow_tester)
            overall_results["게시글은 상단 노출 적용 컨텐츠부터 등록일 순으로 노출되며 그 뒤로 상단 노출 비적용 컨텐츠가 등록일 순으로 노출된다. (B/O 확인 필요)"] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            """
            update_test_result_in_sheet(sheets_service, test_no, "No Run", tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"셀프홍보영상 페이지 구성 실패: {e}"

        # --- 셀프홍보영상 게시글 상세 페이지 이동 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 게시글 상세 페이지 이동 확인 ---")
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_bulletin_click(flow_tester)
            overall_results["게시글 선택시 상세페이지로 이동된다."] = {
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
            overall_test_message = f"셀프홍보영상 게시글 상세 페이지 이동 확인 실패: {e}"

        # --- 셀프홍보영상 게시글 상세 페이지 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 게시글 상세 페이지 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_bulletin_view(flow_tester)
            overall_results["글제목, 등록일, 조회수, 파일링크, 본문, 목록버튼으로 페이지가 노출된다."] = {
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
            overall_test_message = f"셀프홍보영상 게시글 상세 페이지 노출 확인 실패: {e}"

        # --- 셀프홍보영상 파일링크 다운로드 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 파일링크 다운로드 확인 ---")
            """
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_bulletin_view(flow_tester)
            overall_results["파일링크 선택시 해당 URL을 호출하여 자료가 다운로드 된다."] = {
                "test_no": test_no,  # 동적 번호 할당
                "passed": my_page_view_passed,
                "message": my_page_view_message
            }
            if not my_page_view_passed:
                overall_test_passed = False  # Mark overall test as failed
                overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
            # 스프레드시트에 테스트 결과 기록
            status = "Pass" if my_page_view_passed else "Fail"
            """
            update_test_result_in_sheet(sheets_service, test_no, "No Run", tester_name)
            print(f"{test_no} 테스트 케이스 완료.")
            print("-" * 50)  # Separator
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"셀프홍보영상 게시글 상세 페이지 이동 확인 실패: {e}"

        # --- 셀프홍보영상 게시글 목록 버튼 클릭 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  셀프홍보영상 게시글 목록 버튼 클릭 확인 ---")
            my_page_view_passed, my_page_view_message = test_etc_self_promotional_video_bulletin_list_button_click(flow_tester)
            overall_results["[목록] 버튼 선택시 게시물 목록화면으로 이동된다."] = {
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
            overall_test_message = f"셀프홍보영상 게시글 상세 페이지 이동 확인 실패: {e}"

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
        print(f"마지막 테스트 케이스 번호: {test_no_counter}")

    return overall_test_passed, overall_test_message

"""
if __name__ == "__main__":
    print("\n--- 테스트 완료 ---")
"""