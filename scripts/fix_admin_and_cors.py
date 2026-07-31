import re

# 1. Fix worker CORS
with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

worker = worker.replace('"Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE"', '"Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE, PUT"')
with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)


# 2. Fix admin.html
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Fix the broken fetchRequests function
broken_str = """        function logout() {
            authKey = "";
            document.getElementById('dashboard-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
            document.getElementById('admin-pass').value = '';
        }

            
            try {
                const res = await fetch(`${API_URL}/api/admin/requests`, {"""

fixed_str = """        function logout() {
            authKey = "";
            document.getElementById('dashboard-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
            document.getElementById('admin-pass').value = '';
        }

        async function fetchRequests(token) {
            try {
                const res = await fetch(`${API_URL}/api/admin/requests`, {"""

admin = admin.replace(broken_str, fixed_str)

# Change the API_URL to the real one
admin = admin.replace('"https://vitaseed-api.seunome.workers.dev"', '"https://vitaseed-api.9h9rnjjcrf.workers.dev"')

# Fix login() calling loadRequests
admin = admin.replace('await loadRequests();', 'await fetchRequests(authKey);')
admin = admin.replace('loadRequests(); // Recarrega a tabela', 'fetchRequests(authKey); // Recarrega a tabela')
admin = admin.replace('await loadRequests(); // mock refresh', 'await fetchRequests(authKey); // mock refresh')

# Remove duplicate authKey variable logic if any, but above replaces are enough.
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("Worker and admin.html fixed!")
