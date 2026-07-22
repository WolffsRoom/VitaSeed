import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

migrate_old = """    if (url.pathname === "/api/migrate") {
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
    }"""

migrate_new = """    if (url.pathname === "/api/migrate") {
      try {
        if (!env.DB) throw new Error("env.DB is not bound!");
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
      } catch (err) {
        return new Response("Erro na migracao: " + err.message + " - Stack: " + err.stack, { status: 500, headers: corsHeaders });
      }
    }"""

worker = worker.replace(migrate_old, migrate_new)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Updated migrate endpoint with try-catch")
