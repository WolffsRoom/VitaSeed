import glob
import re

# 1. Update HTML files to change text input to file input
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace URL label
    html = re.sub(
        r'<label[^>]*>URL da Foto de Perfil</label>',
        '<label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">Foto de Perfil (Envie uma imagem)</label>',
        html
    )
    
    # Replace text input with file input
    html = re.sub(
        r'<input type="text" id="profile-edit-avatar" class="search-bar" placeholder="https://\.\.\." style="width: 100%; box-sizing: border-box;" onchange="[^"]+">',
        '<input type="file" id="profile-edit-avatar" accept="image/*" class="search-bar" style="width: 100%; box-sizing: border-box; padding: 0.5rem;" onchange="handleAvatarUpload(event)">',
        html
    )
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# 2. Update auth.js
with open('js/auth.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the save logic for avatar
js = js.replace("const avatar = document.getElementById('profile-edit-avatar').value;", "const avatar = document.getElementById('profile-edit-avatar-preview').src;")

# Ensure openProfileModal does NOT set the value of the file input (since it can't be set programmatically easily)
js = js.replace("document.getElementById('profile-edit-avatar').value = userProfileData.avatar_url || '';", "")

# Add handleAvatarUpload function
upload_fn = """
window.handleAvatarUpload = function(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const MAX_SIZE = 150; // Limitar tamanho para no estourar base64
            let width = img.width;
            let height = img.height;
            
            if (width > height) {
                if (width > MAX_SIZE) {
                    height *= MAX_SIZE / width;
                    width = MAX_SIZE;
                }
            } else {
                if (height > MAX_SIZE) {
                    width *= MAX_SIZE / height;
                    height = MAX_SIZE;
                }
            }
            
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            
            // Converter para base64 JPEG com qualidade 80%
            const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
            document.getElementById('profile-edit-avatar-preview').src = dataUrl;
        }
        img.src = e.target.result;
    }
    reader.readAsDataURL(file);
}
"""

if 'window.handleAvatarUpload' not in js:
    js += '\n' + upload_fn

with open('js/auth.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Avatar upload implemented!")
