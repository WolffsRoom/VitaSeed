import glob

old_nav = '''                <li class="nav-section">GERAL</li>
                <li><a href="index.html" data-page="index"><span>HOME</span></a></li>
                
                <li class="nav-section">BIBLIOTECA</li>'''

new_nav = '''                <li><a href="index.html" data-page="index"><span>HOME</span></a></li>
                
                <li class="nav-section">BIBLIOTECA</li>'''

old_recompensas = '''<li><a href="https://zealouschuck.com/ps-vita-bounty" target="_blank"><span>Recompensas <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>'''
new_recompensas = '''<li><a href="https://zealouschuck.com/ps-vita-bounty" target="_blank"><span>RECOMPENSAS <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>'''

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old_nav, new_nav)
    content = content.replace(old_recompensas, new_recompensas)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Reduce gap in nav-links
css = css.replace(
    '.nav-links, .sidebar-footer ul {\n    list-style: none;\n    display: flex;\n    flex-direction: column;\n    gap: 0.8rem;\n}',
    '.nav-links, .sidebar-footer ul {\n    list-style: none;\n    display: flex;\n    flex-direction: column;\n    gap: 0.2rem;\n}'
)

# If it fails, try original without `.sidebar-footer ul`
css = css.replace(
    'gap: 0.8rem;',
    'gap: 0.3rem;'
)

css = css.replace(
    'padding: 0.8rem 1.2rem;',
    'padding: 0.6rem 1.2rem;'
)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
