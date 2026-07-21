import glob
import re

for file in glob.glob('*.html'):
    if file == 'admin.html':
        # Add to admin login screen
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'Entrar com GitHub (Conta Admin)' not in content:
            github_btn = """
        <button class="btn-secondary" onclick="loginWithGitHubAdmin()" style="width: 100%; justify-content: center; padding: 0.8rem; font-size: 1rem; background: #24292e; color: white; border-color: #24292e; margin-top: 0.5rem;">
            <i class="fa-brands fa-github" style="font-size: 1.2rem; margin-right: 0.5rem;"></i>
            Entrar com GitHub (Conta Admin)
        </button>"""
            content = content.replace('Entrar com Google (Conta Admin)\n        </button>', 'Entrar com Google (Conta Admin)\n        </button>' + github_btn)
            
            # Add function to admin.html
            github_func = """
        async function loginWithGitHubAdmin() {
            if (!auth) return;
            try {
                const res = await auth.signInWithPopup(githubProvider);
                const token = "Bearer " + await res.user.getIdToken();
                authKey = token;
                await fetchRequests(token);
            } catch (error) {
                document.getElementById('login-err').innerText = "Erro ao fazer login com GitHub.";
            }
        }
"""
            content = content.replace('async function loginWithGoogleAdmin() {', github_func + '\n        async function loginWithGoogleAdmin() {')
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Entrar com GitHub' not in content:
        github_btn = """
            <button class="btn-secondary" onclick="loginWithGitHub()" style="width: 100%; justify-content: center; padding: 0.8rem; font-size: 1rem; background: #24292e; color: white; border-color: #24292e; margin-top: 0.5rem;">
                <i class="fa-brands fa-github" style="font-size: 1.2rem; margin-right: 0.5rem;"></i>
                Entrar com GitHub
            </button>"""
        content = content.replace('Entrar com Google\n            </button>', 'Entrar com Google\n            </button>' + github_btn)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("GitHub login added to HTML files.")
