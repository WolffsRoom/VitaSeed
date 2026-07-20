// theme.js
document.addEventListener('DOMContentLoaded', () => {
    // 0. Loader hide logic
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => loader.classList.add('hidden'), 800);
    }

    // 1. Check local storage for theme
    const savedTheme = localStorage.getItem('vita-theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
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
    if (devFilter && typeof projectsData !== 'undefined') {
        const devs = new Set();
        projectsData.forEach(p => devs.add(p.responsibles));
        devs.forEach(dev => {
            const opt = document.createElement('option');
            opt.value = dev;
            opt.innerText = dev;
            devFilter.appendChild(opt);
        });
    }
});
