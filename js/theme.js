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
        themeBtnText.innerHTML = next === 'light' ? '<i class="ph ph-sun"></i>' : (next === 'sony' ? '<i class="ph ph-game-controller"></i>' : '<i class="ph ph-moon"></i>');
    }
};

document.addEventListener('DOMContentLoaded', async () => {
    const isHomePage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/VitARCH/') || window.location.pathname.endsWith('/vitarch/');
    
    // Terminal Typing Loader Effect (Only for inner pages or navigation)
    let termLoader = document.getElementById('terminal-loader');
    if (!termLoader) {
        termLoader = document.createElement('div');
        termLoader.id = 'terminal-loader';
        termLoader.innerHTML = `
            <div class="cmd-box">
                <span class="cmd-prompt">~/vitarch $</span>
                <span id="cmd-typed"></span><span class="cmd-cursor"></span>
            </div>
        `;
        const topbar = document.querySelector('.topbar');
        if (topbar && topbar.parentNode) {
            topbar.parentNode.insertBefore(termLoader, topbar.nextSibling);
        } else {
            document.body.appendChild(termLoader);
        }
    }

    // Determine initial command text
    const params = new URLSearchParams(window.location.search);
    let catParam = params.get('cat') || 'catalogo';
    if (window.location.pathname.includes('project.html')) catParam = 'project';
    if (window.location.pathname.includes('contribution.html')) catParam = 'colaboracoes';
    
    const commandText = isHomePage ? "" : `ls --${catParam.toLowerCase().replace(/\s+/g, '')}`;
    const typedEl = document.getElementById('cmd-typed');
    let charIdx = 0;

    // Hide loader initial state unless navigating
    if (termLoader) termLoader.classList.add('fade-out');

    // Re-trigger typing animation when clicking internal links
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.href && link.href.startsWith(window.location.origin) && !link.target && !link.href.includes('#')) {
            const urlObj = new URL(link.href);
            let linkCat = urlObj.searchParams.get('cat') || 'all';
            if (urlObj.pathname.includes('project.html')) linkCat = 'details';
            if (urlObj.pathname.includes('contribution.html')) linkCat = 'colaboracoes';
            if (urlObj.pathname.endsWith('index.html') || urlObj.pathname === '/') linkCat = 'home';
            
            const navCmdText = `ls --${linkCat.toLowerCase().replace(/\s+/g, '')}`;
            
            e.preventDefault();
            termLoader.classList.remove('fade-out');
            if (typedEl) typedEl.textContent = '';
            charIdx = 0;
            const targetUrl = link.href;
            
            function typeOutNav() {
                if (charIdx < navCmdText.length) {
                    if (typedEl) typedEl.textContent += navCmdText.charAt(charIdx);
                    charIdx++;
                    setTimeout(typeOutNav, 25);
                } else {
                    setTimeout(() => {
                        window.location.href = targetUrl;
                    }, 120);
                }
            }
            typeOutNav();
        }
    });

    // 1. Check local storage for theme
    const savedTheme = localStorage.getItem('vita-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeBtnText = document.getElementById('theme-btn-text');
    if (themeBtnText) {
        themeBtnText.innerHTML = savedTheme === 'light' ? '<i class="ph ph-sun"></i>' : (savedTheme === 'sony' ? '<i class="ph ph-game-controller"></i>' : '<i class="ph ph-moon"></i>');
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
