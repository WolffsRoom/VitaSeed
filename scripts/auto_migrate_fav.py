import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

getuser_old = """      if (env.DB) {
        let user = null;
        try {
            user = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(payloadDecoded.email).first();
        } catch (dbErr) {
            // Se a tabela não existe, cria ela dinamicamente
            if (dbErr.message.includes('no such table')) {
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
            } else {
                throw dbErr;
            }
        }"""

getuser_new = """      if (env.DB) {
        let user = null;
        try {
            user = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(payloadDecoded.email).first();
        } catch (dbErr) {
            // Se a tabela não existe, cria ela dinamicamente
            if (dbErr.message.includes('no such table')) {
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
                await env.DB.prepare(`CREATE TABLE IF NOT EXISTS favorites (
                    user_email TEXT,
                    post_id TEXT,
                    PRIMARY KEY(user_email, post_id)
                )`).run();
            } else {
                throw dbErr;
            }
        }"""

worker = worker.replace(getuser_old, getuser_new)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Added auto-migration for favorites table in getUser")
