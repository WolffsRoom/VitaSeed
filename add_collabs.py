import json

# 1. Add collaborators field to catalog.json
with open('api/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for proj in catalog['projects']:
    if proj['title'] == 'Zombie Tsunami':
        proj['collaborators'] = ['Wolff']
    if proj['title'] == 'Beach Buggy Racing':
        proj['collaborators'] = ['Wolff']

with open('api/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

print("Catalog updated!")
