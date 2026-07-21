import re

with open('project.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the messy grid with a cleaner 2fr 1fr grid
old_grid = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">'
new_grid = """
                <style>
                    .project-layout {
                        display: grid;
                        grid-template-columns: 1fr;
                        gap: 2rem;
                    }
                    @media (min-width: 900px) {
                        .project-layout {
                            grid-template-columns: 2fr 1fr;
                        }
                    }
                </style>
                <div class="project-layout">
"""
content = content.replace(old_grid, new_grid)

# Move Media section into the left column (currently it's outside the grid at the bottom)
# Find media section
media_section = """
                <div id="media-section" class="section-box hidden" style="margin-bottom: 0;">
                    <h3><i class="ph ph-image"></i> Mídia (Prints & Vídeos)</h3>
                    <div id="media-container" class="media-grid"></div>
                </div>
"""
content = content.replace(media_section, "")

# Insert media section inside the left column, right after install-section
install_section = """                        <div id="install-section" class="section-box hidden" style="margin-bottom: 0;">
                            <h3><i class="ph ph-wrench"></i> Instruções de Instalação</h3>
                            <p id="install-text" style="color: var(--text-muted); line-height: 1.6; white-space: pre-line;"></p>
                        </div>"""

content = content.replace(install_section, install_section + "\n" + media_section)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(content)
