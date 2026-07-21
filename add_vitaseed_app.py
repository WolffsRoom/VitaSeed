import json

with open('api/catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Find the max ID to assign a new one
max_id = max([p['id'] for p in catalog['projects']]) if catalog['projects'] else 0
new_id = max_id + 1

new_project = {
    "id": new_id,
    "title": "VitaSeed",
    "category": "Apps",
    "responsibles": "Wolff",
    "description": "O aplicativo nativo do VitaSeed para o PSVita! Uma forma de navegar e baixar todos os Ports, Mods, Traduções, Apps e Ferramentas diretamente do seu console. (Esqueleto/Base em desenvolvimento)",
    "status": "Em desenvolvimento",
    "playable": "Em progresso",
    "source_link": "https://github.com/WolffsRoom/VitaSeed",
    "bannerUrl": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400",
    "ai_used": False,
    "install_instructions": "O aplicativo ainda está na fase inicial de desenvolvimento. Fique ligado para futuras atualizações e lançamentos de VPKs testáveis!"
}

catalog['projects'].append(new_project)

with open('api/catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)
