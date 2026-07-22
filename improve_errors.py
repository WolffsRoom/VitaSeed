import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

# Change getUser to attach the error string if it fails
worker = worker.replace('} catch (e) {\n      console.error("Token decoding failed", e);\n    }\n    return null;', '} catch (e) {\n      console.error("Token decoding failed", e);\n      return { is_error: true, message: e.message };\n    }\n    return null;')

# Change unauthorized to accept a message
worker = worker.replace('function unauthorized() {\n    return new Response(JSON.stringify({ error: "Acesso negado. Apenas administradores." }), {', 'function unauthorized(msg) {\n    return new Response(JSON.stringify({ error: msg || "Acesso negado." }), {')

# Update handleGetProfile to use it
worker = worker.replace('async function handleGetProfile(request, env) {\n  const user = await getUser(request, env);\n  if (!user) return unauthorized();', 'async function handleGetProfile(request, env) {\n  const user = await getUser(request, env);\n  if (!user) return unauthorized();\n  if (user.is_error) return unauthorized("Auth Error: " + user.message);')

# Update handleUpdateProfile to use it
worker = worker.replace('async function handleUpdateProfile(request, env) {\n    const user = await getUser(request, env);\n    if (!user) return unauthorized();', 'async function handleUpdateProfile(request, env) {\n    const user = await getUser(request, env);\n    if (!user) return unauthorized();\n    if (user.is_error) return unauthorized("Auth Error: " + user.message);')

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Worker error handling improved.")
