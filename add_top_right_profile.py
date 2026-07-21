import glob

for file in glob.glob('*.html'):
    if file == 'admin.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <div class="content-wrapper">
    if '<div class="content-wrapper">' in content and 'id="top-right-profile"' not in content:
        top_bar = """<div class="content-wrapper">
        <!-- Top Right Auth Bar -->
        <div id="top-right-profile" style="position: absolute; top: 1.5rem; right: 2rem; display: flex; align-items: center; gap: 1rem; z-index: 100;">
            <button id="tr-login-btn" class="btn-secondary" onclick="document.getElementById('modal-login').classList.add('show')" style="padding: 0.4rem 1rem; font-size: 0.85rem;">
                <i class="fa-solid fa-right-to-bracket"></i> Entrar
            </button>
            <div id="tr-user-avatar" class="hidden" style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-muted); font-size: 0.85rem; background: var(--bg-card); padding: 0.3rem 0.8rem 0.3rem 0.3rem; border-radius: 50px; border: 1px solid var(--border-color);">
                <!-- Avatar image here -->
            </div>
        </div>
"""
        content = content.replace('<div class="content-wrapper">', top_bar)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")

print("Top right profile injected.")
