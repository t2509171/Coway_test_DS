import time
import logging

# 로거 설정 (선택 사항이지만 권장)
log = logging.getLogger(__name__)


def switch_to_webview(driver, timeout=10):
    """
    사용 가능한 첫 번째 웹뷰(WEBVIEW) 컨텍스트로 전환합니다.
    전환에 성공하면 True, 실패하면 False를 반환합니다.
    """
    print("웹뷰 컨텍스트로 전환을 시도합니다...")
    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            contexts = driver.contexts
            # print(f"사용 가능한 컨텍스트: {contexts}") # 디버깅 시 사용

            webview_context = next((ctx for ctx in contexts if ctx.startswith('WEBVIEW')), None)

            if webview_context:
                driver.switch_to.context(webview_context)
                print(f"성공: {webview_context} 컨텍스트로 전환되었습니다.")
                # 웹뷰 페이지가 로드될 시간을 잠시 줍니다.
                time.sleep(3)
                return True

        except Exception as e:
            # 드라이버가 아직 컨텍스트를 가져올 준비가 안되었을 수 있음
            log.warning(f"컨텍스트 조회 중 오류 (재시도): {e}")

        time.sleep(0.5)  # 0.5초 간격으로 재시도

    print("실패: 시간 내에 웹뷰 컨텍스트를 찾지 못했습니다.")
    return False


def switch_to_native(driver):
    """
    네이티브 앱(NATIVE_APP) 컨텍스트로 복귀합니다.
    """
    try:
        driver.switch_to.context('NATIVE_APP')
        print("NATIVE_APP 컨텍스트로 복귀했습니다.")
    except Exception as e:
        log.error(f"NATIVE_APP 컨텍스트 복귀 중 오류: {e}")