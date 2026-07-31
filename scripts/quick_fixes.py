import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix favicon cache
    content = content.replace('href="seed.svg"', 'href="seed.svg?v=2"')
    
    # Fix About modal icon
    if '<h2>Sobre o VitaSeed' in content and 'seed-icon' not in content.split('<h2>Sobre o VitaSeed')[0][-100:]:
        content = content.replace('<h2>Sobre o VitaSeed', '<div class="seed-icon" style="width: 48px; height: 48px; margin: 0 auto 1rem auto;"></div>\n              <h2>Sobre o VitaSeed')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Quick fixes applied!")
