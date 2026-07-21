import json

# 1. Update catalog.json to add bgPosition to Deltarune
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['bgPosition'] = "center bottom"
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Update js/main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(
    "style=\"background-image: url('${heroBanner}')\"",
    "style=\"background-image: url('${heroBanner}'); background-position: ${heroProj.bgPosition || 'center'};\""
)
js = js.replace(
    "style=\"background-image: url('${banner}')\"",
    "style=\"background-image: url('${banner}'); background-position: ${proj.bgPosition || 'center'};\""
)
js = js.replace(
    "style=\"background-image: url('${bannerUrl}');\"",
    "style=\"background-image: url('${bannerUrl}'); background-position: ${proj.bgPosition || 'center'};\""
)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Update category.html
with open('category.html', 'r', encoding='utf-8') as f:
    cat = f.read()

cat = cat.replace(
    "style=\"background-image: url('${bannerUrl}');\"",
    "style=\"background-image: url('${bannerUrl}'); background-position: ${proj.bgPosition || 'center'};\""
)

with open('category.html', 'w', encoding='utf-8') as f:
    f.write(cat)

# 4. Update project.html
with open('project.html', 'r', encoding='utf-8') as f:
    proj = f.read()

proj = proj.replace(
    "document.getElementById('proj-header-banner').style.backgroundImage = `url('${banner}')`;",
    "document.getElementById('proj-header-banner').style.backgroundImage = `url('${banner}')`;\n                document.getElementById('proj-header-banner').style.backgroundPosition = proj.bgPosition || 'center';"
)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(proj)

# 5. Remove center bottom from global CSS to let inline styles govern
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('background-position: center bottom;', 'background-position: center;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=22', 'css/style.css?v=23')
    content = content.replace('js/main.js?v=3', 'js/main.js?v=4')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
