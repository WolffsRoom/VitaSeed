import os
import re

new_sidebar = """    <aside id="sidebar">
        <div>
            <div class="logo-container" style="flex-direction: column; align-items: flex-start; gap: 0.2rem;">
                <a href="index.html" style="display: flex; align-items: center; gap: 0.5rem; text-decoration: none; color: inherit; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <div class="seed-icon"></div>
                    <div class="logo">VITA<strong style="font-weight: 800;">SEED</strong> <span style="font-size:0.6rem; color:var(--text-muted); font-weight: normal;">by Wolff</span></div>
                </a>
            </div>
            
            <ul class="nav-links accordion-menu">
                <li><a href="index.html" data-page="index"><span data-i18n="menu_home">HOME</span></a></li>
                
                <li class="nav-section accordion-header" onclick="toggleAccordion(this, 'lib')">BIBLIOTECA <i class="fa-solid fa-chevron-down"></i></li>
                <ul class="accordion-content" id="accordion-lib">
                    <li><a href="category.html?cat=Tudo" data-page="tudo"><span>TUDO</span></a></li>
                    <li><a href="category.html?cat=Ports" data-page="ports"><span>PORTS</span></a></li>
                    <li><a href="category.html?cat=Original games" data-page="original games"><span>ORIGINAL GAMES</span></a></li>
                    <li><a href="category.html?cat=Mods" data-page="mods"><span>MODS</span></a></li>
                    <li><a href="category.html?cat=Translations" data-page="translations"><span>TRADUÇÕES</span></a></li>
                    <li><a href="category.html?cat=Apps" data-page="apps"><span>APPS</span></a></li>
                    <li><a href="category.html?cat=Tools" data-page="tools"><span>TOOLS</span></a></li>
                    <li><a href="category.html?cat=Plugin" data-page="plugins"><span>PLUGINS</span></a></li>
                </ul>
                
                <li class="nav-section accordion-header" onclick="toggleAccordion(this, 'com')">COMUNIDADE <i class="fa-solid fa-chevron-down"></i></li>
                <ul class="accordion-content" id="accordion-com">
                    <li><a href="contribution.html" data-page="contribution"><span data-i18n="menu_colab">COLABORAÇÕES</span></a></li>
                    <li><a href="https://zealouschuck.com/ps-vita-bounty" target="_blank"><span>RECOMPENSAS <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                </ul>
                
                <li class="nav-section accordion-header" onclick="toggleAccordion(this, 'cena')">CENA PSVITA <i class="fa-solid fa-chevron-down"></i></li>
                <ul class="accordion-content" id="accordion-cena">
                    <li><a href="http://brewology.com/" target="_blank"><span>Brewology <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                    <li><a href="https://wololo.net/" target="_blank"><span>Wololo.net <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                    <li><a href="https://www.youtube.com/@TitiClash" target="_blank"><span>Titi Clash <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>
                </ul>
            </ul>
        </div>
        
        <div class="sidebar-footer">
            <div class="version">0.3.0 (beta)</div>
        </div>
    </aside>"""

for f in os.listdir('.'):
    if f.endswith('.html') and f != 'modals_to_inject.html':
        content = open(f, encoding='utf-8').read()
        new_content = re.sub(r'(?s)<aside id="sidebar">.*?</aside>', new_sidebar, content)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Updated {f}')
