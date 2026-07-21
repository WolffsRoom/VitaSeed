const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE",
  "Access-Control-Allow-Headers": "Content-Type, Authorization"
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

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
    const payloadBase64 = token.split('.')[1];
    const payloadDecoded = JSON.parse(atob(payloadBase64.replace(/-/g, '+').replace(/_/g, '/')));
    
    if (!payloadDecoded.email) return null;
    
    if (env.DB) {
      let user = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(payloadDecoded.email).first();
      if (!user) {
        // Criação automática no primeiro login
        await env.DB.prepare(
          "INSERT INTO users (email, display_name, avatar_url, role) VALUES (?, ?, ?, 'viteiro')"
        ).bind(payloadDecoded.email, payloadDecoded.name || "Viteiro", payloadDecoded.picture || "").run();
        user = { email: payloadDecoded.email, role: 'viteiro', display_name: payloadDecoded.name, avatar_url: payloadDecoded.picture };
      }
      return user;
    }
  } catch (e) {
    console.error("Token decoding failed", e);
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
