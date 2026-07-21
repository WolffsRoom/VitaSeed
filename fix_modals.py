import glob
import re

# New modal HTML (correct, centered Request form + ? in About title)
new_modals = '''    <!-- Modals -->
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

modal_pattern = re.compile(r'    <!-- Modals -->.*?</div>\s*\n\s*\n</body>', re.DOTALL)

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'modal-about' not in html:
        continue

    # Replace modal block
    html = modal_pattern.sub(new_modals + '\n\n</body>', html)

    # Bump cache versions
    html = html.replace('css/style.css?v=30', 'css/style.css?v=31')
    html = html.replace('js/main.js?v=14', 'js/main.js?v=15')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# Add ESC key and closeModal function to main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

esc_logic = '''
// Modal Utility
function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.show').forEach(m => m.classList.remove('show'));
    }
});
'''

if 'function closeModal' not in js:
    js = esc_logic + '\n' + js

# Fix the sendRequest function to also use closeModal
js = js.replace(
    "document.getElementById('modal-request').classList.remove('show');",
    "closeModal('modal-request');"
)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
