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
      // 1. Submit Request (Public)
      if (url.pathname === "/api/request" && request.method === "POST") {
        return await handleNewRequest(request, env);
      }
      
      // 2. Admin: List Requests
      if (url.pathname === "/api/admin/requests" && request.method === "GET") {
        if (!checkAuth(request, env)) return unauthorized();
        return await handleGetRequests(env);
      }

      // 3. Admin: Resolve/Delete Request
      if (url.pathname.startsWith("/api/admin/requests/") && request.method === "DELETE") {
        if (!checkAuth(request, env)) return unauthorized();
        const id = url.pathname.split("/").pop();
        return await handleResolveRequest(id, env);
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

function checkAuth(request, env) {
  const authHeader = request.headers.get("Authorization");
  const expectedPassword = env.ADMIN_PASSWORD || "admin123"; // Fallback apenas para teste
  return authHeader === expectedPassword;
}

function unauthorized() {
  return new Response(JSON.stringify({ error: "Não autorizado" }), {
    status: 401,
    headers: { ...corsHeaders, "Content-Type": "application/json" }
  });
}

async function handleNewRequest(request, env) {
  const body = await request.json();
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";

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
      "INSERT INTO requests (title, link, description, ip_address) VALUES (?, ?, ?, ?)"
    ).bind(body.title, body.link, body.desc, ip).run();
  }

  // GitHub Integration (Optional)
  if (env.GITHUB_TOKEN && env.GITHUB_REPO) {
    const issueBody = `**Project Link:** ${body.link}\n**Reason:** ${body.desc}\n\n*Requested via VitaSeed Web Form*`;
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
