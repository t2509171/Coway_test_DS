# 라이브러리 임포트
import os
import sys

# Google Sheets API 연동을 위해 필요한 함수를 임포트
from Utils.test_result_input import update_test_result_in_sheet

from My_Page.test_my_page_view import test_my_page_button_view,test_my_page_button_click
from My_Page.test_business_card import test_business_card_button_view,test_business_card_page_view,test_greeting_edit_button_view,test_download_business_card_button_view,test_copy_text_business_card_button_view
from My_Page.test_share_status import test_sharing_tab_click_view,test_share_count_consistency

# Ensure the Login directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Login')))


def test_my_page_view_run(flow_tester, sheets_service, tester_name):
    """
    모든 로그인 테스트 시나리오 (성공 및 실패)를 실행하고 결과를 종합하여 보고합니다.
    """
    print("=========================================")
    print("   검색 확인 테스트 스위트 시작")
    print("=========================================\n")

    overall_results = {}
    overall_test_passed = True  # Initialize for the overall test result
    overall_test_message = "모든 검색 확인 테스트 시나리오가 성공적으로 완료되었습니다."  # Initialize success message

    # 테스트 체크리스트 번호 동적 생성을 위한 카운터 변수 추가 (시작에서 -1을 한다)
    test_no_counter = 16
