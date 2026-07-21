import glob

dropdown_html = """
                <div id="user-profile-dropdown" class="profile-dropdown hidden" style="margin-left: 0.5rem;">
                    <!-- Avatar will be injected here -->
                    <div id="profile-menu" class="profile-menu">
                        <div style="padding: 1rem; text-align: center; border-bottom: 1px solid var(--border-color);">
                            <strong id="menu-user-name" style="color: var(--text-main);">User</strong><br>
                            <span id="menu-user-email" style="font-size: 0.8rem; color: var(--text-muted);">email</span>
                        </div>
                        <a href="#" onclick="alert('Funcionalidade em breve: Alterar dados'); return false;"><i class="fa-solid fa-pen-to-square"></i> Editar Perfil</a>
                        <a href="#" onclick="alert('Funcionalidade em breve: Meus Projetos'); return false;"><i class="fa-solid fa-folder"></i> Meus Projetos</a>
                        <hr>
                        <button onclick="logout()"><i class="fa-solid fa-arrow-right-from-bracket"></i> Sair</button>
                    </div>
                </div>"""

for file in glob.glob('*.html'):
    if file == 'admin.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Top Right Profile
    if '<div id="top-right-profile"' in content:
        import re
        content = re.sub(r'<!-- Top Right Auth Bar -->\s*<div id="top-right-profile"[\s\S]*?</div>\s*</div>', '', content)
        # Also clean up empty content-wrappers if left broken, but actually my previous script just replaced `<div class="content-wrapper">` with `<div class="content-wrapper">...bar...`
        content = re.sub(r'<div class="content-wrapper">\s*<!-- Top Right Auth Bar -->\s*<div id="top-right-profile"[\s\S]*?</div>\s*</div>\s*', '<div class="content-wrapper">\n', content)

    # 2. Insert next to btn-request
    target = '<button id="btn-request"'
    if target in content and 'user-profile-dropdown' not in content:
        # Split on btn-request and insert after the closing button tag
        parts = content.split('</button>\n            </div>\n        </header>')
        if len(parts) == 2:
            content = parts[0] + '</button>\n' + dropdown_html + '\n            </div>\n        </header>' + parts[1]
        else:
            # Fallback if the string splitting is slightly different
            content = content.replace('</button>\n            </div>', '</button>\n' + dropdown_html + '\n            </div>')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Moved profile icon next to request button.")
