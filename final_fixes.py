import glob

# 1. Fix the 'About' button text replacement issue
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('data-i18n="about_title" onclick="document.getElementById(\'modal-about\')', 'onclick="document.getElementById(\'modal-about\')')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)

# 2. Fix Sony Theme CSS
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'background-size: cover;' not in css:
    css = css.replace("background-image: url('../assets/sony_bg.jpg');", "background-image: url('../assets/sony_bg.jpg');\n    background-repeat: no-repeat;\n    background-size: cover;\n    background-attachment: fixed;")
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

# 3. Add Language selector to settings.html body
with open('settings.html', 'r', encoding='utf-8') as f:
    settings = f.read()

lang_html = """
                <div style="margin-top: 2rem;">
                    <h3 style="margin-bottom: 0.5rem; font-size: 1rem; color: var(--text-muted);" data-i18n="settings_lang">Idioma do Site</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">Escolha o idioma do site.</p>
                    <select id="settings-lang-select-main" class="filter-select" style="width: 100%; max-width: 400px; margin-top: 1rem;" onchange="changeLanguage(this.value)">
                        <option value="pt-BR">Português (Brasil)</option>
                        <option value="en">English</option>
                    </select>
                </div>
"""
if 'settings-lang-select-main' not in settings:
    # Let's find a reliable place to inject it. 
    # Let's put it right after the theme grid closes.
    # We can search for the closing div of settings-grid
    import re
    # We know it's in <div class="settings-container"> ... </div>
    settings = re.sub(r'(<div class="settings-grid">.*?</div>\s*</div>)', r'\1' + lang_html, settings, flags=re.DOTALL)
    with open('settings.html', 'w', encoding='utf-8') as f:
        f.write(settings)

print("Final fixes applied!")
