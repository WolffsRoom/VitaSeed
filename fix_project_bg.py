with open('project.html', 'r', encoding='utf-8') as f:
    proj = f.read()

target = "document.getElementById('proj-header-banner').style.backgroundImage = `url('${bannerUrl}')`;"
replacement = target + "\n                document.getElementById('proj-header-banner').style.backgroundPosition = proj.bgPosition || 'center';"

proj = proj.replace(target, replacement)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(proj)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=24', 'css/style.css?v=25')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
