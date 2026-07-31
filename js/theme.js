// theme.js
window.toggleTheme = function() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    let next = 'light';
    if (current === 'light') next = 'sony';
    else if (current === 'sony') next = 'dark';
    else next = 'light';
    
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('vita-theme', next);
    
    const themeBtnText = document.getElementById('theme-btn-text');
    if (themeBtnText) {
        themeBtnText.innerText = next === 'light' ? 'modo claro' : (next === 'sony' ? 'modo sony' : 'modo escuro');
    }
};

document.addEventListener('DOMContentLoaded', async () => {
    // 0. Loader hide logic
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => loader.classList.add('hidden'), 800);
    }

    // 1. Check local storage for theme
    const savedTheme = localStorage.getItem('vita-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeBtnText = document.getElementById('theme-btn-text');
    if (themeBtnText) {
        themeBtnText.innerText = savedTheme === 'light' ? 'modo claro' : (savedTheme === 'sony' ? 'modo sony' : 'modo escuro');
    }

    // 2. Mobile Sidebar Toggle logic
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // 3. Extract Dev Filter Logic if it exists
    const devFilter = document.getElementById('dev-filter');
    if (devFilter) {
        let pData = window.projectsData;
        if (!pData && window.fetchCatalog) {
            pData = await window.fetchCatalog();
        }
        if (pData) {
            const devs = new Set();
            pData.forEach(p => devs.add(p.responsibles));
            devs.forEach(dev => {
                const opt = document.createElement('option');
                opt.value = dev;
                opt.innerText = dev;
                devFilter.appendChild(opt);
            });
        }
    }
});

    const path = window.location.pathname;
    const params = new URLSearchParams(window.location.search);
    const cat = params.get('cat')?.toLowerCase();
    
    document.querySelectorAll('.nav-links a, .sidebar-footer a').forEach(link => {
        const dataPage = link.getAttribute('data-page');
        if (!dataPage) return;
        
        if (cat && dataPage === cat) {
            link.classList.add('active');
        } else if (!cat && path.includes(dataPage)) {
            link.classList.add('active');
        } else if (!cat && (path.endsWith('/') || path.endsWith('index.html')) && dataPage === 'index') {
            link.classList.add('active');
        }
    });
