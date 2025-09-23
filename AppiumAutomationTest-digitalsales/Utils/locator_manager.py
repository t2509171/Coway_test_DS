import json
from appium.webdriver.common.appiumby import AppiumBy
import os

class LocatorManager:
    """
    주석이 포함된 JSON 파일에서 로케이터 정보를 읽어와 반환하는 클래스입니다.
    """

# locator_file_name 인자를 추가
def __init__(self, platform, locator_file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'locators', locator_file_name)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            # JSON 파일을 읽어올 때 주석을 제거하는 로직 추가
            content = f.read()
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                if not line.strip().startswith('//'):
                    cleaned_lines.append(line)
            cleaned_content = '\n'.join(cleaned_lines)

            self.locators = json.loads(cleaned_content)
    except FileNotFoundError:
        raise FileNotFoundError(f"Locator file not found: {json_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON file: {json_path}. Details: {e}")

    self.platform = platform

def get_locator(self, page_locator_name):
    """
    '페이지명_로케이터명' 형식의 이름을 기반으로 로케이터를 가져옵니다.
    예: get_locator("AuthPage_INDIVIDUAL_BUTTON")
    """
    locator_info = self.locators.get(page_locator_name, {}).get(self.platform)

    if not locator_info:
        raise ValueError(f"Locator not found for name: {page_locator_name}, platform: {self.platform}")

    # 문자열 로케이터를 AppiumBy 형식으로 변환합니다.
    locator_type, locator_value = locator_info.split(':', 1)

    if locator_type == 'id':
        return (AppiumBy.ID, locator_value)
    elif locator_type == 'xpath':
        return (AppiumBy.XPATH, locator_value)
    elif locator_type == 'accessibility_id':
        return (AppiumBy.ACCESSIBILITY_ID, locator_value)
    elif locator_type == 'predicate':
        return (AppiumBy.IOS_PREDICATE, locator_value)
    else:
        raise ValueError(f"Unknown locator type: {locator_type}")
