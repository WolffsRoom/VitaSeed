import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('href="seed.svg" type="image/svg+xml"', 'href="seed.png" type="image/png"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated favicon in HTML files to seed.png")
