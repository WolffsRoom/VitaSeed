import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = re.sub(r'css/style\.css\?v=\d+', 'css/style.css?v=33', html)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Standardized CSS version across all HTML files.")
