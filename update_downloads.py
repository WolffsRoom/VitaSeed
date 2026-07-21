import json
import re

# 1. Update Catalog
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['version'] = "0.52"
        p['update_date'] = "20/07/2026"
        p['downloads_list'] = [
            {"name": "Baixar VPK (v0.52)", "url": "https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.52/Deltarune-v0.52.vpk"},
            {"name": "Baixar Patcher (ZIP)", "url": "https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.52/Deltarune.Vita.Patcher.v0.52.zip"}
        ]
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Update main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

old_meta = '<span>${proj.responsibles}</span>'
new_meta = '''<span>${proj.responsibles}</span>
                            ${proj.version ? `<span style="opacity:0.5; margin:0 4px;">•</span> <span>v${proj.version}</span>` : ''}
                            ${proj.update_date ? `<span style="opacity:0.5; margin:0 4px;">•</span> <span>${proj.update_date}</span>` : ''}'''
main_js = main_js.replace(old_meta, new_meta)
with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

# 3. Update category.html
with open('category.html', 'r', encoding='utf-8') as f:
    cat_html = f.read()

cat_html = cat_html.replace(old_meta, new_meta)
with open('category.html', 'w', encoding='utf-8') as f:
    f.write(cat_html)

# 4. Update project.html Action Bar and QR Code
with open('project.html', 'r', encoding='utf-8') as f:
    proj_html = f.read()

# Replace hardcoded QR code logic
qr_old = '''                // Gerar QR Code (Link Fake para o demo)
                const downloadLink = "https://vita.hacks.guide"; // VPK URL simulada
                new QRCode(document.getElementById("qrcode"), {
                    text: downloadLink,'''

qr_new = '''                // Setup Download Buttons
                const actionBar = document.querySelector('.action-bar');
                // Remove old single button
                const oldBtn = document.getElementById('btn-download');
                if (oldBtn) oldBtn.remove();
                
                let qrUrl = window.location.href; // Fallback to current page
                
                if (proj.downloads_list && proj.downloads_list.length > 0) {
                    qrUrl = proj.downloads_list[0].url; // First download link for QR code
                    
                    proj.downloads_list.forEach((dl, index) => {
                        const btn = document.createElement('a');
                        btn.href = dl.url;
                        btn.className = index === 0 ? 'btn btn-primary' : 'btn btn-secondary';
                        btn.innerHTML = `<i class="ph ph-download-simple"></i> ${dl.name}`;
                        actionBar.insertBefore(btn, document.getElementById('btn-support'));
                    });
                } else {
                    // Fallback to source link
                    const btn = document.createElement('a');
                    btn.href = proj.source_link || '#';
                    btn.className = 'btn btn-primary';
                    btn.innerHTML = `<i class="ph ph-download-simple"></i> Download`;
                    actionBar.insertBefore(btn, document.getElementById('btn-support'));
                    if (proj.source_link) qrUrl = proj.source_link;
                }

                // Gerar QR Code
                document.getElementById("qrcode").innerHTML = ""; // Clear if previously rendered
                new QRCode(document.getElementById("qrcode"), {
                    text: qrUrl,'''
proj_html = proj_html.replace(qr_old, qr_new)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(proj_html)
