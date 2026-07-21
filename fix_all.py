import re

# 1. Fix project header CSS
css_fix = """
/* Project Header Banner */
.project-header {
    height: 350px;
    background-size: cover;
    background-position: center;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    border: 1px solid var(--card-border);
}

.project-header::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 80%;
    background: linear-gradient(to top, rgba(14, 14, 14, 1) 0%, rgba(14, 14, 14, 0) 100%);
    pointer-events: none;
}

.project-header-content {
    position: relative;
    padding: 2rem;
    width: 100%;
    z-index: 2;
}
"""

with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(css_fix)

# 2. Fix project.html corrupted HTML and change "Apoie o Desenvolvedor"
with open('project.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change button text
html = html.replace('Apoie o Desenvolvedor', 'Apoie o Responsável')

# Fix corrupted layout. The corrupted part starts around `<div id="media-section"` and ends somewhere near `</div>` 
# I will just replace the whole main-column part.
# Let's locate the exact corrupted string.
bad_html = r'<div id="media-section" class="section-box hidden" style="margin-bottom: 0;">\s*<h3><i class="ph ph-image"></i> Mídia \(Prints & Vídeos\)</h3>\s*<div id="media-container" class="media-grid"></div>\s*<div id="install-section" class="section-box hidden" style="margin-bottom: 0;">\s*<h3><i class="ph ph-wrench"></i> Instruções de Instalação</h3>'

good_html = """
                        <div id="media-section" class="section-box hidden">
                            <h3><i class="ph ph-image"></i> Mídia (Prints & Vídeos)</h3>
                            <div id="media-container" class="media-grid"></div>
                        </div>

                        <div id="install-section" class="section-box hidden">
                            <h3><i class="ph ph-wrench"></i> Instruções de Instalação</h3>
                            <div id="install-text" style="line-height: 1.6;"></div>
                        </div>
"""

# Let's use regex to replace anything between <div id="media-section"... and the end of install-section if possible, 
# or just carefully replace the messed up block.
# Actually, let's just do it directly.
html = re.sub(r'<div id="media-section".*?<h3><i class="ph ph-wrench"></i> Instruções de Instalação</h3>', good_html.strip(), html, flags=re.DOTALL)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(html)
