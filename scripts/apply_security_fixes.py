import re

with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add meta tag for CSP
if 'upgrade-insecure-requests' not in html:
    html = html.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">')

# Add escapeHTML function
escape_func = """
        function escapeHTML(str) {
            if (!str) return '';
            return str.toString()
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }
"""
if 'function escapeHTML' not in html:
    html = html.replace('<script>', '<script>\n' + escape_func)

# Remove authKey global var
html = re.sub(r'let authKey = "".*?;\n', '', html)

# Modify loginWithGitHubAdmin
html = html.replace("""const res = await auth.signInWithPopup(githubProvider);
                const token = "Bearer " + await res.user.getIdToken();
                authKey = token;
                await fetchRequests(token);""", """const res = await auth.signInWithPopup(githubProvider);
                const token = "Bearer " + await res.user.getIdToken();
                await fetchRequests(token);""")

# Modify loginWithGoogleAdmin
html = html.replace("""const res = await auth.signInWithPopup(googleProvider);
                const token = "Bearer " + await res.user.getIdToken();
                authKey = token;
                await fetchRequests(token);""", """const res = await auth.signInWithPopup(googleProvider);
                const token = "Bearer " + await res.user.getIdToken();
                await fetchRequests(token);""")

# Remove legacy login function block entirely or just modify it
# Actually, the user approved removing legacy login if needed, let's just make it throw an alert
html = re.sub(r'async function login\(\) \{.*?\n\s+\}', 'async function login() {\n            alert("Login por senha desativado. Use Google ou GitHub.");\n        }', html, flags=re.DOTALL)

# Update logout function to call auth.signOut()
html = re.sub(r'function logout\(\) \{.*?authKey = "";', 'function logout() {\n            if (window.auth) auth.signOut();', html, flags=re.DOTALL)

# Update fetchRequests to not rely on global authKey if not provided, but actually fetchRequests receives the token as argument OR fetches it
fetch_req_replacement = """async function fetchRequests(tokenParam) {
            let token = tokenParam;
            if (!token && auth.currentUser) {
                token = "Bearer " + await auth.currentUser.getIdToken();
            }
            if (!token) {
                alert("Sessão inválida. Faça login novamente.");
                logout();
                return;
            }"""
html = re.sub(r'async function fetchRequests\(token\) \{', fetch_req_replacement, html)

# Update the rendering logic to use escapeHTML
old_tr_inner = """<td style="font-weight:bold; color:var(--text-main);">${req.title}<br><span style="font-size:0.8rem; font-weight:normal; color:var(--text-muted);"><i class="fa-solid fa-user"></i> ${req.user_name || 'Anônimo'}</span></td>
                    <td style="color:var(--text-muted); font-size:0.9rem; max-width: 300px;">${req.description || '-'}</td>
                    <td>${req.link ? `<a href="${req.link}" target="_blank" style="color:var(--accent-green); text-decoration:none;"><i class="fa-solid fa-link"></i> Abrir Link</a>` : '-'}</td>"""

new_tr_inner = """<td style="font-weight:bold; color:var(--text-main);">${escapeHTML(req.title)}<br><span style="font-size:0.8rem; font-weight:normal; color:var(--text-muted);"><i class="fa-solid fa-user"></i> ${escapeHTML(req.user_name) || 'Anônimo'}</span></td>
                    <td style="color:var(--text-muted); font-size:0.9rem; max-width: 300px;">${escapeHTML(req.description) || '-'}</td>
                    <td>${req.link ? `<a href="${escapeHTML(req.link)}" target="_blank" style="color:var(--accent-green); text-decoration:none;"><i class="fa-solid fa-link"></i> Abrir Link</a>` : '-'}</td>"""

html = html.replace(old_tr_inner, new_tr_inner)

# Update resolveRequest
resolve_old = """async function resolveRequest(id) {
            if (API_URL.includes("seunome")) {
                alert("Simulação: item marcado como resolvido e deletado do banco!");
                await fetchRequests(authKey); // mock refresh
                return;
            }

            if(confirm("Marcar esta requisição como resolvida?")) {
                try {
                    await fetch(`${API_URL}/api/admin/requests/${id}`, {
                        method: "DELETE",
                        headers: { "Authorization": authKey }
                    });
                    fetchRequests(authKey); // Recarrega a tabela"""

resolve_new = """async function resolveRequest(id) {
            let token = null;
            if (auth.currentUser) token = "Bearer " + await auth.currentUser.getIdToken();
            
            if (API_URL.includes("seunome")) {
                alert("Simulação: item marcado como resolvido e deletado do banco!");
                if(token) await fetchRequests(token); // mock refresh
                return;
            }

            if(confirm("Marcar esta requisição como resolvida?")) {
                try {
                    await fetch(`${API_URL}/api/admin/requests/${id}`, {
                        method: "DELETE",
                        headers: { "Authorization": token }
                    });
                    if(token) fetchRequests(token); // Recarrega a tabela"""

html = html.replace(resolve_old, resolve_new)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied security fixes to admin.html")
