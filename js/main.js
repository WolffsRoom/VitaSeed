
// Modal Utility
function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.show').forEach(m => m.classList.remove('show'));
    }
});

document.addEventListener("DOMContentLoaded", async () => {
    // ---- DOM Elements ----
    const grid = document.getElementById('project-grid');
    const loader = document.getElementById('loader');
    const searchInput = document.getElementById('search-input');
    const catFilter = document.getElementById('category-filter');
    const devFilter = document.getElementById('dev-filter');

    // ---- Initialization ----
    const projectsData = await window.fetchCatalog();
    if (grid && projectsData) {
        renderProjects(projectsData);
    }

    // ---- Functions ----
    function renderProjects(projects) {
        if (!grid) return;
        
        const heroSection = document.getElementById('hero-section');
        const top10Section = document.getElementById('top10-section');
        const top10Container = document.getElementById('top10-container');
        
        grid.innerHTML = '';
        if (heroSection) heroSection.innerHTML = '';
        if (top10Container) top10Container.innerHTML = '';
        
        const isFiltered = (searchInput && searchInput.value) || (catFilter && catFilter.value !== 'all') || (devFilter && devFilter.value !== 'all');
        let gridProjects = projects;
        
        // Apenas renderiza faixas Apple-style se estiver na home e sem filtros ativos
        if (heroSection && !isFiltered && projects.length > 0) {
            const heroProj = projects[0];
            const heroBanner = heroProj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=1200';
            
            heroSection.innerHTML = `
                <a href="project.html?id=${heroProj.id}" class="hero-card" style="background-image: url('${heroBanner}'); background-position: ${heroProj.bgPosition || 'center bottom'};">
                    <div class="hero-overlay">
                        <span class="tag" style="background:var(--accent-green); color:#000; width:max-content; margin-bottom:0.5rem;">Lançamento em Destaque</span>
                        <h2 class="hero-title">${window.formatTitle(heroProj.title)}</h2>
                        <div class="hero-meta">${heroProj.category} • Por ${heroProj.responsibles}</div>
                    </div>
                </a>
            `;
            
            if (projects.length > 1) {
                top10Section.style.display = 'block';
                const top10 = projects.slice(1, Math.min(11, projects.length));
                top10.forEach((proj, i) => {
                    const banner = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';
                    top10Container.innerHTML += `
                        <a href="project.html?id=${proj.id}" class="top10-card" style="background-image: url('${banner}'); background-position: ${proj.bgPosition || 'center'};">
                            <div class="top10-number">${i + 1}</div>
                            <div class="top10-overlay">
                                <div class="top10-title">${window.formatTitle(proj.title)}</div>
                                <div class="top10-cat" style="font-weight: bold;">${proj.category}</div>
                                <div class="top10-resp"><i class="ph ph-user"></i> ${proj.responsibles}</div>
                            </div>
                        </a>
                    `;
                });
                
                
                // Clona para criar um loop infinito visual
                const cards = Array.from(top10Container.children);
                cards.forEach(card => {
                    let clone = card.cloneNode(true);
                    top10Container.appendChild(clone);
                });
                
                // Agora top10Container tem 20 itens (1-10, 1-10)
                
                // Scroll Logic

                const scrollLeftBtn = document.querySelector('.scroll-left');
                const scrollRightBtn = document.querySelector('.scroll-right');
                if(scrollLeftBtn && scrollRightBtn) {
                    scrollRightBtn.addEventListener('click', () => {
                        const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                        if (top10Container.scrollLeft >= maxScrollLeft - 50) {
                            // Volta silenciosamente para o começo do segundo bloco (item 11) ou do primeiro bloco (item 1)
                            top10Container.scrollTo({ left: 0, behavior: 'auto' }); // Pula invisivelmente
                            setTimeout(() => { top10Container.scrollBy({ left: 300, behavior: 'smooth' }); }, 50);
                        } else {
                            top10Container.scrollBy({ left: 300, behavior: 'smooth' });
                        }
                    });

                    scrollLeftBtn.addEventListener('click', () => {
                        if (top10Container.scrollLeft <= 10) {
                            const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                            top10Container.scrollTo({ left: maxScrollLeft / 2, behavior: 'auto' }); // Pula invisivelmente para o meio
                            setTimeout(() => { top10Container.scrollBy({ left: -300, behavior: 'smooth' }); }, 50);
                        } else {
                            top10Container.scrollBy({ left: -300, behavior: 'smooth' });
                        }
                    });
                    
                    let scrollTimeout;
                    top10Container.addEventListener('scroll', () => {
                        // Sempre que estiver rolando (e não estiver no início absoluto), mostra o fade
                        if (top10Container.scrollLeft > 10) {
                            top10Container.classList.add('scrolled');
                        } else {
                            top10Container.classList.remove('scrolled');
                        }
                        
                        // Quando parar de rolar, remove o fade da esquerda
                        clearTimeout(scrollTimeout);
                        scrollTimeout = setTimeout(() => {
                            top10Container.classList.remove('scrolled');
                        }, 250);
                    });
                }
            }
            
            // O catálogo completo exibe do 2º em diante (ou todos) para não parecer vazio
            gridProjects = projects.slice(1);
        } else {
            if (heroSection) heroSection.innerHTML = '';
            if (top10Section) top10Section.style.display = 'none';
        }

        gridProjects.forEach((proj, index) => {
            const card = document.createElement('a');
            card.href = `project.html?id=${proj.id}`; // Dedicated page
            card.className = 'card';
            card.style.animationDelay = `${index * 0.05}s`;
            
            // Generate tags
            let tagClass = proj.category.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            let badgesHtml = `<span class="tag ${tagClass}">${proj.category}</span>`;
            
            

            const bannerUrl = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';

            card.innerHTML = `
                <div class="card-banner" style="background-image: url('${bannerUrl}'); background-position: ${proj.bgPosition || 'center'};"></div>
                <div class="card-content">
                    <div class="card-tags">
                        ${badgesHtml}
                    </div>
                    <h3 class="card-title">${window.formatTitle(proj.title)}</h3>
                    <div class="card-meta" style="display: flex; flex-wrap: wrap; gap: 0.8rem; align-items: center; color: var(--text-muted); font-size: 0.75rem; margin-top: auto; padding-top: 0.5rem;">
                            <span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-user"></i> ${proj.responsibles}</span>
                            ${proj.version ? `<span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-tag"></i> v${proj.version}</span>` : ''}
                            ${proj.update_date ? `<span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-calendar-blank"></i> ${proj.update_date}</span>` : ''}
                        </div>
                </div>
            `;
            grid.appendChild(card);
        });
        
        // Inicializa animação 3D estilo Apple TV em todos os cards e hero
        if (typeof VanillaTilt !== 'undefined') {
            VanillaTilt.init(document.querySelectorAll('.card, .top10-card'), {
                max: 10,
                speed: 400,
                glare: true,
                "max-glare": 0.15,
                scale: 1.02
            });
        }
    }

    // ---- Event Listeners ----
    const filterData = () => {
        if (!grid) return;
        const search = searchInput ? searchInput.value.toLowerCase() : '';
        const cat = catFilter ? catFilter.value : 'all';
        const dev = devFilter ? devFilter.value : 'all';
        
        const filtered = window.projectsData.filter(p => {
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

// Modal Request Logic
const API_URL = "https://vitaseed-api.seunome.workers.dev"; // A SER SUBSTITUIDO

async function sendRequest() {
    const title = document.getElementById('req-title').value.trim();
    const link = document.getElementById('req-link').value.trim();
    const desc = document.getElementById('req-desc').value.trim();
    const msgBox = document.getElementById('req-msg');
    
    if(!title) {
        msgBox.style.color = '#ff4d4d';
        msgBox.innerText = 'Por favor, informe o nome do projeto.';
        return;
    }
    
    // Desabilitar o botão temporariamente
    const btn = document.querySelector('#modal-request .btn-primary');
    const oldHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Enviando...';
    btn.style.pointerEvents = 'none';
    
    try {
        if (API_URL.includes("seunome")) {
            // Se ainda não configurou a API, simula sucesso para visualização
            await new Promise(r => setTimeout(r, 1000));
            msgBox.style.color = 'var(--accent-green)';
            msgBox.innerText = 'Simulação: Request enviado com sucesso!';
        } else {
            // Envia para a API real no Cloudflare
            const res = await fetch(`${API_URL}/api/request`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, link, desc })
            });
            
            const data = await res.json();
            
            if (!res.ok) {
                throw new Error(data.error || "Erro ao enviar request.");
            }
            
            msgBox.style.color = 'var(--accent-green)';
            msgBox.innerText = 'Request enviado com sucesso!';
        }
        
        // Limpar campos
        document.getElementById('req-title').value = '';
        document.getElementById('req-link').value = '';
        document.getElementById('req-desc').value = '';
        
        setTimeout(() => {
            closeModal('modal-request');
            msgBox.innerText = '';
        }, 2000);
        
    } catch (e) {
        msgBox.style.color = '#ff4d4d';
        msgBox.innerText = e.message;
    } finally {
        btn.innerHTML = oldHtml;
        btn.style.pointerEvents = 'auto';
    }
}
