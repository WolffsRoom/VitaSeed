import re

# 1. Add API_URL to top of auth.js
with open('js/auth.js', 'r', encoding='utf-8') as f:
    auth = f.read()
if 'const API_URL' not in auth:
    auth = 'const API_URL = "https://vitaseed-api.9h9rnjjcrf.workers.dev";\n' + auth
    with open('js/auth.js', 'w', encoding='utf-8') as f:
        f.write(auth)

# 2. Remove API_URL from main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main = f.read()
main = re.sub(r'const API_URL = "[^"]+";\s*(//.*)?\n', '', main)
with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main)

# 3. Remove API_URL from admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()
admin = re.sub(r'const API_URL = window\.location\.hostname.*?;// <-- MUDAR PARA SEU LINK REAL\n', '', admin, flags=re.DOTALL)
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("API_URL refactored to auth.js globally.")
