# Xpath/xpath_repository.py

class UpdateKilLocators:
    """Update_kil 폴더 테스트용 로케이터"""

    class AOS:
        permission_guide_title = '//android.widget.TextView[@text="디지털세일즈 앱 사용 접근 권한 안내"]'
        required_perms_xpath = '//android.widget.TextView[@text="필수적 접근권한"]'
        optional_perms_xpath = '//android.widget.TextView[@text="선택적 접근권한"]'
        confirm_button_text_xpath = '//android.widget.Button[@text="확인"]'
        permission_item_template = '//android.view.View[@text="{permission_name}"]' # 사용되지 않지만 유지
        permission_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        login_button_xpath = '//android.widget.Button[@text="로그인"]'
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        latest_version_xpath = '//android.widget.TextView[@text="최신 버전 입니다."]' # 사용되지 않지만 유지
        # test_update_alert.py 내 변수명 사용
        permission_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]' # system_message_xpath 와 동일값
        update_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]' # system_message_xpath 와 동일값
        confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]' # confirm_button_system_xpath 와 동일값
        switch_xpath = '//android.widget.Switch[@resource-id="android:id/switch_widget"]'
        allow_notification_switch_xpath = '//android.widget.Switch[@content-desc="알림 허용"]'
        install_confirm_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_confirm_question_update"]'
        install_success_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_success"]'
        login_id_field_xpath = '//android.webkit.WebView[@text="Coway"]'

    class IOS:
        permission_guide_title = None
        required_perms_xpath = None
        optional_perms_xpath = None
        confirm_button_text_xpath = None
        permission_item_template = None
        permission_button_xpath = None
        login_button_xpath = None
        menu_button_xpath = None
        latest_version_xpath = None
        permission_alert_msg_xpath = None
        update_alert_msg_xpath = None
        confirm_button_xpath = None
        switch_xpath = None
        allow_notification_switch_xpath = None
        install_confirm_xpath = None
        install_success_xpath = None
        login_id_field_xpath = None


class LoginLocators:
    """Login 폴더 테스트용 로케이터"""

    class AOS:
        id_field = '//android.widget.EditText[@resource-id="id"]'
        pwd_field = '//android.widget.EditText[@resource-id="pwd"]'
        auto_login_checkbox_locator = '//android.widget.CheckBox[@resource-id="autoLogin"]'
        login_button = '//android.widget.Button[@text="로그인"]'
        error_message_xpath = '//android.widget.TextView[@text="업무포탈 통합계정 정보를 확인해 주세요."]'
        main_page_element_locator = '//android.widget.TextView[@text="디지털세일즈"]'
        login_page_title_xpath = '//android.widget.TextView[@text="디지털 세일즈"]'
        login_page_id_title_xpath = '//android.widget.TextView[@text="아이디"]'
        login_page_pw_title_xpath = '//android.widget.TextView[@text="비밀번호"]'
        password_change_button_xpath = '//android.widget.Button[@text="비밀번호 변경"]'
        password_reset_button_xpath = '//android.widget.Button[@text="비밀번호 초기화"]'

    class IOS:
        id_field = None
        pwd_field = None
        auto_login_checkbox_locator = None
        login_button = None
        error_message_xpath = None
        main_page_element_locator = '//XCUIElementTypeOther[@name="디지털세일즈"]'
        login_page_title_xpath = None
        login_page_id_title_xpath = None
        login_page_pw_title_xpath = None
        password_change_button_xpath = None
        password_reset_button_xpath = None

# --- [추가됨] ---
class HomeKilLocators:
    """Home_kil 폴더 테스트용 로케이터"""

    class AOS:
        # --- 명시적으로 정의된 공통 XPath ---
        home_button_xpath = '//android.view.View[@content-desc="홈"]' # home_container_xpath 로 사용됨
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]' # full_menu_button 로 사용됨
        sidenav_button_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button' # full_menu_sidenav 로 사용됨
        digital_sales_title_xpath = '//android.widget.TextView[@text="디지털세일즈"]' # banner_xpath 로 사용됨 (test_item)
        mobile_order_button_xpath = '//android.view.View[@content-desc="모바일 주문"]' # mobile_order_xpath 로 사용됨
        mypage_icon_xpath = '(//android.view.View[@content-desc="마이페이지"])[1]' # my_page_xpath 로 사용됨
        mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]' # my_page_title_xpath 로 사용됨
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]' # final_title_xpath 로 사용됨 (test_promotion)
        sales_sort_button_xpath = '//android.widget.Button[@text="판매순"]' # target_text_xpath, sales_sort_button_xpath, unit_container_xpath 로 사용됨
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]' # final_page_text_xpath, content_detail_page_title_xpath 로 사용됨
        search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]' # facebook_option_xpath 로 사용됨

        # --- HomeKil 고유 XPath ---
        # test_banner.py
        # banner_xpath 는 로컬 XPath 사용

        # test_gallery_sharing.py
        gallery_link_xpath = '//android.widget.TextView[@text="코웨이 갤러리 체험 공유하기"]'
        share_button_gallery_xpath = '//android.widget.Button[@resource-id="gallery-promotion-share-button"]' # share_button_xpath 로 사용됨
        facebook_webview_xpath = '//android.webkit.WebView[@text="Facebook에 공유"]'

        # test_home_etc.py
        notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        first_item_xpath = '(//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]/android.view.View)[1]'
        notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'

        # test_item.py
        management_customer_xpath = '//android.view.View[@content-desc="관리고객"]'
        management_customer_title_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        mobile_order_title_xpath = '(//android.widget.TextView[@text="모바일 주문"])[1]'

        # test_product_shortcuts.py
        target_text_xpath = '//android.widget.TextView[@text="제품 바로가기"]'
        water_purifier_xpath = '//android.view.View[@content-desc="정수기"]'

        # test_promotion.py
        target_menu_xpath = '//android.widget.TextView[@text="판매인 프로모션"]'
        # final_title_xpath 은 promotion_title_xpath 사용

        # test_recommended_products.py
        # target_text_xpath 은 sales_sort_button_xpath 사용
        # sales_sort_button_xpath 중복 정의

        # test_sales_content.py
        title_xpath = '//android.view.View[@content-desc="공유할 영업 콘텐츠를 추천 드려요"]'
        sort_button_xpath = '//android.widget.Button[@text="신규"]'
        # final_page_text_xpath 은 lifestory_title_xpath 사용

        # test_sales_tip.py
        sales_tip_xpath = '//android.widget.TextView[@text="공지사항으로 이동하기 >"]'

        # test_search.py
        search_page_title_xpath = '//android.widget.TextView[@text="검색"]'

        # test_units.py
        unit_container_xpath = '//android.widget.Button[@text="판매순"]' # product_unit 에서 사용 (sales_sort_button_xpath와 동일)
        unit_index_xpath = '//android.widget.TextView[@text="1"]'
        content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]' # product_unit 에서 사용
        # content_unit 에서는 title_xpath, lifestory_title_xpath 사용
        # client_unit 에서는 로컬 XPath 사용


    class IOS:
        # --- 명시적으로 정의된 공통 XPath ---
        home_button_xpath = '//XCUIElementTypeLink[@name="홈"]'
        menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        sidenav_button_xpath = None
        digital_sales_title_xpath = '//XCUIElementTypeOther[@name="디지털세일즈"]'
        mobile_order_button_xpath = '//XCUIElementTypeLink[@name="모바일 주문"]'
        mypage_icon_xpath = '(//XCUIElementTypeLink[@name="마이페이지"])[1]'
        mypage_title_xpath = '(//XCUIElementTypeStaticText[@name="마이페이지"])[1]'
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]' # IOS 값 필요
        sales_sort_button_xpath = '' # IOS 값 필요
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]' # IOS 값 필요
        search_button_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeButton[1]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]' # IOS 값 필요
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]' # IOS 값 필요

        # --- HomeKil 고유 XPath ---
        notice_container_xpath = '(//XCUIElementTypeButton[@name="닫기"])'
        first_item_xpath = '(//XCUIElementTypeButton[@name="닫기"])[1]'
        notice_page_title_xpath = '//XCUIElementTypeStaticText[@name="공지사항"]'
        management_customer_xpath = '(//XCUIElementTypeLink[@name="라이프스토리"])[3]'
        management_customer_title_xpath = None # Base 값 사용 불가
        mobile_order_title_xpath = '//XCUIElementTypeLink[@name="모바일 주문"]'
        target_text_xpath = '//XCUIElementTypeOther[@name="제품 바로가기"]'
        water_purifier_xpath = '(//XCUIElementTypeLink[@name="정수기"])[1]'
        target_menu_xpath = '//XCUIElementTypeLink[@name="판매인 프로모션" and @value="2"]'
        title_xpath = '//XCUIElementTypeLink[@name="공유할 영업 콘텐츠를 추천 드려요"]'
        sort_button_xpath = '//XCUIElementTypeButton[@name="신규"]'
        sales_tip_xpath = '//XCUIElementTypeStaticText[@name="공지사항으로 이동하기 >"]'
        search_page_title_xpath = '//XCUIElementTypeStaticText[@name="검색"]'
        unit_container_xpath = '' # IOS 값 필요
        unit_index_xpath = '//XCUIElementTypeStaticText[@name="2"]'
        content_detail_page_title_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]'
        gallery_link_xpath = None
        share_button_gallery_xpath = None
        facebook_webview_xpath = '//XCUIElementTypeStaticText[@name="페이스북"]'

# --- [추가 완료] ---

class SearchLocators:
    """Search 폴더 테스트용 로케이터"""

    class AOS:
        search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
        recent_Search_Words_details_view_xpath = '//android.widget.ListView'
        recent_product_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        popular_search_details_view_xpath = '//android.widget.ListView'
        ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        search_input_xpath = '//android.widget.EditText'
        search_result_text_xpath = '//android.widget.TextView[contains(@text, "총 ")]'

    class IOS:
        search_button_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeButton[1]'
        recent_Search_Words_details_view_xpath = None
        recent_product_details_view_xpath = None
        popular_search_details_view_xpath = None
        ls_dv_tab1_details_view_xpath = None
        search_input_xpath = None
        search_result_text_xpath = '//XCUIElementTypeStaticText[@name="총 "]'


class MyPageKilLocators:
    """My_Page_kil 폴더 테스트용 로케이터"""

    class AOS:
        greeting_label_xpath = '//android.widget.TextView[@text="인사말"]'
        greeting_text_xpath = '//android.widget.TextView[@text="인사말"]/following-sibling::android.widget.TextView[1]'
        edit_button_xpath = '//android.widget.Button[@text="편집"]'
        edit_field_xpath = '//android.widget.EditText'
        dialog_confirm_button_xpath = '//android.app.Dialog/android.widget.Button'
        download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'
        confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
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
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        mypage_icon_xpath = '(//android.view.View[@content-desc="마이페이지"])[1]'
        mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
        share_button_xpath = '//android.view.View[@text="공유하기"]' # test_my_page_view.py 내 변수명 사용 (Base와 다름)
        share_page_title_xpath = '//android.widget.TextView[@text="공유하기"]'
        total_share_count_xpath = '//android.widget.TextView[contains(@text, "총 공유")]'
        channel_count_xpath_template = '//android.view.View[.//android.widget.TextView[@text="{channel_name}"]]//android.widget.TextView[contains(@text, "건")]'
        item_xpath_template = '//android.widget.TextView[@text="{item}"]'
        share_element_xpath = '//android.widget.TextView[@text="콘텐츠 공유 현황"]'
        total_order_xpath = '//android.widget.TextView[@text="총주문"]'
        net_order_complete_xpath = '//android.widget.TextView[@text="순주문완료"]'


    class IOS:
        greeting_label_xpath = None
        greeting_text_xpath = None
        edit_button_xpath = None
        edit_field_xpath = None
        dialog_confirm_button_xpath = None
        download_button_xpath = None
        confirm_button_xpath = None
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
        menu_button_xpath = None
        mypage_icon_xpath = None
        mypage_title_xpath = None
        share_button_xpath = None
        share_page_title_xpath = None
        total_share_count_xpath = None
        channel_count_xpath_template = None
        item_xpath_template = None
        share_element_xpath = None
        total_order_xpath = None
        net_order_complete_xpath = None


class MobileOrderLocators:
    """Mobile_Order 폴더 테스트용 로케이터"""

    class AOS:
        home_main_element_xpath = '//android.view.View[@content-desc="홈"]'
        mobile_order_button_xpath = '//android.view.View[@content-desc="모바일 주문"]'
        order_start_title_xpath = '//android.widget.TextView[@text="주문 시작하기"]'
        general_order_button_xpath = '//android.widget.Button[@text="일반 주문하기"]'
        order_receipt_title_xpath = '//android.widget.TextView[@text="주문접수"]'
        confirm_button_xpath = '//android.widget.Button[@text="확인"]'
        pre_contract_order_button_xpath = '//android.widget.Button[@text="사전계약 주문하기"]'
        re_rental_pre_contract_title_xpath = '//android.widget.TextView[@text="재렌탈 사전계약"]'
        general_order_text_xpath = '//android.widget.TextView[@text="일반주문"]'
        general_tab_title_xpath = '//android.view.View[@text="일반"]'
        pre_contract_text_xpath = '//android.widget.TextView[@text="사전계약 주문"]'
        pre_contract_tab_title_xpath = '//android.view.View[@text="사전계약"]'
        home_button_xpath = '//android.view.View[@content-desc="홈"]'

    class IOS:
        home_main_element_xpath = '//XCUIElementTypeLink[@name="홈"]'
        mobile_order_button_xpath = '//XCUIElementTypeLink[@name="모바일 주문"]'
        order_start_title_xpath = '//XCUIElementTypeStaticText[@name="주문 시작하기"]'
        general_order_button_xpath = '//XCUIElementTypeButton[@name="일반 주문하기"]'
        order_receipt_title_xpath = '//XCUIElementTypeStaticText[@name="주문접수"]'
        confirm_button_xpath = None
        pre_contract_order_button_xpath = '//XCUIElementTypeButton[@name="사전계약 주문하기"]'
        re_rental_pre_contract_title_xpath = '//XCUIElementTypeStaticText[@name="재렌탈 사전계약"]'
        general_order_text_xpath = '//XCUIElementTypeStaticText[@name="일반주문"]'
        general_tab_title_xpath = '//XCUIElementTypeButton[@name="일반"]'
        pre_contract_text_xpath = '//XCUIElementTypeStaticText[@name="사전계약 주문"]'
        pre_contract_tab_title_xpath = '//XCUIElementTypeButton[@name="사전계약"]'
        home_button_xpath = '//XCUIElementTypeLink[@name="홈"]'


class LifeStoryLocators:
    """Life_Story 폴더 테스트용 로케이터"""

    class AOS:
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        lifestory_button_xpath = '//android.view.View[@content-desc="라이프스토리"]'
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]'
        lifestory_tab_xpath = '//android.widget.ListView'
        lifestory_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        ls_dv_1_title_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        ls_dv_tab1_details_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.view.View[2]'
        ls_dv_tab1_details_title_xpath = '//android.widget.TextView[@text="라이프 스토리"]'
        ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        ls_dv_tab2_title_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        ls_dv_tab2_details_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]/android.view.View[2]'
        ls_dv_tab2_details_title_xpath = '//android.widget.TextView[@text="라이프 스토리"]'
        ls_dv_tab2_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        home_mypage_button_xpath = '//android.view.View[@content-desc="마이페이지"]'
        ls_dv_tab2_Sharing_button_xpath = '(//android.widget.Button[@text="공유하기"])[1]'
        ls_dv_tab2_Sharing_kakao_button_xpath = '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.coway.catalog.seller.stg:id/layout_kakao"]/android.widget.ImageView[2]'
        ls_dv_tab2_Sharing_popup_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        ls_dv_tab2_Sharing_kakao_tab_button_xpath = '//android.widget.TextView[@resource-id="com.kakao.talk:id/txt_title" and @text="친구"]'
        ls_dv_tab2_Sharing_kakao_profile_button_xpath = '(//android.widget.CheckBox[@resource-id="com.kakao.talk:id/check"])[1]'
        ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath = '//android.widget.Button[@resource-id="com.kakao.talk:id/button"]'
        mypage_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'

    class IOS:
        menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        lifestory_button_xpath = None
        lifestory_title_xpath = '//android.widget.TextView[@text="라이프스토리"]'
        lifestory_tab_xpath = None
        lifestory_view_xpath = None
        ls_dv_1_title_xpath = None
        ls_dv_tab1_details_button_xpath = None
        ls_dv_tab1_details_title_xpath = None
        ls_dv_tab1_details_view_xpath = None
        ls_dv_tab2_title_xpath = None
        ls_dv_tab2_details_button_xpath = None
        ls_dv_tab2_details_title_xpath = None
        ls_dv_tab2_details_view_xpath = None
        home_mypage_button_xpath = '(//XCUIElementTypeLink[@name="마이페이지"])[3]'
        ls_dv_tab2_Sharing_button_xpath = '//XCUIElementTypeStaticText[@name="공유하기"]'
        ls_dv_tab2_Sharing_kakao_button_xpath = None
        ls_dv_tab2_Sharing_popup_button_xpath = None
        ls_dv_tab2_Sharing_kakao_tab_button_xpath = None
        ls_dv_tab2_Sharing_kakao_profile_button_xpath = None
        ls_dv_tab2_Sharing_kakao_profile_ok_button_xpath = None
        mypage_title_xpath = '(//XCUIElementTypeStaticText[@name="마이페이지"])[1]'


class ManagedCustomersKilLocators:
    """Managed_Customers_kil 폴더 테스트용 로케이터"""

    class AOS:
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        target_text_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        menu_item_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        title_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        filter1_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[1]'
        result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
        filter2_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[2]'
        filter3_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[3]'

    class IOS:
        menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        target_text_xpath = None
        menu_item_xpath = None
        title_xpath = None
        filter1_xpath = None
        result_count_xpath = None
        filter2_xpath = None
        filter3_xpath = None


class PromotionLocators:
    """Promotion 폴더 테스트용 로케이터"""

    class AOS:
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]' # _navigate_to_full_menu 에서 사용
        customer_promotion_button_xpath = '//android.view.View[@content-desc="고객 프로모션"]'
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'
        promotion_tab_xpath = '//android.widget.ListView'
        promotion_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        customer_promotion_detailed_post_button_xpath = '(//android.view.View[@content-desc="#"])'
        promotion_list_xpath = '//android.widget.Button[@text="목록"]'
        promotion_sharing_xpath = '//android.widget.Button[@text="공유하기"]'
        salesperson_promotion_button_xpath = '//android.view.View[@content-desc="판매인 프로모션"]'

    class IOS:
        all_menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        customer_promotion_button_xpath = '//XCUIElementTypeStaticText[@name="고객 프로모션"]'
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'
        promotion_tab_xpath = None
        promotion_view_xpath = None
        customer_promotion_detailed_post_button_xpath = 'None'
        promotion_list_xpath = None
        promotion_sharing_xpath = None
        salesperson_promotion_button_xpath = '//XCUIElementTypeStaticText[@name="판매인 프로모션"]'


class SelfPvLocators:
    """Self_pv 폴더 테스트용 로케이터"""

    class AOS:
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        self_promotional_video_button_xpath = '//android.view.View[@content-desc="셀프 홍보영상"]'
        self_promotional_video_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]'
        self_promotional_video_search_xpath = '//android.widget.EditText'
        self_promotional_video_bulletin_xpath = '(//android.view.View[@content-desc])[1]'
        self_promotional_video_details_button_xpath = '//android.view.View[contains(@content-desc, "Test")]'
        self_promotional_video_details_title_xpath = '//android.widget.TextView[@text="셀프 홍보영상"]'
        self_promotional_video_dateregistration_xpath = '//android.widget.TextView[@text="등록일"]'
        self_promotional_video_viewers_xpath = '//android.widget.TextView[@text="조회수"]'
        self_promotional_video_earlierarticle_xpath = '//android.view.View[@content-desc="이전글"]'
        self_promotional_video_list_xpath = '//android.view.View[@content-desc="목록"]'
        self_promotional_video_bulletin_list_button_xpath = '//android.view.View[@content-desc="목록"]'
        self_promotional_video_texttitle_xpath = '//android.widget.TextView[@text="셀프 홍보영상 등록 - Sotatek test"]'

    class IOS:
        menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        self_promotional_video_button_xpath = None
        self_promotional_video_title_xpath = None
        self_promotional_video_search_xpath = None
        self_promotional_video_bulletin_xpath = None
        self_promotional_video_details_button_xpath = None
        self_promotional_video_details_title_xpath = None
        self_promotional_video_dateregistration_xpath = None
        self_promotional_video_viewers_xpath = None
        self_promotional_video_earlierarticle_xpath = None
        self_promotional_video_list_xpath = None
        self_promotional_video_bulletin_list_button_xpath = None
        self_promotional_video_texttitle_xpath = None


class SharedContentKilLocators:
    """Shared_Content_kil 폴더 테스트용 로케이터"""

    class AOS:
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
        share_button_xpath = '//android.widget.Button[@text="공유하기"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        download_button_xpath = '//android.widget.Button[@text="다운로드"]'
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]'
        home_button_xpath = '//android.view.View[@content-desc="홈"]'

    class IOS:
        menu_button_xpath = '//XCUIElementTypeLink[@name="전체메뉴"]'
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
        share_button_xpath = '//android.widget.Button[@text="공유하기"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        download_button_xpath = ''
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]'
        home_button_xpath = '//XCUIElementTypeLink[@name="홈"]'


class HomeViewKilLocators:
    """Home_View_kil 폴더 테스트용 로케이터"""

    class AOS:
        home_button_alt_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[3]'
        ai_cody_title_xpath = '//android.widget.TextView[@text="AI 코디 비서"]'
        input_field_xpath = '//android.widget.EditText[@resource-id="txtBotMessage"]'
        send_button_xpath = '//android.widget.Button[@text="전송"]'
        error_message_xpath = '//android.widget.TextView[@text="답변을 생성할 수 없습니다. 잠시 후 다시 시도해 주세요."]'
        ambiguous_message_xpath = '//android.widget.TextView[@text="말씀하신 내용을 제가 정확히 파악하기 어렵네요. 혹시 다음 키워드 중 궁금하신 점이 있으신가요?"]'
        other_keyword_button_xpath = '//android.widget.Button[@text="다른 키워드 선택"]'
        greeting_button_xpath = '//android.widget.Button[@text="안녕하세요. 무엇을 도와드릴까요?"]'
        sidenav_button_xpath = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
        large_font_button_xpath = '//android.widget.Button[@text="큰글씨"]'
        description_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[1]'
        managed_customer_button_xpath = '//android.widget.Button[@text="관리고객"]'
        recommendation_text_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[2]'
        # 추가된 XPath
        first_recommended_question_xpath = '(//android.view.View[@resource-id="root"]/android.view.View[2]/android.widget.ListView[2]/android.widget.Button)[1]'
        chat_message_xpath_template = '//android.widget.TextView[@text="{message_text}"]'
        answer_area_xpath = '//android.view.View[contains(@resource-id,"botMessage")]'
        webview_element_xpath = '//android.webkit.WebView[@text="Seller AI"]'
        answer_link_xpath = '//android.widget.TextView[contains(@text, "http")]'

    class IOS:
        home_button_alt_xpath = '//XCUIElementTypeOther[@name="Coway"]/XCUIElementTypeButton[3]'
        ai_cody_title_xpath = None
        input_field_xpath = None
        send_button_xpath = '//XCUIElementTypeButton[@name="Done"]'
        error_message_xpath = None
        ambiguous_message_xpath = None
        other_keyword_button_xpath = None
        greeting_button_xpath = None
        sidenav_button_xpath = None
        large_font_button_xpath = None
        description_xpath = None
        managed_customer_button_xpath = None
        recommendation_text_xpath = None
        # 추가된 XPath
        first_recommended_question_xpath = None
        chat_message_xpath_template = None
        answer_area_xpath = None
        webview_element_xpath = None
        answer_link_xpath = None