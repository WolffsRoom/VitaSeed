import re

# Update JS to remove inline background-position from hero-card
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# The line is: style="background-image: url('${heroBanner}'); background-position: ${heroProj.bgPosition || 'center'};"
js = js.replace(
    "style=\"background-image: url('${heroBanner}'); background-position: ${heroProj.bgPosition || 'center'};\"",
    "style=\"background-image: url('${heroBanner}');\""
)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update CSS to set hero-card to center 60%
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'(\.hero-card\s*\{[^}]*?background-position:\s*)center;', r'\1center 60%;', css)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=23', 'css/style.css?v=24')
    content = content.replace('js/main.js?v=4', 'js/main.js?v=5')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
