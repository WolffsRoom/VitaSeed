with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_snippet = '''                        <div class="top10-info">
                            <h3 class="top10-title">${window.formatTitle ? window.formatTitle(proj.title) : proj.title}</h3>
                            <div class="top10-category">${proj.category}</div>
                        </div>'''

new_snippet = '''                        <div class="top10-info">
                            <h3 class="top10-title">${window.formatTitle ? window.formatTitle(proj.title) : proj.title}</h3>
                            <div class="top10-category" style="font-weight: bold;">${proj.category}</div>
                            <div class="top10-responsible" style="font-size: 0.8rem; color: var(--text-muted); margin-top: 2px;"><i class="ph ph-user"></i> ${proj.responsibles}</div>
                        </div>'''

js = js.replace(old_snippet, new_snippet)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=6', 'js/main.js?v=7')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
