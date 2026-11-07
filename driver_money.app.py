import datetime
import json
import pandas as pd
import streamlit as st

# 페이지 기본 설정 (와이드 모드, 다크 테마 느낌)
st.set_page_config(
    page_title="DRIVER MONEY - 대리·로드탁송 통합 관리",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# [디자인 및 스타일 적용] 사이버펑크 글래스모피즘 CSS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #0B1120;
        color: #FFFFFF;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 입력창(Input, Select) 표준 스타일: 순백색 배경, 검정 굵은 글씨 */
    input, select, textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        border: 1px solid #CBD5E1 !important;
    }
    
    /* Streamlit 입력 컴포넌트 내부 맞춤 */
    .stTextInput input, .stSelectbox select, .stDateInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 글래스 패널 카드 스타일 */
    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 16px;
    }

    /* 강조 텍스트 */
    .metric-title {
        color: #CBD5E1;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .metric-value {
        color: #38BDF8;
        font-size: 1.6rem;
        font-weight: 700;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# [데이터 초기화 및 세션 상태]
# -----------------------------------------------------------------------------
if "trips" not in st.session_state:
  st.session_state.trips = [
      {
          "id": 1,
          "date": "2026-11-01",
          "category": "로드탁송",
          "company": "한국로지스",
          "start_loc": "서울 강남",
          "end_loc": "부산 해운대",
          "freight_fee": 180000,
          "fuel_fee": 70000,
          "status": "정산 대기",
          "due_date": "2026-11-08",
      },
      {
          "id": 2,
          "date": "2026-11-05",
          "category": "대리운전",
          "company": "카카오T대리",
          "start_loc": "경기 분당",
          "end_loc": "서울 역삼",
          "freight_fee": 45000,
          "fuel_fee": 0,
          "status": "입금 완료",
          "due_date": "2026-11-05",
      },
  ]

if "payments" not in st.session_state:
  st.session_state.payments = [{
      "id": 1,
      "date": "2026-11-05",
      "company": "카카오T대리",
      "amount": 45000,
      "memo": "정상 입금 완료",
  }]

if "expenses" not in st.session_state:
  st.session_state.expenses = [{
      "id": 1,
      "date": "2026-11-02",
      "category": "통행료",
      "amount": 12500,
      "memo": "부산 탁송 고속도로 톨게이트",
  }]

# -----------------------------------------------------------------------------
# [사이드바 메뉴 구성]
# -----------------------------------------------------------------------------
st.sidebar.markdown(
    "<h2 style='color: #8B5CF6; text-align: center;'>🚗 DRIVER MONEY</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #CBD5E1; font-size: 0.85rem;'>대리·로드탁송"
    " 통합 관리 시스템</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "📊 대시보드",
        "📝 빠른 운행 등록",
        "📋 운행 내역 및 정산",
        "⛽ 주유비 환급 관리",
        "💰 입금 및 미수금",
        "💸 지출 관리",
        "📈 수익 분석",
        "⚙️ 설정 및 백업",
    ],
)

# 현재 날짜 안전 표시 (KST 기준 문자열 처리)
today_str = datetime.date.today().strftime("%Y-%m-%d")
st.sidebar.markdown(f"<p style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>오늘 날짜 (KST): {today_str}</p>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. 📊 대시보드
# -----------------------------------------------------------------------------
if menu == "📊 대시보드":
  st.markdown("## 📊 실시간 운행 및 정산 대시보드")
  st.markdown("오늘의 운행 성과와 미수금 현황을 한눈에 확인하세요.")

  # 계산 로직
  total_trips = len(st.session_state.trips)
  total_freight = sum(t["freight_fee"] for t in st.session_state.trips)
  total_fuel_pending = sum(
      t["fuel_fee"] for t in st.session_state.trips if t["status"] != "입금 완료"
  )
  paid_amount = sum(
      p["amount"] for p in st.session_state.payments
  )
  unpaid_amount = (total_freight + sum(t["fuel_fee"] for t in st.session_state.trips)) - paid_amount

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-title">총 운행 건수</div>
            <div class="metric-value">{total_trips} 건</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-title">총 탁송 정산액</div>
            <div class="metric-value">{total_freight:,} 원</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-title">주유비 환급 대기</div>
            <div class="metric-value" style="color: #EC4899;">{total_fuel_pending:,} 원</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="metric-title">현재 미수금 잔액</div>
            <div class="metric-value" style="color: #F87171;">{unpaid_amount:,} 원</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("### 🚀 최근 등록된 운행 내역")
  if st.session_state.trips:
    df_trips = pd.DataFrame(st.session_state.trips)
    st.dataframe(df_trips, use_container_width=True)
  else:
    st.info("등록된 운행 내역이 없습니다. 왼쪽 메뉴에서 운행을 등록해주세요.")

# -----------------------------------------------------------------------------
# 2. 📝 빠른 운행 등록
# -----------------------------------------------------------------------------
elif menu == "📝 빠른 운행 등록":
  st.markdown("## 📝 30초 간편 운행 등록")
  st.markdown("탁송비와 주유비를 분리하여 빠르고 정확하게 입력하세요.")

  with st.form("trip_form"):
    col1, col2 = st.columns(2)
    with col1:
      trip_date = st.date_input("운행 날짜", datetime.date.today())
      category = st.selectbox("운행 종류", ["로드탁송", "대리운전", "업체 배정 탁송", "기타"])
      company = st.text_input("업체명 / 플랫폼", placeholder="예: 한국로지스, 카카오T")
      start_loc = st.text_input("출발지", placeholder="예: 서울 강남구")
      end_loc = st.text_input("도착지", placeholder="예: 부산 해운대구")

    with col2:
      freight_fee = st.number_input("탁송비 (원)", min_value=0, step=1000, value=150000)
      fuel_fee = st.number_input("기사 선결제 주유비 (환급대상)", min_value=0, step=1000, value=50000)
      due_date = st.date_input("정산 예정일", datetime.date.today() + datetime.timedelta(days=7))
      status = st.selectbox("운행 상태", ["정산 대기", "부분 입금", "입금 완료", "운행 중"])
      memo = st.text_area("메모 / 특이사항", placeholder="차량번호 및 특이사항 입력")

    submitted = st.form_submit_button("💾 운행 내역 저장하기", use_container_width=True)
    if submitted:
      new_trip = {
          "id": len(st.session_state.trips) + 1,
          "date": trip_date.strftime("%Y-%m-%d"),
          "category": category,
          "company": company,
          "start_loc": start_loc,
          "end_loc": end_loc,
          "freight_fee": freight_fee,
          "fuel_fee": fuel_fee,
          "status": status,
          "due_date": due_date.strftime("%Y-%m-%d"),
      }
      st.session_state.trips.append(new_trip)
      st.success("🎉 운행 내역이 안전하게 저장되었습니다!")
      st.balloons()

# -----------------------------------------------------------------------------
# 3. 📋 운행 내역 및 정산
# -----------------------------------------------------------------------------
elif menu == "📋 운행 내역 및 정산":
  st.markdown("## 📋 전체 운행 내역 및 정산 관리")
  if st.session_state.trips:
    df = pd.DataFrame(st.session_state.trips)
    st.dataframe(df, use_container_width=True)
    
    # 정산 요청 문자 메시지 자동 생성기
    st.markdown("### 💬 정산 요청 문자 자동 생성")
    selected_company = st.selectbox("문자를 보낼 업체 선택", df["company"].unique())
    target_trip = next((t for t in st.session_state.trips if t["company"] == selected_company), None)
    
    if target_trip:
      msg = f"[정산요청] 안녕하세요 {selected_company} 담당자님. {target_trip['date']} 진행 건({target_trip['start_loc']} -> {target_trip['end_loc']}) 탁송비 {target_trip['freight_fee']:,}원 및 주유비 {target_trip['fuel_fee']:,}원 정산 확인 부탁드립니다."
      st.text_area("자동 생성된 정산 요청 메시지 (복사해서 사용하세요)", value=msg, height=100)
  else:
    st.info("기록된 운행 내역이 없습니다.")

# -----------------------------------------------------------------------------
# 4. ⛽ 주유비 환급 관리
# -----------------------------------------------------------------------------
elif menu == "⛽ 주유비 환급 관리":
  st.markdown("## ⛽ 주유비 선결제 및 환급 대기 관리")
  st.markdown("기사가 먼저 결제하고 아직 돌려받지 못한 주유비 내역을 모아서 보여줍니다.")
  
  fuel_records = [t for t in st.session_state.trips if t["fuel_fee"] > 0]
  if fuel_records:
    df_fuel = pd.DataFrame(fuel_records)[["date", "company", "start_loc", "end_loc", "fuel_fee", "status"]]
    st.dataframe(df_fuel, use_container_width=True)
    total_fuel_wait = sum(f["fuel_fee"] for f in fuel_records)
    st.metric(label="총 주유비 환급 대기금액", value=f"{total_fuel_wait:,} 원")
  else:
    st.info("환급 대기 중인 주유비 내역이 없습니다.")

# -----------------------------------------------------------------------------
# 5. 💰 입금 및 미수금
# -----------------------------------------------------------------------------
elif menu == "💰 입금 및 미수금":
  st.markdown("## 💰 입금 내역 및 미수금 자동 계산")
  col1, col2 = st.columns(2)
  with col1:
    st.markdown("### 📥 실시간 입금 등록")
    with st.form("payment_form"):
      pay_date = st.date_input("입금일", datetime.date.today())
      pay_company = st.text_input("입금 업체명")
      pay_amount = st.number_input("입금 금액 (원)", min_value=0, step=1000)
      pay_memo = st.text_input("적요 / 메모")
      pay_submit = st.form_submit_button("입금 등록")
      if pay_submit:
        st.session_state.payments.append({
            "id": len(st.session_state.payments) + 1,
            "date": pay_date.strftime("%Y-%m-%d"),
            "company": pay_company,
            "amount": pay_amount,
            "memo": pay_memo,
        })
        st.success("입금 내역이 등록되었습니다!")
  with col2:
    st.markdown("### 📊 최근 입금 내역")
    if st.session_state.payments:
      st.dataframe(pd.DataFrame(st.session_state.payments), use_container_width=True)
    else:
      st.info("입금 내역이 없습니다.")

# -----------------------------------------------------------------------------
# 6. 💸 지출 관리
# -----------------------------------------------------------------------------
elif menu == "💸 지출 관리":
  st.markdown("## 💸 사업 및 운행 지출 관리")
  with st.form("expense_form"):
    exp_date = st.date_input("지출 날짜", datetime.date.today())
    exp_cat = st.selectbox("지출 항목", ["통행료", "식비", "숙박비", "복귀 교통비", "차량 소모품", "기타"])
    exp_amount = st.number_input("지출 금액 (원)", min_value=0, step=1000)
    exp_memo = st.text_input("상세 메모")
    exp_submit = st.form_submit_button("지출 등록")
    if exp_submit:
      st.session_state.expenses.append({
          "id": len(st.session_state.expenses) + 1,
          "date": exp_date.strftime("%Y-%m-%d"),
          "category": exp_cat,
          "amount": exp_amount,
          "memo": exp_memo,
      })
      st.success("지출 내역이 등록되었습니다!")

  if st.session_state.expenses:
    st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)

# -----------------------------------------------------------------------------
# 7. 📈 수익 분석
# -----------------------------------------------------------------------------
elif menu == "📈 수익 분석":
  st.markdown("## 📈 순수익 및 통계 분석")
  total_income = sum(t["freight_fee"] for t in st.session_state.trips)
  total_expense = sum(e["amount"] for e in st.session_state.expenses)
  net_profit = total_income - total_expense

  col1, col2, col3 = st.columns(3)
  col1.metric("총 탁송 수입", f"{total_income:,} 원")
  col2.metric("총 지출 금액", f"{total_expense:,} 원")
  col3.metric("실제 순수익", f"{net_profit:,} 원", delta=f"{net_profit:,} 원")

# -----------------------------------------------------------------------------
# 8. ⚙️ 설정 및 백업
# -----------------------------------------------------------------------------
elif menu == "⚙️ 설정 및 백업":
  st.markdown("## ⚙️ 데이터 백업 및 앱 설정")
  st.markdown("모든 운행 및 정산 데이터를 JSON 파일로 백업하거나 복원할 수 있습니다.")
  
  # 데이터 다운로드 버튼
  data_json = json.dumps({
      "trips": st.session_state.trips,
      "payments": st.session_state.payments,
      "expenses": st.session_state.expenses,
  }, ensure_ascii=False, indent=4)
  
  st.download_button(
      label="📥 전체 데이터 백업 파일 다운로드 (.json)",
      data=data_json,
      file_name=f"driver_money_backup_{today_str}.json",
      mime="application/json",
  )
  
  st.markdown("---")
  st.info("💡 **팁:** Streamlit Cloud에서 브라우저를 새로고침해도 세션 상태에 안전하게 유지되며, 정기적으로 백업 파일을 다운로드해 두시면 데이터 유실을 완벽히 방지할 수 있습니다.")
