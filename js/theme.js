function updateThemeIcon(themeName) {
    const themeBtnText = document.getElementById('theme-btn-text');
    if (themeBtnText) {
        const iconClass = themeName === 'light' ? 'ph-sun' : (themeName === 'sony' ? 'ph-game-controller' : 'ph-moon');
        themeBtnText.innerHTML = `<i class="ph ${iconClass}"></i>`;
    }
}

// Check and apply theme immediately before render
(function() {
    const savedTheme = localStorage.getItem('vita-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();

window.toggleTheme = function() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    let next = 'light';
    if (current === 'light') next = 'sony';
    else if (current === 'sony') next = 'dark';
    else next = 'light';
    
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('vita-theme', next);
    updateThemeIcon(next);
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
    let pageName = 'home';
    
    if (window.location.pathname.includes('project.html')) {
        pageName = 'project';
    } else if (window.location.pathname.includes('contribution.html')) {
        pageName = 'collaborations';
    } else if (window.location.pathname.includes('category.html')) {
        const cat = params.get('cat');
        const engine = params.get('engine');
        if (engine) pageName = engine.toLowerCase();
        else if (cat) pageName = cat.toLowerCase();
        else pageName = 'all';
    }
    
    const commandText = isHomePage ? "" : `ls --${pageName.replace(/\s+/g, '')}`;
    const typedEl = document.getElementById('cmd-typed');
    let charIdx = 0;

    // Hide loader initial state unless navigating
    if (termLoader) termLoader.classList.add('fade-out');

    // Re-trigger typing animation when clicking internal links (Instant navigation for project details)
    let isNavigating = false;
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.href && link.href.startsWith(window.location.origin) && !link.target && !link.href.includes('#')) {
            const urlObj = new URL(link.href);
            
            // If navigating to project.html, navigate instantly without artificial delay
            if (urlObj.pathname.includes('project.html')) {
                return; // Standard link navigation
            }

            if (isNavigating) return;
            isNavigating = true;

            let linkCat = 'home';
            if (urlObj.pathname.includes('contribution.html')) {
                linkCat = 'collaborations';
            } else if (urlObj.pathname.includes('category.html')) {
                const cat = urlObj.searchParams.get('cat');
                const engine = urlObj.searchParams.get('engine');
                if (engine) linkCat = engine.toLowerCase();
                else if (cat) linkCat = cat.toLowerCase();
                else linkCat = 'all';
            }
            
            const navCmdText = `ls --${linkCat.replace(/\s+/g, '')}`;
            
            e.preventDefault();
            termLoader.classList.remove('fade-out');
            if (typedEl) typedEl.textContent = navCmdText;
            const targetUrl = link.href;
            
            setTimeout(() => {
                window.location.href = targetUrl;
            }, 120);
        }
    });

    // 1. Check local storage for theme
    const savedTheme = localStorage.getItem('vita-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

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
    const pagePath = window.location.pathname;
    const pageParams = new URLSearchParams(window.location.search);
    const cat = pageParams.get('cat')?.toLowerCase();
    
    document.querySelectorAll('.nav-links a, .sidebar-footer a').forEach(link => {
        const dataPage = link.getAttribute('data-page');
        if (!dataPage) return;
        
        if (cat && dataPage === cat) {
            link.classList.add('active');
        } else if (!cat && pagePath.includes(dataPage)) {
            link.classList.add('active');
        } else if (!cat && (pagePath.endsWith('/') || pagePath.endsWith('index.html')) && dataPage === 'index') {
            link.classList.add('active');
        }
    });
});
