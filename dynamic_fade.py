import re

# 1. Update CSS
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Revert .top10-scroll to right-fade only
old_fade = '''    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);'''

new_fade = '''    -webkit-mask-image: linear-gradient(to right, black 85%, transparent 100%);
    mask-image: linear-gradient(to right, black 85%, transparent 100%);
    transition: mask-image 0.3s ease, -webkit-mask-image 0.3s ease;'''

css = css.replace(old_fade, new_fade)

# Add .scrolled class for double fade
scrolled_css = '''
.top10-scroll.scrolled {
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 5%, black 95%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 5%, black 95%, transparent 100%);
}
'''
if '.top10-scroll.scrolled' not in css:
    css += scrolled_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update JS
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js_event = '''
                top10Container.addEventListener('scroll', () => {
                    if (top10Container.scrollLeft > 10) {
                        top10Container.classList.add('scrolled');
                    } else {
                        top10Container.classList.remove('scrolled');
                    }
                });
'''

# Inject after btnRight.addEventListener
if "top10Container.classList.add('scrolled')" not in js:
    js = js.replace("btnRight.addEventListener('click', () => {\n                    top10Container.scrollBy({ left: 400, behavior: 'smooth' });\n                });",
                    "btnRight.addEventListener('click', () => {\n                    top10Container.scrollBy({ left: 400, behavior: 'smooth' });\n                });" + js_event)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=19', 'css/style.css?v=20')
    content = content.replace('js/main.js?v=2', 'js/main.js?v=3')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
