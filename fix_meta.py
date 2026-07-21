import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the desktop-subtitle div added previously
    content = re.sub(r'<div class="desktop-subtitle"[^>]*>Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita\.</div>\s*', '', content)
    
    # Remove any other rogue text nodes with this exact string if it was somehow placed differently
    content = content.replace('Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.', '')
    
    # Add meta description if not present
    if '<meta name="description"' not in content:
        meta_tag = '<meta name="description" content="Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.">\n    '
        # Insert it right after <title>
        content = re.sub(r'(<title>.*?</title>)', r'\1\n    ' + meta_tag.strip(), content)
    else:
        # If it's already there, ensure it has the correct content
        content = re.sub(r'<meta name="description" content="[^"]*">', 
                         '<meta name="description" content="Repositório brasileiro de jogos, ports, ferramentas, mods e traduções para PSVita.">', 
                         content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
