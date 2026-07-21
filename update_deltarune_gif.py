import json

catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['bannerUrl'] = "https://i.pinimg.com/originals/f3/c9/c7/f3c9c725757e4b19e460f1be9f10c353.gif"
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)
