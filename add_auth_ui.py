import glob
import re

auth_scripts = """
    <!-- Firebase Auth -->
    <script src="https://www.gstatic.com/firebasejs/10.4.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.4.0/firebase-auth-compat.js"></script>
    <script src="js/auth.js"></script>
"""

login_modal = """
    <!-- Modal Login -->
    <div id="modal-login" class="modal">
        <div class="modal-content" style="max-width: 400px; text-align: center;">
            <div class="seed-icon" style="width: 48px; height: 48px; margin: 0 auto 1rem auto;"></div>
            <h2>Acesse o VitaSeed</h2>
            <p style="color: var(--text-muted); margin-bottom: 2rem; font-size: 0.9rem;">Faça login para solicitar a adição de novos jogos ao catálogo.</p>
            
            <button class="btn-secondary" onclick="loginWithGoogle()" style="width: 100%; justify-content: center; padding: 0.8rem; font-size: 1rem; background: white; color: black; border-color: white;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" width="18" height="18" style="margin-right: 0.5rem;">
                Entrar com Google
            </button>
            <button onclick="closeModal('modal-login')" class="btn-primary" style="width: 100%; justify-content: center; margin-top: 1rem; background: transparent; border: none; color: var(--text-muted);">Cancelar</button>
        </div>
    </div>
"""

for file in glob.glob('*.html'):
    if file == 'admin.html':
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject scripts before </body>
    if 'firebase-app-compat.js' not in content:
        content = content.replace('</body>', auth_scripts + login_modal + '\n</body>')

    # Inject login button in sidebar
    if 'id="login-btn"' not in content:
        sidebar_injection = """
                <li id="sidebar-login-container">
                    <a href="#" id="login-btn" onclick="document.getElementById('modal-login').classList.add('show'); return false;"><span style="color: var(--accent-green);"><i class="fa-solid fa-right-to-bracket"></i> Login / Register</span></a>
                    <div id="user-profile" class="hidden" style="padding: 1rem; padding-left: 2rem; display: flex; align-items: center; gap: 0.5rem; color: var(--text-muted); font-size: 0.85rem;">
                        <!-- Avatar will go here -->
                    </div>
                </li>"""
        # Find <li class="nav-section">BIBLIOTECA</li> and inject before it
        content = content.replace('<li class="nav-section">BIBLIOTECA</li>', sidebar_injection + '\n                <li class="nav-section">BIBLIOTECA</li>')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Auth UI injected into HTML files.")
