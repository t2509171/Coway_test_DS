# 라이브러리 임포트
import os
import sys

# AppiumLoginTest 클래스를 임포트합니다.
from Home.test_Menu_view import (test_my_page_view,test_recent_main_product_menu_view,test_water_purifier_menu_view,test_cleaner_menu_view,test_bide_salter_menu_view,
                                 test_berex_bed_menu_view,test_berex_massage_chair_menu_view,test_kitchen_home_appliances_menu_view,test_refurbished_exhibition_Menu_view)
from Mobile_Order.test_mobile_order import test_mobile_order_view,test_general_order_acceptance_order_view,test_pre_ordering_view,test_general_order_status_view
from Home.test_promotion import test_customer_promotion_view,test_salesperson_promotion
from Home.test_Shared_Content import test_shared_content_lifestory,test_shared_content_ecatalog,test_shared_content_productguide
from Home.test_etc import test_etc_Notice,test_etc_self_promotional_video,test_etc_setting_view,test_etc_setting_set_notifications,test_etc_setting_sign_out

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))

def test_fullMenu_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   Appium 로그인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 전체메뉴 클릭 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
    test_no_counter = 48

    try:

        # 전체메뉴 > 마이페이지/주문 테스트 실행
        try: 
            # --- 마이페이지 클릭 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  마이페이지 버튼 노출 확인 ---")
                my_page_view_passed, my_page_view_message = test_my_page_view(flow_tester)
                overall_results["마이페이지 화면으로 이동된다."] = {
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

            # --- 최근 본 제품 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  최근 본 제품 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_recent_main_product_menu_view(flow_tester)
                overall_results["최근 본 제품 화면으로 이동된다."] = {
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
    
            # --- 정수기 제품군 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  정수기 제품군 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_water_purifier_menu_view(flow_tester)
                overall_results["정수기 제품군 페이지로 이동한다."] = {
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
    
            # --- 청정기 제품군 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  청정기 제품군 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_cleaner_menu_view(flow_tester)
                overall_results["공기청정기 제품군 페이지로 이동한다."] = {
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
    
            # --- 비데/연수기 제품군 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  비데/연수기 제품군 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_bide_salter_menu_view(flow_tester)
                overall_results["비데/연수기 제품군 페이지로 이동한다."] = {
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
    
            # --- BEREX 침대 제품군 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  BEREX 침대 제품군 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_berex_bed_menu_view(flow_tester)
                overall_results["BEREX 침대 제품군 페이지로 이동한다."] = {
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
    
            # --- BEREX 안마의자 제품군 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  BEREX 안마의자 제품군 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_berex_massage_chair_menu_view(flow_tester)
                overall_results["BEREX 안마의자/안마베드 제품군 페이지로 이동한다."] = {
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
    
            # --- 주방/생활가전 제품군 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  주방/생활가전 제품군 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_kitchen_home_appliances_menu_view(flow_tester)
                overall_results["주방.생활가전 제품군 페이지로 이동한다."] = {
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
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"전체메뉴>마이페이지/제품 테스트 확인 실패: {e}"

        # 전체메뉴 > 주문 테스트 실행
        try:
            # --- 모바일 주문 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  모바일 주문 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_mobile_order_view(flow_tester)
                overall_results["홈 화면 > 독바(모바일주문) > 모바일주문 화면으로 이동된다."] = {
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

            # --- 일반 주문접수 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  일반 주문접수 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_general_order_acceptance_order_view(flow_tester)
                overall_results["모바일 주문 접수 페이지로 이동된다."] = {
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

            # --- 사전계약 주문접수 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  사전계약 주문접수 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_pre_ordering_view(flow_tester)
                overall_results["사전계약 고객 리스트(재렌탈 사전계약) 페이지로 이동된다. (CL/HC 조직만 가능)"] = {
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

            # --- 주문현황 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  주문현황 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_general_order_status_view(flow_tester)
                overall_results["모바일 주문 주문현황 페이지로 이동된다."] = {
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
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"전체메뉴>주문 테스트 확인 실패: {e}"

        # 전체메뉴 > 프로모션 테스트 실행
        try:
            # --- 고객 프로모션 목록 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  고객 프로모션 목록 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_customer_promotion_view(flow_tester)
                overall_results["고객 프로모션 목록 화면으로 이동된다."] = {
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
                overall_test_message = f"고객 프로모션 목록 화면 이동 노출 확인 실패: {e}"

            # --- 판매인 프로모션 목록 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  판매인 프로모션 목록 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_salesperson_promotion(flow_tester)
                overall_results["판매인 프로모션 목록 화면으로 이동된다."] = {
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
                overall_test_message = f"판매인 프로모션 목록 화면 이동 노출 확인 실패: {e}"
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"전체메뉴>프로모션 테스트 확인 실패: {e}"

        # 전체메뉴 > 공유 콘텐츠/자료실 테스트 실행
        try:
            # --- 라이프스토리 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  라이프스토리 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_shared_content_lifestory(flow_tester)
                overall_results["라이프스토리 화면으로 이동된다."] = {
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
                overall_test_message = f"라이프스토리 화면 이동 확인 실패: {e}"

            # --- e카탈로그 탭 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  e카탈로그 탭 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_shared_content_ecatalog(flow_tester)
                overall_results["라이브러리 > e카탈로그 탭 화면으로 이동된다."] = {
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
                overall_test_message = f"e카탈로그 탭 화면 이동 확인 실패: {e}"

            # --- 제품 사용설명서 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  제품 사용설명서 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_shared_content_productguide(flow_tester)
                overall_results["라이브러리 > 제품 사용설명서 탭 화면으로 이동된다."] = {
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
                overall_test_message = f"제품 사용설명서 화면 이동 노출 확인 실패: {e}"
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"전체메뉴>프로모션 테스트 확인 실패: {e}"

        # 전체메뉴 > 기타/설정 테스트 실행
        try:

            # --- 공지사항 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  공지사항 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_etc_Notice(flow_tester)
                overall_results["공지사항 화면으로 이동된다."] = {
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
                overall_test_message = f"공지사항 화면 이동 확인 실패: {e}"

            # --- 셀프 홍보영상 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  셀프 홍보영상 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_etc_self_promotional_video(flow_tester)
                overall_results["셀프 홍보영상 화면으로 이동된다."] = {
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
                overall_test_message = f"셀프 홍보영상 화면 이동 확인 실패: {e}"

            # --- 설정 화면 이동 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  설정 화면 이동 확인 ---")
                my_page_view_passed, my_page_view_message = test_etc_setting_view(flow_tester)
                overall_results["설정 화면으로 이동된다."] = {
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
                overall_test_message = f"설정 화면 이동 확인 실패: {e}"

            # --- 설정 > 알림 기능 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  설정 > 알림 기능 확인 ---")
                my_page_view_passed, my_page_view_message = test_etc_setting_set_notifications(flow_tester)
                overall_results["PUSH 설정 및 수신동의를 ON / OFF 진행 할 수 있다."] = {
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
                overall_test_message = f"설정 > 알림 기능 확인 실패: {e}"

            # --- 설정 > 전화알림 기능 확인 테스트 수행(권한 획득 여부에 따라) ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  설정 > 전화알림 기능 확인 ---")
                """
                copy_text_business_card_button_click_passed, copy_text_business_card_button_click_message = test_copy_text_business_card_button_view(
                    flow_tester)

                overall_results["전화 알림 기능을 On/Off 할수 있다. (권한 획득 여부에 따라)] = {
                    "test_no": test_no,  # 동적 번호 할당
                    "passed": copy_text_business_card_button_click_passed,
                    "message": copy_text_business_card_button_click_message
                }
                if not copy_text_business_card_button_click_passed:
                    overall_test_passed = False  # Mark overall test as failed
                    overall_test_message = "일부 전체메뉴 클릭 테스트 시나리오에서 실패가 발생했습니다. 상세 로그를 확인하세요."
                # 스프레드시트에 테스트 결과 기록
                status = "Pass" if copy_text_business_card_button_click_passed else "Fail"
                """
                # 자동화 테스트 임시 제외 (코디 계정으로 로그인해서 확인 필요)
                update_test_result_in_sheet(sheets_service, test_no, "No Run", tester_name)
                print(f"{test_no} 테스트 케이스 완료.")
                print("-" * 50)  # Separator
            except Exception as e:
                overall_test_passed = False
                overall_test_message = f"설정 > 전화알림 기능 확인 실패: {e}"

            # --- 설정 > 로그아웃 기능 확인 테스트 실행 ---
            try:
                test_no_counter += 1
                test_no = f"Seller app checklist-{test_no_counter}"
                print(f"\n--- {test_no}:  설정 > 로그아웃 기능 확인 ---")
                my_page_view_passed, my_page_view_message = test_etc_setting_sign_out(flow_tester)
                overall_results["로그아웃을 묻는 팝업 창이 출력된다."] = {
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
                overall_test_message = f"설정 > 로그아웃 기능 확인 실패: {e}"
        except Exception as e:
            overall_test_passed = False
            overall_test_message = f"전체메뉴>기타/설정 테스트 확인 실패: {e}"

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