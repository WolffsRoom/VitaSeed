import glob

new_menu = """                      <div id="profile-menu" class="profile-menu">
                          <div style="padding: 1rem; text-align: center; border-bottom: 1px solid var(--border-color);">
                              <strong id="menu-user-name" style="color: var(--text-main);">User</strong><br>
                              <span id="menu-user-email" style="font-size: 0.8rem; color: var(--text-muted);">email</span>
                          </div>
                          <a href="#" onclick="openProfileModal(); return false;" data-i18n="profile_edit"><i class="fa-solid fa-pen-to-square"></i> Editar Perfil</a>
                          <a href="#" onclick="filterUserProjects(); return false;" data-i18n="profile_projects"><i class="fa-solid fa-folder"></i> Meus Projetos</a>
                          <a href="#" id="menu-admin-publish" class="hidden" onclick="document.getElementById('modal-publish').classList.add('show'); return false;"><i class="fa-solid fa-upload"></i> Aprovar Publicação</a>
                          <a href="#" onclick="openSettingsModal(); return false;" data-i18n="profile_settings"><i class="fa-solid fa-gear"></i> Configurações</a>
                          <hr>
                          <button onclick="logout()" data-i18n="profile_logout"><i class="fa-solid fa-arrow-right-from-bracket"></i> Sair</button>
                      </div>"""

import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the old profile-menu div
    content = re.sub(r'<div id="profile-menu" class="profile-menu">.*?</div>\n\s*</div>\n\s*</div>\n\s*</header>', 
                     new_menu + '\n                  </div>\n              </div>\n          </header>', content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print("Updated profile menus.")
