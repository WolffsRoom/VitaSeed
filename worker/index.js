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
        if (!(await checkAuth(request, env))) return unauthorized();
        return await handleGetRequests(env);
      }

      // 3. Admin: Resolve/Delete Request
      if (url.pathname.startsWith("/api/admin/requests/") && request.method === "DELETE") {
        if (!(await checkAuth(request, env))) return unauthorized();
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

async function checkAuth(request, env) {
  const authHeader = request.headers.get("Authorization") || "";
  
  // Fallback para senha antiga enquanto o Firebase não estiver configurado
  const expectedPassword = env.ADMIN_PASSWORD || "admin123";
  if (authHeader === expectedPassword) return true;

  if (authHeader.startsWith("Bearer ")) {
    try {
      const token = authHeader.split(" ")[1];
      const payloadBase64 = token.split('.')[1];
      const payloadDecoded = JSON.parse(atob(payloadBase64.replace(/-/g, '+').replace(/_/g, '/')));
      const userEmail = payloadDecoded.email;
      
      if (!userEmail) return false;
      
      // Checar banco de dados para a role
      if (env.DB) {
        const user = await env.DB.prepare("SELECT role FROM users WHERE email = ?").bind(userEmail).first();
        if (user && user.role === 'admin') {
          return true;
        }
      }
    } catch (e) {
      console.error("Auth check failed", e);
    }
  }
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
  const authHeader = request.headers.get("Authorization") || "";
  let userName = "Anônimo";
  let userEmail = "";
  let userId = "";

  if (authHeader.startsWith("Bearer ")) {
    try {
      const token = authHeader.split(" ")[1];
      // Basic JWT Decode (Assuming token is validly formatted Firebase JWT)
      // For production security, signature should be verified with Google Public Keys.
      const payloadBase64 = token.split('.')[1];
      const payloadDecoded = JSON.parse(atob(payloadBase64.replace(/-/g, '+').replace(/_/g, '/')));
      userName = payloadDecoded.name || "Usuário do Google";
      userEmail = payloadDecoded.email || "";
      userId = payloadDecoded.user_id || payloadDecoded.sub || "";
    } catch (e) {
      console.error("Token decoding failed", e);
    }
  }

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
