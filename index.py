# 에이전트 내에서 index.html 파일 생성을 위한 파이썬 실행 코드
code = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>스마트 맞춤형 시험 플래너</title>
<!-- Tailwind CSS v4 CDN -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<!-- HTML to PDF 변환 라이브러리 추가 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css?family=Pretendard:wght@300;400;500;600;700&display=swap');
body {
    font-family: 'Pretendard', sans-serif;
    background-color: #2D3142;
    color: #F4F5F6;
}
.bg-charcoal { background-color: #2D3142; }
.bg-dark-gray { background-color: #1F222E; }
.bg-light-gray { background-color: #4F5D75; }
.bg-deep-green { background-color: #024428; }
/* 과목별 테마 컬러 클래스 */
.sub-red { background-color: #E07A5F !important; color: white; }
.sub-orange { background-color: #F4A261 !important; color: white; }
.sub-yellow { background-color: #E9C46A !important; color: #2D3142; }
.sub-green { background-color: #2A9D8F !important; color: white; }
.sub-blue { background-color: #457B9D !important; color: white; }
.sub-indigo { background-color: #1D3557 !important; color: white; }
.sub-purple { background-color: #8338EC !important; color: white; }
</style>
</head>
<body class="min-h-screen flex flex-col">
<header class="bg-dark-gray border-b border-gray-700 px-6 py-4 flex justify-between items-center shadow-lg">
    <div class="flex items-center gap-3">
        <span class="text-2xl">📅</span>
        <h1 class="text-xl font-bold tracking-tight text-white">스마트 맞춤형 시험 플래너</h1>
    </div>
    <div id="auth-status-area" class="flex items-center gap-4"></div>
</header>

<div id="auth-view" class="flex-1 flex flex-col justify-center items-center text-center p-6">
    <div class="bg-dark-gray p-8 rounded-2xl border border-gray-800 shadow-2xl max-w-md w-full">
        <span class="text-5xl block mb-4">🚀</span>
        <h2 class="text-2xl font-bold mb-2 text-white">시험 플래너 시작하기</h2>
        <p class="text-sm text-gray-400 mb-6 leading-relaxed">계정이 없으실 경우 기입하신 정보로<br>계정이 자동 생성되어 안전하게 분리 저장됩니다.</p>
        <div class="space-y-3 text-left">
            <div>
                <label class="block text-xs text-gray-400 mb-1">아이디 (이메일 형태)</label>
                <input type="email" id="username" class="w-full bg-charcoal border border-gray-700 rounded-xl p-3 text-sm focus:outline-none focus:border-blue-500 text-white" value="student@planner.com">
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">비밀번호</label>
                <input type="password" id="password" class="w-full bg-charcoal border border-gray-700 rounded-xl p-3 text-sm focus:outline-none focus:border-blue-500 text-white" value="123456">
            </div>
            <button onclick="handleGatewayLogin()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 rounded-xl transition-all shadow-lg text-sm cursor-pointer mt-2">
                로그인 / 플래너 시작
            </button>
        </div>
    </div>
</div>

<main class="flex-1 p-6 max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-4 gap-6 hidden" id="planner-view">
    <section class="space-y-6 lg:col-span-1">
        <div class="bg-dark-gray p-5 rounded-2xl border border-gray-700 space-y-4 shadow-md">
            <h3 class="text-md font-semibold text-white border-b border-gray-700 pb-2">⚙️ 플랜 주기 설정</h3>
            <div>
                <label class="block text-xs text-gray-400 mb-1">시험 대비 기간</label>
                <select id="exam-weeks" onchange="updateWeeksDropdown()" class="w-full bg-charcoal border border-gray-600 rounded-xl px-3 py-2 text-sm text-white focus:outline-none">
                    <option value="4">4주 전 대비 플랜</option>
                    <option value="5" selected>5주 전 대비 플랜</option>
                </select>
            </div>
            <div>
                <label class="block text-xs text-gray-400 mb-1">나의 과목 순위 관리 (Drag & Drop)</label>
                <div id="subject-list" class="space-y-2 mt-2"></div>
                <div class="mt-3 flex gap-1"> 
                    <input type="text" id="new-subject-name" placeholder="과목 추가" class="w-full bg-charcoal border border-gray-600 rounded-lg px-2 py-1 text-xs text-white focus:outline-none">
                    <select id="new-subject-color" class="bg-charcoal border border-gray-600 rounded-lg px-1 py-1 text-xs text-white">
                        <option value="sub-red">빨강</option>
                        <option value="sub-orange">주황</option>
                        <option value="sub-yellow">노랑</option>
                        <option value="sub-green">초록</option>
                        <option value="sub-blue">파랑</option>
                        <option value="sub-purple">보라</option>
                    </select>
                    <button onclick="addNewSubject()" class="bg-[#024428] text-white px-2 rounded-lg text-xs font-bold cursor-pointer">+</button>
                </div>
            </div>
        </div>

        <div class="bg-dark-gray rounded-2xl p-5 border border-gray-700 shadow-md">
            <h2 class="text-md font-bold mb-3 text-emerald-400">⏱️ 요일별 자습 가용 시간</h2>
            <div class="grid grid-cols-2 gap-2 text-xs" id="available-hours-inputs"></div>
        </div>

        <div class="bg-dark-gray rounded-2xl p-5 border border-gray-700 shadow-md flex flex-col">
            <h2 class="text-md font-bold mb-1 text-purple-400">✍️ 공부 분량 일괄 입력</h2>
            <p class="text-[11px] text-gray-400 mb-3 leading-relaxed">과목 이름 뒤에 하이픈(-)을 넣고 소요시간을 적어주세요.<br>예시: 수학-쎈 함수 풀기(2.5), 영어-본문암기(1.5)</p>
            <textarea id="bulk-input-area" class="w-full h-40 bg-charcoal border border-gray-700 rounded-lg p-3 text-xs text-white focus:outline-none focus:border-purple-500 font-mono" placeholder="수학-지수 문제집(3)&#10;국어-교사용 2회독(2)"></textarea>
            <button onclick="processBulkPlacement()" class="mt-3 w-full bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2.5 rounded-lg text-xs transition-all shadow-md cursor-pointer">스마트 분할 자동 배정</button>
        </div>
    </section>

    <section class="lg:col-span-3 flex flex-col gap-4">
        <div class="flex justify-between items-center bg-dark-gray p-4 rounded-xl border border-gray-800">
            <div class="flex items-center gap-4">
                <span class="text-sm font-semibold text-gray-300">현재 확인 주차:</span>
                <select id="current-week-select" onchange="changeWeekView()" class="bg-charcoal border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none"></select>
            </div>
            <!-- PDF 내보내기 버튼 추가 -->
            <button onclick="exportToPDF()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-1.5 px-4 rounded-lg text-sm transition-all shadow-md cursor-pointer flex items-center gap-1">
                📄 PDF 내보내기
            </button>
        </div>
        <div id="pdf-canvas" class="bg-dark-gray rounded-xl p-5 border border-gray-800 shadow-xl overflow-x-auto">
            <div class="grid grid-cols-7 gap-3 min-w-[850px]" id="weekly-calendar-grid"></div>
        </div>
    </section>
</main>

<div id="task-modal" class="fixed inset-0 bg-black/70 flex justify-center items-center z-50 hidden">
    <div class="bg-dark-gray border border-gray-700 w-full max-w-sm rounded-2xl p-6 shadow-2xl">
        <h3 class="text-md font-bold text-white mb-4">📝 요일별 할 일 직접 등록</h3>
        <div class="flex flex-col gap-3 text-xs">
            <div>
                <label class="block text-gray-400 mb-1">배정 과목</label>
                <select id="task-subject-select" class="w-full bg-charcoal border border-gray-700 rounded-lg p-2 text-white"></select>
            </div>
            <div>
                <label class="block text-gray-400 mb-1">상세 내용 설명</label>
                <input type="text" id="task-name-input" placeholder="학원 숙제, 오답 정리, 단어 암기 등" class="w-full bg-charcoal border border-gray-700 rounded-lg p-2 text-white">
            </div>
            <div>
                <label class="block text-gray-400 mb-1">공부 소요 시간 (단위: 시간)</label>
                <input type="number" id="task-hours-input" step="0.5" min="0.5" value="1" class="w-full bg-charcoal border border-gray-700 rounded-lg p-2 text-white">
            </div>
            <div class="flex items-center gap-2 py-1">
                <input type="checkbox" id="task-review-checkbox" class="rounded border-gray-700 bg-charcoal text-purple-600 focus:ring-0 w-4 h-4">
                <label for="task-review-checkbox" class="text-purple-300 font-medium cursor-pointer">암기 패턴 복습 활성화 (7일 뒤 리마인드 자동 복사)</label>
            </div>
            <div class="flex gap-2 mt-2">
                <button onclick="addCustomTaskToDay()" class="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-lg transition-all shadow-md cursor-pointer">일정 등록</button>
                <button onclick="document.getElementById('task-modal').classList.add('hidden')" class="bg-gray-700 text-gray-300 px-4 rounded-lg transition-all cursor-pointer">취소</button>
            </div>
        </div>
    </div>
</div>

<script>
function createDefaultState() {
    return {
        currentUser: null,
        currentWeek: 5,
        totalWeeks: 5,
        availableHours: { '월': 3, '화': 3, '수': 4, '목': 3, '금': 4, '토': 6, '일': 6},
        subjects: [
            { id: 'sub-red', name: '수학' },
            { id: 'sub-orange', name: '영어'},
            { id: 'sub-yellow', name: '국어' }
        ],
        schedules: {}
    };
}

window.state = createDefaultState();
const daysOfWeek = ['월', '화', '수', '목', '금', '토', '일'];
window.targetDayForModal = '월';
let draggedSubjectIndex = null;
let draggedTaskId = null;
let draggedOriginDay = null;

window.dragStartTask = function(e) {
    draggedTaskId = e.currentTarget.getAttribute('data-task-id');
    draggedOriginDay = e.currentTarget.getAttribute('data-origin-day');
    e.dataTransfer.effectAllowed = 'move';
};

window.dropTaskToDay = function(e) {
    e.preventDefault();
    const targetDay = e.currentTarget.getAttribute('data-day');
    if(!targetDay || !draggedTaskId || draggedOriginDay === targetDay) return;
    
    const curW = window.state.currentWeek;
    const originList = window.state.schedules[`${curW}-${draggedOriginDay}`] || [];
    const taskObj = originList.find(t => t.id === draggedTaskId);
    
    if(taskObj) {
        window.state.schedules[`${curW}-${draggedOriginDay}`] = originList.filter(t => t.id !== draggedTaskId);
        if(!window.state.schedules[`${curW}-${targetDay}`]) {
            window.state.schedules[`${curW}-${targetDay}`] = [];
        }
        window.state.schedules[`${curW}-${targetDay}`].push(taskObj);
        
        saveAllDataToStorage();
        renderWeekSchedule();
        checkOverload();
    }
    draggedTaskId = null;
    draggedOriginDay = null;
};

window.handleGatewayLogin = async function() {
    const email = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    if(!email || !password) return alert("계정 정보를 가득 채워주세요.");
    
    window.state.currentUser = email;
    loadAllDataFromStorage();
    updateAuthUI(true);
    syncViewRoute();
};

window.handleGatewayLogout = async function() {
    window.state = createDefaultState();
    updateAuthUI(false);
    showView('auth-view');
};

function showView(id) {
    document.getElementById('auth-view').classList.add('hidden');
    document.getElementById('planner-view').classList.add('hidden');
    document.getElementById(id).classList.remove('hidden');
}

function syncViewRoute() {
    showView('planner-view');
    initDashboardComponents();
}

function saveAllDataToStorage() {
    if (!window.state.currentUser) return;
    const safeKey = `smart_planner_v2_${window.state.currentUser.replace(/[^a-zA-Z0-9]/g, '_')}`;
    const packet = {
        currentUser: window.state.currentUser,
        availableHours: window.state.availableHours,
        schedules: window.state.schedules,
        subjects: window.state.subjects,
        totalWeeks: window.state.totalWeeks
    };
    localStorage.setItem(safeKey, JSON.stringify(packet));
}

function loadAllDataFromStorage() {
    if (!window.state.currentUser) return;
    const safeKey = `smart_planner_v2_${window.state.currentUser.replace(/[^a-zA-Z0-9]/g, '_')}`;
    const raw = localStorage.getItem(safeKey);
    if(raw) {
        try {
            const parsed = JSON.parse(raw);
            if (parsed.currentUser === window.state.currentUser) {
                window.state.availableHours = parsed.availableHours || window.state.availableHours;
                window.state.schedules = parsed.schedules || {};
                window.state.subjects = parsed.subjects || window.state.subjects;
                window.state.totalWeeks = parsed.totalWeeks || 5;
                window.state.currentWeek = parsed.totalWeeks || 5;
            }
        } catch(e) {
            console.error("복구 실패", e);
        }
    } else {
        window.state.schedules = {};
    }
}

function updateAuthUI(isLoggedIn) {
    const area = document.getElementById('auth-status-area');
    if(isLoggedIn && window.state.currentUser) {
        area.innerHTML = `
        <div class="flex items-center gap-2 text-xs">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-gray-300 font-mono font-medium">${window.state.currentUser.split('@')[0]}님 동기화 중</span>
        </div>
        <button onclick="handleGatewayLogout()" class="border border-gray-600 hover:bg-gray-800 text-gray-400 font-medium px-3 py-1.5 rounded-lg text-xs transition-all cursor-pointer">로그아웃</button>
        `;
    } else {
        area.innerHTML = "";
    }
}

function initDashboardComponents() {
    updateWeeksDropdown();
    initAvailableHoursUI();
    window.renderSubjectListUI();
}

window.parseBulkInput = function(text) {
    const lines = text.split('\n');
    const tasks = [];
    lines.forEach(line => {
        if (!line.trim()) return;
        const dashIndex = line.indexOf('-');
        if (dashIndex === -1) return;
        
        const subjectName = line.substring(0, dashIndex).trim();
        const tasksString = line.substring(dashIndex + 1).trim();
        
        const taskParts = tasksString.split(/,\s*(?![^()]*\))/);
        taskParts.forEach(part => {
            const trimmedPart = part.trim();
            if (!trimmedPart) return;
            
            const timeMatch = trimmedPart.match(/\(([^)]+)\)$/);
            if (timeMatch) {
                const taskName = trimmedPart.replace(/\(([^)]+)\)$/, "").trim();
                const hours = parseFloat(timeMatch[1]);
                if (!isNaN(hours)) {
                    tasks.push({ subject: subjectName, name: taskName, hours: hours });
                }
            } else {
                tasks.push({ subject: subjectName, name: trimmedPart, hours: 1.0 });
            }
        });
    });
    return tasks;
};

window.processBulkPlacement = function() {
    const rawText = document.getElementById('bulk-input-area').value;
    const parsed = window.parseBulkInput(rawText);
    if(parsed.length === 0) return;
    
    const curW = window.state.currentWeek;
    if(!window.state.schedules) window.state.schedules = {};
    
    parsed.forEach(task => {
        const subObj = window.state.subjects.find(s => s.name === task.subject) || { id: 'sub-purple', name: task.subject };
        let remaining = task.hours;
        let seq = 1;
        
        while(remaining > 0) {
            const slice = Math.min(remaining, 1.5);
            let bestDay = '월';
            let minRatio = Infinity;
            
            daysOfWeek.forEach(d => {
                const spent = (window.state.schedules[`${curW}-${d}`] || []).reduce((sum, t) => sum + t.hours, 0);
                const ratio = spent / (window.state.availableHours[d] || 1);
                if(ratio < minRatio) { 
                    minRatio = ratio; 
                    bestDay = d; 
                }
            });
            
            if(!window.state.schedules[`${curW}-${bestDay}`]) {
                window.state.schedules[`${curW}-${bestDay}`] = [];
            }
            
            window.state.schedules[`${curW}-${bestDay}`].push({
                id: 'task-split-' + Math.random().toString(36).substr(2, 9),
                subject: subObj.name,
                subjectId: subObj.id,
                name: task.hours > 1.5 ? `${task.name} (${seq}회차 분할)` : task.name,
                hours: slice,
                completed: false
            });
            remaining -= slice;
            seq++;
        }
    });
    
    document.getElementById('bulk-input-area').value = "";
    saveAllDataToStorage();
    renderWeekSchedule();
    checkOverload();
};

function checkOverload() {
    let limit = 0; 
    let plan = 0;
    const curW = window.state.currentWeek;
    daysOfWeek.forEach(d => {
        limit += window.state.availableHours[d];
        plan += (window.state.schedules[`${curW}-${d}`] || []).reduce((sum, t) => sum + t.hours, 0);
    });
    if(plan > limit) {
        alert(`⚠️ 가용 자습 시간 오버페이스 경고!\n이번 주 공부 계획량(${plan}시간)이 설정해 둔 가용 임계치(${limit}시간)를 초과하여 무리한 계획 상태입니다.`);
    }
}

window.updateWeeksDropdown = function() {
    const selectWeeks = document.getElementById('exam-weeks');
    const total = parseInt(selectWeeks.value);
    window.state.totalWeeks = total;
    
    const currentWeekSelect = document.getElementById('current-week-select');
    currentWeekSelect.innerHTML = "";
    for(let i = total; i >= 1; i--) {
        let note = i === 1 ? ' (최종 마무리 직보)' : i === total ? ' (기초 수립 및 수집)' : '';
        currentWeekSelect.innerHTML += `<option value="${i}">대비 D-${i}주차${note}</option>`;
    }
    window.state.currentWeek = total;
    saveAllDataToStorage();
    renderWeekSchedule();
};

function initAvailableHoursUI() {
    const container = document.getElementById('available-hours-inputs');
    if(!container) return;
    container.innerHTML = "";
    daysOfWeek.forEach(d => {
        const div = document.createElement('div');
        div.className = 'flex items-center justify-between bg-charcoal p-2 rounded-lg border border-gray-700';
        div.innerHTML = `
            <span class="font-bold text-gray-300">${d}요일</span>
            <input type="number" value="${window.state.availableHours[d]}" min="0" step="0.5" onchange="changeDayHour('${d}', this.value)" class="w-12 bg-dark-gray text-center text-white rounded border border-gray-600 focus:outline-none focus:border-emerald-500 p-0.5 text-xs">
        `;
        container.appendChild(div);
    });
}

window.changeDayHour = function(day, val) {
    window.state.availableHours[day] = parseFloat(val) || 0;
    saveAllDataToStorage();
    renderWeekSchedule();
};

window.renderSubjectListUI = function() {
    const container = document.getElementById('subject-list');
    if(!container) return;
    container.innerHTML = "";
    window.state.subjects.forEach((sub, idx) => {
        const div = document.createElement('div');
        div.className = `${sub.id} p-2 rounded-xl text-xs font-semibold shadow-sm flex justify-between items-center cursor-grab select-none`;
        div.setAttribute('draggable', 'true');
        div.addEventListener('dragstart', () => { draggedSubjectIndex = idx; });
        div.addEventListener('dragover', (e) => e.preventDefault());
        div.addEventListener('drop', (e) => {
            e.preventDefault();
            if(draggedSubjectIndex === null || draggedSubjectIndex === idx) return;
            const moved = window.state.subjects.splice(draggedSubjectIndex, 1)[0];
            window.state.subjects.splice(idx, 0, moved);
            draggedSubjectIndex = null;
            saveAllDataToStorage();
            window.renderSubjectListUI();
        });
        div.innerHTML = `<span>☰ ${sub.name}</span><button onclick="removeSubjectItem(${idx})" class="text-[10px] bg-black/20 hover:bg-black/40 px-1.5 py-0.5 rounded cursor-pointer">✕</button>`;
        container.appendChild(div);
    });
};

window.addNewSubject = function() {
    const name = document.getElementById('new-subject-name').value.trim();
    const color = document.getElementById('new-subject-color').value;
    if(!name) return;
    window.state.subjects.push({ id: color, name: name });
    document.getElementById('new-subject-name').value = '';
    saveAllDataToStorage();
    window.renderSubjectListUI();
};

window.removeSubjectItem = function(idx) {
    window.state.subjects.splice(idx, 1);
    saveAllDataToStorage();
    window.renderSubjectListUI();
};

function renderWeekSchedule() {
    const grid = document.getElementById('weekly-calendar-grid');
    if(!grid) return;
    grid.innerHTML = '';
    const curW = window.state.currentWeek;
    
    daysOfWeek.forEach(d => {
        const dayTasks = window.state.schedules[`${curW}-${d}`] || [];
        const totalSpent = dayTasks.reduce((sum, t) => sum + t.hours, 0); 
        const limit = window.state.availableHours[d];
        const isOver = totalSpent > limit;
        
        const card = document.createElement('div');
        card.className = `bg-charcoal rounded-xl border p-3 flex flex-col min-h-[450px] transition-all ${isOver ? 'border-red-500 ring-2 ring-red-500/20' : 'border-gray-800'}`;
        card.setAttribute('data-day', d);
        card.addEventListener('dragover', (e) => e.preventDefault());
        card.addEventListener('drop', window.dropTaskToDay);
        
        card.innerHTML = `
        <div class="flex justify-between items-center border-b border-gray-700 pb-2 mb-2">
            <div>
                <span class="font-bold text-sm text-white">${d}요일</span>
                <span class="text-[10px] block ${isOver ? 'text-red-400 font-bold' : 'text-gray-400'}">${totalSpent}h / ${limit}h</span>
            </div>
            <button onclick="openAddTaskModal('${d}')" class="text-xs bg-dark-gray p-1 rounded border border-gray-700 cursor-pointer text-gray-400 hover:text-white transition-all">+</button>
        </div>
        <div class="flex-1 flex flex-col gap-2 overflow-y-auto" id="box-${d}"></div>
        `;
        grid.appendChild(card);
        
        const box = document.getElementById(`box-${d}`);
        dayTasks.forEach(t => {
            const item = document.createElement('div');
            item.className = `${t.subjectId || 'sub-purple'} p-2.5 rounded-lg text-xs flex flex-col gap-1 relative cursor-grab active:cursor-grabbing select-none group shadow-md`;
            item.setAttribute('draggable', 'true');
            item.setAttribute('data-task-id', t.id);
            item.setAttribute('data-origin-day', d);
            item.addEventListener('dragstart', window.dragStartTask);
            
            item.innerHTML = `
            <div class="flex justify-between font-bold">
                <span class="truncate pr-2">${t.subject}</span>
                <button onclick="deleteItem('${d}','${t.id}')" class="cursor-pointer font-bold opacity-0 group-hover:opacity-100 transition-all text-[10px] bg-black/20 hover:bg-black/50 px-1 rounded">X</button>
            </div>
            <p class="text-[11px] opacity-90 leading-snug line-clamp-2">${t.name}</p>
            <div class="flex justify-between items-center mt-1 pt-1 border-t border-white/20 text-[10px]">
                <span class="bg-black/20 px-1 rounded font-mono font-bold">${t.hours}h</span>
                <input type="checkbox" ${t.completed ? 'checked' : ''} onchange="toggleTask('${d}','${t.id}',this.checked)" class="cursor-pointer w-3.5 h-3.5 rounded border-none bg-white/20 text-dark-gray focus:ring-0">
            </div>
            `;
            box.appendChild(item);
        });
    });
}

window.openAddTaskModal = function(day) {
    window.targetDayForModal = day;
    const sel = document.getElementById('task-subject-select');
    if(!sel) return;
    sel.innerHTML = "";
    window.state.subjects.forEach(s => {
        sel.innerHTML += `<option value="${s.id}">${s.name}</option>`;
    });
    document.getElementById('task-name-input').value = "";
    document.getElementById('task-hours-input').value = '1';
    document.getElementById('task-review-checkbox').checked = false;
    document.getElementById('task-modal').classList.remove('hidden');
};

window.addCustomTaskToDay = function() {
    const sel = document.getElementById('task-subject-select');
    const name = document.getElementById('task-name-input').value.trim();
    const hours = parseFloat(document.getElementById('task-hours-input').value) || 1;
    const reviewTrigger = document.getElementById('task-review-checkbox').checked;
    const curW = window.state.currentWeek;
    
    if(!name) return alert("상세 내용을 기록해 주세요.");
    
    if(!window.state.schedules[`${curW}-${window.targetDayForModal}`]) {
        window.state.schedules[`${curW}-${window.targetDayForModal}`] = [];
    }
    
    window.state.schedules[`${curW}-${window.targetDayForModal}`].push({
        id: 'task-custom-' + Math.random().toString(36).substr(2, 9),
        subject: sel.options[sel.selectedIndex].text,
        subjectId: sel.value,
        name: name,
        hours: hours,
        completed: false
    });
    
    if (reviewTrigger) {
        const nextWeek = curW - 1;
        if (nextWeek >= 1) {
            if(!window.state.schedules[`${nextWeek}-${window.targetDayForModal}`]) {
                window.state.schedules[`${nextWeek}-${window.targetDayForModal}`] = [];
            }
            window.state.schedules[`${nextWeek}-${window.targetDayForModal}`].push({
                id: 'task-review-' + Math.random().toString(36).substr(2, 9),
                subject: sel.options[sel.selectedIndex].text,
                subjectId: 'sub-indigo',
                name: `[누적 복습] ${name}`,
                hours: Math.max(0.5, hours * 0.5),
                completed: false
            });
        }
    }
    
    document.getElementById('task-modal').classList.add('hidden');
    saveAllDataToStorage();
    renderWeekSchedule();
    checkOverload();
};

window.deleteItem = function(day, id) {
    const curW = window.state.currentWeek;
    window.state.schedules[`${curW}-${day}`] = (window.state.schedules[`${curW}-${day}`] || []).filter(t => t.id !== id);
    saveAllDataToStorage();
    renderWeekSchedule();
};

window.toggleTask = function(day, id, chk) {
    const curW = window.state.currentWeek;
    const task = (window.state.schedules[`${curW}-${day}`] || []).find(t => t.id === id);
    if(task) { 
        task.completed = chk; 
        saveAllDataToStorage(); 
    }
};

window.changeWeekView = function() {
    window.state.currentWeek = parseInt(document.getElementById('current-week-select').value);
    renderWeekSchedule();
};

// PDF 저장 기능 추가 함수
window.exportToPDF = function() {
    const element = document.getElementById('pdf-canvas');
    const currentWeekText = document.getElementById('current-week-select').options[document.getElementById('current-week-select').selectedIndex].text;
    
    // PDF 변환 옵션 설정
    const opt = {
        margin:       10,
        filename:     `[${currentWeekText.trim()}]_시험_플래너.pdf`,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: true, backgroundColor: '#1F222E' },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'landscape' }
    };
    
    // PDF 저장 실행
    html2pdf().set(opt).from(element).save();
};

showView('auth-view');
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(code)
print("File generated successfully.")