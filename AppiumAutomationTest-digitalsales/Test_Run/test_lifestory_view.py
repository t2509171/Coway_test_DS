import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

from Life_Story.test_LS_view import test_lifestory_view,test_lifestory_details_list_view,test_lifestory_details_list_click,test_lifestory_sharing_kakao,test_lifestory_share_count_increase

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

# AppiumLoginTest 클래스를 임포트합니다.


def test_lifestory_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   라이프스토리 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 라이프스토리 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
    test_no_counter = 71

    try:
        # --- 라이프스토리 항목 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  라이프스토리 항목 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_view(flow_tester)
            overall_results["전체메뉴에 라이프스토리 항목이 노출된다."] = {
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
            overall_test_message = f"라이프스토리 항목 노출 확인 실패: {e}"

        # --- 라이프스토리 게시물 목록 페이지 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  라이프스토리 게시물 목록 페이지 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_view(flow_tester)
            overall_results["전체메뉴에서 라이프스토리 항목  선택시 라이프스토리 게시물 목록 페이지로 이동한다."] = {
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
            overall_test_message = f"라이프스토리 게시물 목록 페이지 노출 확인 실패: {e}"

        # --- 라이프스토리 게시물 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  라이프스토리 게시물 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_view(flow_tester)
            overall_results["검색영역, 카테고리영역, 게시글이 노출된다."] = {
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
            overall_test_message = f"라이프스토리 게시물 노출 확인 실패: {e}"

        # --- 라이프스토리 카테고리 글목록 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  라이프스토리 카테고리 글목록 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_details_list_view(flow_tester)
            overall_results["카테고리 선택시 해당 카테고리에 맞는 글목록이 노출된다."] = {
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
            overall_test_message = f"라이프스토리 카테고리 글목록 노출 확인 실패: {e}"

        # --- 라이프스토리 글목록 상세페이지 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  라이프스토리 글목록 상세페이지 노출 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_details_list_click(flow_tester)
            overall_results["글목록에서 임의의 글 선택시 상세페이지로 이동한다."] = {
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
            overall_test_message = f"라이프스토리 글목록 상세페이지 노출 확인 실패: {e}"

        # --- 라이프스토리 카카오톡 공유하기 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  라이프스토리 카카오톡 공유하기 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_sharing_kakao(flow_tester)
            overall_results["채널 선택 팝업창에서 카카오톡을 선택하면 '광고성 정보 전송에 따른 의무사항' 팝업창이 노출되고 '동의'버튼을 터치하면  카카오톡앱이 호출되며 수신자 선택시 공유가 진행된다."] = {
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
            overall_test_message = f"라이프스토리 카카오톡 공유하기 확인 실패: {e}"

        # --- 마이페이지 공유하기 카운트 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  마이페이지 공유하기 카운트 확인 ---")
            my_page_view_passed, my_page_view_message = test_lifestory_share_count_increase(flow_tester)
            overall_results["마이페이지 공유하기 카운트가 올라간다."] = {
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
            overall_test_message = f"마이페이지 공유하기 카운트 확인 실패: {e}"

        # --- 판매인 정보 노출 확인 테스트 실행 ---
        try:
            test_no_counter += 1
            test_no = f"Seller app checklist-{test_no_counter}"
            print(f"\n--- {test_no}:  판매인 정보 노출 확인 ---")
            """
            my_page_view_passed, my_page_view_message = test_lifestory_share_count_increase(flow_tester)
            overall_results["고객이 수신 받은 URL 진입 > 추천 판매인 항목의 판매인 명이 자동 등록된다."] = {
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
            overall_test_message = f"판매인 정보 노출 확인 실패: {e}"

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