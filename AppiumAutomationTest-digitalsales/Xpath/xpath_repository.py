# Xpath/xpath_repository.py

class BaseLocators:
    """플랫폼별 로케이터 클래스를 그룹화하는 기본 클래스입니다."""

    class AOS:
        pass

    class IOS:
        # iOS는 accessibility_id나 name을 사용하는 것이 더 안정적일 수 있습니다.
        pass


class UpdateKilLocators(BaseLocators):
    """Update_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        permission_guide_title = '//android.widget.TextView[@text="디지털세일즈 앱 사용 접근 권한 안내"]'
        required_perms_xpath = '//android.widget.TextView[@text="필수적 접근권한"]'
        optional_perms_xpath = '//android.widget.TextView[@text="선택적 접근권한"]'
        permission_item_template = '//android.view.View[@text="{permission_name}"]'
        confirm_button_xpath = '//android.widget.Button[@text="확인"]'
        login_button_xpath = '//android.widget.Button[@text="로그인"]'
        permission_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        latest_version_xpath = '//android.widget.TextView[@text="최신 버전 입니다."]'
        permission_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
        confirm_button_xpath_system = '//android.widget.Button[@resource-id="android:id/button1"]'
        switch_xpath = '//android.widget.Switch[@resource-id="android:id/switch_widget"]'
        update_alert_msg_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
        allow_notification_switch_xpath = '//android.widget.Switch[@content-desc="알림 허용"]'
        install_confirm_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_confirm_question_update"]'
        install_success_xpath = '//android.widget.TextView[@resource-id="com.android.packageinstaller:id/install_success"]'
        login_id_field_xpath = '//android.webkit.WebView[@text="Coway"]'

    class IOS(BaseLocators.IOS):
        pass


class LoginLocators(BaseLocators):
    """Login 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
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

    class IOS(BaseLocators.IOS):
        pass

class HomeKilLocators(BaseLocators):
    """Home_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        banner_xpath = '//android.widget.TextView[@text="디지털세일즈"]'
        home_container_xpath = '//android.view.View[@content-desc="홈"]'
        notice_container_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]'
        first_item_xpath = '(//android.view.View[@resource-id="root"]/android.view.View[2]/android.view.View/android.view.View/android.view.View[1]/android.view.View)[1]'
        notice_page_title_xpath = '//android.widget.TextView[@text="공지사항"]'
        full_menu_button = '//android.view.View[@content-desc="전체메뉴"]'
        full_menu_sidenav = '//android.view.View[@resource-id="mySidenav"]/android.view.View[1]/android.widget.Button'
        management_customer_xpath = '//android.view.View[@content-desc="관리고객"]'
        management_customer_title_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        mobile_order_xpath = '//android.view.View[@content-desc="모바일 주문"]'
        mobile_order_title_xpath = '(//android.widget.TextView[@text="모바일 주문"])[1]'
        my_page_xpath = '//android.view.View[@content-desc="마이페이지"]'
        my_page_title_xpath = '(//android.widget.TextView[@text="마이페이지"])[1]'
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
        unit_container_xpath = '//android.widget.Button[@text="판매순"]'
        unit_index_xpath = '//android.widget.TextView[@text="1"]'
        content_detail_page_title_xpath = '//android.view.View[@resource-id="iframe"]'
        gallery_link_xpath = '//android.widget.TextView[@text="코웨이 갤러리 체험 공유하기"]'
        share_button_xpath = '//android.widget.Button[@resource-id="gallery-promotion-share-button"]'
        facebook_option_xpath = '//android.widget.TextView[@text="페이스북"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        facebook_webview_xpath = '//android.webkit.WebView[@text="Facebook에 공유"]'

    class IOS(BaseLocators.IOS):
        pass

class SearchLocators(BaseLocators):
    """Search 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        search_button_xpath = '//android.view.View[@resource-id="root"]/android.view.View[1]/android.view.View/android.widget.Button[1]'
        recent_Search_Words_details_view_xpath = '//android.widget.ListView'
        recent_product_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[3]'
        popular_search_details_view_xpath = '//android.widget.ListView'
        ls_dv_tab1_details_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        search_input_xpath = '//android.widget.EditText'
        search_result_text_xpath = '//android.widget.TextView[contains(@text, "총 ")]'

    class IOS(BaseLocators.IOS):
        pass

class MyPageKilLocators(BaseLocators):
    """My_Page_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        greeting_label_xpath = '//android.widget.TextView[@text="인사말"]'
        initial_greeting_text_xpath = '//android.widget.TextView[@text="항상 고객님만을 생각하겠습니다!!"]'
        edit_button_xpath = '//android.widget.Button[@text="편집"]'
        dialog_confirm_button_xpath = '//android.app.Dialog/android.widget.Button'
        download_button_xpath = '//android.widget.Button[@text="명함 다운로드"]'
        dialog_message_xpath = '//android.widget.TextView[@resource-id="android:id/message"]'
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
        share_button_xpath = '//android.view.View[@text="공유하기"]'
        share_page_title_xpath = '//android.widget.TextView[@text="공유하기"]'
        total_share_count_xpath = '//android.widget.TextView[contains(@text, "총 공유")]'
        channel_count_xpath_template = '//android.view.View[.//android.widget.TextView[@text="{channel_name}"]]//android.widget.TextView[contains(@text, "건")]'
        item_xpath_template = '//android.widget.TextView[@text="{item}"]'
        total_order_xpath = '//android.widget.TextView[@text="총주문"]'
        net_order_complete_xpath = '//android.widget.TextView[@text="순주문완료"]'
        share_element_xpath = '//android.widget.TextView[@text="콘텐츠 공유 현황"]'

    class IOS(BaseLocators.IOS):
        pass

class MobileOrderLocators(BaseLocators):
    """Mobile_Order 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
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

    class IOS(BaseLocators.IOS):
        pass

class LifeStoryLocators(BaseLocators):
    """Life_Story 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
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

    class IOS(BaseLocators.IOS):
        pass


class ManagedCustomersKilLocators(BaseLocators):
    """Managed_Customers_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        target_text_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        menu_item_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        title_xpath = '//android.widget.TextView[@text="관리고객 맞춤 공유하기"]'
        filter1_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[1]'
        result_count_xpath = '//android.widget.TextView[contains(@text, "조회결과")]'
        filter2_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[2]'
        filter3_xpath = '//android.view.View[@resource-id="root"]/android.widget.ListView[2]/android.view.View[3]'

    class IOS(BaseLocators.IOS):
        pass





class PromotionLocators(BaseLocators):
    """Promotion 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        customer_promotion_button_xpath = '//android.view.View[@content-desc="고객 프로모션"]'
        promotion_title_xpath = '//android.widget.TextView[@text="프로모션"]'
        promotion_tab_xpath = '//android.widget.ListView'
        promotion_view_xpath = '//android.view.View[@resource-id="root"]/android.view.View[2]'
        customer_promotion_detailed_post_button_xpath = '(//android.view.View[@content-desc="#"])'
        promotion_list_xpath = '//android.widget.Button[@text="목록"]'
        promotion_sharing_xpath = '//android.widget.Button[@text="공유하기"]'
        salesperson_promotion_button_xpath = '//android.view.View[@content-desc="판매인 프로모션"]'

    class IOS(BaseLocators.IOS):
        pass





class SelfPvLocators(BaseLocators):
    """Self_pv 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        all_menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
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

    class IOS(BaseLocators.IOS):
        pass


class SharedContentKilLocators(BaseLocators):
    """Shared_Content_kil 폴더 테스트용 로케이터"""

    class AOS(BaseLocators.AOS):
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        home_item_xpath = '//android.view.View[@content-desc="홈"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
        share_button_xpath = '//android.widget.Button[@text="공유하기"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        delete_button_xpath = '//android.widget.Button[@text="삭제"]'
        download_button_xpath = '//android.widget.Button[@text="다운로드"]'
        confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]'

    class IOS(BaseLocators.IOS):
        menu_button_xpath = '//android.view.View[@content-desc="전체메뉴"]'
        ecatalog_item_xpath = '//android.view.View[@content-desc="e카탈로그"]'
        home_item_xpath = '//android.view.View[@content-desc="홈"]'
        library_text_xpath = '//android.widget.TextView[@text="라이브러리"]'
        share_button_xpath = '//android.widget.Button[@text="공유하기"]'
        facebook_xpath = '//android.widget.TextView[@text="페이스북"]'
        legal_notice_xpath = '//android.widget.TextView[@resource-id="com.coway.catalog.seller.stg:id/tv_title"]'
        agree_button_xpath = '//android.widget.Button[@resource-id="com.coway.catalog.seller.stg:id/btn_agree"]'
        delete_button_xpath = '//android.widget.Button[@text="삭제"]'
        download_button_xpath = '//android.widget.Button[@text="다운로드"]'
        confirm_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
        manual_item_xpath = '//android.view.View[@content-desc="제품 사용설명서"]'
        kakaotalk_xpath = '//android.widget.TextView[@text="카카오톡"]'
        pass


class HomeViewKilLocators(BaseLocators):
    """Home_View_kil 폴더 테스트용 로케이터"""

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
