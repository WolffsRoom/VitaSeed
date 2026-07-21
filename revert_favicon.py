import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('href="seed.png" type="image/png"', 'href="seed.svg" type="image/svg+xml"')
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file}")
