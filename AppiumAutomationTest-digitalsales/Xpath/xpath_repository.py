# Xpath/xpath_repository.py

class BaseLocators:
    """플랫폼별 로케이터 클래스를 그룹화하는 기본 클래스입니다."""

    class AOS:
        """
        공통 AOS 로케이터
        (파일 전체에서 2회 이상 사용된 XPath 모음)
        """
        # --- 공통 네비게이션 ---
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        home_button_xpath = '//android.view.View[@content-desc="홈"]'
        mypage_icon_xpath = '(//android.view.View[@content-desc="마이페이지"])[1]'
        mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
        sidenav_button_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
        home_button_alt_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'

        # --- 공통 버튼 ---
        confirm_button_text_xpath = '//android.widget.Button[@text="확인"]'
        confirm_button_system_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        share_button_xpath = '//android.widget.Button[@text="공유하기"]'
        delete_button_xpath = '//android.widget.Button[@text="삭제"]'
        download_button_xpath = '//android.widget.Button[@text="다운로드"]'
        login_button_xpath = '//android.widget.Button[@text="로그인"]'
        sales_sort_button_xpath = '//android.widget.Button[@text="판매순"]'
        promotion_list_xpath = '//android.widget.Button[@text="목록"]'

        # --- 공통 페이지/항목 ---
        digital_sales_title_xpath = '//android.widget.TextView[@text="디지털세일즈"]'
        managed_customer_title_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        mobile_order_button_xpath = '//android.view.View[@content-desc="모바일 주문"]'
        lifestory_button_xpath = '//android.view.View[@content-desc="라이프스토리"]'
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]'
        lifestory_details_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.view.View[2]'
        lifestory_details_title_xpath = '//android.widget.TextView[@text="라이프 스토리"]'
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'
        self_promo_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]'
        self_promo_list_button_xpath = '//android.view.View[@content-desc="목록"]'

        # --- 공통 라이브러리/공유 ---
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]'
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'

        # --- 공통 View/Template ---
        system_message_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
        list_view_xpath = '//android.widget.ListView'
        view_root_view3_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        view_root_view2_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        search_input_xpath = '//android.widget.EditText'

    class IOS:
        """
        공통 IOS 로케이터
        (HomeKilLocators.IOS 및 SharedContentKilLocators.IOS에서 가져온 값들입니다.)
        """
        # --- 공통 네비게이션 ---
        menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        home_button_xpath = '//XCUIElementTypeLink[@name="홈"]'
        mypage_icon_xpath = '(//XCUIElementTypeLink[@name="마이페이지"])[1]'
        mypage_title_xpath = '(//XCUIElementTypeStaticText[@name="마이페이지"])[1]'
        search_button_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeButton[1]'
        sidenav_button_xpath = None
        home_button_alt_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeButton[3]'

        # --- 공통 버튼 ---
        confirm_button_text_xpath = ''
        confirm_button_system_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        share_button_xpath = '//android.widget.Button[@text="공유하기"]'
        delete_button_xpath = ''
        download_button_xpath = ''
        login_button_xpath = ''
        sales_sort_button_xpath = ''
        promotion_list_xpath = None

        # --- 공통 페이지/항목 ---
        digital_sales_title_xpath = '//XCUIElementTypeOther[@name="디지털세일즈"]'
        managed_customer_title_xpath = None
        mobile_order_button_xpath = '//XCUIElementTypeLink[@name="모바일 주문"]'
        lifestory_button_xpath = None
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]'
        lifestory_details_button_xpath = None
        lifestory_details_title_xpath = None
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'
        self_promo_title_xpath = None
        self_promo_list_button_xpath = None

        # --- 공통 라이브러리/공유 ---
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]'
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'

        # --- 공통 View/Template ---
        system_message_xpath = None
        list_view_xpath = None
        view_root_view3_xpath = None
        view_root_view2_xpath = None
        search_input_xpath = None


class UpdateKilLocators(BaseLocators):
    """Update_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        permission_guide_title = '//android.widget.TextView[@text="디지털세일즈 앱 사용 접근 권한 안내"]'
        required_perms_xpath = '//android.widget.TextView[@text="필수적 접근권한"]'
        optional_perms_xpath = '//android.widget.TextView[@text="선택적 접근권한"]'
        permission_item_template = '//android.view.View[@text="{permission_name}"]'
        # login_button_xpath (공통)
        permission_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        # menu_button_xpath (공통)
        latest_version_xpath = '//android.widget.TextView[@text="최신 버전 입니다."]'
        # system_message_xpath (공통, 'permission_alert_msg_xpath', 'update_alert_msg_xpath')
        # confirm_button_system_xpath (공통)
        switch_xpath = '//android.widget.Switch[@resource-id="android:id/switch_widget"]'
        allow_notification_switch_xpath = '//android.widget.Switch[@content-desc="알림 허용"]'
        install_confirm_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_confirm_question_update"]'
        install_success_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_success"]'
        login_id_field_xpath = '//android.webkit.WebView[@text="Coway"]'

    class IOS(BaseLocators.IOS):
        permission_guide_title = None
        required_perms_xpath = None
        optional_perms_xpath = None
        permission_item_template = None
        permission_button_xpath = None
        latest_version_xpath = None
        switch_xpath = None
        allow_notification_switch_xpath = None
        install_confirm_xpath = None
        install_success_xpath = None
        login_id_field_xpath = None


class LoginLocators(BaseLocators):
    """Login 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        id_field = '//android.widget.EditText[@resource-id="id"]'
        pwd_field = '//android.widget.EditText[@resource-id="pwd"]'
        auto_login_checkbox_locator = '//android.widget.CheckBox[@resource-id="autoLogin"]'
        # login_button_xpath (공통, 'login_button')
        error_message_xpath = '//android.widget.TextView[@text="업무포탈 통합계정 정보를 확인해 주세요."]'
        # digital_sales_title_xpath (공통, 'main_page_element_locator')
        login_page_title_xpath = '//android.widget.TextView[@text="디지털 세일즈"]'
        login_page_id_title_xpath = '//android.widget.TextView[@text="아이디"]'
        login_page_pw_title_xpath = '//android.widget.TextView[@text="비밀번호"]'
        password_change_button_xpath = '//android.widget.Button[@text="비밀번호 변경"]'
        password_reset_button_xpath = '//android.widget.Button[@text="비밀번호 초기화"]'

    class IOS(BaseLocators.IOS):
        id_field = None
        pwd_field = None
        auto_login_checkbox_locator = None
        error_message_xpath = None
        login_page_title_xpath = None
        login_page_id_title_xpath = None
        login_page_pw_title_xpath = None
        password_change_button_xpath = None
        password_reset_button_xpath = None


class HomeKilLocators(BaseLocators):
    """Home_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # digital_sales_title_xpath (공통, 'banner_xpath')
        # home_button_xpath (공통)
        notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        first_item_xpath = '(//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]/android.view.View)[1]'
        notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'
        # menu_button_xpath (공통)
        # sidenav_button_xpath (공통, 'full_menu_sidenav')
        management_customer_xpath = '//android.view.View[@content-desc="관리고객"]'
        # managed_customer_title_xpath (공통)
        # mobile_order_button_xpath (공통, 'mobile_order_xpath')
        mobile_order_title_xpath = '(//android.widget.TextView[@text="모바일 주문"])[1]'
        # mypage_icon_xpath (공통)
        # mypage_title_xpath (공통)
        target_text_xpath = '//android.widget.TextView[@text="제품 바로가기"]'
        water_purifier_xpath = '//android.view.View[@content-desc="정수기"]'
        target_menu_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'
        # promotion_title_xpath (공통)
        # sales_sort_button_xpath (공통)
        title_xpath = '//android.view.View[@content-desc="공유할 영업 콘텐츠를 추천 드려요"]'
        sort_button_xpath = '//android.widget.Button[@text="신규"]'
        # lifestory_title_xpath (공통)
        sales_tip_xpath = '//android.widget.TextView[@text="공지사항으로 이동하기 >"]'
        # search_button_xpath (공통)
        search_page_title_xpath = '//android.widget.TextView[@text="검색"]'
        # sales_sort_button_xpath (공통, 'unit_container_xpath')
        unit_index_xpath = '//android.widget.TextView[@text="1"]'
        content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]'
        gallery_link_xpath = '//android.widget.TextView[@text="코웨이 갤러리 체험 공유하기"]'
        share_button_gallery_xpath = '//android.widget.Button[@resource-id="gallery-promotion-share-button"]'
        # facebook_xpath (공통)
        # agree_button_xpath (공통)
        facebook_webview_xpath = '//android.webkit.WebView[@text="Facebook에 공유"]'

    class IOS(BaseLocators.IOS):
        # --- 공통 항목은 BaseLocators.IOS에서 상속됨 ---

        # --- HomeKil 고유 항목 (사용자님께서 제공한 값) ---
        notice_container_xpath = '(//XCUIElementTypeButton[@name="닫기"])'
        first_item_xpath = '(//XCUIElementTypeButton[@name="닫기"])[1]'
        notice_page_title_xpath = '//XCUIElementTypeStaticText[@name="공지사항"]'
        management_customer_xpath = '(//XCUIElementTypeLink[@name="라이프스토리"])[3]'
        mobile_order_title_xpath = '//XCUIElementTypeLink[@name="모바일 주문"]'
        target_text_xpath = '//XCUIElementTypeOther[@name="제품 바로가기"]'
        water_purifier_xpath = '(//XCUIElementTypeLink[@name="정수기"])[1]'
        target_menu_xpath = '//XCUIElementTypeLink[@name="판매인 프로모션" and @value="2"]'
        title_xpath = '//XCUIElementTypeLink[@name="공유할 영업 콘텐츠를 추천 드려요"]'
        sort_button_xpath = '//XCUIElementTypeButton[@name="신규"]'
        sales_tip_xpath = '//XCUIElementTypeStaticText[@name="공지사항으로 이동하기 >"]'
        search_page_title_xpath = '//XCUIElementTypeStaticText[@name="검색"]'
        unit_index_xpath = '//XCUIElementTypeStaticText[@name="2"]'
        content_detail_page_title_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]'
        gallery_link_xpath = None
        share_button_gallery_xpath = None
        facebook_webview_xpath = '//XCUIElementTypeStaticText[@name="페이스북"]'
        pass


class SearchLocators(BaseLocators):
    """Search 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # search_button_xpath (공통)
        # list_view_xpath (공통, 'recent_Search_Words_details_view_xpath', 'popular_search_details_view_xpath')
        # view_root_view3_xpath (공통, 'recent_product_details_view_xpath')
        # view_root_view2_xpath (공통, 'ls_dv_tab1_details_view_xpath')
        # search_input_xpath (공통)
        search_result_text_xpath = '//android.widget.TextView[contains(@text, "총 ")]'

    class IOS(BaseLocators.IOS):
        search_result_text_xpath = '//XCUIElementTypeStaticText[@name="총 "]'


class MyPageKilLocators(BaseLocators):
    """My_Page_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        greeting_label_xpath = '//android.widget.TextView[@text="인사말"]'
        initial_greeting_text_xpath = '//android.widget.TextView[@text="항상 고객님만을 생각하겠습니다!!"]'
        edit_button_xpath = '//android.widget.Button[@text="편집"]'
        dialog_confirm_button_xpath = '//android.app.Dialog/android.widget.Button'
        download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'  # 고유 (Base의 download_button_xpath와 다름)
        # system_message_xpath (공통, 'dialog_message_xpath')
        permission_allow_once_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]'
        permission_allow_all_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_all_button"]'
        toast_message_xpath = '//android.widget.Toast'
        business_card_button_xpath = '//android.widget.Button[@text="명함설정"]'
        page_verification_xpath = '//android.widget.TextView[@text="명함 설정"]'
        copy_button_xpath = '//android.widget.Button[@text="텍스트 명함 복사"]'
        dynamic_username_xpath_template = '//android.widget.TextView[@text="안녕하세요\n{username} {title}입니다."]'
        dynamic_title_xpath_template = '//android.widget.TextView[@text="{title}"]'
        dynamic_affiliation_xpath_template = '//android.widget.TextView[contains(@text, "{affiliation}")]'
        dynamic_contact_information_xpath_template = '//android.widget.TextView[@text="{contact_information}"]'
        total_order_label_xpath = '//android.widget.TextView[@text="코디매칭 총주문"]'
        success_order_label_xpath = '//android.widget.TextView[@text="코디매칭 성공"]'
        commission_tab_xpath = '//android.view.View[@text="수수료"]'
        commission_title_xpath = '//android.widget.TextView[@text="수수료"]'
        production_rate_label_xpath = '//android.widget.TextView[@text="생산율"]'
        commission_detail_label_xpath = '//android.widget.TextView[@text="수수료 상세"]'
        # menu_button_xpath (공통)
        # mypage_icon_xpath (공통)
        # mypage_title_xpath (공통)
        share_button_mypage_xpath = '//android.view.View[@text="공유하기"]'  # 고유 (Base의 share_button_xpath와 다름)
        share_page_title_xpath = '//android.widget.TextView[@text="공유하기"]'
        total_share_count_xpath = '//android.widget.TextView[contains(@text, "총 공유")]'
        channel_count_xpath_template = '//android.view.View[.//android.widget.TextView[@text="{channel_name}"]]//android.widget.TextView[contains(@text, "건")]'
        item_xpath_template = '//android.widget.TextView[@text="{item}"]'
        total_order_xpath = '//android.widget.TextView[@text="총주문"]'
        net_order_complete_xpath = '//android.widget.TextView[@text="순주문완료"]'
        share_element_xpath = '//android.widget.TextView[@text="콘텐츠 공유 현황"]'

    class IOS(BaseLocators.IOS):
        greeting_label_xpath = None
        initial_greeting_text_xpath = None
        edit_button_xpath = None
        dialog_confirm_button_xpath = None
        download_button_xpath = None
        permission_allow_once_button_xpath = None
        permission_allow_all_button_xpath = None
        toast_message_xpath = None
        business_card_button_xpath = None
        page_verification_xpath = None
        copy_button_xpath = None
        dynamic_username_xpath_template = None
        dynamic_title_xpath_template = None
        dynamic_affiliation_xpath_template = None
        dynamic_contact_information_xpath_template = None
        total_order_label_xpath = None
        success_order_label_xpath = None
        commission_tab_xpath = None
        commission_title_xpath = None
        production_rate_label_xpath = None
        commission_detail_label_xpath = None
        share_button_mypage_xpath = None
        share_page_title_xpath = None
        total_share_count_xpath = None
        channel_count_xpath_template = None
        item_xpath_template = None
        total_order_xpath = None
        net_order_complete_xpath = None
        share_element_xpath = None


class MobileOrderLocators(BaseLocators):
    """Mobile_Order 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # home_button_xpath (공통)
        # mobile_order_button_xpath (공통)
        order_start_title_xpath = '//android.widget.TextView[@text="주문 시작하기"]'
        general_order_button_xpath = '//android.widget.Button[@text="일반 주문하기"]'
        order_receipt_title_xpath = '//android.widget.TextView[@text="주문접수"]'
        # confirm_button_text_xpath (공통)
        pre_contract_order_button_xpath = '//android.widget.Button[@text="사전계약 주문하기"]'
        re_rental_pre_contract_title_xpath = '//android.widget.TextView[@text="재렌탈 사전계약"]'
        general_order_text_xpath = '//android.widget.TextView[@text="일반주문"]'
        general_tab_title_xpath = '//android.view.View[@text="일반"]'
        pre_contract_text_xpath = '//android.widget.TextView[@text="사전계약 주문"]'
        pre_contract_tab_title_xpath = '//android.view.View[@text="사전계약"]'

    class IOS(BaseLocators.IOS):
        order_start_title_xpath = '//XCUIElementTypeStaticText[@name="주문 시작하기"]'
        general_order_button_xpath = '//XCUIElementTypeButton[@name="일반 주문하기"]'
        order_receipt_title_xpath = '//XCUIElementTypeStaticText[@name="주문접수"]'

        pre_contract_order_button_xpath = '//XCUIElementTypeButton[@name="사전계약 주문하기"]'
        re_rental_pre_contract_title_xpath = '//XCUIElementTypeStaticText[@name="재렌탈 사전계약"]'
        general_order_text_xpath = '//XCUIElementTypeStaticText[@name="일반주문"]'
        general_tab_title_xpath = '//XCUIElementTypeButton[@name="일반"]'
        pre_contract_text_xpath = '//XCUIElementTypeStaticText[@name="사전계약 주문"]'
        pre_contract_tab_title_xpath = '//XCUIElementTypeButton[@name="사전계약"]'


class LifeStoryLocators(BaseLocators):
    """Life_Story 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # lifestory_button_xpath (공통)
        # lifestory_title_xpath (공통)
        # list_view_xpath (공통, 'lifestory_tab_xpath')
        # view_root_view3_xpath (공통, 'lifestory_view_xpath', 'ls_dv_1_title_xpath', 'ls_dv_tab2_title_xpath')
        # lifestory_details_button_xpath (공통, 'ls_dv_tab1_details_button_xpath', 'ls_dv_tab2_details_button_xpath')
        # lifestory_details_title_xpath (공통, 'ls_dv_tab1_details_title_xpath', 'ls_dv_tab2_details_title_xpath')
        # view_root_view2_xpath (공통, 'ls_dv_tab1_details_view_xpath', 'ls_dv_tab2_details_view_xpath')
        home_mypage_button_xpath = '//android.view.View[@content-desc="마이페이지"]'  # 고유 (Base의 mypage_icon_xpath와 다름)
        ls_dv_tab2_Sharing_button_xpath = '(//android.widget.Button[@text="공유하기"])[1]'  # 고유 (Base의 share_button_xpath와 다름)
        ls_dv_tab2_Sharing_kakao_button_xpath = '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.coway.catalog.seller.stg:id/layout_kakao"]/android.widget.ImageView[2]'
        # agree_button_xpath (공통)
        ls_dv_tab2_Sharing_kakao_tab_button_xpath = '//android.widget.TextView[@resource-id="com.kakao.talk:id/txt_title" and @text="친구"]'
        ls_dv_tab2_Sharing_kakao_profile_button_xpath = '(//android.widget.CheckBox[@resource-id="com.kakao.talk:id/check"])[1]'
        ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath = '//android.widget.Button[@resource-id="com.kakao.talk:id/button"]'

    class IOS(BaseLocators.IOS):
        home_mypage_button_xpath = '(//XCUIElementTypeLink[@name="마이페이지"])[3]'
        ls_dv_tab2_Sharing_button_xpath = '//XCUIElementTypeStaticText[@name="공유하기"]'
        ls_dv_tab2_Sharing_kakao_button_xpath = None
        ls_dv_tab2_Sharing_kakao_tab_button_xpath = None
        ls_dv_tab2_Sharing_kakao_profile_button_xpath = None
        ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath = None


class ManagedCustomersKilLocators(BaseLocators):
    """Managed_Customers_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # menu_button_xpath (공통)
        # managed_customer_title_xpath (공통, 'target_text_xpath', 'menu_item_xpath', 'title_xpath')
        filter1_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[1]'
        result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
        filter2_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[2]'
        filter3_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[3]'

    class IOS(BaseLocators.IOS):
        filter1_xpath = None
        result_count_xpath = None
        filter2_xpath = None
        filter3_xpath = None


class PromotionLocators(BaseLocators):
    """Promotion 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # menu_button_xpath (공통)
        customer_promotion_button_xpath = '//android.view.View[@content-desc="고객 프로모션"]'
        # promotion_title_xpath (공통)
        # list_view_xpath (공통, 'promotion_tab_xpath')
        # view_root_view2_xpath (공통, 'promotion_view_xpath')
        customer_promotion_detailed_post_button_xpath = '(//android.view.View[@content-desc="#"])'
        # promotion_list_xpath (공통)
        # share_button_xpath (공통)
        salesperson_promotion_button_xpath = '//android.view.View[@content-desc="판매인 프로모션"]'

    class IOS(BaseLocators.IOS):
        customer_promotion_button_xpath = '//XCUIElementTypeStaticText[@name="고객 프로모션"]'
        customer_promotion_detailed_post_button_xpath = 'None'
        salesperson_promotion_button_xpath = '//XCUIElementTypeStaticText[@name="판매인 프로모션"]'


class SelfPvLocators(BaseLocators):
    """Self_pv 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # menu_button_xpath (공통)
        self_promotional_video_button_xpath = '//android.view.View[@content-desc="셀프 홍보영상"]'
        # self_promo_title_xpath (공통, 'self_promotional_video_title_xpath', 'self_promotional_video_details_title_xpath')
        # search_input_xpath (공통, 'self_promotional_video_search_xpath')
        self_promotional_video_bulletin_xpath = '(//android.view.View[@content-desc])[1]'
        self_promotional_video_details_button_xpath = '//android.view.View[contains(@content-desc, "Test")]'
        self_promotional_video_dateregistration_xpath = '//android.widget.TextView[@text="등록일"]'
        self_promotional_video_viewers_xpath = '//android.widget.TextView[@text="조회수"]'
        self_promotional_video_earlierarticle_xpath = '//android.view.View[@content-desc="이전글"]'
        # self_promo_list_button_xpath (공통, 'self_promotional_video_list_xpath', 'self_promotional_video_bulletin_list_button_xpath')
        self_promotional_video_texttitle_xpath = '//android.widget.TextView[@text="셀프 홍보영상 등록 - Sotatek test"]'

    class IOS(BaseLocators.IOS):
        self_promotional_video_button_xpath = None
        self_promotional_video_bulletin_xpath = None
        self_promotional_video_details_button_xpath = None
        self_promotional_video_dateregistration_xpath = None
        self_promotional_video_viewers_xpath = None
        self_promotional_video_earlierarticle_xpath = None
        self_promotional_video_texttitle_xpath = None


class SharedContentKilLocators(BaseLocators):
    """Shared_Content_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # 모든 항목이 BaseLocators.AOS로 이동되었습니다.
        pass

    class IOS(BaseLocators.IOS):
        # 모든 항목이 BaseLocators.IOS로 이동되었습니다.
        pass


class HomeViewKilLocators(BaseLocators):
    """Home_View_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        # home_button_alt_xpath (공통, 'ai_cody_button_xpath', 'home_button_alt_xpath')
        ai_cody_title_xpath = '//android.widget.TextView[@text="AI 코디 비서"]'
        input_field_xpath = '//android.widget.EditText[@resource-id="txtBotMessage"]'
        send_button_xpath = '//android.widget.Button[@text="전송"]'
        error_message_xpath = '//android.widget.TextView[@text="답변을 생성할 수 없습니다. 잠시 후 다시 시도해 주세요."]'
        ambiguous_message_xpath = '//android.widget.TextView[@text="말씀하신 내용을 제가 정확히 파악하기 어렵네요. 혹시 다음 키워드 중 궁금하신 점이 있으신가요?"]'
        other_keyword_button_xpath = '//android.widget.Button[@text="다른 키워드 선택"]'
        greeting_button_xpath = '//android.widget.Button[@text="안녕하세요. 무엇을 도와드릴까요?"]'
        # sidenav_button_xpath (공통)
        description_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[1]'
        large_font_button_xpath = '//android.widget.Button[@text="큰글씨"]'
        managed_customer_button_xpath = '//android.widget.Button[@text="관리고객"]'
        recommendation_text_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[2]'
        webview_xpath = '//android.webkit.WebView[@text="Seller AI"]'

    class IOS(BaseLocators.IOS):
        ai_cody_title_xpath = None
        input_field_xpath = None
        send_button_xpath = '//XCUIElementTypeButton[@name="Done"]'
        error_message_xpath = None
        ambiguous_message_xpath = None
        other_keyword_button_xpath = None
        greeting_button_xpath = None
        description_xpath = None
        large_font_button_xpath = None
        managed_customer_button_xpath = None
        recommendation_text_xpath = None
        webview_xpath = None