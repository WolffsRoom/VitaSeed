import json
import os

catalog_path = 'api/catalog.json'

with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Check if Deltarune is already in catalog
if not any(p.get('id') == 222 for p in catalog.get('projects', [])):
    new_project = {
        "id": 222,
        "title": "Deltarune (Chapters 1 to 5)",
        "category": "Ports",
        "ai_used": False,
        "vibecoded": False,
        "responsibles": "Wolff",
        "description": "Deltarune (Chapters 1 to 5) Port to PSVita.",
        "install_instructions": "1. Baixe o VPK.\n2. Instale via VitaShell.\n3. Divirta-se!",
        "bannerUrl": "https://github.com/WolffsRoom/DeltaruneVita/raw/main/assets/banner.jpg",  # Assuming banner exists
        "screenshots": [
            "https://github.com/WolffsRoom/DeltaruneVita/raw/main/assets/screen1.jpg",
            "https://github.com/WolffsRoom/DeltaruneVita/raw/main/assets/screen2.jpg"
        ],
        "source_link": "https://github.com/WolffsRoom/DeltaruneVita",
        "publish_date": "21/07/2026",
        "update_date": "21/07/2026",
        "downloads": 0,
        "support_link": "https://ko-fi.com/wolff"
    }
    catalog['projects'].append(new_project)
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)
