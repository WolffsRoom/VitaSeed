import re

with open('project.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add qrcode.js to head
if 'qrcode.min.js' not in content:
    content = content.replace('</head>', '    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n</head>')

# Rewrite the main project-details structure
new_structure = """
            <div id="project-details" style="max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 2rem;">
                
                <div id="proj-header-banner" class="project-header">
                    <div class="project-header-content">
                        <h1 id="proj-title">Loading...</h1>
                        <div id="proj-badges" style="display: flex; gap: 0.5rem; flex-wrap: wrap;"></div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                    
                    <div style="display: flex; flex-direction: column; gap: 2rem;">
                        <div class="section-box" style="margin-bottom: 0;">
                            <h3><i class="ph ph-info"></i> Descrição</h3>
                            <p id="proj-desc" style="color: var(--text-main); line-height: 1.6;"></p>
                            
                            <div class="action-bar" style="align-items: center; justify-content: space-between;">
                                <div style="display:flex; gap:1rem;">
                                    <a id="btn-download" href="#" class="btn-primary"><i class="ph ph-download-simple"></i> Download VPK</a>
                                    <a id="btn-source" href="#" class="btn-secondary" target="_blank"><i class="ph ph-github-logo"></i> Source Code</a>
                                </div>
                                <div class="qr-container" title="Escaneie para baixar no Vita">
                                    <div id="qrcode"></div>
                                </div>
                            </div>
                        </div>

                        <div id="install-section" class="section-box hidden" style="margin-bottom: 0;">
                            <h3><i class="ph ph-wrench"></i> Instruções de Instalação</h3>
                            <p id="install-text" style="color: var(--text-muted); line-height: 1.6; white-space: pre-line;"></p>
                        </div>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 2rem;">
                        <div class="meta-grid">
                            <div class="meta-item">
                                <div class="meta-label">Publicação Original</div>
                                <div id="meta-pub" class="meta-val">--/--/--</div>
                            </div>
                            <div class="meta-item">
                                <div class="meta-label">Última Atualização</div>
                                <div id="meta-upd" class="meta-val">--/--/--</div>
                            </div>
                            <div class="meta-item">
                                <div class="meta-label">Total Downloads</div>
                                <div id="meta-down" class="meta-val">---</div>
                            </div>
                        </div>

                        <div class="section-box support-panel" style="margin-bottom: 0;">
                            <h3><i class="ph ph-heart"></i> Apoie o Desenvolvedor</h3>
                            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">Gostou do projeto? Considere apoiar o responsável para que ele continue trazendo novidades para o PSVita!</p>
                            <a id="btn-support" href="#" target="_blank" class="btn-primary" style="background: var(--accent-green); color: #000; width: 100%; justify-content: center;"><i class="ph ph-coffee"></i> Apoiar Projeto</a>
                        </div>
                    </div>
                </div>

                <div id="media-section" class="section-box hidden" style="margin-bottom: 0;">
                    <h3><i class="ph ph-image"></i> Mídia (Prints & Vídeos)</h3>
                    <div id="media-container" class="media-grid"></div>
                </div>

            </div>
"""

# Replace the interior of the content-wrapper main tag
content = re.sub(r'<div id="project-details" style="max-width: 1000px; margin: 0 auto;">.*?</main>', new_structure + '\n        </main>', content, flags=re.DOTALL)

# Update the JS logic
js_logic = """
            if (proj) {
                document.getElementById('proj-title').innerText = proj.title;
                document.getElementById('proj-desc').innerText = proj.description;
                document.getElementById('btn-source').href = proj.source_link;
                
                // Metadados
                if(proj.publish_date) document.getElementById('meta-pub').innerText = proj.publish_date;
                if(proj.update_date) document.getElementById('meta-upd').innerText = proj.update_date;
                if(proj.downloads) document.getElementById('meta-down').innerText = proj.downloads.toLocaleString('pt-BR');
                if(proj.support_link) {
                    document.getElementById('btn-support').href = proj.support_link;
                }

                // Gerar QR Code (Link Fake para o demo)
                const downloadLink = "https://vita.hacks.guide"; // VPK URL simulada
                new QRCode(document.getElementById("qrcode"), {
                    text: downloadLink,
                    width: 60,
                    height: 60,
                    colorDark : "#000000",
                    colorLight : "#ffffff",
                    correctLevel : QRCode.CorrectLevel.L
                });

                // Cover Banner
"""
content = content.replace("""
            if (proj) {
                document.getElementById('proj-title').innerText = proj.title;
                document.getElementById('proj-desc').innerText = proj.description;
                document.getElementById('btn-source').href = proj.source_link;

                // Cover Banner""", js_logic)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(content)
