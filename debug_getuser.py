import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

getuser_old = """  async function getUser(request, env) {
    const authHeader = request.headers.get("Authorization") || "";
    if (!authHeader.startsWith("Bearer ")) return null;
    
    try {
      const token = authHeader.split(" ")[1];
      let payloadBase64 = token.split('.')[1];
      payloadBase64 = payloadBase64.replace(/-/g, '+').replace(/_/g, '/');
      while (payloadBase64.length % 4) { payloadBase64 += '='; }
      const payloadDecoded = JSON.parse(atob(payloadBase64));
      
      if (!payloadDecoded.email) return null;
      
      if (env.DB) {
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
        }

        if (!user) {
          // Criação automática no primeiro login
          await env.DB.prepare(
            "INSERT INTO users (email, display_name, avatar_url, role) VALUES (?, ?, ?, 'viteiro')"
          ).bind(payloadDecoded.email, payloadDecoded.name || "Viteiro", payloadDecoded.picture || "").run();
          user = { email: payloadDecoded.email, role: 'viteiro', display_name: payloadDecoded.name, avatar_url: payloadDecoded.picture };
        }
        
          if (user.email.toLowerCase() === 'gabrielfwchaves@gmail.com' && user.role !== 'admin') {
              await env.DB.prepare("UPDATE users SET role = 'admin' WHERE email = ?").bind(user.email).run();
              user.role = 'admin';
          }
  
          return user;
      } else {
          return { is_error: true, message: "env.DB undefined" };
      }
    } catch (e) {
      return { is_error: true, message: e.message };
    }
  }"""

# I need to be careful with replace since I changed toLowerCase() above. Let's just do a manual regex block replace
worker = re.sub(r'async function getUser\(request, env\) \{.*?\n  \}', getuser_old, worker, flags=re.DOTALL)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Updated getUser to return debug info")
