with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace(
    'padding-top: 1rem;\n    padding-bottom: 2rem;',
    'padding-top: 1.5rem;\n    padding-bottom: 2rem;\n    padding-left: 1.5rem;\n    padding-right: 1.5rem;'
)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=21', 'css/style.css?v=22')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
