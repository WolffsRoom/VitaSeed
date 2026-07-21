with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add #top10-section { position: relative; }
if '#top10-section {' not in css:
    css += '\n#top10-section {\n    position: relative;\n}\n'

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=26', 'css/style.css?v=27')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
