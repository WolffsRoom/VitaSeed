import json

with open('api/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for proj in catalog.get('projects', []):
    if proj.get('title') in ['GreenVita', 'DSVita']:
        proj['category'] = 'Apps'

with open('api/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)
