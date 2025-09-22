import sys
import os
import time
from datetime import datetime
import gspread

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 서비스 계정 인증에 필요한 라이브러리 임포트만 남김
from google.oauth2 import service_account

# --- Google 스프레드시트 설정 ---
# 다운로드한 OAuth 클라이언트 ID JSON 파일의 경로를 입력하세요.
# (예: Google Cloud Console에서 다운로드한 'credentials.json' 파일)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CLIENT_SECRET_FILE = os.path.join(project_root, 'coway-qa-autotest-3b54f818ce8f.json')
# 인증 토큰을 저장할 파일 경로. (한번 인증 후 재사용)
TOKEN_FILE = 'token.json'

# 결과를 기록할 Google 스프레드시트 ID를 입력하세요. (스프레드시트 URL에서 확인 가능)
SPREADSHEET_ID = '1WF8mTVaTLJiXzrOmXqlP4LstsPletEi-OdIm2wxOHD0'
# 결과를 기록할 시트 이름을 입력하세요.
SHEET_NAME = 'Digital sales checklist 자동화' # 시트 이름만 필요합니다.

# 필요한 SCOPES: 스프레드시트 읽기/쓰기 권한
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 서비스 계정 키 파일을 사용하여 Google Sheet API 서비스 객체를 반환
def get_google_sheet_service_oauth():
    """
       서비스 계정 키 파일을 사용하여 Google Sheet API 서비스 객체를 반환합니다.
    """
    try:
        # 서비스 계정 키 파일에서 직접 자격 증명 생성
        creds = service_account.Credentials.from_service_account_file(
            CLIENT_SECRET_FILE, scopes=SCOPES)

        service = build('sheets', 'v4', credentials=creds)
        print("Google Sheet API 서비스에 성공적으로 연결되었습니다. (서비스 계정)")
        return service
    except Exception as e:
        print(f"Google Sheet API 서비스 연결 오류: {e}")
        return None

# 'No Run' 자동 입력
def initialize_test_results_in_sheet(service, sheet_name):
    """
    스프레드시트의 L, M, N 열의 데이터를 초기화하고,
    B열에 테스트 ID가 있는 만큼 L열에 'No Run' 텍스트를 입력합니다.
    """
    if not service:
        print("Google Sheet 서비스가 초기화되지 않아 스프레드시트 초기화 작업을 건너뜁니다.")
        return

    try:
        # 1. L, M, N 열의 기존 데이터를 초기화
        clear_range = f'{sheet_name}!L18:N'
        service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=clear_range
        ).execute()
        print(f"✅ 스프레드시트 '{clear_range}' 범위의 데이터가 성공적으로 초기화되었습니다.")

        # 2. B열의 테스트 ID를 읽어와 업데이트할 행의 수를 확인
        read_range = f'{sheet_name}!B18:B'
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=read_range
        ).execute()
        values = result.get('values', [])
        num_rows_to_update = len(values)

        if num_rows_to_update > 0:
            # 3. 'No Run' 텍스트로 채워진 데이터 생성
            no_run_data = [['No Run'] for _ in range(num_rows_to_update)]

            # 4. L열에 'No Run' 텍스트를 일괄 업데이트
            update_range = f'{sheet_name}!L18:L{17 + num_rows_to_update}'
            body = {
                'values': no_run_data
            }
            service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            print(f"✅ '{update_range}' 범위의 L열에 'No Run' 텍스트가 성공적으로 입력되었습니다.")
        else:
            print("경고: B18 열에 테스트 ID가 없어 'No Run' 텍스트를 입력하지 못했습니다.")

    except HttpError as err:
        print(f"Google 스프레드시트 API 오류: {err}")
    except Exception as e:
        print(f"스프레드시트 초기화 중 오류 발생: {e}")

# 테스터 이름 가져오기
def get_tester_name_from_sheet(service, sheet_name):
    """
    지정된 스프레드시트의 K13 셀에서 테스터 이름을 가져옵니다.
    """
    if not service:
        return "Unknown Tester"

    try:
        range_name = f'{sheet_name}!M13'
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        values = result.get('values', [])

        if values and len(values[0]) > 0:
            tester_name = values[0][0].strip()
            print(f"✅ 스프레드시트에서 테스터 이름 '{tester_name}'을 성공적으로 가져왔습니다.")
            return tester_name
        else:
            print(f"경고: 스프레드시트 '{range_name}' 셀에 테스터 이름이 비어있습니다. 기본값으로 'Unknown Tester'를 사용합니다.")
            return "Unknown Tester"
    except HttpError as err:
        print(f"Google 스프레드시트 API 오류: {err}")
        return "Unknown Tester"
    except Exception as e:
        print(f"스프레드시트에서 테스터 이름 읽기 중 오류 발생: {e}")
        return "Unknown Tester"

# 테스트 결과 입력
def update_test_result_in_sheet(service, test_case_id, status, tester_name):
    """
    테스트 케이스 ID에 맞는 행을 찾아 L, M, N열에 테스트 결과(Pass/Fail), Tester, 타임스탬프를 업데이트합니다.
    """
    if not service:
        print("Google Sheet 서비스가 초기화되지 않아 결과를 기록할 수 없습니다.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # B열 전체를 읽어와서 test_case_id에 해당하는 행을 찾습니다.
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!B:B' # B열에서 ID를 찾도록 수정
        ).execute()
        values = result.get('values', [])

        row_to_update = -1
        # 스프레드시트의 행은 1부터 시작하므로, 인덱스에 1을 더합니다.
        for i, row in enumerate(values):
            if row and row[0] == test_case_id:
                row_to_update = i + 1
                break

        if row_to_update != -1:
            # L열: Status, M열: Tester, N열: Timestamp
            update_range = f'{SHEET_NAME}!L{row_to_update}:N{row_to_update}'
            body = {
                'values': [
                    [status, tester_name, timestamp]
                ]
            }
            service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            print(f"스프레드시트 {test_case_id} ({row_to_update}행) 업데이트 완료: Status={status}, Tester='{tester_name}'")
        else:
            print(f"경고: 스프레드시트 B열에서 테스트 케이스 ID '{test_case_id}'를 찾을 수 없습니다. 결과를 업데이트하지 못했습니다.")

    except HttpError as err:
        print(f"Google 스프레드시트 API 오류: {err}")
    except Exception as e:
        print(f"스프레드시트 기록/업데이트 중 오류 발생: {e}")