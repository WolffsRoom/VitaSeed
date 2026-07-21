import json

# 1. Update catalog.json
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('title') == "NoDRTrophiesGODOT":
        p['title'] = "NoTrpDrmGODOT"
        p['category'] = "Plugin"
        p['responsibles'] = "Wolff"
        p['status'] = "Análise"
        p['playable'] = "Não"
        p['description'] = "uso de IA analisar estrutura do NoTrpDrm (by Rinnegatemente) para aplicar funcionamento em jogos baseados GODOT 3.5.rc5 + Vita(by SonicMastr)"
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Update project.html
with open('project.html', 'r', encoding='utf-8') as f:
    proj = f.read()

# Add ID to meta-label
proj = proj.replace('<div class="meta-label">Jogável?</div>\n                                <div id="meta-playable"',
                    '<div id="meta-playable-label" class="meta-label">Jogável?</div>\n                                <div id="meta-playable"')

# Inject JS for dynamic label
js_inject = '''
                if (proj.category === 'Mods' || proj.category === 'Plugins' || proj.category === 'Plugin') {
                    document.getElementById('meta-playable-label').innerText = 'Funcional?';
                }
'''
if "meta-playable-label" not in proj or "Funcional?" not in proj:
    proj = proj.replace("if(proj.playable) {", js_inject + "\n                if(proj.playable) {")

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(proj)

# 3. Update contribution.html to add Plugin option
with open('contribution.html', 'r', encoding='utf-8') as f:
    contrib = f.read()

if '<option value="Plugin">Plugin</option>' not in contrib:
    contrib = contrib.replace('<option value="Mods">Mods</option>', '<option value="Mods">Mods</option>\n                <option value="Plugin">Plugin</option>')

with open('contribution.html', 'w', encoding='utf-8') as f:
    f.write(contrib)

# 4. Also add "Plugin" to Sidebar?
# The user already has "MODS", it might cover plugins, or we could leave the sidebar as is since they didn't explicitly request a new sidebar link, just the category.

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=10', 'js/main.js?v=11')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
