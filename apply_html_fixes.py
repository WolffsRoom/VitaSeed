import glob
import re

footer_html = """
    <!-- Footer -->
    <footer class="app-footer">
        <p>&copy; 2026 VitaSeed. Todos os direitos reservados.</p>
        <p style="margin-top:0.5rem; font-size:0.75rem;">Repositório não oficial. Todos os jogos, ports e marcas pertencem aos seus respectivos donos.</p>
        <div style="margin-top:1rem;">
            <a href="https://github.com/WolffsRoom/VitaSeed" target="_blank"><i class="fa-brands fa-github"></i> GitHub do Projeto</a>
        </div>
    </footer>
"""

logo_fix_regex = r'<div class="logo-container">.*?<div class="seed-icon"></div>.*?<div class="logo">VITA<strong style="font-weight: 800;">SEED</strong>.*?<div style="font-size: 0.65rem; color: var\(--text-muted\); line-height: 1.4; margin-top: 0.5rem; text-transform: none; letter-spacing: 0;">Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.</div>.*?</div>'

fixed_logo = """<div class="logo-container" style="flex-direction: column; align-items: flex-start; gap: 0.2rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div class="seed-icon"></div>
                    <div class="logo">VITA<strong style="font-weight: 800;">SEED</strong> <span style="font-size:0.6rem; color:var(--text-muted); font-weight: normal;">by Wolff</span></div>
                </div>
                <div style="font-size: 0.65rem; color: var(--text-muted); line-height: 1.2; padding-left: 0.2rem;">Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.</div>
            </div>"""

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply Footer
    # Look for </main></div> or similar where we can safely insert footer
    if '<!-- Footer -->' not in content:
        if '</main>' in content:
            content = content.replace('</main>', f'</main>\n{footer_html}')
        elif '<script src="js/' in content:
            # Fallback for pages without main
            content = content.replace('<script src="js/', f'{footer_html}\n    <script src="js/')

    # Apply Logo Fix using regex DOTALL
    content = re.sub(r'<div class="logo-container">.*?Repositório brasileiro de jogos.*?</div>\n.*?</div>', fixed_logo, content, flags=re.DOTALL)
    
    # Alternatively, just use string matching for the specific known block
    block_to_replace = """<div class="logo-container">
                <div class="seed-icon"></div>
                                <div class="logo">VITA<strong style="font-weight: 800;">SEED</strong> <span style="font-size:0.6rem; color:var(--text-muted); font-weight: normal;">by Wolff</span></div>
                <div style="font-size: 0.65rem; color: var(--text-muted); line-height: 1.4; margin-top: 0.5rem; text-transform: none; letter-spacing: 0;">Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.</div>
            </div>"""
    content = content.replace(block_to_replace, fixed_logo)
    
    # contribution.html specific
    if file == 'contribution.html':
        content = re.sub(r'<img\s+src="https://ui-avatars.com.*?>\s*', '', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
