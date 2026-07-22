import re

with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Add stats cards and search bar to admin header
header_old = """    <!-- Main Content -->
    <main style="padding-top: 3rem;">
        <div id="dashboard-screen" class="hidden">
            <div class="admin-container">
                <div class="admin-header">
                    <h2><i class="fa-solid fa-shield-halved"></i> Painel de Moderaǜo</h2>
                </div>"""

header_new = """    <!-- Main Content -->
    <main style="padding-top: 3rem;">
        <div id="dashboard-screen" class="hidden">
            <div class="admin-container" style="max-width: 1200px;">
                <div class="admin-header" style="flex-wrap: wrap; gap: 1rem;">
                    <h2><i class="fa-solid fa-shield-halved"></i> Painel de Administração</h2>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <input type="text" id="admin-search" placeholder="Buscar..." class="search-bar" style="width: 250px;" onkeyup="filterAdminTable()">
                        <button class="btn-secondary" onclick="fetchRequests(null)"><i class="fa-solid fa-rotate-right"></i> Atualizar</button>
                    </div>
                </div>
                
                <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
                    <div class="card" style="flex: 1; padding: 1.5rem; text-align: center;">
                        <i class="fa-solid fa-envelope-open-text" style="font-size: 2rem; color: var(--accent-green); margin-bottom: 0.5rem;"></i>
                        <h3 style="font-size: 1rem; color: var(--text-muted);">Total de Pedidos</h3>
                        <div id="stat-total" style="font-size: 2rem; font-weight: bold; margin-top: 0.5rem;">0</div>
                    </div>
                    <div class="card" style="flex: 1; padding: 1.5rem; text-align: center;">
                        <i class="fa-solid fa-clock-rotate-left" style="font-size: 2rem; color: var(--tag-port); margin-bottom: 0.5rem;"></i>
                        <h3 style="font-size: 1rem; color: var(--text-muted);">Aguardando Análise</h3>
                        <div id="stat-pending" style="font-size: 2rem; font-weight: bold; margin-top: 0.5rem;">0</div>
                    </div>
                    <div class="card" style="flex: 1; padding: 1.5rem; text-align: center;">
                        <i class="fa-solid fa-check-circle" style="font-size: 2rem; color: var(--text-muted); margin-bottom: 0.5rem;"></i>
                        <h3 style="font-size: 1rem; color: var(--text-muted);">Resolvidos (Hoje)</h3>
                        <div id="stat-resolved" style="font-size: 2rem; font-weight: bold; margin-top: 0.5rem;">0</div>
                    </div>
                </div>"""

admin = admin.replace(header_old, header_new)

# Add filter table logic and update stats inside fetchRequests
render_old = """            document.getElementById('empty-msg').classList.add('hidden');

            requests.forEach(req => {"""

render_new = """            document.getElementById('empty-msg').classList.add('hidden');
            
            document.getElementById('stat-total').innerText = requests.length;
            document.getElementById('stat-pending').innerText = requests.length;

            requests.forEach(req => {"""

admin = admin.replace(render_old, render_new)

filter_logic = """
        function filterAdminTable() {
            const input = document.getElementById("admin-search").value.toLowerCase();
            const rows = document.querySelectorAll("#requests-tbody tr");
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(input) ? "" : "none";
            });
        }
"""
admin = admin.replace('function logout() {', filter_logic + '\n        function logout() {')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("Admin screen improved with stats and search")
