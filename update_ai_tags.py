import json
import re

# 1. Update Catalog to put Deltarune first
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

projects = catalog.get('projects', [])
deltarune_idx = next((i for i, p in enumerate(projects) if p.get('id') == 222), -1)

if deltarune_idx > 0:
    delta = projects.pop(deltarune_idx)
    projects.insert(0, delta)
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Remove AI Tags from main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

# Look for: if (proj.ai_used || proj.vibecoded) { badgesHtml += ...; }
ai_tag_pattern = r'if\s*\(proj\.ai_used\s*\|\|\s*proj\.vibecoded\)\s*\{\s*badgesHtml\s*\+=\s*`<span class="tag" style="background:var\(--bg-main\); border:1px solid var\(--border-color\);" title="Utiliza IA">IA</span>`;\s*\}'
main_js = re.sub(ai_tag_pattern, '', main_js)
with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

# Remove from category.html as well
with open('category.html', 'r', encoding='utf-8') as f:
    cat_html = f.read()

ai_tag_cat = r'if\s*\(proj\.ai_used && !proj\.vibecoded\)\s*badgesHtml\s*\+=\s*`<span class="ai-indicator">AI Assisted</span>`;\s*else if\s*\(proj\.vibecoded\)\s*badgesHtml\s*\+=\s*`<span class="ai-indicator vibecoded-badge">100% Vibecoded</span>`;'
cat_html = re.sub(ai_tag_cat, '', cat_html)
with open('category.html', 'w', encoding='utf-8') as f:
    f.write(cat_html)

# 3. Add AI details inside project.html
with open('project.html', 'r', encoding='utf-8') as f:
    proj_html = f.read()

# First, remove the AI tag generation from project.html header badges
proj_ai_badge = r'if\s*\(proj\.ai_used\s*\|\|\s*proj\.vibecoded\)\s*\{\s*badgesHtml\s*\+=\s*`<span class="tag" style="background:var\(--bg-main\); border:1px solid var\(--border-color\);" title="Utiliza IA">IA</span>`;\s*\}'
proj_html = re.sub(proj_ai_badge, '', proj_html)

# Add AI details block below the description
# We can find `document.getElementById('proj-desc').innerText = proj.description;`
ai_block_js = """
                document.getElementById('proj-desc').innerText = proj.description;
                
                // Add AI Details if present
                const descContainer = document.getElementById('proj-desc').parentElement;
                // Remove any old ai box if running multiple times
                const oldAiBox = document.getElementById('ai-details-box');
                if (oldAiBox) oldAiBox.remove();
                
                if (proj.ai_used && proj.ai_details) {
                    const aiBox = document.createElement('div');
                    aiBox.id = 'ai-details-box';
                    aiBox.style.cssText = "margin-top: 1.5rem; padding: 1rem; border-radius: 8px; background: rgba(0,230,118,0.05); border: 1px solid rgba(0,230,118,0.2);";
                    aiBox.innerHTML = `
                        <h4 style="color: var(--accent-green); display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.9rem;">
                            <i class="ph ph-robot"></i> Desenvolvimento Assistido por IA
                        </h4>
                        <div style="font-size: 0.85rem; color: var(--text-main); line-height: 1.5;">
                            <strong>IA Utilizada:</strong> ${proj.ai_details.name} <br>
                            <strong>Propósito:</strong> ${proj.ai_details.reason} <br>
                            <strong>Ação:</strong> ${proj.ai_details.action}
                        </div>
                    `;
                    descContainer.insertBefore(aiBox, document.querySelector('.action-bar'));
                }
"""

proj_html = proj_html.replace("document.getElementById('proj-desc').innerText = proj.description;", ai_block_js)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(proj_html)
