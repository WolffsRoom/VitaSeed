import glob

old_nav = '''                <li class="nav-section">GERAL</li>
                <li><a href="index.html" data-page="index"><span>Menu Principal</span></a></li>
                
                <li class="nav-section">BIBLIOTECA</li>
                <li><a href="category.html?cat=Ports" data-page="ports"><span>Ports</span></a></li>
                <li><a href="category.html?cat=Original games" data-page="original games"><span>Original Games</span></a></li>
                <li><a href="category.html?cat=Mods" data-page="mods"><span>Mods</span></a></li>
                <li><a href="category.html?cat=Translations" data-page="translations"><span>Translations</span></a></li>
                
                <li class="nav-section">COMUNIDADE</li>
                <li><a href="contribution.html" data-page="contribution"><span>Contribution Tree</span></a></li>'''

new_nav = '''                <li class="nav-section">GERAL</li>
                <li><a href="index.html" data-page="index"><span>HOME</span></a></li>
                
                <li class="nav-section">BIBLIOTECA</li>
                <li><a href="category.html?cat=Ports" data-page="ports"><span>PORTS</span></a></li>
                <li><a href="category.html?cat=Original games" data-page="original games"><span>ORIGINAL GAMES</span></a></li>
                <li><a href="category.html?cat=Mods" data-page="mods"><span>MODS</span></a></li>
                <li><a href="category.html?cat=Translations" data-page="translations"><span>TRADUÇÕES</span></a></li>
                
                <li class="nav-section">COMUNIDADE</li>
                <li><a href="contribution.html" data-page="contribution"><span>Colaborações</span></a></li>
                <li><a href="https://zealouschuck.com/ps-vita-bounty" target="_blank"><span>Recompensas <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                
                <li class="nav-section">CENA PSVITA</li>
                <li><a href="https://www.rinnegatamante.eu/vitadb/#/" target="_blank"><span>VitaDB <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                <li><a href="http://brewology.com/" target="_blank"><span>Brewology <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                <li><a href="https://wololo.net/" target="_blank"><span>Wololo.net <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>'''

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old_nav, new_nav)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
