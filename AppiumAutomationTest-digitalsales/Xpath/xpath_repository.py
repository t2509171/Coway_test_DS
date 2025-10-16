# Xpath/xpath_repository.py

class BaseLocators:
    """
    플랫폼별 로케이터 클래스를 그룹화하는 기본 클래스입니다.
    """
    class AOS:
        pass

    class IOS:
        # iOS 로케이터는 accessibility_id나 name을 사용하는 것이 더 안정적일 수 있습니다.
        # 예시: home_button = "homeButtonAccessibilityId"
        pass

class UpdateKilLocators(BaseLocators):
    """
    Update_kil 폴더의 테스트에서 사용되는 로케이터
    """
    class AOS(BaseLocators.AOS):
        # --- test_app_permissions.py ---
        permission_guide_title = '//android.widget.TextView[@text="디지털세일즈 앱 사용 접근 권한 안내"]'
        required_perms_xpath = '//android.widget.TextView[@text="필수적 접근권한"]'
        optional_perms_xpath = '//android.widget.TextView[@text="선택적 접근권한"]'
        permission_item_template = '//android.view.View[@text="{permission_name}"]'
        confirm_button_xpath = '//android.widget.Button[@text="확인"]'
        login_button_xpath = '//android.widget.Button[@text="로그인"]'
        permission_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        latest_version_xpath = '//android.widget.TextView[@text="최신 버전 입니다."]'

        # --- test_update_alert.py ---
        permission_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
        confirm_button_xpath_system = '//android.widget.Button[@resource-id="android:id/button1"]'
        switch_xpath = '//android.widget.Switch[@resource-id="android:id/switch_widget"]'
        update_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
        allow_notification_switch_xpath = '//android.widget.Switch[@content-desc="알림 허용"]'
        install_confirm_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_confirm_question_update"]'
        install_success_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_success"]'
        login_id_field_xpath = '//android.webkit.WebView[@text="Coway"]'

    class IOS(BaseLocators.IOS):
        # 예시: permission_guide_title = '//XCUIElementTypeStaticText[@name="디지털세일즈 앱 사용 접근 권한 안내"]'
        pass


class LoginLocators(BaseLocators):
    """
    Login 폴더의 테스트에서 사용되는 로케이터
    """
    class AOS(BaseLocators.AOS):
        id_field = '//android.widget.EditText[@resource-id="id"]'
        pwd_field = '//android.widget.EditText[@resource-id="pwd"]'
        auto_login_checkbox = '//android.widget.CheckBox[@resource-id="autoLogin"]'
        login_button = '//android.widget.Button[@text="로그인"]'
        error_message_xpath = '//android.widget.TextView[@text="업무포탈 통합계정 정보를 확인해 주세요."]'
        main_page_element_locator = '//android.widget.TextView[@text="디지털세일즈"]'
        login_page_title_xpath = '//android.widget.TextView[@text="디지털 세일즈"]'
        login_page_id_title_xpath = '//android.widget.TextView[@text="아이디"]'
        login_page_pw_title_xpath = '//android.widget.TextView[@text="비밀번호"]'
        password_change_button_xpath = '//android.widget.Button[@text="비밀번호 변경"]'
        password_reset_button_xpath = '//android.widget.Button[@text="비밀번호 초기화"]'

    class IOS(BaseLocators.IOS):
        # 예시: id_field = '//XCUIElementTypeTextField[@name="id"]'
        pass

class HomeKilLocators(BaseLocators):
    """
    Home_kil 폴더의 테스트에서 사용되는 로케이터
    """
    class AOS(BaseLocators.AOS):
        banner_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[4]/android.view.View'
        home_container_xpath = '//android.view.View[@content-desc="홈"]'
        notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        first_item_xpath = '(//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]/android.view.View)[1]'
        notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'
        full_menu_button = '//android.view.View[@content-desc="전체메뉴"]'
        full_menu_sidenav = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
        management_customer = '//android.view.View[@content-desc="관리고객"]'
        management_customer_title = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        mobile_order = '//android.view.View[@content-desc="모바일 주문"]'
        mobile_order_title = '(//android.widget.TextView[@text="모바일 주문"])[1]'
        my_page = '//android.view.View[@content-desc="마이페이지"]'
        my_page_title = '(//android.widget.TextView[@text="마이페이지"])[1]'
        target_text_xpath = '//android.widget.TextView[@text="제품 바로가기"]'
        water_purifier_xpath = '//android.view.View[@content-desc="정수기"]'
        target_menu_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'
        final_title_xpath = '//android.widget.TextView[@text="프로모션"]'
        sales_sort_button_xpath = '//android.widget.Button[@text="판매순"]'
        title_xpath = '//android.view.View[@content-desc="공유할 영업 콘텐츠를 추천 드려요"]'
        sort_button_xpath = '//android.widget.Button[@text="신규"]'
        final_page_text_xpath = '//android.widget.TextView[@text="라이프스토리"]'
        sales_tip_xpath = '//android.widget.TextView[@text="공지사항으로 이동하기 >"]'
        search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
        search_page_title_xpath = '//android.widget.TextView[@text="검색"]'
        unit_container_xpath = '//android.widget.Button[@text="판매순"]' # Product Unit
        unit_index_xpath = '//android.widget.TextView[@text="1"]'
        content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]' # Product Unit
        gallery_link_xpath = '//android.widget.TextView[@text="코웨이 갤러리 체험 공유하기"]'
        share_button_xpath = '//android.widget.Button[@resource-id="gallery-promotion-share-button"]'
        facebook_option_xpath = '//android.widget.TextView[@text="페이스북"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        facebook_webview_xpath = '//android.webkit.WebView[@text="Facebook에 공유"]'

    class IOS(BaseLocators.IOS):
        pass

class HomeViewKilLocators(BaseLocators):
    """
    Home_View_kil 폴더의 테스트에서 사용되는 로케이터
    """
    class AOS(BaseLocators.AOS):
        ai_cody_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
        ai_cody_title_xpath = '//android.widget.TextView[@text="AI 코디 비서"]'
        input_field_xpath = '//android.widget.EditText[@resource-id="txtBotMessage"]'
        send_button_xpath = '//android.widget.Button[@text="전송"]'
        error_message_xpath = '//android.widget.TextView[@text="답변을 생성할 수 없습니다. 잠시 후 다시 시도해 주세요."]'
        ambiguous_message_xpath = '//android.widget.TextView[@text="말씀하신 내용을 제가 정확히 파악하기 어렵네요. 혹시 다음 키워드 중 궁금하신 점이 있으신가요?"]'
        other_keyword_button_xpath = '//android.widget.Button[@text="다른 키워드 선택"]'
        greeting_button_xpath = '//android.widget.Button[@text="안녕하세요. 무엇을 도와드릴까요?"]'
        sidenav_button_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
        home_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
        description_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[1]'
        large_font_button_xpath = '//android.widget.Button[@text="큰글씨"]'
        managed_customer_button_xpath = '//android.widget.Button[@text="관리고객"]'
        recommendation_text_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[2]'
        webview_xpath = '//android.webkit.WebView[@text="Seller AI"]'

    class IOS(BaseLocators.IOS):
        pass