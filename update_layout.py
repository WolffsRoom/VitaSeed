import glob
import re

# 1. New Modals HTML
modals_html = '''
    <!-- Modals -->
    <div id="modal-about" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('modal-about')">&times;</span>
            <h2>Sobre o VitaSeed</h2>
            <p style="margin-top: 1rem; line-height: 1.6; color: var(--text-muted);">
                O VitaSeed é o seu diretório definitivo para a cena homebrew do PSVita. 
                Aqui centralizamos Ports, Mods, Traduções, Plugins e Jogos Originais, 
                garantindo que você sempre tenha acesso às versões mais atualizadas 
                e perfeitamente categorizadas.
            </p>
        </div>
    </div>

    <div id="modal-request" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal('modal-request')">&times;</span>
            <h2>Solicitar Projeto</h2>
            <p style="margin-top: 1rem; margin-bottom: 1.5rem; font-size: 0.9rem; color: var(--text-muted);">
                Não encontrou o que procurava? Envie um request para adicionarmos o projeto ao catálogo! (Limite: 2 envios por dia)
            </p>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <input type="text" id="req-title" class="search-bar" placeholder="Nome do Projeto / Jogo">
                <input type="text" id="req-link" class="search-bar" placeholder="Link de Referência (GitHub, VitaDB, etc)">
                <textarea id="req-desc" class="search-bar" rows="3" placeholder="Por que devemos adicionar?" style="resize: vertical; font-family: inherit;"></textarea>
                <button class="btn-primary" onclick="sendRequest()" style="width: 100%; justify-content: center; margin-top: 0.5rem;"><i class="ph ph-paper-plane-tilt"></i> Enviar Pedido</button>
                <div id="req-msg" style="text-align: center; font-size: 0.9rem; margin-top: 0.5rem;"></div>
            </div>
        </div>
    </div>
'''

def update_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Change Sidebar
    # Insert PLUGINS below MODS
    if 'data-page="mods"><span>MODS</span></a></li>' in html and 'data-page="plugins"><span>PLUGINS' not in html:
        html = html.replace(
            '<li><a href="category.html?c=Mods" data-page="mods"><span>MODS</span></a></li>',
            '<li><a href="category.html?c=Mods" data-page="mods"><span>MODS</span></a></li>\n                <li><a href="category.html?c=Plugin" data-page="plugins"><span>PLUGINS</span></a></li>'
        )
    # Add APPS below Translations
    if 'data-page="translations"><span>TRADUÇÕES</span></a></li>' in html and 'data-page="apps"><span>APPS' not in html:
        html = html.replace(
            '<li><a href="category.html?c=Translations" data-page="translations"><span>TRADUÇÕES</span></a></li>',
            '<li><a href="category.html?c=Translations" data-page="translations"><span>TRADUÇÕES</span></a></li>\n                <li><a href="category.html?c=Apps" data-page="apps"><span>APPS</span></a></li>'
        )

    # Change category options (Tools -> Apps)
    html = html.replace('<option value="Tools">Tools</option>', '<option value="Apps">Apps</option>')

    # Update Header Structure
    # Use regex to find <header>...</header>
    header_pattern = r'<header>.*?</header>'
    
    new_header = '''<header style="display: flex; gap: 1rem; align-items: center; justify-content: space-between; flex-wrap: wrap;">
            <div style="display: flex; gap: 1rem; flex: 1; min-width: 200px;">
                <input type="text" id="search-input" class="search-bar" placeholder="Buscar por título ou responsável..." style="flex: 1;">
            </div>
            <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                <select id="category-filter" class="filter-select">
                    <option value="all">Todas as Categorias</option>
                    <option value="Ports">Ports</option>
                    <option value="Original games">Original games</option>
                    <option value="Mods">Mods</option>
                    <option value="Plugin">Plugin</option>
                    <option value="Translations">Translations</option>
                    <option value="Apps">Apps</option>
                    <option value="PC Tools">PC Tools</option>
                </select>
                <select id="dev-filter" class="filter-select">
                    <option value="all">Todos os responsáveis</option>
                </select>
                <button id="btn-about" class="btn-icon" style="background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border-color); padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer;" onclick="document.getElementById('modal-about').classList.add('show')"><i class="ph ph-question"></i></button>
                <button id="btn-request" class="btn-primary" onclick="document.getElementById('modal-request').classList.add('show')"><i class="ph ph-paper-plane-tilt"></i> Request</button>
            </div>
        </header>'''
    
    html = re.sub(header_pattern, new_header, html, flags=re.DOTALL)

    # Inject Modals before closing body
    if 'id="modal-about"' not in html:
        html = html.replace('</body>', modals_html + '\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

for file in glob.glob('*.html'):
    update_html(file)
