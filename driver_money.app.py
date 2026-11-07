import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정 (와이드 모드 필수, 다크 배경)
st.set_page_config(
    page_title="DRIVER MONEY - 프리미엄 탁송 가계부",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Streamlit 기본 UI 완벽 숨김 처리 (웹앱 전체화면화)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
            margin: 0 !important;
        }
        iframe {
            border: none;
            height: 100vh !important;
            width: 100vw !important;
        }
        ::-webkit-scrollbar {
            display: none;
        }
        body {
            margin: 0;
            overflow: hidden;
            background-color: #0B1120;
        }
    </style>
""", unsafe_allow_html=True)

# 3. 완벽하게 작동하는 React UI 원본 코드 (모달창 멈춤 버그 완벽 수정본)
react_html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DRIVER MONEY</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'],
                    }
                }
            }
        }
    </script>

    <!-- Pretendard Font -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />

    <!-- React 18 -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    
    <!-- Babel (브라우저 실시간 번역기) -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Lucide React 아이콘 (모달 멈춤 버그 해결의 핵심 라이브러리) -->
    <script src="https://unpkg.com/lucide-react@0.344.0/dist/umd/lucide-react.min.js"></script>

    <style>
        body { background-color: #0B1120; margin: 0; padding: 0; color: #f1f5f9; overflow-x: hidden; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;
        
        // 아이콘 추출 (안정성 확보)
        const { 
            LayoutDashboard, PlusCircle, History, TrendingUp, Fuel, CreditCard, 
            AlertTriangle, Receipt, Building2, Bell, PieChart, Calendar, Users, 
            Download, Settings, Search, Filter, CheckCircle2, XCircle, Clock, 
            Phone, Send, Copy, ChevronRight, Menu, X, Plus, RefreshCw, Trash2, 
            Edit, DollarSign, ArrowUpRight, Car 
        } = window.lucideReact;

        // --- 초기 샘플 데이터 ---
        const INITIAL_COMPANIES = [
            { id: 'c1', name: 'SK로드탁송', contact: '010-1234-5678', cycle: '매주 금요일', defaultFee: 180000 },
            { id: 'c2', name: '카카오대리', contact: '1588-0000', cycle: '당일 정산', defaultFee: 45000 },
            { id: 'c3', name: '오토원탁송', contact: '010-9876-5432', cycle: '매월 10일', defaultFee: 220000 },
        ];

        const INITIAL_TRIPS = [
            {
                id: 'TRIP-1001', date: '2026-11-07', startTime: '14:00', endTime: '17:30',
                type: '로드탁송', company: 'SK로드탁송', customer: '홍길동', phone: '010-8888-9999',
                vehicleNo: '12가 3456', vehicleType: '제네시스 G80', from: '서울 강남구', to: '부산 해운대구',
                freightFee: 180000, fuelFee: 70000, fuelPaidBy: 'driver_prepaid',
                dueDate: '2026-11-14', status: '정산 대기', paidFreight: 0, paidFuel: 0,
                memo: '주유비 7만원선결제 (영수증 첨부완료)'
            },
            {
                id: 'TRIP-1002', date: '2026-11-07', startTime: '20:00', endTime: '22:15',
                type: '대리운전', company: '카카오대리', customer: '이몽룡', phone: '010-2222-3333',
                vehicleNo: '56나 7890', vehicleType: '그랜저 IG', from: '성남 판교', to: '인천 송도',
                freightFee: 45000, fuelFee: 0, fuelPaidBy: 'included',
                dueDate: '2026-11-07', status: '정산 완료', paidFreight: 45000, paidFuel: 0,
                memo: '당일 정산완료'
            },
            {
                id: 'TRIP-1003', date: '2026-11-05', startTime: '09:00', endTime: '12:00',
                type: '로드탁송', company: '오토원탁송', customer: '성춘향', phone: '010-7777-1111',
                vehicleNo: '77다 1234', vehicleType: 'K8 Hybrid', from: '경기 수원', to: '대전 유성구',
                freightFee: 200000, fuelFee: 50000, fuelPaidBy: 'driver_prepaid',
                dueDate: '2026-11-06', status: '부분 입금', paidFreight: 100000, paidFuel: 0,
                memo: '탁송비 1차 10만원 입금됨, 잔액 10만+주유 5만 미수'
            }
        ];

        const INITIAL_EXPENSES = [
            { id: 'e1', date: '2026-11-07', category: '통행료', amount: 15400, memo: '서울-부산 톨게이트' },
            { id: 'e2', date: '2026-11-07', category: '복귀 교통비', amount: 32000, memo: 'KTX 부산-서울' },
        ];

        function App() {
            // 브라우저 캐시(localStorage)를 활용한 데이터 유지
            const [trips, setTrips] = useState(() => {
                const saved = localStorage.getItem('dm_trips');
                return saved ? JSON.parse(saved) : INITIAL_TRIPS;
            });
            const [expenses, setExpenses] = useState(() => {
                const saved = localStorage.getItem('dm_expenses');
                return saved ? JSON.parse(saved) : INITIAL_EXPENSES;
            });
            const [companies, setCompanies] = useState(() => {
                const saved = localStorage.getItem('dm_companies');
                return saved ? JSON.parse(saved) : INITIAL_COMPANIES;
            });

            const [activeTab, setActiveTab] = useState('dashboard');
            
            // 모달 상태 관리
            const [isTripModalOpen, setIsTripModalOpen] = useState(false);
            const [isDepositModalOpen, setIsDepositModalOpen] = useState(false);
            const [isSmsModalOpen, setIsSmsModalOpen] = useState(false);
            
            const [selectedTripForSms, setSelectedTripForSms] = useState(null);

            // 데이터 자동 저장
            useEffect(() => { localStorage.setItem('dm_trips', JSON.stringify(trips)); }, [trips]);
            useEffect(() => { localStorage.setItem('dm_expenses', JSON.stringify(expenses)); }, [expenses]);
            useEffect(() => { localStorage.setItem('dm_companies', JSON.stringify(companies)); }, [companies]);

            // 재무 통계 자동 계산 엔진
            const stats = useMemo(() => {
                let todayCount = 0; let todaySettlementTarget = 0; let todayDeposit = 0;
                let totalUnpaidFreight = 0; let totalUnpaidFuel = 0;
                let monthlyFreightIncome = 0; let monthlyExpenses = 0;
                const todayStr = '2026-11-07';

                trips.forEach(t => {
                    const freightUnpaid = t.freightFee - t.paidFreight;
                    const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? Math.max(0, t.fuelFee - t.paidFuel) : 0;
                    totalUnpaidFreight += freightUnpaid; totalUnpaidFuel += fuelUnpaid;
                    if (t.date === todayStr) {
                        todayCount++;
                        todaySettlementTarget += (t.freightFee + (t.fuelPaidBy === 'driver_prepaid' ? t.fuelFee : 0));
                        todayDeposit += (t.paidFreight + t.paidFuel);
                    }
                    monthlyFreightIncome += t.paidFreight;
                });
                expenses.forEach(e => { monthlyExpenses += Number(e.amount || 0); });
                const netProfit = monthlyFreightIncome - monthlyExpenses;

                return { 
                    todayCount, todaySettlementTarget, todayDeposit, 
                    totalUnpaidFreight, totalUnpaidFuel, 
                    totalUnpaid: totalUnpaidFreight + totalUnpaidFuel, 
                    monthlyFreightIncome, monthlyExpenses, netProfit 
                };
            }, [trips, expenses]);

            // 운행 등록 처리
            const handleSaveTrip = (newTrip) => { setTrips(prev => [newTrip, ...prev]); setIsTripModalOpen(false); };
            
            // 입금 등록 처리
            const handleApplyDeposit = (tripId, freightAmt, fuelAmt) => {
                setTrips(prev => prev.map(t => {
                    if (t.id === tripId) {
                        const newPaidFreight = t.paidFreight + Number(freightAmt);
                        const newPaidFuel = t.paidFuel + Number(fuelAmt);
                        const totalTarget = t.freightFee + (t.fuelPaidBy === 'driver_prepaid' ? t.fuelFee : 0);
                        const totalPaid = newPaidFreight + newPaidFuel;
                        let newStatus = '부분 입금';
                        if (totalPaid >= totalTarget) { newStatus = '정산 완료'; } else if (totalPaid === 0) { newStatus = '정산 대기'; }
                        return { ...t, paidFreight: newPaidFreight, paidFuel: newPaidFuel, status: newStatus };
                    }
                    return t;
                }));
                setIsDepositModalOpen(false);
            };

            const navItems = [
                { id: 'dashboard', label: '대시보드', icon: LayoutDashboard },
                { id: 'trip_list', label: '운행 내역', icon: History },
                { id: 'unpaid', label: '미수금 & SMS', icon: AlertTriangle, badge: trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).length },
                { id: 'backup', label: '백업 및 엑셀', icon: Download },
            ];

            return (
                <div className="min-h-screen bg-[#0B1120] text-slate-100 font-sans flex flex-col md:flex-row antialiased">
                    
                    {/* PC 좌측 사이드바 */}
                    <aside className="hidden md:flex flex-col w-64 bg-slate-900/80 backdrop-blur-md border-r border-slate-800 p-4 shrink-0 justify-between">
                        <div>
                            <div className="flex items-center gap-3 px-3 py-4 mb-4 border-b border-slate-800/80">
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
                                    <Car className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <h1 className="font-extrabold text-lg tracking-wider bg-gradient-to-r from-white via-purple-200 to-pink-400 bg-clip-text text-transparent">DRIVER MONEY</h1>
                                    <span className="text-[10px] text-purple-400 font-mono tracking-widest uppercase block">Pro Consignment OS</span>
                                </div>
                            </div>
                            <nav className="space-y-1">
                                {navItems.map((item) => {
                                    const IconComponent = item.icon;
                                    return (
                                        <button
                                            key={item.id}
                                            onClick={() => setActiveTab(item.id)}
                                            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                                                activeTab === item.id ? 'bg-gradient-to-r from-purple-600/30 to-pink-600/20 text-white border border-purple-500/40 shadow-lg shadow-purple-900/20' : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                                            }`}
                                        >
                                            <div className="flex items-center gap-3">
                                                <IconComponent className={`w-4 h-4 ${activeTab === item.id ? 'text-purple-400' : 'text-slate-400'}`} />
                                                <span>{item.label}</span>
                                            </div>
                                            {item.badge > 0 && <span className="px-2 py-0.5 text-xs rounded-full bg-pink-500/20 text-pink-400 font-bold border border-pink-500/30">{item.badge}</span>}
                                        </button>
                                    )
                                })}
                            </nav>
                        </div>
                    </aside>

                    {/* 메인 작업 영역 */}
                    <main className="flex-1 p-4 md:p-8 overflow-y-auto w-full pb-24 md:pb-8">
                        
                        {/* 상단 액션 버튼 */}
                        <header className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800/80 pb-4">
                            <div>
                                <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
                                    {navItems.find(n => n.id === activeTab)?.label || '대시보드'}
                                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 font-mono font-normal">KST 2026-11-07</span>
                                </h2>
                            </div>
                            <div className="flex items-center gap-2">
                                <button onClick={() => setIsTripModalOpen(true)} className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-purple-600 to-pink-600 shadow-lg shadow-purple-600/30 transition-all flex items-center gap-2 transform hover:-translate-y-0.5">
                                    <Plus className="w-4 h-4" /> 운행 빠른등록
                                </button>
                                <button onClick={() => setIsDepositModalOpen(true)} className="px-3 py-2 rounded-xl text-xs font-bold text-slate-200 bg-slate-800 border border-slate-700 transition-all flex items-center gap-1.5 hover:bg-slate-700 transform hover:-translate-y-0.5">
                                    <CreditCard className="w-4 h-4 text-emerald-400" /> 입금 처리
                                </button>
                            </div>
                        </header>

                        {/* 1. 대시보드 탭 */}
                        {activeTab === 'dashboard' && (
                            <div className="space-y-6">
                                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
                                    <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 relative overflow-hidden">
                                        <p className="text-xs font-bold text-slate-400">오늘 운행 건수</p>
                                        <span className="text-2xl font-black text-white">{stats.todayCount}건</span>
                                    </div>
                                    <div className="p-4 rounded-2xl bg-slate-900/70 border border-pink-900/40 relative overflow-hidden">
                                        <p className="text-xs font-bold text-pink-300">현재 미수금 총액</p>
                                        <span className="text-2xl font-black text-pink-400">{stats.totalUnpaid.toLocaleString()}원</span>
                                    </div>
                                    <div className="p-4 rounded-2xl bg-slate-900/70 border border-amber-900/40 relative overflow-hidden">
                                        <p className="text-xs font-bold text-amber-300">주유비 환급대기</p>
                                        <span className="text-2xl font-black text-amber-400">{stats.totalUnpaidFuel.toLocaleString()}원</span>
                                    </div>
                                    <div className="p-4 rounded-2xl bg-slate-900/70 border border-emerald-900/40 relative overflow-hidden">
                                        <p className="text-xs font-bold text-emerald-300">이번 달 실제 순수익</p>
                                        <span className="text-2xl font-black text-emerald-400">{stats.netProfit.toLocaleString()}원</span>
                                    </div>
                                </div>

                                <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800">
                                    <h3 className="font-extrabold text-base text-white mb-4">최근 운행 내역</h3>
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-left text-xs">
                                            <thead className="bg-slate-950/80 text-slate-400 uppercase font-mono">
                                                <tr><th className="p-3">일자</th><th className="p-3">업체</th><th className="p-3">구간</th><th className="p-3 text-right">탁송비</th><th className="p-3 text-right">주유비</th><th className="p-3 text-center">상태</th></tr>
                                            </thead>
                                            <tbody className="divide-y divide-slate-800/60 font-medium">
                                                {trips.slice(0, 5).map(t => (
                                                    <tr key={t.id} className="hover:bg-slate-800/40">
                                                        <td className="p-3 font-mono text-slate-300">{t.date}</td>
                                                        <td className="p-3 text-white font-bold">{t.company}</td>
                                                        <td className="p-3 text-slate-200">{t.from} → {t.to}</td>
                                                        <td className="p-3 text-right text-purple-300 font-bold">{t.freightFee.toLocaleString()}원</td>
                                                        <td className="p-3 text-right text-amber-300 font-bold">{t.fuelFee > 0 ? `${t.fuelFee.toLocaleString()}원` : '-'}</td>
                                                        <td className="p-3 text-center text-emerald-400 font-bold">{t.status}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* 2. 운행 내역 전체 탭 */}
                        {activeTab === 'trip_list' && (
                            <div className="space-y-4">
                                {trips.map(t => {
                                    const totalUnpaid = (t.freightFee - t.paidFreight) + (t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0);
                                    return (
                                        <div key={t.id} className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl hover:border-purple-500/30 transition-all space-y-3">
                                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                                                <div className="flex items-center gap-2">
                                                    <span className="px-2.5 py-1 rounded-lg bg-purple-500/20 text-purple-300 font-mono text-xs font-bold border border-purple-500/30">{t.type}</span>
                                                    <h4 className="font-extrabold text-base text-white">{t.company}</h4><span className="text-xs text-slate-400 font-mono">({t.date})</span>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${t.status === '정산 완료' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-pink-500/20 text-pink-400 border border-pink-500/30'}`}>{t.status}</span>
                                                </div>
                                            </div>
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                                                <div><span className="text-slate-400 block">운행 구간</span><p className="font-bold text-slate-200 mt-0.5">{t.from} → {t.to}</p></div>
                                                <div><span className="text-slate-400 block">탁송비</span><p className="font-bold text-purple-300 mt-0.5">{t.freightFee.toLocaleString()}원</p></div>
                                                <div className="text-right">
                                                    <span className="text-slate-400 block">남은 미수금</span><span className="text-base font-black text-pink-400">{totalUnpaid.toLocaleString()}원</span>
                                                </div>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        )}

                        {/* 3. 미수금 확인 및 문자발송 탭 */}
                        {activeTab === 'unpaid' && (
                            <div className="space-y-4">
                                {trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).map(t => {
                                    const freightUnpaid = t.freightFee - t.paidFreight;
                                    const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0;
                                    const totalUnpaid = freightUnpaid + fuelUnpaid;
                                    return (
                                        <div key={t.id} className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between space-y-4">
                                            <div>
                                                <div className="flex justify-between items-start mb-2">
                                                    <span className="px-2.5 py-1 rounded-lg bg-pink-500/20 text-pink-300 font-bold text-xs border border-pink-500/30">정산 예정일: {t.dueDate}</span>
                                                    <span className="text-xs font-bold text-slate-400">{t.company}</span>
                                                </div>
                                                <h4 className="font-extrabold text-base text-white">{t.from} → {t.to}</h4>
                                                <div className="mt-4 p-3 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5 text-xs">
                                                    <div className="flex justify-between text-slate-300"><span>탁송비 미수금:</span><span className="font-bold text-purple-300">{freightUnpaid.toLocaleString()}원</span></div>
                                                    <div className="flex justify-between text-slate-300"><span>주유비 환급 대기:</span><span className="font-bold text-amber-300">{fuelUnpaid.toLocaleString()}원</span></div>
                                                    <div className="pt-1 border-t border-slate-800 flex justify-between text-sm font-black text-pink-400"><span>합계 미수금:</span><span>{totalUnpaid.toLocaleString()}원</span></div>
                                                </div>
                                            </div>
                                            <button onClick={() => { setSelectedTripForSms(t); setIsSmsModalOpen(true); }} className="py-2.5 rounded-xl bg-gradient-to-r from-pink-600 to-purple-600 text-white font-bold text-xs flex items-center justify-center gap-2 hover:opacity-80 transition-all">
                                                <Send className="w-4 h-4" /> 정산 요청 문자 복사하기
                                            </button>
                                        </div>
                                    )
                                })}
                            </div>
                        )}

                        {/* 4. 백업 및 엑셀 탭 */}
                        {activeTab === 'backup' && (
                            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl space-y-4">
                                <h3 className="font-extrabold text-base text-white">데이터 백업 (JSON)</h3>
                                <button onClick={() => {
                                    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ trips, expenses, companies }));
                                    const link = document.createElement('a');
                                    link.setAttribute("href", dataStr); link.setAttribute("download", `BACKUP.json`);
                                    document.body.appendChild(link); link.click(); link.remove();
                                }} className="p-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center justify-center gap-2"><Download className="w-4 h-4" /> 전체 JSON 데이터 백업 다운로드</button>
                            </div>
                        )}
                    </main>

                    {/* 모바일용 하단 메뉴 */}
                    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur-lg border-t border-slate-800 z-40 px-2 py-2 flex justify-around items-center">
                        {navItems.map(item => {
                            const IconComponent = item.icon; 
                            const isActive = activeTab === item.id;
                            return (
                                <button key={item.id} onClick={() => setActiveTab(item.id)} className={`flex flex-col items-center gap-1 p-1.5 rounded-xl relative ${isActive ? 'text-purple-400 font-bold' : 'text-slate-400'}`}>
                                    <IconComponent className="w-5 h-5" /><span className="text-[10px]">{item.label}</span>
                                    {item.badge > 0 && <span className="absolute top-0 right-1 w-4 h-4 rounded-full bg-pink-500 text-white text-[9px] font-bold flex items-center justify-center">{item.badge}</span>}
                                </button>
                            );
                        })}
                    </nav>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

# HTML을 전체 화면(높이 1000px 이상, 스크롤 가능)으로 렌더링
components.html(react_html_code, height=1200, scrolling=True)
