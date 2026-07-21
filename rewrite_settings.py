import re

with open('settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_settings = """
            <div class="settings-container">
                <h2 style="margin-bottom: 1.5rem;">Configurações</h2>
                
                <div>
                    <h3 style="margin-bottom: 0.5rem; font-size: 1rem; color: var(--text-muted);">Aparência (Tema)</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">Escolha o esquema de cores de sua preferência. Será salvo no seu navegador.</p>
                    
                    <div class="settings-grid">
                        <div class="settings-card theme-btn" data-theme-value="">
                            <i class="ph ph-moon"></i>
                            <div style="font-weight: 700;">Dark Mode</div>
                            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.3rem;">Padrão elegante</div>
                        </div>
                        <div class="settings-card theme-btn" data-theme-value="light">
                            <i class="ph ph-sun"></i>
                            <div style="font-weight: 700;">Light Mode</div>
                            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.3rem;">Visual claro</div>
                        </div>
                        <div class="settings-card theme-btn" data-theme-value="sony" style="border-bottom: 4px solid #003399;">
                            <i class="ph ph-gamepad"></i>
                            <div style="font-weight: 700;">Sony Blue</div>
                            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.3rem;">Inspirado no console</div>
                        </div>
                    </div>
                </div>
            </div>
"""

# Include Phosphor Icons in head if missing
if '@phosphor-icons' not in content:
    content = content.replace('</head>', '    <script src="https://unpkg.com/@phosphor-icons/web"></script>\n</head>')

# Remove old inline styles in <head> for settings
content = re.sub(r'<style>.*?\.settings-container {.*?</style>', '', content, flags=re.DOTALL)

# Replace the inner block
content = re.sub(r'<div class="settings-container">.*?</div>\n                </div>\n            </div>', new_settings, content, flags=re.DOTALL)

with open('settings.html', 'w', encoding='utf-8') as f:
    f.write(content)
