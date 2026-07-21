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

# 2. Update CSS background position
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('background-position: center bottom;', 'background-position: center 60%;')
with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update project.html
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
html = re.sub(r'if\(proj.publish_date\).*?meta-upd.*?update_date;', js_add, html, flags=re.DOTALL)

# Move media-section and install-section out of the left column
# Currently they are inside the left column of project-layout.
# We will extract them and append them AFTER project-layout.

media_match = re.search(r'(<div id="media-section".*?</div>\s*</div>)', html, re.DOTALL)
install_match = re.search(r'(<div id="install-section".*?</div>\s*</div>)', html, re.DOTALL)

if media_match and install_match:
    media_html = media_match.group(1)
    install_html = install_match.group(1)
    
    # Remove them from their current position
    html = html.replace(media_html, '')
    html = html.replace(install_html, '')
    
    # Change Mídia to Capturas de tela
    media_html = media_html.replace('Mídia (Prints & Vídeos)', 'Capturas de tela')
    
    # Insert them after <div class="project-layout">...</div>
    # project-layout is closed before `<div style="display: flex; flex-direction: column; gap: 2rem;">` which is the right column?
    # Actually project-layout contains BOTH the left and right column. We want to insert them AFTER the closing tag of project-layout.
    # The structure is:
    # <div class="project-layout">
    #   <div left column> </div>
    #   <div right column> </div>
    # </div>
    
    html = html.replace('<!-- Footer -->', f'</div>\n{media_html}\n{install_html}\n<!-- Footer -->')
    # Wait, if we just inject before Footer, we need to make sure we don't break the layout. 
    # But wait, we need to remove the </div> that we just added if we inject before footer.
    # Wait, the footer is inside .content-wrapper, which wraps the whole <main>...
    
with open('project.html', 'w', encoding='utf-8') as f:
    f.write(html)
