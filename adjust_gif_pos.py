with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('background-position: center 60%;', 'background-position: center bottom;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=17', 'css/style.css?v=18')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
