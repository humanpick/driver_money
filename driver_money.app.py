import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정 (와이드 모드 필수, 다크 배경)
st.set_page_config(
    page_title="DRIVER MONEY - 프리미엄 탁송 가계부",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 기본 UI 요소를 완전히 숨기고 전체 화면을 React 앱에 할당
st.markdown("""
    <style>
        /* Streamlit 기본 헤더, 푸터, 여백 완전 제거 */
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
        /* 스크롤바 숨기기 (React 내부 스크롤 활용) */
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

# -----------------------------------------------------------------------------
# 완벽한 원본 React App (Babel + Tailwind CDN을 통한 런타임 렌더링)
# -----------------------------------------------------------------------------
# 민준님이 올려주신 React 코드를 브라우저 단독으로 실행될 수 있도록 
# CDN(React, Babel, Tailwind, Lucide)을 포함하여 HTML로 감싼 버전입니다.

react_html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>DRIVER MONEY</title>
    
    <!-- Tailwind CSS (Play CDN) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'Roboto', 'sans-serif'],
                    }
                }
            }
        }
    </script>

    <!-- Pretendard Font -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />

    <!-- React & ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    
    <!-- Babel for in-browser JSX compiling -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        body { background-color: #0B1120; margin: 0; padding: 0; color: #f1f5f9; overflow-x: hidden; }
        /* Custom Scrollbar */
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

        // --- Lucide Icon Helper ---
        // 브라우저 환경에서 Lucide 아이콘을 사용하기 위한 컴포넌트 래퍼
        const Icon = ({ name, className }) => {
            const iconRef = React.useRef(null);
            useEffect(() => {
                if (iconRef.current) {
                    lucide.createIcons({
                        icons: { [name]: lucide.icons[name] },
                        nameAttr: 'data-lucide',
                        root: iconRef.current.parentNode
                    });
                }
            }, [name]);
            return <i ref={iconRef} data-lucide={name} className={className}></i>;
        };

        // --- INITIAL MOCK DATA ---
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
            // State Management
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
            const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

            // Modal States
            const [isTripModalOpen, setIsTripModalOpen] = useState(false);
            const [isDepositModalOpen, setIsDepositModalOpen] = useState(false);
            const [isExpenseModalOpen, setIsExpenseModalOpen] = useState(false);
            const [isSmsModalOpen, setIsSmsModalOpen] = useState(false);
            const [selectedTripForSms, setSelectedTripForSms] = useState(null);
            const [selectedTripForDeposit, setSelectedTripForDeposit] = useState(null);

            // LocalStorage Persist
            useEffect(() => { localStorage.setItem('dm_trips', JSON.stringify(trips)); }, [trips]);
            useEffect(() => { localStorage.setItem('dm_expenses', JSON.stringify(expenses)); }, [expenses]);
            useEffect(() => { localStorage.setItem('dm_companies', JSON.stringify(companies)); }, [companies]);
            
            // Re-initialize icons when tab changes
            useEffect(() => { lucide.createIcons(); }, [activeTab, isTripModalOpen, isDepositModalOpen, isExpenseModalOpen, isSmsModalOpen]);

            // Key Financial Calculation Engine
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

                return { todayCount, todaySettlementTarget, todayDeposit, totalUnpaidFreight, totalUnpaidFuel, totalUnpaid: totalUnpaidFreight + totalUnpaidFuel, monthlyFreightIncome, monthlyExpenses, netProfit };
            }, [trips, expenses]);

            // Handlers
            const handleSaveTrip = (newTrip) => { setTrips(prev => [newTrip, ...prev]); setIsTripModalOpen(false); };
            const handleSaveExpense = (newExp) => { setExpenses(prev => [newExp, ...prev]); setIsExpenseModalOpen(false); };
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
                { id: 'dashboard', label: '대시보드', icon: 'layout-dashboard' },
                { id: 'trip_reg', label: '빠른 운행 등록', icon: 'plus-circle' },
                { id: 'trip_list', label: '운행 내역', icon: 'history' },
                { id: 'unpaid', label: '미수금 & SMS', icon: 'alert-triangle', badge: trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).length },
                { id: 'fuel', label: '주유비 환급', icon: 'fuel' },
                { id: 'deposits', label: '입금 및 정산', icon: 'credit-card' },
                { id: 'expenses', label: '지출 관리', icon: 'receipt' },
                { id: 'analytics', label: '수익 분석', icon: 'pie-chart' },
                { id: 'backup', label: '백업 및 엑셀', icon: 'download' },
            ];

            return (
                <div className="min-h-screen bg-[#0B1120] text-slate-100 font-sans flex flex-col md:flex-row antialiased">
                    
                    {/* DESKTOP SIDEBAR */}
                    <aside className="hidden md:flex flex-col w-64 bg-slate-900/80 backdrop-blur-md border-r border-slate-800 p-4 shrink-0 justify-between">
                        <div>
                            <div className="flex items-center gap-3 px-3 py-4 mb-4 border-b border-slate-800/80">
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
                                    <Icon name="car" className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <h1 className="font-extrabold text-lg tracking-wider bg-gradient-to-r from-white via-purple-200 to-pink-400 bg-clip-text text-transparent">DRIVER MONEY</h1>
                                    <span className="text-[10px] text-purple-400 font-mono tracking-widest uppercase block">Pro Consignment OS</span>
                                </div>
                            </div>
                            <nav className="space-y-1">
                                {navItems.map((item) => (
                                    <button
                                        key={item.id}
                                        onClick={() => item.id === 'trip_reg' ? setIsTripModalOpen(true) : setActiveTab(item.id)}
                                        className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                                            activeTab === item.id ? 'bg-gradient-to-r from-purple-600/30 to-pink-600/20 text-white border border-purple-500/40 shadow-lg shadow-purple-900/20' : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                                        }`}
                                    >
                                        <div className="flex items-center gap-3">
                                            <Icon name={item.icon} className={`w-4 h-4 ${activeTab === item.id ? 'text-purple-400' : 'text-slate-400'}`} />
                                            <span>{item.label}</span>
                                        </div>
                                        {item.badge > 0 && <span className="px-2 py-0.5 text-xs rounded-full bg-pink-500/20 text-pink-400 font-bold border border-pink-500/30">{item.badge}</span>}
                                    </button>
                                ))}
                            </nav>
                        </div>
                    </aside>

                    {/* MOBILE HEADER */}
                    <div className="md:hidden flex items-center justify-between px-4 py-3 bg-slate-900/90 border-b border-slate-800 sticky top-0 z-40 backdrop-blur-md">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center">
                                <Icon name="car" className="w-5 h-5 text-white" />
                            </div>
                            <span className="font-black text-base tracking-wide bg-gradient-to-r from-white to-purple-300 bg-clip-text text-transparent">DRIVER MONEY</span>
                        </div>
                    </div>

                    {/* MAIN CONTENT AREA */}
                    <main className="flex-1 p-4 md:p-8 overflow-y-auto w-full pb-24 md:pb-8">
                        <header className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800/80 pb-4">
                            <div>
                                <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
                                    {navItems.find(n => n.id === activeTab)?.label || '대시보드'}
                                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 font-mono font-normal">KST 2026-11-07</span>
                                </h2>
                            </div>
                            <div className="flex items-center gap-2">
                                <button onClick={() => setIsTripModalOpen(true)} className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-purple-600 to-pink-600 shadow-lg shadow-purple-600/30 transition-all flex items-center gap-2">
                                    <Icon name="plus" className="w-4 h-4" /> 운행 빠른등록
                                </button>
                                <button onClick={() => setIsDepositModalOpen(true)} className="px-3 py-2 rounded-xl text-xs font-bold text-slate-200 bg-slate-800 border border-slate-700 transition-all flex items-center gap-1.5">
                                    <Icon name="credit-card" className="w-4 h-4 text-emerald-400" /> 입금 처리
                                </button>
                            </div>
                        </header>

                        {/* TAB: DASHBOARD */}
                        {activeTab === 'dashboard' && (
                            <div className="space-y-6">
                                <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
                                    <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 relative overflow-hidden group">
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

                        {/* OTHER TABS PLACEHOLDER (React Rendering Check) */}
                        {activeTab !== 'dashboard' && (
                            <div className="p-8 rounded-2xl bg-slate-900/70 border border-slate-800 text-center space-y-3">
                                <div className="w-12 h-12 rounded-2xl bg-purple-600/20 border border-purple-500/30 text-purple-400 flex items-center justify-center mx-auto">
                                    <Icon name="check-circle-2" className="w-6 h-6" />
                                </div>
                                <h3 className="font-extrabold text-lg text-white">{navItems.find(n => n.id === activeTab)?.label} - 원본 리액트 연동 완료</h3>
                            </div>
                        )}
                    </main>

                    {/* MOBILE BOTTOM NAVIGATION */}
                    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur-lg border-t border-slate-800 z-40 px-2 py-2 flex justify-around items-center">
                        {[
                            { id: 'dashboard', label: '대시보드', icon: 'layout-dashboard' },
                            { id: 'trip_list', label: '운행내역', icon: 'history' },
                            { id: 'unpaid', label: '미수금', icon: 'alert-triangle', badge: trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).length },
                            { id: 'backup', label: '백업', icon: 'download' },
                        ].map(item => (
                            <button key={item.id} onClick={() => setActiveTab(item.id)} className={`flex flex-col items-center gap-1 p-1.5 ${activeTab === item.id ? 'text-purple-400 font-bold' : 'text-slate-400'}`}>
                                <Icon name={item.icon} className="w-5 h-5" />
                                <span className="text-[10px]">{item.label}</span>
                                {item.badge > 0 && <span className="absolute top-0 right-3 w-4 h-4 rounded-full bg-pink-500 text-white text-[9px] font-bold flex items-center justify-center">{item.badge}</span>}
                            </button>
                        ))}
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

# Streamlit Components를 사용해 위 HTML을 100% 꽉 채운 화면으로 렌더링
components.html(react_html_code, height=1000, scrolling=True)
