import re

# 1. Update main.js to add bgPosition to hero-card again
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace: style="background-image: url('${heroBanner}')"
# With: style="background-image: url('${heroBanner}'); background-position: ${heroProj.bgPosition || 'center'};"
js = js.replace(
    "style=\"background-image: url('${heroBanner}');\"",
    "style=\"background-image: url('${heroBanner}'); background-position: ${heroProj.bgPosition || 'center bottom'};\""
)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update project.html to add backgroundPosition
with open('project.html', 'r', encoding='utf-8') as f:
    proj = f.read()

target = "document.getElementById('proj-header-banner').style.backgroundImage = `url('${bannerUrl}')`;"
replacement = target + "\n                document.getElementById('proj-header-banner').style.backgroundPosition = proj.bgPosition || 'center bottom';"

# Make sure we don't duplicate it
if "document.getElementById('proj-header-banner').style.backgroundPosition" not in proj:
    proj = proj.replace(target, replacement)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(proj)

# 3. Just to be safe, update css/style.css to center bottom for hero-card as a fallback
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'(\.hero-card\s*\{[^}]*?background-position:\s*)center 60%;', r'\1center bottom;', css)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=24', 'css/style.css?v=25')
    content = content.replace('css/style.css?v=25', 'css/style.css?v=26')
    content = content.replace('js/main.js?v=5', 'js/main.js?v=6')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
