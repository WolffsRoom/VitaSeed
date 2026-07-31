import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

getprofile_old = """    if (env.DB) {
      const { results } = await env.DB.prepare("SELECT post_id FROM favorites WHERE user_email = ?").bind(user.email).all();
      user.favorites = results.map(r => r.post_id);
    }"""

getprofile_new = """    if (env.DB) {
      try {
        const { results } = await env.DB.prepare("SELECT post_id FROM favorites WHERE user_email = ?").bind(user.email).all();
        user.favorites = results.map(r => r.post_id);
      } catch(e) {
        if (e.message.includes('no such table')) {
            await env.DB.prepare(`CREATE TABLE IF NOT EXISTS favorites (user_email TEXT, post_id TEXT, PRIMARY KEY(user_email, post_id))`).run();
            user.favorites = [];
        } else {
            console.error(e);
            user.favorites = [];
        }
      }
    }"""

handlefav_old = """    // Check if exists
    const exists = await env.DB.prepare("SELECT * FROM favorites WHERE user_email = ? AND post_id = ?").bind(user.email, postId).first();
    
    if (exists) {
      await env.DB.prepare("DELETE FROM favorites WHERE user_email = ? AND post_id = ?").bind(user.email, postId).run();
      return new Response(JSON.stringify({ status: "removed" }), { status: 200, headers: corsHeaders });
    } else {
      await env.DB.prepare("INSERT INTO favorites (user_email, post_id) VALUES (?, ?)").bind(user.email, postId).run();
      return new Response(JSON.stringify({ status: "added" }), { status: 200, headers: corsHeaders });
    }"""

handlefav_new = """    // Check if exists
    let exists = false;
    try {
        exists = await env.DB.prepare("SELECT * FROM favorites WHERE user_email = ? AND post_id = ?").bind(user.email, postId).first();
    } catch(e) {
        if (e.message.includes('no such table')) {
            await env.DB.prepare(`CREATE TABLE IF NOT EXISTS favorites (user_email TEXT, post_id TEXT, PRIMARY KEY(user_email, post_id))`).run();
        } else {
            throw e;
        }
    }
    
    if (exists) {
      await env.DB.prepare("DELETE FROM favorites WHERE user_email = ? AND post_id = ?").bind(user.email, postId).run();
      return new Response(JSON.stringify({ status: "removed" }), { status: 200, headers: corsHeaders });
    } else {
      await env.DB.prepare("INSERT INTO favorites (user_email, post_id) VALUES (?, ?)").bind(user.email, postId).run();
      return new Response(JSON.stringify({ status: "added" }), { status: 200, headers: corsHeaders });
    }"""

worker = worker.replace(getprofile_old, getprofile_new).replace(handlefav_old, handlefav_new)

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Safeguarded all favorites queries with auto-migration")
