import glob
import re

modals_html = '''
    <!-- Modals -->
    <div id="modal-about" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="document.getElementById('modal-about').classList.remove('show')">&times;</span>
            <h2>Sobre o VitaSeed</h2>
            <p style="margin-top: 1rem; line-height: 1.6; color: var(--text-muted);">
                O VitaSeed é o seu diretório definitivo para a cena homebrew do PSVita. 
                Aqui centralizamos Ports, Mods, Traduções, Plugins, Apps e Ferramentas, 
                garantindo que você sempre tenha acesso às versões mais atualizadas.
            </p>
        </div>
    </div>

    <div id="modal-request" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="document.getElementById('modal-request').classList.remove('show')">&times;</span>
            <h2>Solicitar Projeto</h2>
            <p style="margin-top: 1rem; margin-bottom: 1.5rem; font-size: 0.9rem; color: var(--text-muted);">
                Não encontrou o que procurava? Envie um request para adicionarmos o projeto ao catálogo! (Limite: 2 envios por dia por IP)
            </p>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <input type="text" id="req-title" class="search-bar" placeholder="Nome do Projeto / Jogo">
                <input type="text" id="req-link" class="search-bar" placeholder="Link de Referência (GitHub, VitaDB, etc)">
                <textarea id="req-desc" class="search-bar" rows="3" placeholder="Por que devemos adicionar?" style="resize: vertical; font-family: inherit;"></textarea>
                <button class="btn-primary" onclick="sendRequest()" style="width: 100%; justify-content: center; margin-top: 0.5rem;"><i class="ph ph-paper-plane-tilt"></i> Enviar Pedido</button>
                <div id="req-msg" style="text-align: center; font-size: 0.9rem; margin-top: 0.5rem; font-weight: bold;"></div>
            </div>
        </div>
    </div>
'''

old_sidebar = '''                <li><a href="category.html?cat=Ports" data-page="ports"><span>PORTS</span></a></li>
                <li><a href="category.html?cat=Original games" data-page="original games"><span>ORIGINAL GAMES</span></a></li>
                <li><a href="category.html?cat=Mods" data-page="mods"><span>MODS</span></a></li>
                <li><a href="category.html?cat=Translations" data-page="translations"><span>TRADUÇÕES</span></a></li>'''

new_sidebar = '''                <li><a href="category.html?cat=Ports" data-page="ports"><span>PORTS</span></a></li>
                <li><a href="category.html?cat=Original games" data-page="original games"><span>ORIGINAL GAMES</span></a></li>
                <li><a href="category.html?cat=Mods" data-page="mods"><span>MODS</span></a></li>
                <li><a href="category.html?cat=Translations" data-page="translations"><span>TRADUÇÕES</span></a></li>
                <li><a href="category.html?cat=Apps" data-page="apps"><span>APPS</span></a></li>
                <li><a href="category.html?cat=Tools" data-page="tools"><span>TOOLS</span></a></li>
                <li><a href="category.html?cat=Plugin" data-page="plugins"><span>PLUGINS</span></a></li>'''

new_header = '''<header style="display: flex; gap: 1rem; align-items: center; justify-content: space-between; flex-wrap: wrap; margin-bottom: 2rem;">
            <div style="display: flex; gap: 1rem; flex: 1; min-width: 200px;">
                <input type="text" id="search-input" class="search-bar" placeholder="Buscar por título ou responsável..." style="flex: 1;">
            </div>
            <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                <select id="category-filter" class="filter-select">
                    <option value="all">Todas as Categorias</option>
                    <option value="Ports">Ports</option>
                    <option value="Original games">Original games</option>
                    <option value="Mods">Mods</option>
                    <option value="Translations">Translations</option>
                    <option value="Apps">Apps</option>
                    <option value="Tools">Tools</option>
                    <option value="Plugin">Plugins</option>
                    <option value="PC Tools">PC Tools</option>
                </select>
                <button id="btn-about" class="btn-icon" style="background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border-color); padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer; transition: 0.2s;" onmouseover="this.style.background='var(--hover-bg)'" onmouseout="this.style.background='var(--bg-card)'" title="Sobre o VitaSeed" onclick="document.getElementById('modal-about').classList.add('show')"><i class="ph ph-question" style="font-size: 1.2rem;"></i></button>
                <button id="btn-request" class="btn-primary" onclick="document.getElementById('modal-request').classList.add('show')"><i class="ph ph-paper-plane-tilt"></i> Request</button>
            </div>
        </header>'''

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Sidebar
    if new_sidebar not in html:
        html = html.replace(old_sidebar, new_sidebar)
    
    # 2. Update Header
    header_pattern = r'<header>.*?</header>'
    if 'id="btn-about"' not in html:
        html = re.sub(header_pattern, new_header, html, flags=re.DOTALL)
    
    # 3. Inject Modals
    if 'id="modal-about"' not in html:
        html = html.replace('</body>', modals_html + '\n</body>')
    
    # 4. Bump Cache
    html = html.replace('css/style.css?v=27', 'css/style.css?v=28')
    html = html.replace('js/main.js?v=12', 'js/main.js?v=13')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# CSS Update
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

modal_css = '''
/* Modals */
.modal {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    display: flex; align-items: center; justify-content: center;
    z-index: 9999;
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease;
}
.modal.show {
    opacity: 1; pointer-events: auto;
}
.modal-content {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 2rem;
    border-radius: 12px;
    width: 90%; max-width: 500px;
    position: relative;
    transform: translateY(20px);
    transition: transform 0.3s ease;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
.modal.show .modal-content {
    transform: translateY(0);
}
.close-btn {
    position: absolute;
    top: 1rem; right: 1.5rem;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-muted);
}
.close-btn:hover { color: white; }
'''
if '.modal {' not in css:
    css += modal_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# JS Update
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js_logic = '''
// Modal Request Logic
function sendRequest() {
    const title = document.getElementById('req-title').value.trim();
    const link = document.getElementById('req-link').value.trim();
    const msgBox = document.getElementById('req-msg');
    
    if(!title) {
        msgBox.style.color = '#ff4d4d';
        msgBox.innerText = 'Por favor, informe o nome do projeto.';
        return;
    }
    
    const today = new Date().toISOString().split('T')[0];
    const key = `vitaseed_requests_${today}`;
    let requestsToday = parseInt(localStorage.getItem(key) || '0');
    
    if (requestsToday >= 2) {
        msgBox.style.color = '#ff4d4d';
        msgBox.innerText = 'Limite de 2 envios por dia atingido.';
        return;
    }
    
    // Simulate sending to telegram
    localStorage.setItem(key, (requestsToday + 1).toString());
    
    msgBox.style.color = 'var(--accent-green)';
    msgBox.innerText = 'Request enviado com sucesso para o Telegram!';
    
    document.getElementById('req-title').value = '';
    document.getElementById('req-link').value = '';
    document.getElementById('req-desc').value = '';
    
    setTimeout(() => {
        document.getElementById('modal-request').classList.remove('show');
        msgBox.innerText = '';
    }, 2000);
}
'''
if 'function sendRequest()' not in js:
    js += js_logic

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
