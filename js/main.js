document.addEventListener("DOMContentLoaded", () => {
    // ---- DOM Elements ----
    const grid = document.getElementById('project-grid');
    const loader = document.getElementById('loader');
    const searchInput = document.getElementById('search-input');
    const catFilter = document.getElementById('category-filter');
    const devFilter = document.getElementById('dev-filter');

    // ---- Initialization ----
    if (grid && typeof projectsData !== 'undefined') {
        renderProjects(projectsData);
    }

    // ---- Functions ----
    function renderProjects(projects) {
        if (!grid) return;
        grid.innerHTML = '';
        projects.forEach(proj => {
            const card = document.createElement('a');
            card.href = `project.html?id=${proj.id}`; // Dedicated page
            card.className = 'card';
            
            // Generate tags
            let tagClass = proj.category.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            let badgesHtml = `<span class="tag ${tagClass}">${proj.category}</span>`;
            
            if (proj.ai_used && !proj.vibecoded) {
                badgesHtml += `<span class="ai-indicator">AI Assisted</span>`;
            } else if (proj.vibecoded) {
                badgesHtml += `<span class="ai-indicator vibecoded-badge">100% Vibecoded</span>`;
            }

            const bannerUrl = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';

            card.innerHTML = `
                <div class="card-banner" style="background-image: url('${bannerUrl}');"></div>
                <div class="card-content">
                    <div class="card-tags">
                        ${badgesHtml}
                    </div>
                    <h3 class="card-title">${proj.title}</h3>
                    <div class="card-meta">
                        <span>v1.0</span>
                        <span>${proj.responsibles}</span>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // ---- Event Listeners ----
    const filterData = () => {
        if (!grid) return;
        const search = searchInput ? searchInput.value.toLowerCase() : '';
        const cat = catFilter ? catFilter.value : 'all';
        const dev = devFilter ? devFilter.value : 'all';
        
        const filtered = projectsData.filter(p => {
            const matchesSearch = p.title.toLowerCase().includes(search) || p.responsibles.toLowerCase().includes(search);
            const matchesCat = cat === 'all' || p.category === cat;
            const matchesDev = dev === 'all' || p.responsibles === dev;
            return matchesSearch && matchesCat && matchesDev;
        });
        renderProjects(filtered);
    };

    if (searchInput) searchInput.addEventListener('input', filterData);
    if (catFilter) catFilter.addEventListener('change', filterData);
    if (devFilter) devFilter.addEventListener('change', filterData);
});
