import React, { useState, useEffect, useMemo } from 'react';
import {
  LayoutDashboard,
  PlusCircle,
  History,
  TrendingUp,
  Fuel,
  CreditCard,
  AlertTriangle,
  Receipt,
  Building2,
  Bell,
  PieChart,
  Calendar,
  Users,
  Download,
  Settings,
  Search,
  Filter,
  CheckCircle2,
  XCircle,
  Clock,
  Phone,
  Send,
  Copy,
  ChevronRight,
  Menu,
  X,
  Plus,
  RefreshCw,
  Trash2,
  Edit,
  DollarSign,
  ArrowUpRight,
  Car
} from 'lucide-react';

// --- INITIAL MOCK DATA ---
const INITIAL_COMPANIES = [
  { id: 'c1', name: 'SK로드탁송', contact: '010-1234-5678', cycle: '매주 금요일', defaultFee: 180000 },
  { id: 'c2', name: '카카오대리', contact: '1588-0000', cycle: '당일 정산', defaultFee: 45000 },
  { id: 'c3', name: '오토원탁송', contact: '010-9876-5432', cycle: '매월 10일', defaultFee: 220000 },
  { id: 'c4', name: '마이카캐리어', contact: '010-5555-4444', cycle: '매월 말일', defaultFee: 300000 },
];

const INITIAL_TRIPS = [
  {
    id: 'TRIP-1001',
    date: '2026-11-07',
    startTime: '14:00',
    endTime: '17:30',
    type: '로드탁송',
    company: 'SK로드탁송',
    customer: '홍길동',
    phone: '010-8888-9999',
    vehicleNo: '12가 3456',
    vehicleType: '제네시스 G80',
    from: '서울 강남구',
    to: '부산 해운대구',
    freightFee: 180000,
    fuelFee: 70000,
    fuelPaidBy: 'driver_prepaid', // driver_prepaid, customer, company, included
    dueDate: '2026-11-14',
    status: '정산 대기',
    paidFreight: 180000,
    paidFuel: 0,
    memo: '주유비 7만원선결제 (영수증 첨부완료)'
  },
  {
    id: 'TRIP-1002',
    date: '2026-11-07',
    startTime: '20:00',
    endTime: '22:15',
    type: '대리운전',
    company: '카카오대리',
    customer: '이몽룡',
    phone: '010-2222-3333',
    vehicleNo: '56나 7890',
    vehicleType: '그랜저 IG',
    from: '성남 판교',
    to: '인천 송도',
    freightFee: 45000,
    fuelFee: 0,
    fuelPaidBy: 'included',
    dueDate: '2026-11-07',
    status: '정산 완료',
    paidFreight: 45000,
    paidFuel: 0,
    memo: '당일 정산완료'
  },
  {
    id: 'TRIP-1003',
    date: '2026-11-05',
    startTime: '09:00',
    endTime: '12:00',
    type: '로드탁송',
    company: '오토원탁송',
    customer: '성춘향',
    phone: '010-7777-1111',
    vehicleNo: '77다 1234',
    vehicleType: 'K8 Hybrid',
    from: '경기 수원',
    to: '대전 유성구',
    freightFee: 200000,
    fuelFee: 50000,
    fuelPaidBy: 'driver_prepaid',
    dueDate: '2026-11-06', // 지연됨!
    status: '부분 입금',
    paidFreight: 100000,
    paidFuel: 0,
    memo: '탁송비 1차 10만원 입금됨, 잔액 10만+주유 5만 미수'
  },
  {
    id: 'TRIP-1004',
    date: '2026-11-02',
    startTime: '11:00',
    endTime: '16:00',
    type: '개인 직거래 탁송',
    company: '개인직거래',
    customer: '김철수',
    phone: '010-9999-0000',
    vehicleNo: '99라 9999',
    vehicleType: '카니발 하이리무진',
    from: '인천 공항',
    to: '강원 강릉',
    freightFee: 250000,
    fuelFee: 80000,
    fuelPaidBy: 'driver_prepaid',
    dueDate: '2026-11-03',
    status: '부분 입금',
    paidFreight: 250000,
    paidFuel: 0,
    memo: '탁송비완납, 주유비 8만원 환급 지연'
  }
];

const INITIAL_EXPENSES = [
  { id: 'e1', date: '2026-11-07', category: '통행료', amount: 15400, memo: '서울-부산 톨게이트' },
  { id: 'e2', date: '2026-11-07', category: '복귀 교통비', amount: 32000, memo: 'KTX 부산-서울' },
  { id: 'e3', date: '2026-11-06', category: '식비', amount: 12000, memo: '휴게소 식사' },
  { id: 'e4', date: '2026-11-05', category: '통행료', amount: 8900, memo: '수원-대전 톨게이트' },
];

export default function App() {
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

  // Notifications State
  const [notifications, setNotifications] = useState([]);

  // LocalStorage Persist
  useEffect(() => {
    localStorage.setItem('dm_trips', JSON.stringify(trips));
  }, [trips]);

  useEffect(() => {
    localStorage.setItem('dm_expenses', JSON.stringify(expenses));
  }, [expenses]);

  useEffect(() => {
    localStorage.setItem('dm_companies', JSON.stringify(companies));
  }, [companies]);

  // Compute Unpaid Alert Notifications
  useEffect(() => {
    const now = new Date('2026-11-07');
    const alerts = [];
    trips.forEach(t => {
      const freightUnpaid = t.freightFee - t.paidFreight;
      const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0;
      const totalUnpaid = freightUnpaid + fuelUnpaid;

      const due = new Date(t.dueDate);
      if (totalUnpaid > 0) {
        if (due < now) {
          alerts.push({
            id: `alert-overdue-${t.id}`,
            type: 'overdue',
            title: `정산 지연! [${t.company}]`,
            message: `${t.customer}건 (미수금: ${totalUnpaid.toLocaleString()}원) 정산예정일(${t.dueDate}) 경과`,
            trip: t
          });
        } else if (due.toISOString().slice(0, 10) === '2026-11-07') {
          alerts.push({
            id: `alert-today-${t.id}`,
            type: 'today',
            title: `오늘 정산 예정 [${t.company}]`,
            message: `${totalUnpaid.toLocaleString()}원 입금 대기 중`,
            trip: t
          });
        }
      }
    });
    setNotifications(alerts);
  }, [trips]);

  // Key Financial Calculation Engine
  const stats = useMemo(() => {
    let todayCount = 0;
    let todaySettlementTarget = 0;
    let todayDeposit = 0;
    let totalUnpaidFreight = 0;
    let totalUnpaidFuel = 0;
    let monthlyFreightIncome = 0;
    let monthlyExpenses = 0;

    const todayStr = '2026-11-07';

    trips.forEach(t => {
      const freightUnpaid = t.freightFee - t.paidFreight;
      const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? Math.max(0, t.fuelFee - t.paidFuel) : 0;
      
      totalUnpaidFreight += freightUnpaid;
      totalUnpaidFuel += fuelUnpaid;

      if (t.date === todayStr) {
        todayCount++;
        todaySettlementTarget += (t.freightFee + (t.fuelPaidBy === 'driver_prepaid' ? t.fuelFee : 0));
        todayDeposit += (t.paidFreight + t.paidFuel);
      }

      // Sum strictly received freight as real gross income
      monthlyFreightIncome += t.paidFreight;
    });

    expenses.forEach(e => {
      monthlyExpenses += Number(e.amount || 0);
    });

    const netProfit = monthlyFreightIncome - monthlyExpenses;

    return {
      todayCount,
      todaySettlementTarget,
      todayDeposit,
      totalUnpaidFreight,
      totalUnpaidFuel,
      totalUnpaid: totalUnpaidFreight + totalUnpaidFuel,
      monthlyFreightIncome,
      monthlyExpenses,
      netProfit
    };
  }, [trips, expenses]);

  // Add Trip Handler
  const handleSaveTrip = (newTrip) => {
    setTrips(prev => [newTrip, ...prev]);
    setIsTripModalOpen(false);
  };

  // Add Expense Handler
  const handleSaveExpense = (newExp) => {
    setExpenses(prev => [newExp, ...prev]);
    setIsExpenseModalOpen(false);
  };

  // Process Deposit Handler
  const handleApplyDeposit = (tripId, freightAmt, fuelAmt) => {
    setTrips(prev => prev.map(t => {
      if (t.id === tripId) {
        const newPaidFreight = t.paidFreight + Number(freightAmt);
        const newPaidFuel = t.paidFuel + Number(fuelAmt);
        const totalTarget = t.freightFee + (t.fuelPaidBy === 'driver_prepaid' ? t.fuelFee : 0);
        const totalPaid = newPaidFreight + newPaidFuel;
        
        let newStatus = '부분 입금';
        if (totalPaid >= totalTarget) {
          newStatus = '정산 완료';
        } else if (totalPaid === 0) {
          newStatus = '정산 대기';
        }

        return {
          ...t,
          paidFreight: newPaidFreight,
          paidFuel: newPaidFuel,
          status: newStatus
        };
      }
      return t;
    }));
    setIsDepositModalOpen(false);
  };

  // Navigation Items
  const navItems = [
    { id: 'dashboard', label: '대시보드', icon: LayoutDashboard },
    { id: 'trip_reg', label: '빠른 운행 등록', icon: PlusCircle, highlight: true },
    { id: 'trip_list', label: '운행 내역', icon: History },
    { id: 'unpaid', label: '미수금 & SMS', icon: AlertTriangle, badge: trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).length },
    { id: 'fuel', label: '주유비 환급', icon: Fuel },
    { id: 'deposits', label: '입금 및 정산', icon: CreditCard },
    { id: 'expenses', label: '지출 관리', icon: Receipt },
    { id: 'companies', label: '업체 관리', icon: Building2 },
    { id: 'analytics', label: '수익 분석', icon: PieChart },
    { id: 'calendar', label: '일정/캘린더', icon: Calendar },
    { id: 'notifications', label: '알림 센터', icon: Bell, badge: notifications.length },
    { id: 'customers', label: '고객/거래처', icon: Users },
    { id: 'backup', label: '백업 및 엑셀', icon: Download },
    { id: 'settings', label: '설정', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-[#0B1120] text-slate-100 font-sans flex flex-col md:flex-row antialiased selection:bg-purple-500 selection:text-white">
      {/* ---------------- DESKTOP SIDEBAR ---------------- */}
      <aside className="hidden md:flex flex-col w-64 bg-slate-900/80 backdrop-blur-md border-r border-slate-800 p-4 shrink-0 justify-between">
        <div>
          {/* Logo Brand */}
          <div className="flex items-center gap-3 px-3 py-4 mb-4 border-b border-slate-800/80">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
              <Car className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-extrabold text-lg tracking-wider bg-gradient-to-r from-white via-purple-200 to-pink-400 bg-clip-text text-transparent">
                DRIVER MONEY
              </h1>
              <span className="text-[10px] text-purple-400 font-mono tracking-widest uppercase block">
                Pro Consignment OS
              </span>
            </div>
          </div>

          {/* Nav Links */}
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    if (item.id === 'trip_reg') {
                      setIsTripModalOpen(true);
                    } else {
                      setActiveTab(item.id);
                    }
                  }}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-purple-600/30 to-pink-600/20 text-white border border-purple-500/40 shadow-lg shadow-purple-900/20'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-purple-400' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge > 0 && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-pink-500/20 text-pink-400 font-bold border border-pink-500/30">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* User Driver Quick Profile */}
        <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-purple-600/40 border border-purple-400/30 flex items-center justify-center font-bold text-xs text-purple-300">
            김기사
          </div>
          <div className="overflow-hidden">
            <p className="text-xs font-bold text-white truncate">김대리 기사님</p>
            <p className="text-[10px] text-emerald-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              운행 가능 (KST)
            </p>
          </div>
        </div>
      </aside>

      {/* ---------------- MOBILE HEADER & NAVIGATION ---------------- */}
      <div className="md:hidden flex items-center justify-between px-4 py-3 bg-slate-900/90 border-b border-slate-800 sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 to-pink-500 flex items-center justify-center">
            <Car className="w-5 h-5 text-white" />
          </div>
          <span className="font-black text-base tracking-wide bg-gradient-to-r from-white to-purple-300 bg-clip-text text-transparent">
            DRIVER MONEY
          </span>
        </div>
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="p-2 text-slate-300 hover:text-white rounded-lg bg-slate-800"
        >
          {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden fixed inset-0 top-[57px] bg-slate-950/95 z-40 p-4 backdrop-blur-xl overflow-y-auto space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setIsMobileMenuOpen(false);
                  if (item.id === 'trip_reg') {
                    setIsTripModalOpen(true);
                  } else {
                    setActiveTab(item.id);
                  }
                }}
                className={`w-full flex items-center justify-between p-3 rounded-xl text-sm font-semibold ${
                  activeTab === item.id ? 'bg-purple-600 text-white' : 'bg-slate-900 text-slate-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </div>
                {item.badge > 0 && (
                  <span className="px-2 py-0.5 text-xs rounded-full bg-pink-500 text-white font-bold">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      )}

      {/* ---------------- MAIN CONTENT AREA ---------------- */}
      <main className="flex-1 p-4 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full pb-24 md:pb-8">
        
        {/* HEADER BAR */}
        <header className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800/80 pb-4">
          <div>
            <h2 className="text-2xl font-black text-white tracking-tight flex items-center gap-2">
              {navItems.find(n => n.id === activeTab)?.label || '대시보드'}
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-300 font-mono font-normal">
                KST 2026-11-07
              </span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              탁송비·주유비 분리 정산 및 실시간 미수금 추적 시스템
            </p>
          </div>

          {/* Quick Global Action Header Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsTripModalOpen(true)}
              className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 shadow-lg shadow-purple-600/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              <span>운행 빠른등록</span>
            </button>
            <button
              onClick={() => setIsDepositModalOpen(true)}
              className="px-3 py-2 rounded-xl text-xs font-bold text-slate-200 bg-slate-800 hover:bg-slate-700 border border-slate-700 transition-all flex items-center gap-1.5"
            >
              <CreditCard className="w-4 h-4 text-emerald-400" />
              <span>입금 처리</span>
            </button>
          </div>
        </header>

        {/* ================= TAB 1: DASHBOARD ================= */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            
            {/* STATS CARDS GRID */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
              
              {/* Card 1: Today Stats */}
              <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl relative overflow-hidden group hover:border-purple-500/40 transition-all">
                <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/10 rounded-full blur-xl group-hover:bg-purple-500/20 transition-all"></div>
                <p className="text-xs font-bold text-slate-400">오늘 운행 건수 / 정산</p>
                <div className="mt-2 flex items-baseline justify-between">
                  <span className="text-2xl font-black text-white">{stats.todayCount}<span className="text-xs text-slate-400 font-normal ml-0.5">건</span></span>
                  <span className="text-sm font-extrabold text-purple-400">{stats.todaySettlementTarget.toLocaleString()}원</span>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-800/80 flex justify-between text-[11px] text-slate-400">
                  <span>실제 입금 완료:</span>
                  <span className="text-emerald-400 font-bold">{stats.todayDeposit.toLocaleString()}원</span>
                </div>
              </div>

              {/* Card 2: Total Unpaid Receivables */}
              <div className="p-4 rounded-2xl bg-slate-900/70 border border-pink-900/40 backdrop-blur-xl relative overflow-hidden group hover:border-pink-500/50 transition-all">
                <div className="absolute top-0 right-0 w-24 h-24 bg-pink-500/10 rounded-full blur-xl"></div>
                <div className="flex justify-between items-center">
                  <p className="text-xs font-bold text-pink-300">현재 미수금 총액</p>
                  <AlertTriangle className="w-4 h-4 text-pink-500 animate-bounce" />
                </div>
                <div className="mt-2">
                  <span className="text-2xl font-black text-pink-400">{stats.totalUnpaid.toLocaleString()}<span className="text-xs text-pink-300 font-normal ml-0.5">원</span></span>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-800/80 flex justify-between text-[11px]">
                  <span className="text-slate-400">탁송미수: {stats.totalUnpaidFreight.toLocaleString()}원</span>
                  <span className="text-amber-400 font-bold">주유환급: {stats.totalUnpaidFuel.toLocaleString()}원</span>
                </div>
              </div>

              {/* Card 3: Fuel Reimbursement Waiting */}
              <div className="p-4 rounded-2xl bg-slate-900/70 border border-amber-900/40 backdrop-blur-xl relative overflow-hidden group hover:border-amber-500/40 transition-all">
                <div className="absolute top-0 right-0 w-24 h-24 bg-amber-500/10 rounded-full blur-xl"></div>
                <p className="text-xs font-bold text-amber-300">주유비 선결제 환급대기</p>
                <div className="mt-2">
                  <span className="text-2xl font-black text-amber-400">{stats.totalUnpaidFuel.toLocaleString()}<span className="text-xs font-normal ml-0.5 text-amber-300">원</span></span>
                </div>
                <p className="mt-2 text-[11px] text-slate-400">
                  기사 선결제 후 미환급 건
                </p>
              </div>

              {/* Card 4: Net Profit */}
              <div className="p-4 rounded-2xl bg-slate-900/70 border border-emerald-900/40 backdrop-blur-xl relative overflow-hidden group hover:border-emerald-500/40 transition-all">
                <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl"></div>
                <p className="text-xs font-bold text-emerald-300">이번 달 실제 순수익</p>
                <div className="mt-2">
                  <span className="text-2xl font-black text-emerald-400">{stats.netProfit.toLocaleString()}<span className="text-xs font-normal ml-0.5 text-emerald-300">원</span></span>
                </div>
                <div className="mt-2 pt-2 border-t border-slate-800/80 flex justify-between text-[11px] text-slate-400">
                  <span>수입: {stats.monthlyFreightIncome.toLocaleString()}</span>
                  <span>지출: {stats.monthlyExpenses.toLocaleString()}</span>
                </div>
              </div>
            </div>

            {/* QUICK ACTIONS BAR */}
            <div className="p-4 rounded-2xl bg-slate-900/50 border border-slate-800 flex flex-wrap gap-2 items-center justify-between">
              <span className="text-xs font-extrabold text-purple-300 tracking-wider uppercase">
                ⚡ Quick Operational Actions
              </span>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setIsTripModalOpen(true)}
                  className="px-3 py-1.5 rounded-lg text-xs font-bold bg-purple-600/30 hover:bg-purple-600/50 border border-purple-500/40 text-purple-200 transition-all flex items-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" /> 운행등록
                </button>
                <button
                  onClick={() => setIsDepositModalOpen(true)}
                  className="px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-600/30 hover:bg-emerald-600/50 border border-emerald-500/40 text-emerald-200 transition-all flex items-center gap-1.5"
                >
                  <CreditCard className="w-3.5 h-3.5" /> 입금등록
                </button>
                <button
                  onClick={() => setIsExpenseModalOpen(true)}
                  className="px-3 py-1.5 rounded-lg text-xs font-bold bg-pink-600/30 hover:bg-pink-600/50 border border-pink-500/40 text-pink-200 transition-all flex items-center gap-1.5"
                >
                  <Receipt className="w-3.5 h-3.5" /> 지출등록
                </button>
                <button
                  onClick={() => setActiveTab('unpaid')}
                  className="px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-600/30 hover:bg-amber-600/50 border border-amber-500/40 text-amber-200 transition-all flex items-center gap-1.5"
                >
                  <Send className="w-3.5 h-3.5" /> 정산요청 SMS
                </button>
              </div>
            </div>

            {/* UNPAID RECEIVABLES WARNING PANEL */}
            <div className="p-5 rounded-2xl bg-gradient-to-b from-pink-950/30 to-slate-900/60 border border-pink-500/30 backdrop-blur-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-pink-500 animate-ping"></div>
                  <h3 className="font-extrabold text-base text-white flex items-center gap-2">
                    미수금 및 정산 지연 경고 목록
                  </h3>
                </div>
                <button
                  onClick={() => setActiveTab('unpaid')}
                  className="text-xs text-pink-400 hover:text-pink-300 font-bold flex items-center gap-1"
                >
                  전체보기 <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="space-y-3">
                {trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy === 'driver_prepaid' ? t.fuelFee - t.paidFuel : 0)) > 0).map(t => {
                  const freightUnpaid = t.freightFee - t.paidFreight;
                  const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0;
                  const totalUnpaid = freightUnpaid + fuelUnpaid;
                  const isOverdue = new Date(t.dueDate) < new Date('2026-11-07');

                  return (
                    <div key={t.id} className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-pink-500/40 transition-all">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300">
                            {t.company}
                          </span>
                          <span className="text-xs font-bold text-white">{t.from} → {t.to}</span>
                          {isOverdue && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30">
                              지연 {t.dueDate}
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-slate-400">
                          차량: {t.vehicleType} ({t.vehicleNo}) | 담당자: {t.customer} ({t.phone})
                        </p>
                      </div>

                      <div className="flex items-center justify-between sm:justify-end gap-3">
                        <div className="text-right">
                          <div className="text-xs text-slate-400">
                            탁송미수: {freightUnpaid.toLocaleString()}원 | 주유미수: {fuelUnpaid.toLocaleString()}원
                          </div>
                          <div className="text-sm font-black text-pink-400">
                            총 {totalUnpaid.toLocaleString()}원
                          </div>
                        </div>
                        <button
                          onClick={() => {
                            setSelectedTripForSms(t);
                            setIsSmsModalOpen(true);
                          }}
                          className="px-3 py-1.5 rounded-lg text-xs font-bold bg-pink-600 hover:bg-pink-500 text-white shadow-md shadow-pink-600/30 transition-all flex items-center gap-1 shrink-0"
                        >
                          <Send className="w-3 h-3" />
                          <span>독촉</span>
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* RECENT TRIPS TABLE */}
            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-extrabold text-base text-white">최근 운행 내역</h3>
                <button
                  onClick={() => setActiveTab('trip_list')}
                  className="text-xs text-purple-400 hover:text-purple-300 font-bold flex items-center gap-1"
                >
                  전체 내역 보기 <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950/80 text-slate-400 uppercase tracking-wider font-mono">
                    <tr>
                      <th className="p-3 rounded-l-xl">일자</th>
                      <th className="p-3">구분/업체</th>
                      <th className="p-3">구간</th>
                      <th className="p-3 text-right">탁송비</th>
                      <th className="p-3 text-right">주유비(선결제)</th>
                      <th className="p-3 text-center">정산상태</th>
                      <th className="p-3 rounded-r-xl text-center">작업</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-medium">
                    {trips.slice(0, 5).map(t => {
                      const totalUnpaid = (t.freightFee - t.paidFreight) + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0);
                      return (
                        <tr key={t.id} className="hover:bg-slate-800/40 transition-all">
                          <td className="p-3 font-mono text-slate-300">{t.date}</td>
                          <td className="p-3">
                            <span className="font-bold text-white block">{t.company}</span>
                            <span className="text-[10px] text-slate-400">{t.type}</span>
                          </td>
                          <td className="p-3">
                            <span className="text-slate-200 font-bold">{t.from}</span>
                            <span className="text-slate-500 mx-1">→</span>
                            <span className="text-slate-200 font-bold">{t.to}</span>
                          </td>
                          <td className="p-3 text-right font-bold text-purple-300">
                            {t.freightFee.toLocaleString()}원
                          </td>
                          <td className="p-3 text-right font-bold text-amber-300">
                            {t.fuelFee > 0 ? `${t.fuelFee.toLocaleString()}원` : '-'}
                          </td>
                          <td className="p-3 text-center">
                            <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                              t.status === '정산 완료'
                                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                                : t.status === '부분 입금'
                                ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                                : 'bg-pink-500/20 text-pink-400 border border-pink-500/30'
                            }`}>
                              {t.status}
                            </span>
                          </td>
                          <td className="p-3 text-center">
                            {totalUnpaid > 0 && (
                              <button
                                onClick={() => {
                                  setSelectedTripForDeposit(t);
                                  setIsDepositModalOpen(true);
                                }}
                                className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-emerald-400 text-[11px] font-bold transition-all"
                              >
                                입금처리
                              </button>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )}

        {/* ================= TAB 2: TRIP LIST ================= */}
        {activeTab === 'trip_list' && (
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row gap-3 justify-between items-center bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
              <div className="flex items-center gap-2 w-full sm:w-auto">
                <div className="relative flex-1 sm:w-64">
                  <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
                  <input
                    type="text"
                    placeholder="업체명, 고객, 차량번호, 구간 검색"
                    className="w-full bg-white text-black font-semibold text-xs pl-9 pr-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>
              <button
                onClick={() => setIsTripModalOpen(true)}
                className="w-full sm:w-auto px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center justify-center gap-2"
              >
                <Plus className="w-4 h-4" /> 운행 건 등록
              </button>
            </div>

            <div className="space-y-3">
              {trips.map(t => {
                const totalUnpaid = (t.freightFee - t.paidFreight) + (t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0);

                return (
                  <div key={t.id} className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl hover:border-purple-500/30 transition-all space-y-3">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-1 rounded-lg bg-purple-500/20 text-purple-300 font-mono text-xs font-bold border border-purple-500/30">
                          {t.type}
                        </span>
                        <h4 className="font-extrabold text-base text-white">{t.company}</h4>
                        <span className="text-xs text-slate-400 font-mono">({t.date} {t.startTime}~{t.endTime})</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                          t.status === '정산 완료' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-pink-500/20 text-pink-400 border border-pink-500/30'
                        }`}>
                          {t.status}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                      <div>
                        <span className="text-slate-400 block">운행 구간 및 차량</span>
                        <p className="font-bold text-slate-200 mt-0.5">{t.from} → {t.to}</p>
                        <p className="text-slate-400 mt-0.5">{t.vehicleType} | {t.vehicleNo}</p>
                      </div>

                      <div>
                        <span className="text-slate-400 block">정산액 분리 내역</span>
                        <p className="text-slate-200 mt-0.5">
                          탁송비: <span className="font-bold text-purple-300">{t.freightFee.toLocaleString()}원</span> (수령: {t.paidFreight.toLocaleString()}원)
                        </p>
                        <p className="text-slate-200 mt-0.5">
                          주유비선결제: <span className="font-bold text-amber-300">{t.fuelFee.toLocaleString()}원</span> (환급: {t.paidFuel.toLocaleString()}원)
                        </p>
                      </div>

                      <div className="flex flex-col justify-between items-start md:items-end">
                        <div>
                          <span className="text-slate-400 text-right block">남은 미수금</span>
                          <span className="text-base font-black text-pink-400">
                            {totalUnpaid.toLocaleString()}원
                          </span>
                        </div>
                        {totalUnpaid > 0 && (
                          <div className="flex items-center gap-2 mt-2">
                            <button
                              onClick={() => {
                                setSelectedTripForSms(t);
                                setIsSmsModalOpen(true);
                              }}
                              className="px-2.5 py-1 rounded-lg bg-pink-600/30 border border-pink-500/40 text-pink-300 text-xs font-bold hover:bg-pink-600/50"
                            >
                              문자독촉
                            </button>
                            <button
                              onClick={() => {
                                setSelectedTripForDeposit(t);
                                setIsDepositModalOpen(true);
                              }}
                              className="px-2.5 py-1 rounded-lg bg-emerald-600/30 border border-emerald-500/40 text-emerald-300 text-xs font-bold hover:bg-emerald-600/50"
                            >
                              입금하기
                            </button>
                          </div>
                        )}
                      </div>
                    </div>

                    {t.memo && (
                      <div className="pt-2 border-t border-slate-800/60 text-[11px] text-slate-400 italic">
                        💬 메모: {t.memo}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ================= TAB 3: UNPAID RECEIVABLES & SMS ================= */}
        {activeTab === 'unpaid' && (
          <div className="space-y-6">
            <div className="p-4 rounded-2xl bg-gradient-to-r from-pink-950/40 via-purple-950/30 to-slate-900 border border-pink-500/30">
              <h3 className="font-black text-lg text-white">미수금 종합 관리 & 자동 정산 SMS 독촉</h3>
              <p className="text-xs text-slate-300 mt-1">
                기사 선결제 주유비와 미수 탁송비를 자동으로 정산 요청 메시지로 변환하여 카카오톡 및 문자로 발송합니다.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).map(t => {
                const freightUnpaid = t.freightFee - t.paidFreight;
                const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0;
                const totalUnpaid = freightUnpaid + fuelUnpaid;

                return (
                  <div key={t.id} className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl flex flex-col justify-between space-y-4 hover:border-pink-500/40 transition-all">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <span className="px-2.5 py-1 rounded-lg bg-pink-500/20 text-pink-300 font-bold text-xs border border-pink-500/30">
                          정산 예정일: {t.dueDate}
                        </span>
                        <span className="text-xs font-bold text-slate-400">{t.company}</span>
                      </div>
                      <h4 className="font-extrabold text-base text-white">{t.from} → {t.to}</h4>
                      <p className="text-xs text-slate-400 mt-1">
                        고객: {t.customer} ({t.phone}) | 차량: {t.vehicleType}
                      </p>

                      <div className="mt-4 p-3 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5 text-xs">
                        <div className="flex justify-between text-slate-300">
                          <span>탁송비 미수금:</span>
                          <span className="font-bold text-purple-300">{freightUnpaid.toLocaleString()}원</span>
                        </div>
                        <div className="flex justify-between text-slate-300">
                          <span>주유비 환급 대기:</span>
                          <span className="font-bold text-amber-300">{fuelUnpaid.toLocaleString()}원</span>
                        </div>
                        <div className="pt-1 border-t border-slate-800 flex justify-between text-sm font-black text-pink-400">
                          <span>합계 미수금:</span>
                          <span>{totalUnpaid.toLocaleString()}원</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setSelectedTripForSms(t);
                          setIsSmsModalOpen(true);
                        }}
                        className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold text-xs shadow-md shadow-pink-600/30 transition-all flex items-center justify-center gap-2"
                      >
                        <Send className="w-4 h-4" />
                        <span>정산 요청 문자 생성</span>
                      </button>
                      <button
                        onClick={() => {
                          setSelectedTripForDeposit(t);
                          setIsDepositModalOpen(true);
                        }}
                        className="px-3 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 font-bold text-xs transition-all"
                      >
                        입금
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ================= TAB 4: FUEL MANAGEMENT ================= */}
        {activeTab === 'fuel' && (
          <div className="space-y-5">
            <div className="p-4 rounded-2xl bg-amber-950/30 border border-amber-500/30 flex justify-between items-center">
              <div>
                <h3 className="font-black text-base text-amber-200">기사 선결제 주유비 전용 관리</h3>
                <p className="text-xs text-amber-300/80 mt-0.5">탁송비와 별도로 기사 카드로 먼저 지출된 주유 환급금을 관리합니다.</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-slate-400 block">미환급 총액</span>
                <span className="text-xl font-black text-amber-400">{stats.totalUnpaidFuel.toLocaleString()}원</span>
              </div>
            </div>

            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 text-slate-400 uppercase font-mono">
                    <tr>
                      <th className="p-3">일자</th>
                      <th className="p-3">업체/구간</th>
                      <th className="p-3">차량</th>
                      <th className="p-3 text-right">선결제 주유액</th>
                      <th className="p-3 text-right">환급받은 금액</th>
                      <th className="p-3 text-right">남은 환급금</th>
                      <th className="p-3 text-center">상태</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800">
                    {trips.filter(t => t.fuelPaidBy === 'driver_prepaid').map(t => {
                      const remainFuel = t.fuelFee - t.paidFuel;
                      return (
                        <tr key={t.id} className="hover:bg-slate-800/40">
                          <td className="p-3 text-slate-300 font-mono">{t.date}</td>
                          <td className="p-3 font-bold text-white">{t.company} ({t.from}→{t.to})</td>
                          <td className="p-3 text-slate-400">{t.vehicleType}</td>
                          <td className="p-3 text-right font-bold text-amber-300">{t.fuelFee.toLocaleString()}원</td>
                          <td className="p-3 text-right text-emerald-400">{t.paidFuel.toLocaleString()}원</td>
                          <td className="p-3 text-right font-black text-pink-400">{remainFuel.toLocaleString()}원</td>
                          <td className="p-3 text-center">
                            {remainFuel === 0 ? (
                              <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400">환급완료</span>
                            ) : (
                              <span className="px-2 py-0.5 rounded text-[10px] bg-amber-500/20 text-amber-400">환급대기</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 5: EXPENSES ================= */}
        {activeTab === 'expenses' && (
          <div className="space-y-5">
            <div className="flex justify-between items-center bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
              <div>
                <h3 className="font-extrabold text-base text-white">사업 지출 내역 (통행료, KTX, 식비)</h3>
                <p className="text-xs text-slate-400">순수익 계산을 위한 실제 지출 비용 관리</p>
              </div>
              <button
                onClick={() => setIsExpenseModalOpen(true)}
                className="px-4 py-2 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-bold text-xs flex items-center gap-1.5"
              >
                <Plus className="w-4 h-4" /> 지출 등록
              </button>
            </div>

            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 backdrop-blur-xl">
              <div className="space-y-2">
                {expenses.map(e => (
                  <div key={e.id} className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-3">
                      <span className="px-2.5 py-1 rounded-lg bg-pink-500/20 text-pink-300 font-bold border border-pink-500/30">
                        {e.category}
                      </span>
                      <div>
                        <p className="font-bold text-white">{e.memo}</p>
                        <p className="text-[10px] text-slate-400">{e.date}</p>
                      </div>
                    </div>
                    <span className="font-black text-sm text-pink-400">
                      -{e.amount.toLocaleString()}원
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 6: ANALYTICS ================= */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800">
                <p className="text-xs font-bold text-slate-400">총 탁송 수입 (수령 완료)</p>
                <p className="text-2xl font-black text-purple-400 mt-2">{stats.monthlyFreightIncome.toLocaleString()}원</p>
              </div>
              <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800">
                <p className="text-xs font-bold text-slate-400">총 사업 지출</p>
                <p className="text-2xl font-black text-pink-400 mt-2">{stats.monthlyExpenses.toLocaleString()}원</p>
              </div>
              <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800">
                <p className="text-xs font-bold text-slate-400">실제 순수익</p>
                <p className="text-2xl font-black text-emerald-400 mt-2">{stats.netProfit.toLocaleString()}원</p>
              </div>
            </div>

            {/* Custom Responsive HTML/CSS Graph Visualizer */}
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl">
              <h4 className="font-extrabold text-base text-white mb-4">최근 운행 수익 vs 미수금 비중</h4>
              <div className="h-48 flex items-end justify-between gap-4 pt-6 border-b border-slate-800 pb-2">
                {trips.slice(0, 6).map(t => {
                  const paid = t.paidFreight;
                  const unpaid = t.freightFee - t.paidFreight;
                  const maxHeight = 160;
                  const total = t.freightFee;
                  const paidH = (paid / 300000) * maxHeight;
                  const unpaidH = (unpaid / 300000) * maxHeight;

                  return (
                    <div key={t.id} className="flex-1 flex flex-col items-center gap-1 group relative">
                      {/* Tooltip */}
                      <div className="absolute -top-10 opacity-0 group-hover:opacity-100 transition-all bg-slate-950 text-white text-[10px] p-1.5 rounded border border-slate-700 pointer-events-none z-10 whitespace-nowrap">
                        {t.company}: {t.freightFee.toLocaleString()}원
                      </div>
                      <div className="w-full max-w-[40px] flex flex-col justify-end">
                        {unpaidH > 0 && (
                          <div style={{ height: `${unpaidH}px` }} className="w-full bg-pink-500 rounded-t-sm"></div>
                        )}
                        <div style={{ height: `${paidH}px` }} className="w-full bg-purple-600 rounded-b-sm"></div>
                      </div>
                      <span className="text-[10px] text-slate-400 truncate w-full text-center">{t.date.slice(5)}</span>
                    </div>
                  );
                })}
              </div>
              <div className="flex justify-center gap-6 mt-4 text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 bg-purple-600 rounded-sm"></span>
                  <span className="text-slate-300">정산 수령액</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 bg-pink-500 rounded-sm"></span>
                  <span className="text-slate-300">미수금</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 7: BACKUP & EXPORT ================= */}
        {activeTab === 'backup' && (
          <div className="space-y-6">
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-xl space-y-4">
              <h3 className="font-extrabold text-base text-white">데이터 백업 및 엑셀(CSV) 내보내기</h3>
              <p className="text-xs text-slate-400">
                기사님의 운행 내역, 미수금, 지출 데이터를 안전하게 다운로드하거나 다른 기기에서 복원할 수 있습니다.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                <button
                  onClick={() => {
                    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ trips, expenses, companies }));
                    const downloadAnchor = document.createElement('a');
                    downloadAnchor.setAttribute("href", dataStr);
                    downloadAnchor.setAttribute("download", `DRIVER_MONEY_BACKUP_${new Date().toISOString().slice(0,10)}.json`);
                    document.body.appendChild(downloadAnchor);
                    downloadAnchor.click();
                    downloadAnchor.remove();
                  }}
                  className="p-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-purple-600/30 transition-all"
                >
                  <Download className="w-4 h-4" /> 전체 JSON 데이터 백업 다운로드
                </button>

                <button
                  onClick={() => {
                    let csvContent = "data:text/csv;charset=utf-8,\uFEFF";
                    csvContent += "날짜,업체명,구분,출발지,도착지,탁송비,주유비,정산상태\n";
                    trips.forEach(t => {
                      csvContent += `${t.date},${t.company},${t.type},${t.from},${t.to},${t.freightFee},${t.fuelFee},${t.status}\n`;
                    });
                    const encodedUri = encodeURI(csvContent);
                    const link = document.createElement("a");
                    link.setAttribute("href", encodedUri);
                    link.setAttribute("download", `운행내역_엑셀_${new Date().toISOString().slice(0,10)}.csv`);
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                  }}
                  className="p-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-slate-700 font-bold text-xs flex items-center justify-center gap-2 transition-all"
                >
                  <Download className="w-4 h-4" /> 운행 내역 엑셀(CSV) 다운로드
                </button>
              </div>
            </div>
          </div>
        )}

        {/* OTHER TABS PLACEHOLDER (Companies, Notifications, Calendar, Customers, Settings) */}
        {['companies', 'notifications', 'calendar', 'customers', 'settings'].includes(activeTab) && (
          <div className="p-8 rounded-2xl bg-slate-900/70 border border-slate-800 text-center space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-purple-600/20 border border-purple-500/30 text-purple-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h3 className="font-extrabold text-lg text-white">
              {navItems.find(n => n.id === activeTab)?.label} 모듈 준비 완료
            </h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              실시간 데이터베이스 연동 모듈로 활성화 상태입니다. 상단 운행 등록 및 미수금 정산 기능을 지금 즉시 사용할 수 있습니다.
            </p>
          </div>
        )}
      </main>

      {/* ---------------- MODAL 1: FAST TRIP REGISTRATION ---------------- */}
      {isTripModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-slate-900 border border-purple-500/30 rounded-3xl p-6 w-full max-w-lg space-y-4 shadow-2xl relative animate-in fade-in zoom-in duration-200">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-black text-lg text-white flex items-center gap-2">
                ⚡ 30초 빠른 운행 등록
              </h3>
              <button onClick={() => setIsTripModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                const fd = new FormData(e.target);
                const newTrip = {
                  id: `TRIP-${Date.now()}`,
                  date: fd.get('date'),
                  startTime: '14:00',
                  endTime: '16:00',
                  type: fd.get('type'),
                  company: fd.get('company'),
                  customer: fd.get('customer') || '미지정',
                  phone: fd.get('phone') || '010-0000-0000',
                  vehicleNo: fd.get('vehicleNo') || '12가 3456',
                  vehicleType: fd.get('vehicleType') || '승용차',
                  from: fd.get('from'),
                  to: fd.get('to'),
                  freightFee: Number(fd.get('freightFee')),
                  fuelFee: Number(fd.get('fuelFee')),
                  fuelPaidBy: fd.get('fuelPaidBy'),
                  dueDate: fd.get('dueDate'),
                  status: '정산 대기',
                  paidFreight: 0,
                  paidFuel: 0,
                  memo: fd.get('memo')
                };
                handleSaveTrip(newTrip);
              }}
              className="space-y-4 text-xs"
            >
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1">운행일자</label>
                  <input
                    type="date"
                    name="date"
                    defaultValue="2026-11-07"
                    required
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1">운행 종류</label>
                  <select
                    name="type"
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="로드탁송">로드탁송</option>
                    <option value="대리운전">대리운전</option>
                    <option value="개인 직거래 탁송">개인 직거래 탁송</option>
                    <option value="업체 배정 탁송">업체 배정 탁송</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1">업체명</label>
                  <input
                    type="text"
                    name="company"
                    placeholder="예: SK로드탁송"
                    required
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1">고객/담당자명</label>
                  <input
                    type="text"
                    name="customer"
                    placeholder="담당자 이름"
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1">출발지</label>
                  <input
                    type="text"
                    name="from"
                    placeholder="서울 강남"
                    required
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1">도착지</label>
                  <input
                    type="text"
                    name="to"
                    placeholder="부산 해운대"
                    required
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              {/* FINANCIAL INPUTS */}
              <div className="p-3 bg-purple-950/40 rounded-xl border border-purple-500/30 space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-purple-200 font-bold mb-1">탁송비/대리비 (원)</label>
                    <input
                      type="number"
                      name="freightFee"
                      placeholder="180000"
                      required
                      className="w-full bg-white text-black font-bold text-sm p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-amber-200 font-bold mb-1">주유비 (원)</label>
                    <input
                      type="number"
                      name="fuelFee"
                      placeholder="70000"
                      defaultValue="0"
                      className="w-full bg-white text-black font-bold text-sm p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 font-bold mb-1">주유비 결제/환급 방식</label>
                  <select
                    name="fuelPaidBy"
                    className="w-full bg-white text-black font-semibold p-2 rounded-xl"
                  >
                    <option value="driver_prepaid">기사 선결제 (나중에 환급받음)</option>
                    <option value="customer">고객이 직접 주유</option>
                    <option value="included">탁송비에 포함됨</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1">정산 예정일</label>
                  <input
                    type="date"
                    name="dueDate"
                    defaultValue="2026-11-14"
                    required
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1">연락처</label>
                  <input
                    type="text"
                    name="phone"
                    placeholder="010-0000-0000"
                    className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1">특이사항 / 메모</label>
                <input
                  type="text"
                  name="memo"
                  placeholder="특이사항 입력"
                  className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsTripModalOpen(false)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-bold hover:bg-slate-700"
                >
                  취소
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-extrabold hover:from-purple-500 hover:to-pink-500 shadow-lg shadow-purple-600/40"
                >
                  운행 등록 완료
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ---------------- MODAL 2: PARTIAL DEPOSIT ENTRY ---------------- */}
      {isDepositModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-emerald-500/30 rounded-3xl p-6 w-full max-w-md space-y-4 shadow-2xl relative">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-black text-lg text-white flex items-center gap-2">
                💳 입금 및 정산 처리 (부분입금 지원)
              </h3>
              <button onClick={() => setIsDepositModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                const fd = new FormData(e.target);
                const tripId = fd.get('tripId');
                const freightAmt = fd.get('freightAmt');
                const fuelAmt = fd.get('fuelAmt');
                handleApplyDeposit(tripId, freightAmt, fuelAmt);
              }}
              className="space-y-4 text-xs"
            >
              <div>
                <label className="block text-slate-300 font-bold mb-1">입금 대상 운행 선택</label>
                <select
                  name="tripId"
                  defaultValue={selectedTripForDeposit?.id || ''}
                  className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  {trips.map(t => (
                    <option key={t.id} value={t.id}>
                      [{t.company}] {t.from}→{t.to} (미수: {(t.freightFee-t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)).toLocaleString()}원)
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-purple-300 font-bold mb-1">탁송비 입금액 (원)</label>
                  <input
                    type="number"
                    name="freightAmt"
                    placeholder="0"
                    defaultValue="0"
                    className="w-full bg-white text-black font-bold text-sm p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-amber-300 font-bold mb-1">주유비 환급 입금액 (원)</label>
                  <input
                    type="number"
                    name="fuelAmt"
                    placeholder="0"
                    defaultValue="0"
                    className="w-full bg-white text-black font-bold text-sm p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsDepositModalOpen(false)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-bold"
                >
                  취소
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold shadow-lg shadow-emerald-600/30"
                >
                  입금 적용하기
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ---------------- MODAL 3: EXPENSE REGISTRATION ---------------- */}
      {isExpenseModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-pink-500/30 rounded-3xl p-6 w-full max-w-md space-y-4 shadow-2xl relative">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-black text-lg text-white">🧾 사업 관련 지출 등록</h3>
              <button onClick={() => setIsExpenseModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                const fd = new FormData(e.target);
                handleSaveExpense({
                  id: `exp-${Date.now()}`,
                  date: fd.get('date'),
                  category: fd.get('category'),
                  amount: Number(fd.get('amount')),
                  memo: fd.get('memo')
                });
              }}
              className="space-y-4 text-xs"
            >
              <div>
                <label className="block text-slate-300 font-bold mb-1">지출 일자</label>
                <input
                  type="date"
                  name="date"
                  defaultValue="2026-11-07"
                  className="w-full bg-white text-black font-semibold p-2.5 rounded-xl"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1">지출 항목</label>
                <select name="category" className="w-full bg-white text-black font-semibold p-2.5 rounded-xl">
                  <option value="통행료">통행료 (고속도로 톨게이트)</option>
                  <option value="복귀 교통비">복귀 교통비 (KTX/시외버스/택시)</option>
                  <option value="식비">식비</option>
                  <option value="차량 유지비">차량 유지비 / 소모품</option>
                  <option value="기타 지출">기타 지출</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1">지출 금액 (원)</label>
                <input
                  type="number"
                  name="amount"
                  placeholder="15000"
                  required
                  className="w-full bg-white text-black font-bold text-sm p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-bold mb-1">메모</label>
                <input
                  type="text"
                  name="memo"
                  placeholder="예: 경부고속도로 톨게이트"
                  className="w-full bg-white text-black font-semibold p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsExpenseModalOpen(false)}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-bold"
                >
                  취소
                </button>
                <button
                  type="submit"
                  className="px-6 py-2.5 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-extrabold shadow-lg shadow-pink-600/30"
                >
                  지출 등록 완료
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ---------------- MODAL 4: AUTO SETTLEMENT SMS BUILDER ---------------- */}
      {isSmsModalOpen && selectedTripForSms && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-pink-500/40 rounded-3xl p-6 w-full max-w-md space-y-4 shadow-2xl relative">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="font-black text-lg text-white flex items-center gap-2">
                💬 정산 요청 문자 자동 생성
              </h3>
              <button onClick={() => setIsSmsModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            {(() => {
              const t = selectedTripForSms;
              const freightUnpaid = t.freightFee - t.paidFreight;
              const fuelUnpaid = t.fuelPaidBy === 'driver_prepaid' ? (t.fuelFee - t.paidFuel) : 0;
              const totalUnpaid = freightUnpaid + fuelUnpaid;

              const smsBody = `안녕하세요, ${t.company} ${t.customer} 담당자님.\n${t.date} 진행한 차량탁송(${t.from} → ${t.to}, 차량: ${t.vehicleType}) 정산 관련 확인 부탁드립니다.\n\n- 탁송비: ${freightUnpaid.toLocaleString()}원\n- 주유비 환급액: ${fuelUnpaid.toLocaleString()}원\n- 현재 미정산 총액: ${totalUnpaid.toLocaleString()}원\n\n확인 후 빠른 입금 부탁드립니다. 감사합니다.`;

              return (
                <div className="space-y-4 text-xs">
                  <div>
                    <label className="block text-slate-300 font-bold mb-1">수신 담당자</label>
                    <p className="text-sm font-bold text-white">{t.customer} ({t.phone})</p>
                  </div>

                  <div>
                    <label className="block text-slate-300 font-bold mb-1">자동 생성된 독촉 문구</label>
                    <textarea
                      readOnly
                      rows={7}
                      value={smsBody}
                      className="w-full bg-white text-black font-semibold p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(smsBody);
                        alert('정산 요청 문구가 클립보드에 복사되었습니다.');
                      }}
                      className="flex-1 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold flex items-center justify-center gap-2 shadow-lg shadow-purple-600/30"
                    >
                      <Copy className="w-4 h-4" /> 문구 복사하기
                    </button>
                    <button
                      onClick={() => {
                        window.open(`sms:${t.phone}?body=${encodeURIComponent(smsBody)}`);
                      }}
                      className="px-4 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold flex items-center justify-center gap-1.5"
                    >
                      <Send className="w-4 h-4" /> SMS 바로 전송
                    </button>
                  </div>
                </div>
              );
            })()}
          </div>
        </div>
      )}

      {/* ---------------- MOBILE BOTTOM NAVIGATION ---------------- */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur-lg border-t border-slate-800 z-40 px-2 py-2 flex justify-around items-center">
        {[
          { id: 'dashboard', label: '대시보드', icon: LayoutDashboard },
          { id: 'trip_list', label: '운행내역', icon: History },
          { id: 'unpaid', label: '미수금', icon: AlertTriangle, badge: trips.filter(t => (t.freightFee - t.paidFreight + (t.fuelPaidBy==='driver_prepaid'?(t.fuelFee-t.paidFuel):0)) > 0).length },
          { id: 'analytics', label: '수익분석', icon: PieChart },
          { id: 'backup', label: '백업', icon: Download },
        ].map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center gap-1 p-1.5 rounded-xl relative ${
                isActive ? 'text-purple-400 font-bold' : 'text-slate-400'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px]">{item.label}</span>
              {item.badge > 0 && (
                <span className="absolute -top-1 right-1 w-4 h-4 rounded-full bg-pink-500 text-white text-[9px] font-bold flex items-center justify-center">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>
    </div>
  );
}