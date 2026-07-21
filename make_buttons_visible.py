with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Change default opacity to 0.4, hover to 1
css = css.replace('opacity: 0;\n    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);', 'opacity: 0.5;\n    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);')

# Also remove the #top10-section:hover .scroll-btn { opacity: 0.4; }
css = css.replace('#top10-section:hover .scroll-btn {\n    opacity: 0.4;\n}', '')

# Ensure z-index is super high just in case
css = css.replace('z-index: 10;', 'z-index: 100;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=20', 'css/style.css?v=21')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
