import re
import glob
import os

# 1. Merge api.js into main.js
with open('js/api.js', 'r', encoding='utf-8') as f:
    api_code = f.read()

with open('js/main.js', 'r', encoding='utf-8') as f:
    main_code = f.read()

if 'window.fetchCatalog = async function' not in main_code:
    main_code = api_code + '\n\n' + main_code
    with open('js/main.js', 'w', encoding='utf-8') as f:
        f.write(main_code)

# 2. Remove api.js from all HTML files
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = re.sub(r'<script src="js/api\.js[^"]*"></script>\n?', '', html)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# Delete api.js so it's gone for good
if os.path.exists('js/api.js'):
    os.remove('js/api.js')

# 3. Add migration endpoint to worker
with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

migration_code = """
      if (url.pathname === "/api/migrate") {
        await env.DB.prepare("DROP TABLE IF EXISTS users").run();
        await env.DB.prepare(`CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            role TEXT DEFAULT 'viteiro',
            display_name TEXT,
            avatar_url TEXT,
            languages TEXT,
            website TEXT,
            donation_links TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )`).run();
        return new Response("Migracao concluida com sucesso! Banco de dados atualizado.", { headers: corsHeaders });
      }
"""
if '/api/migrate' not in worker:
    worker = worker.replace('if (request.method === "OPTIONS") {', migration_code + '\n    if (request.method === "OPTIONS") {')
    with open('worker/index.js', 'w', encoding='utf-8') as f:
        f.write(worker)

print("Merged api.js into main.js and added migration endpoint!")
