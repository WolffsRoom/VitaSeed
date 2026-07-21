import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove subtitle from sidebar (both 0.8rem and 0.65rem versions)
    content = re.sub(r'<div style="font-size: 0\.8rem; color: var\(--text-muted\); line-height: 1\.2; padding-left: 0\.2rem;">Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita\.</div>', '', content)
    content = re.sub(r'<div style="font-size: 0\.65rem; color: var\(--text-muted\); line-height: 1\.2; padding-left: 0\.2rem;">Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita\.</div>', '', content)
    
    # Check if header exists and add subtitle
    if '<header>' in content:
        # Check if already added
        if 'desktop-subtitle' not in content:
            # For pages with user-profile (which is inside header-content)
            if '<div class="user-profile">' in content:
                subtitle_html = '<div class="desktop-subtitle" style="color: var(--text-muted); font-size: 0.9rem; flex: 1; text-align: center; margin: 0 1rem;">Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.</div>\n                <div class="user-profile">'
                content = content.replace('<div class="user-profile">', subtitle_html)
            # If no user-profile, check if header-content exists
            elif '<div class="header-content' in content:
                content = content.replace('<div class="header-content', '<div class="header-content')
                
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
