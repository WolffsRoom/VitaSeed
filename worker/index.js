const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE, PUT",
  "Access-Control-Allow-Headers": "Content-Type, Authorization"
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    if (url.pathname === "/api/migrate") {
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
    }

    try {
      // 1. Submit Request
      if (url.pathname === "/api/request" && request.method === "POST") {
        return await handleNewRequest(request, env);
      }
      
      // 2. User Profile (GET/PUT)
      if (url.pathname === "/api/user/profile") {
        if (request.method === "GET") return await handleGetProfile(request, env);
        if (request.method === "PUT") return await handleUpdateProfile(request, env);
      }
      
      // 2.5 Favorites
      if (url.pathname === "/api/user/favorites" && request.method === "POST") {
        return await handleFavorites(request, env);
      }
      
      // 3. Admin: List Requests
      if (url.pathname === "/api/admin/requests" && request.method === "GET") {
        if (!(await checkAuth(request, env))) return unauthorized();
        return await handleGetRequests(env);
      }

      // 4. Admin: Resolve Request (DELETE)
      if (url.pathname.startsWith("/api/admin/requests/") && request.method === "DELETE") {
        if (!(await checkAuth(request, env))) return unauthorized();
        const id = url.pathname.split("/").pop();
        return await handleResolveRequest(id, env);
      }
      
      // 5. Admin: Publish Request to Catalog (POST)
      if (url.pathname === "/api/admin/publish" && request.method === "POST") {
        if (!(await checkAuth(request, env))) return unauthorized();
        return await handlePublishRequest(request, env);
      }

      return new Response("Not found", { status: 404, headers: corsHeaders });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }
  }
};

async function getUser(request, env) {
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
            return { is_error: true, message: dbErr.message };
        }
      }

      if (!user) {
        await env.DB.prepare(
          "INSERT INTO users (email, display_name, avatar_url, role) VALUES (?, ?, ?, 'viteiro')"
        ).bind(payloadDecoded.email, payloadDecoded.name || "Viteiro", payloadDecoded.picture || "").run();
        user = { email: payloadDecoded.email, role: 'viteiro', display_name: payloadDecoded.name, avatar_url: payloadDecoded.picture };
      }
      
      if (user.email.toLowerCase().trim() === 'gabrielfwchaves@gmail.com' && user.role !== 'admin') {
          await env.DB.prepare("UPDATE users SET role = 'admin' WHERE email = ?").bind(user.email).run();
          user.role = 'admin';
      }

      return user;
    } else {
      return { is_error: true, message: "env.DB is missing" };
    }
  } catch (e) {
    return { is_error: true, message: e.message };
  }
  return null;
}

async function checkAuth(request, env) {
  const authHeader = request.headers.get("Authorization") || "";
  const expectedPassword = env.ADMIN_PASSWORD || "admin123";
  if (authHeader === expectedPassword) return true;

  const user = await getUser(request, env);
  if (user && user.role === 'admin') return true;
  
  return false;
}

function unauthorized() {
  return new Response(JSON.stringify({ error: "Acesso negado. Apenas administradores." }), {
    status: 401,
    headers: { ...corsHeaders, "Content-Type": "application/json" }
  });
}

async function handleNewRequest(request, env) {
  const body = await request.json();
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  
  const user = await getUser(request, env);
  
  if (!user || (user.role !== 'admin' && user.role !== 'dev')) {
    return new Response(JSON.stringify({ error: "Apenas Desenvolvedores e Administradores podem fazer Requests." }), {
      status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" }
    });
  }

  let userName = user.display_name || user.email.split('@')[0];
  let userEmail = user.email;
  let userId = user.email;

  // Rate Limiting super simples (se houver RATE_LIMIT configurado)
  if (env.RATE_LIMIT) {
    const today = new Date().toISOString().split('T')[0];
    const key = `req_${ip}_${today}`;
    const count = parseInt(await env.RATE_LIMIT.get(key) || '0');
    if (count >= 2) {
      return new Response(JSON.stringify({ error: "Limite diário atingido." }), {
        status: 429, headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }
    await env.RATE_LIMIT.put(key, (count + 1).toString(), { expirationTtl: 86400 });
  }

  // Insert into DB
  if (env.DB) {
    await env.DB.prepare(
      "INSERT INTO requests (title, link, description, ip_address, user_id, user_name, user_email) VALUES (?, ?, ?, ?, ?, ?, ?)"
    ).bind(body.title, body.link, body.desc, ip, userId, userName, userEmail).run();
  }

  // GitHub Integration (Optional)
  if (env.GITHUB_TOKEN && env.GITHUB_REPO) {
    const issueBody = `**Project Link:** ${body.link}\n**Reason:** ${body.desc}\n\n*Requested by ${userName} (${userEmail}) via VitaSeed Web Form*`;
    await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}/issues`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
        "User-Agent": "VitaSeed-Worker",
        "Accept": "application/vnd.github.v3+json"
      },
      body: JSON.stringify({
        title: `[Request] ${body.title}`,
        body: issueBody,
        labels: ["request"]
      })
    });
  }

  return new Response(JSON.stringify({ ok: true, msg: "Request enviado com sucesso!" }), {
    status: 200,
    headers: { ...corsHeaders, "Content-Type": "application/json" }
  });
}

async function handleGetRequests(env) {
  if (!env.DB) return new Response(JSON.stringify({ error: "Database not configured" }), { status: 500, headers: corsHeaders });
  
  const { results } = await env.DB.prepare("SELECT * FROM requests WHERE status = 'pending' ORDER BY created_at DESC").all();
  
  return new Response(JSON.stringify(results), {
    status: 200,
    headers: { ...corsHeaders, "Content-Type": "application/json" }
  });
}

async function handleResolveRequest(id, env) {
  if (!env.DB) return new Response(JSON.stringify({ error: "Database not configured" }), { status: 500, headers: corsHeaders });
  
  await env.DB.prepare("UPDATE requests SET status = 'resolved' WHERE id = ?").bind(id).run();
  
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { ...corsHeaders, "Content-Type": "application/json" }
  });
}

// User Profile Endpoints
async function handleGetProfile(request, env) {
  const user = await getUser(request, env);
  if (!user) return unauthorized();
  if (user.is_error) return unauthorized("Auth Error: " + user.message);
  
  if (env.DB) {
    const { results } = await env.DB.prepare("SELECT post_id FROM favorites WHERE user_email = ?").bind(user.email).all();
    user.favorites = results.map(r => r.post_id);
  }
  
  return new Response(JSON.stringify(user), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
}

async function handleUpdateProfile(request, env) {
  const user = await getUser(request, env);
  if (!user) return unauthorized();
  
  const body = await request.json();
  
  if (env.DB) {
    await env.DB.prepare(
      "UPDATE users SET display_name = ?, avatar_url = ?, languages = ?, website = ?, donation_links = ? WHERE email = ?"
    ).bind(
      body.display_name || user.display_name,
      body.avatar_url || user.avatar_url,
      body.languages || user.languages,
      body.website || user.website,
      body.donation_links || user.donation_links,
      user.email
    ).run();
  }
  
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
}

// Publish Endpoint
async function handlePublishRequest(request, env) {
  const body = await request.json();
  // Here we would typically insert into a `posts` table or trigger a GitHub Action to update catalog.json
  // For now, we mock the publish and mark the request as resolved.
  
  if (env.DB && body.request_id) {
    await env.DB.prepare("UPDATE requests SET status = 'published' WHERE id = ?").bind(body.request_id).run();
  }

  // TODO: Trigger GitHub workflow to write body.postData to catalog.json if needed.
  return new Response(JSON.stringify({ ok: true, msg: "Publicado com sucesso!" }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
}

async function handleFavorites(request, env) {
  const user = await getUser(request, env);
  if (!user) return unauthorized();
  
  const body = await request.json();
  const postId = body.post_id;
  
  if (!env.DB || !postId) return new Response(JSON.stringify({ error: "Missing data" }), { status: 400, headers: corsHeaders });
  
  // Check if exists
  const exists = await env.DB.prepare("SELECT * FROM favorites WHERE user_email = ? AND post_id = ?").bind(user.email, postId).first();
  
  if (exists) {
    await env.DB.prepare("DELETE FROM favorites WHERE user_email = ? AND post_id = ?").bind(user.email, postId).run();
    return new Response(JSON.stringify({ status: "removed" }), { status: 200, headers: corsHeaders });
  } else {
    await env.DB.prepare("INSERT INTO favorites (user_email, post_id) VALUES (?, ?)").bind(user.email, postId).run();
    return new Response(JSON.stringify({ status: "added" }), { status: 200, headers: corsHeaders });
  }
}
