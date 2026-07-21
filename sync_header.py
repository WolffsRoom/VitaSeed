import glob, re

# New standardized header HTML
new_header = '''<header style="display: flex; gap: 1rem; align-items: center; justify-content: space-between; flex-wrap: wrap; margin-bottom: 2rem;">
            <div style="display: flex; gap: 1rem; flex: 1; min-width: 200px;">
                <input type="text" id="search-input" class="search-bar" placeholder="Buscar por título ou responsável..." style="flex: 1;" oninput="if(window.location.pathname.indexOf('index')===-1&&this.value.length>0){window.location.href='index.html?q='+encodeURIComponent(this.value);}">
            </div>
            <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                <select id="category-filter" class="filter-select" onchange="if(this.value!=='all'){window.location.href='category.html?cat='+this.value;}">
                    <option value="all">Todas as Categorias</option>
                    <option value="Ports">Ports</option>
                    <option value="Original games">Original games</option>
                    <option value="Mods">Mods</option>
                    <option value="Translations">Translations</option>
                    <option value="Apps">Apps</option>
                    <option value="Tools">Tools</option>
                    <option value="Plugin">Plugins</option>
                </select>
                <button id="btn-about" class="btn-icon" style="background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border-color); padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='var(--hover-bg)'" onmouseout="this.style.background='var(--bg-card)'" title="Sobre o VitaSeed" onclick="document.getElementById('modal-about').classList.add('show')"><i class="fa-solid fa-question"></i></button>
                <button id="btn-request" class="btn-primary" onclick="document.getElementById('modal-request').classList.add('show')"><i class="ph ph-paper-plane-tilt"></i> Request</button>
            </div>
        </header>'''

# Modals HTML
modals_html = '''    <!-- Modals -->
    <div id="modal-about" class="modal" onclick="if(event.target===this)closeModal('modal-about')">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('modal-about')">&times;</span>
            <h2>Sobre o VitaSeed <span style="color:var(--accent-green)">?</span></h2>
            <p style="margin-top: 1rem; line-height: 1.7; color: var(--text-muted);">
                O VitaSeed é um centralizador para a cena brasileira homebrew do PSVita. Aqui centralizamos Ports, Mods, Traduções, Plugins, Apps e Ferramentas, garantindo um acesso centralizado.
            </p>
        </div>
    </div>

    <div id="modal-request" class="modal" onclick="if(event.target===this)closeModal('modal-request')">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('modal-request')">&times;</span>
            <h2>Solicitar Projeto</h2>
            <p style="margin-top: 0.75rem; margin-bottom: 1.25rem; font-size: 0.9rem; color: var(--text-muted); line-height: 1.5;">
                Não encontrou o que procurava?<br>Envie um request para adicionarmos o projeto ao catálogo!
            </p>
            <div style="display: flex; flex-direction: column; gap: 0.85rem; text-align: left;">
                <input type="text" id="req-title" class="search-bar" placeholder="Nome do Projeto / Jogo" style="width: 100%; box-sizing: border-box;">
                <input type="text" id="req-link" class="search-bar" placeholder="Link de Referência (GitHub, VitaDB, etc)" style="width: 100%; box-sizing: border-box;">
                <textarea id="req-desc" class="search-bar" rows="3" placeholder="Por que devemos adicionar?" style="resize: vertical; font-family: inherit; width: 100%; box-sizing: border-box;"></textarea>
                <button class="btn-primary" onclick="sendRequest()" style="width: 100%; justify-content: center; margin-top: 0.25rem;">
                    <i class="ph ph-paper-plane-tilt"></i> Enviar Pedido
                </button>
                <div id="req-msg" style="text-align: center; font-size: 0.9rem; font-weight: bold;"></div>
            </div>
        </div>
    </div>'''

# Modal JS for pages that don't load main.js
modal_js = '''    <script>
        if (typeof closeModal === 'undefined') {
            function closeModal(id) { document.getElementById(id).classList.remove('show'); }
            function sendRequest() {
                const title = document.getElementById('req-title').value.trim();
                const msgBox = document.getElementById('req-msg');
                if (!title) { msgBox.style.color = '#ff4d4d'; msgBox.innerText = 'Informe o nome do projeto.'; return; }
                const today = new Date().toISOString().split('T')[0];
                const key = 'vitaseed_requests_' + today;
                let n = parseInt(localStorage.getItem(key) || '0');
                if (n >= 2) { msgBox.style.color = '#ff4d4d'; msgBox.innerText = 'Limite de 2 envios por dia atingido.'; return; }
                localStorage.setItem(key, (n + 1).toString());
                msgBox.style.color = 'var(--accent-green)';
                msgBox.innerText = 'Request enviado com sucesso!';
                document.getElementById('req-title').value = '';
                document.getElementById('req-link').value = '';
                document.getElementById('req-desc').value = '';
                setTimeout(() => { closeModal('modal-request'); msgBox.innerText = ''; }, 2000);
            }
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') document.querySelectorAll('.modal.show').forEach(m => m.classList.remove('show'));
            });
        }
    </script>'''

# Target pages that are MISSING the header
target_pages = ['project.html', 'category.html', 'settings.html']

for file in target_pages:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Inject header after <div class="content-wrapper"> if not present
        if 'btn-about' not in html:
            html = html.replace(
                '<div class="content-wrapper">',
                '<div class="content-wrapper">\n        ' + new_header
            )

        # 2. Inject modals before </body> if not present
        if 'modal-about' not in html:
            html = html.replace('</body>', modals_html + '\n</body>')

        # 3. Inject modal JS before </body> 
        if 'typeof closeModal' not in html:
            html = html.replace('</body>', modal_js + '\n</body>')

        # 4. Fix icon in any already-existing headers
        html = html.replace(
            '<i class="ph ph-question" style="font-size: 1.2rem;"></i>',
            '<i class="fa-solid fa-question"></i>'
        )

        with open(file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated: {file}")
    except FileNotFoundError:
        print(f"Skipped (not found): {file}")

# Also fix icon in index.html and contribution.html
for file in ['index.html', 'contribution.html']:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace(
        '<i class="ph ph-question" style="font-size: 1.2rem;"></i>',
        '<i class="fa-solid fa-question"></i>'
    )
    # Bump cache versions
    html = html.replace('css/style.css?v=31', 'css/style.css?v=32')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

import glob as g
for file in g.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=15', 'js/main.js?v=16')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
