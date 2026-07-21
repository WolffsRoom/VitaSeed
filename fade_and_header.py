import re

# 1. Add mask-image to top10-scroll in style.css
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace(
    '.top10-scroll {\n    display: flex;',
    '.top10-scroll {\n    display: flex;\n    -webkit-mask-image: linear-gradient(to right, black 85%, transparent 100%);\n    mask-image: linear-gradient(to right, black 85%, transparent 100%);'
)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Remove header from contribution.html
with open('contribution.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the <header> block entirely
html = re.sub(r'<header>.*?</header>', '', html, flags=re.DOTALL)

with open('contribution.html', 'w', encoding='utf-8') as f:
    f.write(html)
