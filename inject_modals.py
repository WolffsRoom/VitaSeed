import glob

with open('modals_to_inject.html', 'r', encoding='utf-8') as f:
    modals = f.read()

for file in glob.glob('*.html'):
    if file == 'admin.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject Modals before closing body
    if 'id="modal-profile"' not in content:
        content = content.replace('</body>', modals + '\n</body>')

    # 2. Update Profile Menu links
    # Old menu:
    # <a href="#" onclick="alert('Funcionalidade em breve: Alterar dados'); return false;"><i class="fa-solid fa-pen-to-square"></i> Editar Perfil</a>
    # <a href="#" onclick="alert('Funcionalidade em breve: Meus Projetos'); return false;"><i class="fa-solid fa-folder"></i> Meus Projetos</a>
    
    new_links = """
                          <a href="#" onclick="openProfileModal(); return false;"><i class="fa-solid fa-pen-to-square"></i> Editar Perfil</a>
                          <a href="#" onclick="filterUserProjects(); return false;"><i class="fa-solid fa-folder"></i> Meus Projetos</a>
                          <a href="#" onclick="openSettingsModal(); return false;"><i class="fa-solid fa-gear"></i> Configurações</a>
                          <a href="#" id="menu-admin-publish" class="hidden" onclick="window.location.href='admin.html'; return false;"><i class="fa-solid fa-upload"></i> Publicar / Admin</a>
    """
    
    content = content.replace('<a href="#" onclick="alert(\'Funcionalidade em breve: Alterar dados\'); return false;"><i class="fa-solid fa-pen-to-square"></i> Editar Perfil</a>\n                          <a href="#" onclick="alert(\'Funcionalidade em breve: Meus Projetos\'); return false;"><i class="fa-solid fa-folder"></i> Meus Projetos</a>', new_links.strip())

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Modals and new links injected.")
