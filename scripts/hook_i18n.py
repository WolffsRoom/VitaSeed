import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Configurações menu link
    content = content.replace('<a href="#" onclick="openSettingsModal(); return false;" data-i18n="profile_settings"><i class="fa-solid fa-gear"></i> Configurações</a>', 
                              '<a href="settings.html" data-i18n="profile_settings"><i class="fa-solid fa-gear"></i> Configurações</a>')
    
    # Also fix it if there are weird encodings
    content = re.sub(r'<a href="#" onclick="openSettingsModal\(\); return false;" data-i18n="profile_settings">.*?Configura.*?</a>',
                     '<a href="settings.html" data-i18n="profile_settings"><i class="fa-solid fa-gear"></i> Configurações</a>', content)

    # Search bar placeholder
    content = re.sub(r'id="search-input"\s+class="search-bar"\s+placeholder="[^"]+"',
                     r'id="search-input" class="search-bar" placeholder="Buscar por título ou responsável..." data-i18n="search_placeholder"', content)
    
    # Filter all
    content = re.sub(r'<option value="all">Todas as Categorias</option>',
                     r'<option value="all" data-i18n="filter_all">Todas as Categorias</option>', content)
    
    # About button
    content = re.sub(r'title="Sobre o VitaSeed"', r'title="Sobre o VitaSeed" data-i18n="about_title"', content)

    # Nav links
    content = re.sub(r'<span>HOME</span>', r'<span data-i18n="menu_home">HOME</span>', content)
    content = re.sub(r'<span>COLABORAÇÕES</span>', r'<span data-i18n="menu_colab">COLABORAÇÕES</span>', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

# Now specifically for settings.html, inject the Language option into the main page
with open('settings.html', 'r', encoding='utf-8') as f:
    settings_content = f.read()

lang_div = """
                <div style="margin-top: 2rem;">
                    <h3 style="margin-bottom: 0.5rem; font-size: 1rem; color: var(--text-muted);" data-i18n="settings_lang">Idioma do Site</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">Escolha o idioma do site.</p>
                    <select id="settings-lang-select-main" class="filter-select" style="width: 100%; max-width: 400px; margin-top: 1rem;" onchange="changeLanguage(this.value)">
                        <option value="pt-BR">Português (Brasil)</option>
                        <option value="en">English</option>
                    </select>
                </div>
"""
if 'settings-lang-select-main' not in settings_content:
    settings_content = settings_content.replace('</div>\n            </div>\n        </main>', lang_div + '\n            </div>\n        </main>')
    with open('settings.html', 'w', encoding='utf-8') as f:
        f.write(settings_content)

print("HTML translations hooked up.")
