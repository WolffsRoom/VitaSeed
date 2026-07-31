import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

getuser_old = """      if (env.DB) {
        let user = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(payloadDecoded.email).first();
        if (!user) {
          // Criação automática no primeiro login
          await env.DB.prepare(
            "INSERT INTO users (email, display_name, avatar_url, role) VALUES (?, ?, ?, 'viteiro')"
          ).bind(payloadDecoded.email, payloadDecoded.name || "Viteiro", payloadDecoded.picture || "").run();
          user = { email: payloadDecoded.email, role: 'viteiro', display_name: payloadDecoded.name, avatar_url: payloadDecoded.picture };
        }
        
          if (user.email === 'gabrielfwchaves@gmail.com' && user.role !== 'admin') {
              await env.DB.prepare("UPDATE users SET role = 'admin' WHERE email = ?").bind(user.email).run();
              user.role = 'admin';
          }
  
          return user;
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
            } else {
                throw dbErr;
            }
        }

        if (!user) {
          // Criação automática no primeiro login
          await env.DB.prepare(
            "INSERT INTO users (email, display_name, avatar_url, role) VALUES (?, ?, ?, 'viteiro')"
          ).bind(payloadDecoded.email, payloadDecoded.name || "Viteiro", payloadDecoded.picture || "").run();
          user = { email: payloadDecoded.email, role: 'viteiro', display_name: payloadDecoded.name, avatar_url: payloadDecoded.picture };
        }
        
          if (user.email === 'gabrielfwchaves@gmail.com' && user.role !== 'admin') {
              await env.DB.prepare("UPDATE users SET role = 'admin' WHERE email = ?").bind(user.email).run();
              user.role = 'admin';
          }
  
          return user;
      }"""

worker = worker.replace(getuser_old, getuser_new)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Added auto-migration logic to getUser")
