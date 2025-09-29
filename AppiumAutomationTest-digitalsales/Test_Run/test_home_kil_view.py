# 라이브러리 임포트
import os
import sys

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))
# 새로 추가한 콘텐츠 유닛 테스트 함수 import
from Home_kil.test_search import test_search_button_click
from Home_kil.test_units import test_product_unit, test_content_unit, test_client_unit
from Home_kil.test_home_etc import test_home_notice_count,test_home_notice_click,test_notice_page_navigation
from Home_kil.test_sales_tip import test_sales_tip_interaction
from Home_kil.test_product_shortcuts import test_verify_product_shortcuts_exist
from Home_kil.test_recommended_products import test_find_shared_products_section
from Home_kil.test_sales_content import test_recommended_sales_content
from Home_kil.test_banner import test_banner_swipe
from Home_kil.test_item import test_full_menu,test_checklist_42,test_management_customer,test_home,test_mobile_order,test_my_page
from Home_kil.home_reset import reset_to_home_and_refresh
from Home_kil.test_promotion import test_scroll_and_navigate_to_salesperson_promotion
from Home_kil.test_gallery_sharing import test_gallery_facebook_share

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

def test_home_kil_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   홈 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 홈 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    test_no_counter = 14 # 홈화면 시작 Seller app checklist-15

    # [Seller app checklist-15] --- 검색 아이콘 이동 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 검색 아이콘 이동 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_search_button_click(flow_tester)

        overall_results["검색 아이콘 이동 기능 확인"] = {
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
        print(f"🚨 아이콘 이동 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["아이콘 이동 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    reset_to_home_and_refresh(flow_tester)
    # [Seller app checklist-16] --- 공지사항 노출 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 공지사항 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_home_notice_count(flow_tester)

        overall_results["공지사항 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 공지사항 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 공지사항 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["공지사항 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    # -----------------------------------------

    # [Seller app checklist-17] --- 공지사항 이동 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 공지사항 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_home_notice_click(flow_tester)

        overall_results["공지사항 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 콘텐츠 유닛 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["콘텐츠 유닛 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)
    # -----------------------------------------

    # [Seller app checklist-18] --- 판매 팁 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 판매 팁 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_sales_tip_interaction(flow_tester)

        overall_results["판매 팁 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 판매 팁 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["판매 팁 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    # [Seller app checklist-19] --- 배너 팁 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 배너 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_banner_swipe(flow_tester)

        overall_results["배너 팁 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 배너 팁 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["배너 팁 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    # # [Seller app checklist-23] --- 갤러리아체험 페이스북 공유하기 확인 테스트 실행 ---
    # test_no_counter = 22
    # try:
    #     test_no_counter += 1
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     print(f"\n--- {test_no}: 갤러리아체험 페이스북 공유하기 기능 확인 (항목 수, 클릭) ---")
    #
    #     content_unit_passed, content_unit_message = test_gallery_facebook_share(flow_tester)
    #
    #     overall_results["갤러리아체험 페이스북 공유하기 팁 기능 확인"] = {
    #         "test_no": test_no,
    #         "passed": content_unit_passed,
    #         "message": content_unit_message
    #     }
    #     if not content_unit_passed:
    #         overall_test_passed = False
    #         overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."
    #
    #     status = "Pass" if content_unit_passed else "Fail"
    #     update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
    #     # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
    #     print(f"{test_no}테스트 케이스 완료.")
    #     print("-" * 50)
    # except Exception as e:
    #     print(f"🚨 갤러리아체험 페이스북 공유하기 팁 테스트 중 오류 발생: {e}")
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     overall_results["갤러리아체험 페이스북 공유하기 팁 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
    #     update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


    test_no_counter = 28
    # [Seller app checklist-29] --- 제품 바로가기 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 제품 바로가기 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_verify_product_shortcuts_exist(flow_tester)

        overall_results["제품 바로가기 팁 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 제품 바로가기 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["제품 바로가기 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


    # [Seller app checklist-30] --- 추천 제품 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 추천 제품 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_find_shared_products_section(flow_tester)

        overall_results["추천 제품 팁 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 추천 제품 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["추천 제품 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    #     [Seller app checklist-31] --- 추천 제품 유닛 확인 테스트 실행 ---

    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 추천 제품 유닛 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_product_unit(flow_tester)

        overall_results["추천 제품 유닛 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 추천 제품 유닛 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["추천 제품 유닛 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    # [Seller app checklist-35] --- 추천 콘텐츠 확인 테스트 실행 ---
    test_no_counter = 34
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 추천 콘텐츠 기능 확인 (항목 수, 클릭) ---")

        content_unit_passed, content_unit_message = test_recommended_sales_content(flow_tester)

        overall_results["추천 콘텐츠 팁 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 추천 콘텐츠 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["추천 콘텐츠 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)


        # --- 추가된 부분: '콘텐츠 유닛' 테스트 ---
    test_no_counter = 36
    try:
        test_no_counter += 1
        # [Seller app checklist-37 --- 콘텐츠 유닛 기능 확인 테스트 실행 ---
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 콘텐츠 유닛 기능 확인 (항목 수, 스와이프, 클릭) ---")

        content_unit_passed, content_unit_message = test_content_unit(flow_tester)

        overall_results["콘텐츠 유닛 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 콘텐츠 유닛 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["콘텐츠 유닛 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    # -----------------------------------------

    try:
        test_no_counter += 1
        # [Seller app checklist-38 --- 고객 프로모션 유닛 기능 확인 테스트 실행 ---
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}: 고객 프로모션 유닛 기능 확인 (항목 수, 스와이프, 클릭) ---")

        content_unit_passed, content_unit_message = test_client_unit(flow_tester)

        overall_results["고객 프로모션 유닛 기능 확인"] = {
            "test_no": test_no,
            "passed": content_unit_passed,
            "message": content_unit_message
        }
        if not content_unit_passed:
            overall_test_passed = False
            overall_test_message = "일부 홈 확인 테스트에서 실패가 발생했습니다."

        status = "Pass" if content_unit_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        # 연관된 모든 체크리스트에 동일한 결과를 기록합니다.
        print(f"{test_no}테스트 케이스 완료.")
        print("-" * 50)
    except Exception as e:
        print(f"🚨 고객 프로모션 유닛 테스트 중 오류 발생: {e}")
        test_no = f"Seller app checklist-{test_no_counter}"
        overall_results["고객 프로모션 유닛 기능 확인"] = {"test_no": test_no, "passed": False, "message": str(e)}
        update_test_result_in_sheet(sheets_service, test_no, "Fail", tester_name)

    # -----------------------------------------

    # --- test_checklist_39 판매인 프로모션 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  판매인 프로모션 확인 ---")
        my_page_view_passed, my_page_view_message = test_scroll_and_navigate_to_salesperson_promotion(flow_tester)
        overall_results["판매인 프로모션 확인."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "판매인 프로모션 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"독바 전체메뉴 노출 확인 실패: {e}"



    # --- test_checklist_40 공지사항 이동 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  공지사항 이동 확인 ---")
        my_page_view_passed, my_page_view_message = test_notice_page_navigation(flow_tester)
        overall_results["공지사항 이동 확인."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "공지사항 이동 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"공지사항 이동 확인 실패: {e}"





    # --- 독바 전체메뉴 test_checklist_41 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  독바 전체메뉴 노출 확인 ---")
        my_page_view_passed, my_page_view_message = test_full_menu(flow_tester)
        overall_results["독바 전체메뉴가 노출된다."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "독바 전체메뉴 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"독바 전체메뉴 노출 확인 실패: {e}"

    # AOS 라이프 스토리 노출 안됨 (보류)
    # # --- 독바 전체메뉴 test_checklist_42 확인 테스트 실행 ---
    # try:
    #     test_no_counter += 1
    #     test_no = f"Seller app checklist-{test_no_counter}"
    #     print(f"\n--- {test_no}:  독바 라이프 스토리 노출 확인 ---")
    #     my_page_view_passed, my_page_view_message = test_checklist_42(flow_tester)
    #     overall_results["독바 라이프 스토리 노출된다."] = {
    #         "test_no": test_no,  # 동적 번호 할당
    #         "passed": my_page_view_passed,
    #         "message": my_page_view_message
    #     }
    #     if not my_page_view_passed:
    #         overall_test_passed = False  # Mark overall test as failed
    #         overall_test_message = "독바 라이프 스토리 확인을 실패했습니다. 상세 로그를 확인하세요."
    #     # 스프레드시트에 테스트 결과 기록
    #     status = "Pass" if my_page_view_passed else "Fail"
    #     update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
    #     print(f"{test_no} 테스트 케이스 완료.")
    #     print("-" * 50)  # Separator
    # except Exception as e:
    #     overall_test_passed = False
    #     overall_test_message = f"독바 전체메뉴 노출 확인 실패: {e}"

    # ---------- 독바 관리고객 test_checklist_43 확인 테스트 실행 ----------
    try:
        test_no_counter += 1
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  독바 관리고객 노출 확인 ---")
        my_page_view_passed, my_page_view_message = test_management_customer(flow_tester)
        overall_results["독바 관리고객 노출된다."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "독바 관리고객 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"독바 관리고객 노출 확인 실패: {e}"

    # --- 독바 홈 test_checklist_44 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  독바 홈 노출 확인 ---")
        my_page_view_passed, my_page_view_message = test_home(flow_tester)
        overall_results["독바 홈이 노출된다."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "독바 홈 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"독바 홈 노출 확인 실패: {e}"

    # --- 독바 모바일주문 test_checklist_45 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  독바 모바일주문 노출 확인 ---")
        my_page_view_passed, my_page_view_message = test_mobile_order(flow_tester)
        overall_results["독바 모바일주문 노출된다."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "독바 모바일주문 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"독바 모바일주문 노출 확인 실패: {e}"

    # --- 독바 마이페이지 test_checklist_46 확인 테스트 실행 ---
    try:
        test_no_counter += 1
        test_no = f"Seller app checklist-{test_no_counter}"
        print(f"\n--- {test_no}:  독바 마이페이지 노출 확인 ---")
        my_page_view_passed, my_page_view_message = test_my_page(flow_tester)
        overall_results["독바 마이페이지가 노출된다."] = {
            "test_no": test_no,  # 동적 번호 할당
            "passed": my_page_view_passed,
            "message": my_page_view_message
        }
        if not my_page_view_passed:
            overall_test_passed = False  # Mark overall test as failed
            overall_test_message = "독바 마이페이지 확인을 실패했습니다. 상세 로그를 확인하세요."
        # 스프레드시트에 테스트 결과 기록
        status = "Pass" if my_page_view_passed else "Fail"
        update_test_result_in_sheet(sheets_service, test_no, status, tester_name)
        print(f"{test_no} 테스트 케이스 완료.")
        print("-" * 50)  # Separator
    except Exception as e:
        overall_test_passed = False
        overall_test_message = f"독바 마이페이지 노출 확인 실패: {e}"



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