import json
import glob
import re

# 1. Update Deltarune Cover
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['bannerUrl'] = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiJhB2iaxiwu2BNySLr8IXhsZWLlMF-IjeVJSso5Ju94Imo8tVDU4XS6OJbqqSziAYtsnwyKtcWp8EZ6JKsDIIKwSJ4PIxNpeL1XWy3KjniqLDzXxhS304eQ19VLEwH36Kcy5XBg3THRnmBUwmsoZThAi90CTGux287WAhVXZThe8HaB10YYHv9OdJm900I/s1920/Deltarune-capa.jpg"
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Update HTML files to make logo clickable
for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Desktop Sidebar logo
    old_desktop = '''<div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div class="seed-icon"></div>
                    <div class="logo">VITA<strong style="font-weight: 800;">SEED</strong> <span style="font-size:0.6rem; color:var(--text-muted); font-weight: normal;">by Wolff</span></div>
                </div>'''
    new_desktop = '''<a href="index.html" style="display: flex; align-items: center; gap: 0.5rem; text-decoration: none; color: inherit; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <div class="seed-icon"></div>
                    <div class="logo">VITA<strong style="font-weight: 800;">SEED</strong> <span style="font-size:0.6rem; color:var(--text-muted); font-weight: normal;">by Wolff</span></div>
                </a>'''
    
    # Mobile logo
    old_mobile = '''<div class="logo">Vita<strong>Seed</strong> <span style="font-size:0.6rem; color:var(--text-muted);">by Wolff</span></div>'''
    new_mobile = '''<a href="index.html" style="text-decoration: none; color: inherit;"><div class="logo">Vita<strong>Seed</strong> <span style="font-size:0.6rem; color:var(--text-muted);">by Wolff</span></div></a>'''
    
    content = content.replace(old_desktop, new_desktop)
    
    # For mobile, only replace it inside the mobile header block
    mobile_header_regex = r'(<div class="mobile-header">[\s\S]*?)<div class="logo">Vita<strong>Seed</strong> <span style="font-size:0.6rem; color:var\(--text-muted\);">by Wolff</span></div>'
    content = re.sub(mobile_header_regex, r'\1' + new_mobile, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
