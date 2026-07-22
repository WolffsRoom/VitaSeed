import glob
import re

# 1. Add #menu-admin-panel to all HTML files with a profile menu
for file in glob.glob('*.html'):
    if file == 'admin.html':
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'id="menu-admin-panel"' not in html and 'profile-menu' in html:
        old_str = '<a href="settings.html" data-i18n="profile_settings">'
        new_str = '<a href="admin.html" id="menu-admin-panel" class="hidden"><i class="fa-solid fa-lock"></i> Painel Admin</a>\n                            <a href="settings.html" data-i18n="profile_settings">'
        html = html.replace(old_str, new_str)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html)

# 2. Update auth.js to reveal it
with open('js/auth.js', 'r', encoding='utf-8') as f:
    auth_js = f.read()

auth_replace = """if(menuName) menuName.innerText = user.displayName || 'Viteiro';
            if(menuEmail) menuEmail.innerText = user.email || '';
            
            const adminPanelBtn = container.querySelector('#menu-admin-panel');
            if (adminPanelBtn && (user.email === 'gabrielfwchaves@gmail.com' || window.isAdmin)) {
                adminPanelBtn.classList.remove('hidden');
            }"""

if 'menu-admin-panel' not in auth_js:
    auth_js = auth_js.replace("if(menuName) menuName.innerText = user.displayName || 'Viteiro';\n            if(menuEmail) menuEmail.innerText = user.email || '';", auth_replace)
    with open('js/auth.js', 'w', encoding='utf-8') as f:
        f.write(auth_js)

# 3. Update admin.html to automatically bypass login screen
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

admin_auth_logic = """
        auth.onAuthStateChanged(async (user) => {
            if (user && user.email === 'gabrielfwchaves@gmail.com') {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('dashboard-screen').classList.remove('hidden');
                const token = "Bearer " + await user.getIdToken();
                fetchRequests(token);
            } else {
                document.getElementById('dashboard-screen').classList.add('hidden');
                document.getElementById('login-screen').classList.remove('hidden');
            }
        });
"""

if 'auth.onAuthStateChanged' not in admin:
    admin = admin.replace('async function fetchRequests(tokenParam) {', admin_auth_logic + '\n        async function fetchRequests(tokenParam) {')
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(admin)

print("Updates completed.")
