import json
import re

# 1. Update catalog.json
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['title'] = 'Deltarune <span style="font-weight: 400; font-size: 0.85em;">(Chapters 1 to 5)</span>'
        p['status'] = 'Em Desenvolvimento'
        p['playable'] = 'Sim'
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Update CSS background position and Top 10 fade
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix GIF background-position
css = css.replace('background-position: center bottom;', 'background-position: center 60%;')

# Fix Top 10 Fade (both sides)
css = css.replace(
    '-webkit-mask-image: linear-gradient(to right, black 85%, transparent 100%);\n    mask-image: linear-gradient(to right, black 85%, transparent 100%);',
    '-webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);\n    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);'
)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update project.html safely
with open('project.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Status and Playable to meta-grid
new_meta_grid = '''<div class="meta-grid">
                            <div class="meta-item">
                                <div class="meta-label">Publicação Original</div>
                                <div id="meta-pub" class="meta-val">--/--/--</div>
                            </div>
                            <div class="meta-item">
                                <div class="meta-label">Última Atualização</div>
                                <div id="meta-upd" class="meta-val">--/--/--</div>
                            </div>
                            <div class="meta-item">
                                <div class="meta-label">Status</div>
                                <div id="meta-status" class="meta-val">Concluído</div>
                            </div>
                            <div class="meta-item">
                                <div class="meta-label">Jogável?</div>
                                <div id="meta-playable" class="meta-val">Sim</div>
                            </div>
                        </div>'''

html = re.sub(r'<div class="meta-grid">.*?</div>\s*</div>', new_meta_grid, html, flags=re.DOTALL)

# Add Javascript to populate them
js_add = '''
                if(proj.publish_date) document.getElementById('meta-pub').innerText = proj.publish_date;
                if(proj.update_date) document.getElementById('meta-upd').innerText = proj.update_date;
                if(proj.status) {
                    document.getElementById('meta-status').innerText = proj.status;
                } else {
                    document.getElementById('meta-status').innerText = "Concluído"; // Default
                }
                if(proj.playable) {
                    document.getElementById('meta-playable').innerText = proj.playable;
                } else {
                    document.getElementById('meta-playable').innerText = "Sim"; // Default
                }
'''
html = re.sub(r'if\s*\(\s*proj\.publish_date\s*\).*?meta-upd.*?update_date;', js_add, html, flags=re.DOTALL)

# Safely extract the sections using exact string replacement
block_to_extract = '''                        <div id="media-section" class="section-box hidden">
                            <h3><i class="ph ph-image"></i> Mídia (Prints & Vídeos)</h3>
                            <div id="media-container" class="media-grid"></div>
                        </div>

                        <div id="install-section" class="section-box hidden">
                            <h3><i class="ph ph-wrench"></i> Instruções de Instalação</h3>
                            <div id="install-text" style="line-height: 1.6;"></div>
                        </div>'''

if block_to_extract in html:
    html = html.replace(block_to_extract, '')
    
    # Change Mídia to Capturas de tela
    new_block = block_to_extract.replace('Mídia (Prints & Vídeos)', 'Capturas de tela')
    
    # Ensure they span full width by placing them after the main layout grid
    html = html.replace('</div>\n                </div>\n\n            </div>', f'</div>\n                </div>\n\n                <div style="margin-top: 2rem;">\n{new_block}\n                </div>\n\n            </div>')
else:
    # If it was already moved but the text needs updating:
    html = html.replace('Mídia (Prints & Vídeos)', 'Capturas de tela')

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(html)
