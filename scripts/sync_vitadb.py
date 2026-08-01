import urllib.request
import json
import os

VITADB_RAW_URL = "https://raw.githubusercontent.com/DrDecki/VitaDBtoo-db/main/apps.json"
CATALOG_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "api", "catalog.json")
CATALOG_JS_PATH = os.path.join(os.path.dirname(__file__), "..", "js", "catalog_data.js")

# Mapeamento de tipos do VitaDB
TYPE_MAPPING = {
    "1": "Original Games",
    "2": "Ports",
    "3": "Mods",
    "4": "Apps",
    "5": "Tools",
    "6": "Translations",
    "7": "Plugin",
    "8": "PC Tools"
}

def map_category(type_str, tags_str=""):
    type_key = str(type_str).strip()
    cat = TYPE_MAPPING.get(type_key, "Apps")
    return cat

def sync_vitadb():
    print(f"--> Baixando catálogo do VitaDBtoo-db ({VITADB_RAW_URL})...")
    try:
        req = urllib.request.Request(VITADB_RAW_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            raw_data = json.loads(response.read().decode('utf-8'))
        print(f"--> {len(raw_data)} projetos carregados do VitaDBtoo-db!")
    except Exception as e:
        print(f"Erro ao baixar dados do VitaDBtoo-db: {e}")
        return

    # Lendo catalog.json atual para preservar os projetos nativos criados por Wolff / MeninoSung
    current_projects = []
    if os.path.exists(CATALOG_JSON_PATH):
        try:
            with open(CATALOG_JSON_PATH, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
                current_projects = current_data.get('projects', [])
        except Exception as e:
            print(f"Aviso ao ler catalog.json existente: {e}")

    # Preservar IDs dos projetos nativos
    existing_ids = {p.get('id') for p in current_projects if 'id' in p}
    projects_list = list(current_projects)

    added_count = 0
    updated_count = 0

    for item in raw_data:
        try:
            raw_id = int(item.get('id', 0))
        except (ValueError, TypeError):
            raw_id = 900000 + len(projects_list)

        title = item.get('name') or "Untitled Project"
        author = item.get('author') or "Community"
        version = item.get('version', '1.0').replace('v.', 'v').replace('v', '')
        if not version:
            version = "1.0"

        category = map_category(item.get('type'), item.get('tags'))
        description = item.get('long_description') or item.get('description') or "No description provided."
        source_link = item.get('source') or item.get('release_page') or "https://github.com/DrDecki/VitaDBtoo-db"
        vpk_url = item.get('url', '')

        # Banner image
        icon = item.get('icon', '')
        if icon.startswith('http'):
            banner_url = icon
        elif icon:
            banner_url = f"https://raw.githubusercontent.com/DrDecki/VitaDBtoo-db/main/icons/{icon}"
        else:
            banner_url = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400"

        # Screenshots
        screenshots = []
        raw_shots = item.get('screenshots', '')
        if isinstance(raw_shots, list):
            screenshots = raw_shots
        elif isinstance(raw_shots, str) and raw_shots.strip():
            screenshots = [s.strip() for s in raw_shots.split(',') if s.strip()]

        downloads_list = []
        if vpk_url:
            downloads_list.append({
                "name": f"Download VPK (v{version})",
                "url": vpk_url
            })
        if item.get('release_page') and item.get('release_page') != vpk_url:
            downloads_list.append({
                "name": "Releases Page",
                "url": item.get('release_page')
            })

        # Montar o objeto no formato VitARCH
        proj_obj = {
            "id": raw_id,
            "title": title,
            "category": category,
            "ai_used": item.get('ai') == '1',
            "vibecoded": False,
            "responsibles": author,
            "description": description,
            "install_instructions": item.get('changelog') or "Install the VPK via VitaShell.",
            "bannerUrl": banner_url,
            "screenshots": screenshots,
            "source_link": source_link,
            "publish_date": item.get('date', '2026-08-01'),
            "update_date": item.get('date', '2026-08-01'),
            "downloads": int(item.get('downloads', 0)) if str(item.get('downloads', 0)).isdigit() else 0,
            "support_link": source_link,
            "version": version,
            "downloads_list": downloads_list,
            "status": "Completed" if item.get('status') == '1' else "Active",
            "playable": "Yes"
        }

        if raw_id in existing_ids:
            # Atualiza projeto existente se necessario
            for i, p in enumerate(projects_list):
                if p.get('id') == raw_id:
                    # Manter customizacoes se for Wolff / MeninoSung
                    if p.get('responsibles') in ['Wolff', 'MeninoSung']:
                        pass
                    else:
                        projects_list[i] = proj_obj
                        updated_count += 1
                    break
        else:
            projects_list.append(proj_obj)
            existing_ids.add(raw_id)
            added_count += 1

    print(f"--> Processamento concluído: {added_count} novos projetos adicionados, {updated_count} atualizados.")
    print(f"--> Total de projetos no VitARCH: {len(projects_list)}")

    # Salvar em api/catalog.json
    with open(CATALOG_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({"projects": projects_list}, f, indent=4, ensure_ascii=False)
    print(f"--> Gravado em {CATALOG_JSON_PATH}")

    # Salvar em js/catalog_data.js
    js_content = "window.catalogFallbackData = " + json.dumps(projects_list, indent=4, ensure_ascii=False) + ";\n"
    with open(CATALOG_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"--> Gravado em {CATALOG_JS_PATH}")

if __name__ == "__main__":
    sync_vitadb()
