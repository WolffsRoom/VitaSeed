import re

with open('project.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken meta-item and closing divs that caused footer to appear on the side
broken_snippet = '''                        </div>
                            <div class="meta-item">
                                <div class="meta-label">Última Atualização</div>
                                <div id="meta-upd" class="meta-val">--/--/--</div>
                            </div>
                            
                        </div>'''

html = html.replace(broken_snippet, '                        </div>')

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Change .card-banner background-position to bottom
css = re.sub(r'(\.card-banner\s*\{[^}]*?background-position:\s*)center;', r'\1center bottom;', css)
css = re.sub(r'(\.card-image\s*\{[^}]*?background-position:\s*)center;', r'\1center bottom;', css)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=18', 'css/style.css?v=19')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
