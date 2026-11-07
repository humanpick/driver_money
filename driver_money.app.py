import streamlit as st
import pandas as pd
import datetime
import json

# -----------------------------------------------------------------------------
# 1. 페이지 및 테마 설정 (순수 Streamlit 환경 최적화)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="DRIVER MONEY - 대리·로드탁송 통합 관리",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이버펑크 & 글래스모피즘 CSS (스트림릿 네이티브 요소 커스텀)
st.markdown("""
<style>
    /* 전체 배경 설정 */
    .stApp {
        background-color: #0B1120;
        color: #f1f5f9;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* 라디오 버튼(메뉴) 카드 형태로 변경 */
    div.stRadio > div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.4);
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 8px;
        transition: all 0.3s;
        cursor: pointer;
    }
    div.stRadio > div[role="radiogroup"] > label:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: #8B5CF6;
    }
    /* 라디오 버튼의 기본 원형 마커 숨김 */
    div.stRadio > div[role="radiogroup"] > label > div:first-child { display: none !important; }
    
    /* 메트릭 카드 (통계) 스타일 */
    [data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    .metric-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* 입력 폼 스타일 (고대비) */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stDateInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        color: white !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139,92,246,0.4);
    }
    
    /* 데이터프레임 (표) 헤더 커스텀 */
    th {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 데이터 초기화 (Session State 기반)
# -----------------------------------------------------------------------------
if 'trips' not in st.session_state:
    st.session_state.trips = [
        {"id": "TRIP-1001", "date": "2026-11-07", "type": "로드탁송", "company": "SK로드탁송", "from_loc": "서울 강남구", "to_loc": "부산 해운대구", "freight": 180000, "fuel": 70000, "paid_freight": 0, "paid_fuel": 0, "status": "정산 대기", "due_date": "2026-11-14"},
        {"id": "TRIP-1002", "date": "2026-11-07", "type": "대리운전", "company": "카카오대리", "from_loc": "성남 판교", "to_loc": "인천 송도", "freight": 45000, "fuel": 0, "paid_freight": 45000, "paid_fuel": 0, "status": "정산 완료", "due_date": "2026-11-07"},
        {"id": "TRIP-1003", "date": "2026-11-05", "type": "로드탁송", "company": "오토원탁송", "from_loc": "경기 수원", "to_loc": "대전 유성구", "freight": 200000, "fuel": 50000, "paid_freight": 100000, "paid_fuel": 0, "status": "부분 입금", "due_date": "2026-11-06"}
    ]
if 'expenses' not in st.session_state:
    st.session_state.expenses = [
        {"id": "e1", "date": "2026-11-07", "category": "통행료", "amount": 15400, "memo": "서울-부산 톨게이트"},
        {"id": "e2", "date": "2026-11-07", "category": "복귀 교통비", "amount": 32000, "memo": "KTX 부산-서울"}
    ]

# 핵심 통계 계산 함수
def calculate_stats():
    stats = {
        'today_count': 0, 'today_target': 0, 'today_deposit': 0,
        'unpaid_freight': 0, 'unpaid_fuel': 0, 'total_income': 0, 'total_expense': 0
    }
    today = "2026-11-07"
    for t in st.session_state.trips:
        stats['unpaid_freight'] += (t['freight'] - t['paid_freight'])
        stats['unpaid_fuel'] += (t['fuel'] - t['paid_fuel'])
        stats['total_income'] += t['paid_freight']
        if t['date'] == today:
            stats['today_count'] += 1
            stats['today_target'] += (t['freight'] + t['fuel'])
            stats['today_deposit'] += (t['paid_freight'] + t['paid_fuel'])
            
    for e in st.session_state.expenses:
        stats['total_expense'] += e['amount']
    
    stats['total_unpaid'] = stats['unpaid_freight'] + stats['unpaid_fuel']
    stats['net_profit'] = stats['total_income'] - stats['total_expense']
    return stats

stats = calculate_stats()

# -----------------------------------------------------------------------------
# 3. 사이드바 네비게이션
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #8B5CF6; margin-bottom: 0;'>🚗 DRIVER MONEY</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 0;'>Pro Consignment OS</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "메뉴 선택",
        ["📊 대시보드", "📝 빠른 운행 등록", "📋 전체 운행 내역", "💰 입금 처리 및 미수금", "⛽ 주유비 환급 관리", "💸 지출 관리", "📈 수익 분석", "💾 데이터 백업"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.75rem;'>KST 2026-11-07</p>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 4. 메인 화면 렌더링 로직 (메뉴별 기능)
# -----------------------------------------------------------------------------

# --- [메뉴 1] 대시보드 ---
if menu == "📊 대시보드":
    st.markdown("## 📊 실시간 통합 대시보드")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("오늘 운행 건수", f"{stats['today_count']}건")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-container" style="border-color: rgba(236,72,153,0.3);">', unsafe_allow_html=True)
        st.metric("현재 총 미수금", f"{stats['total_unpaid']:,}원")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-container" style="border-color: rgba(245,158,11,0.3);">', unsafe_allow_html=True)
        st.metric("주유비 환급대기", f"{stats['unpaid_fuel']:,}원")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-container" style="border-color: rgba(16,185,129,0.3);">', unsafe_allow_html=True)
        st.metric("이번달 순수익", f"{stats['net_profit']:,}원")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("### 🚀 최근 등록된 운행 내역")
    df_trips = pd.DataFrame(st.session_state.trips)
    if not df_trips.empty:
        # 데이터프레임 컬럼 순서 및 이름 예쁘게 변경하여 출력
        display_df = df_trips[['date', 'company', 'from_loc', 'to_loc', 'freight', 'fuel', 'status']].copy()
        display_df.columns = ['일자', '업체명', '출발지', '도착지', '탁송비(원)', '선결제주유비(원)', '정산상태']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 운행 내역이 없습니다.")


# --- [메뉴 2] 빠른 운행 등록 ---
elif menu == "📝 빠른 운행 등록":
    st.markdown("## ⚡ 30초 빠른 운행 등록")
    with st.form("trip_form"):
        col1, col2 = st.columns(2)
        with col1:
            t_date = st.date_input("운행 일자", datetime.date(2026,11,7))
            t_type = st.selectbox("운행 종류", ["로드탁송", "대리운전", "개인 직거래", "기타"])
            t_company = st.text_input("업체명", placeholder="예: SK로드탁송")
            t_from = st.text_input("출발지", placeholder="예: 서울 강남")
        with col2:
            t_to = st.text_input("도착지", placeholder="예: 부산 해운대")
            t_freight = st.number_input("탁송비 (원)", value=150000, step=1000)
            t_fuel = st.number_input("기사 선결제 주유비 (원)", value=0, step=1000)
            t_due = st.date_input("정산 예정일", datetime.date(2026,11,14))
            
        submit = st.form_submit_button("운행 내역 저장하기", use_container_width=True)
        if submit:
            new_trip = {
                "id": f"TRIP-{datetime.datetime.now().strftime('%H%M%S')}",
                "date": t_date.strftime("%Y-%m-%d"),
                "type": t_type, "company": t_company, "from_loc": t_from, "to_loc": t_to,
                "freight": int(t_freight), "fuel": int(t_fuel),
                "paid_freight": 0, "paid_fuel": 0,
                "status": "정산 대기", "due_date": t_due.strftime("%Y-%m-%d")
            }
            st.session_state.trips.insert(0, new_trip)
            st.success(f"{t_company} 운행 내역이 성공적으로 저장되었습니다!")


# --- [메뉴 3] 전체 운행 내역 ---
elif menu == "📋 전체 운행 내역":
    st.markdown("## 📋 전체 운행 및 정산 내역")
    df_trips = pd.DataFrame(st.session_state.trips)
    if not df_trips.empty:
        # 미수금 계산 컬럼 추가
        df_trips['unpaid_total'] = (df_trips['freight'] - df_trips['paid_freight']) + (df_trips['fuel'] - df_trips['paid_fuel'])
        
        display_df = df_trips[['date', 'company', 'from_loc', 'to_loc', 'freight', 'fuel', 'status', 'unpaid_total']].copy()
        display_df.columns = ['일자', '업체명', '출발지', '도착지', '탁송비', '주유비', '상태', '남은미수금총액']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 내역이 없습니다.")


# --- [메뉴 4] 입금 처리 및 미수금 ---
elif menu == "💰 입금 처리 및 미수금":
    st.markdown("## 💳 입금 등록 및 미수금 관리")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📥 실시간 입금 처리")
        # 미수금이 있는 운행만 선택옵션으로 제공
        unpaid_trips = [t for t in st.session_state.trips if (t['freight']-t['paid_freight'] + t['fuel']-t['paid_fuel']) > 0]
        
        if unpaid_trips:
            with st.form("deposit_form"):
                trip_options = {t['id']: f"[{t['company']}] {t['from_loc']}→{t['to_loc']} (미수금: {(t['freight']-t['paid_freight'])+(t['fuel']-t['paid_fuel']):,}원)" for t in unpaid_trips}
                selected_trip_id = st.selectbox("입금 대상 운행 선택", options=list(trip_options.keys()), format_func=lambda x: trip_options[x])
                
                d_freight = st.number_input("탁송비 입금액 (원)", value=0, step=1000)
                d_fuel = st.number_input("주유비 환급 입금액 (원)", value=0, step=1000)
                
                d_submit = st.form_submit_button("입금 적용하기")
                if d_submit:
                    for t in st.session_state.trips:
                        if t['id'] == selected_trip_id:
                            t['paid_freight'] += int(d_freight)
                            t['paid_fuel'] += int(d_fuel)
                            
                            total_target = t['freight'] + t['fuel']
                            total_paid = t['paid_freight'] + t['paid_fuel']
                            
                            if total_paid >= total_target: t['status'] = "정산 완료"
                            elif total_paid > 0: t['status'] = "부분 입금"
                            else: t['status'] = "정산 대기"
                            
                    st.success("입금이 정상적으로 반영되었습니다.")
                    st.rerun()
        else:
            st.success("현재 모든 운행의 정산이 완료되었습니다! (미수금 없음)")
            
    with col2:
        st.markdown("### 💬 정산 요청 문자 생성기")
        if unpaid_trips:
            sms_target_id = st.selectbox("문자 발송 대상 선택", options=list(trip_options.keys()), format_func=lambda x: trip_options[x], key="sms_box")
            target = next(t for t in st.session_state.trips if t['id'] == sms_target_id)
            unpaid_fr = target['freight'] - target['paid_freight']
            unpaid_fu = target['fuel'] - target['paid_fuel']
            
            sms_text = f"안녕하세요 {target['company']} 담당자님.\n{target['date']} 진행한 탁송건({target['from_loc']}→{target['to_loc']}) 정산 확인 부탁드립니다.\n\n- 탁송비 미수금: {unpaid_fr:,}원\n- 주유비 환급대기: {unpaid_fu:,}원\n- 총 미정산액: {unpaid_fr + unpaid_fu:,}원\n\n확인 후 입금 부탁드립니다. 감사합니다."
            st.text_area("자동 생성된 문자 내용 (복사해서 카톡/문자로 보내세요)", value=sms_text, height=200)


# --- [메뉴 5] 주유비 환급 관리 ---
elif menu == "⛽ 주유비 환급 관리":
    st.markdown("## ⛽ 주유비 선결제 전용 관리")
    fuel_trips = [t for t in st.session_state.trips if t['fuel'] > 0]
    
    if fuel_trips:
        st.metric("현재 돌려받아야 할 총 주유비", f"{stats['unpaid_fuel']:,}원")
        df_fuel = pd.DataFrame(fuel_trips)
        df_fuel['remain_fuel'] = df_fuel['fuel'] - df_fuel['paid_fuel']
        display_fuel = df_fuel[['date', 'company', 'from_loc', 'to_loc', 'fuel', 'paid_fuel', 'remain_fuel']].copy()
        display_fuel.columns = ['일자', '업체명', '출발지', '도착지', '기사 선결제액', '환급받은 금액', '남은 미환급금']
        st.dataframe(display_fuel, use_container_width=True, hide_index=True)
    else:
        st.info("선결제한 주유비 내역이 없습니다.")


# --- [메뉴 6] 지출 관리 ---
elif menu == "💸 지출 관리":
    st.markdown("## 🧾 사업 및 운행 지출 관리")
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            e_date = st.date_input("지출 일자", datetime.date.today())
            e_cat = st.selectbox("지출 항목", ["통행료", "복귀 교통비", "식비", "차량 유지비", "기타"])
        with col2:
            e_amt = st.number_input("지출 금액 (원)", value=10000, step=1000)
            e_memo = st.text_input("메모", placeholder="예: 톨게이트비")
        
        e_submit = st.form_submit_button("지출 내역 등록")
        if e_submit:
            st.session_state.expenses.insert(0, {
                "id": f"EXP-{datetime.datetime.now().strftime('%H%M%S')}",
                "date": e_date.strftime("%Y-%m-%d"),
                "category": e_cat, "amount": int(e_amt), "memo": e_memo
            })
            st.success("지출 내역이 등록되었습니다!")
            
    st.markdown("### 지출 내역 목록")
    if st.session_state.expenses:
        st.dataframe(pd.DataFrame(st.session_state.expenses)[['date', 'category', 'amount', 'memo']], use_container_width=True, hide_index=True)


# --- [메뉴 7] 수익 분석 ---
elif menu == "📈 수익 분석":
    st.markdown("## 📈 이달의 순수익 분석")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 탁송 수입 (수령완료액)", f"{stats['total_income']:,}원")
    col2.metric("총 사업 지출", f"{stats['total_expense']:,}원")
    col3.metric("최종 순수익", f"{stats['net_profit']:,}원")


# --- [메뉴 8] 데이터 백업 ---
elif menu == "💾 데이터 백업":
    st.markdown("## 💾 안전한 데이터 백업 (JSON)")
    st.write("입력하신 모든 운행 및 지출 데이터를 파일로 안전하게 백업합니다.")
    
    backup_data = {
        "trips": st.session_state.trips,
        "expenses": st.session_state.expenses
    }
    json_str = json.dumps(backup_data, ensure_ascii=False, indent=2)
    
    st.download_button(
        label="📥 전체 백업 데이터 다운로드 (.json)",
        data=json_str,
        file_name=f"DRIVER_MONEY_BACKUP_20261107.json",
        mime="application/json",
        use_container_width=True
    )
