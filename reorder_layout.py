import re

with open('project.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Swap media section and install section in HTML
# They are both inside the left column.
# I'll find them and swap their order.
install_block_regex = r'(<div id="install-section"[^>]*>.*?</div>)'
media_block_regex = r'(<div id="media-section"[^>]*>.*?</div>)'

# Let's extract them
install_match = re.search(install_block_regex, content, re.DOTALL)
media_match = re.search(media_block_regex, content, re.DOTALL)

if install_match and media_match:
    # First remove them from their original spots
    temp_content = content.replace(install_match.group(1), '<!-- INSTALL_PLACEHOLDER -->')
    temp_content = temp_content.replace(media_match.group(1), '<!-- MEDIA_PLACEHOLDER -->')
    
    # We want MEDIA first, then INSTALL. So where INSTALL was, we put both (MEDIA then INSTALL)
    # And we remove the MEDIA_PLACEHOLDER entirely.
    new_blocks = f"{media_match.group(1)}\n\n{install_match.group(1)}"
    
    temp_content = temp_content.replace('<!-- INSTALL_PLACEHOLDER -->', new_blocks)
    temp_content = temp_content.replace('<!-- MEDIA_PLACEHOLDER -->', '')
    content = temp_content

# 2. Remove "Total Downloads" from meta-grid
# The HTML looks like this:
'''
                            <div class="meta-item">
                                <div class="meta-label">Total Downloads</div>
                                <div id="meta-down" class="meta-val">---</div>
                            </div>
'''
downloads_html_regex = r'<div class="meta-item">\s*<div class="meta-label">Total Downloads</div>\s*<div id="meta-down" class="meta-val">---</div>\s*</div>'
content = re.sub(downloads_html_regex, '', content)

# 3. Clean up JS for fetchGithubDownloads so it doesn't throw errors trying to find #meta-down
js_to_remove_regex = r'// Fetch real downloads.*?\}'
content = re.sub(js_to_remove_regex, '', content, flags=re.DOTALL)

# But wait, there is an else if inside that block I might break.
# I'll just remove the element and let the JS fail gracefully by adding `if (document.getElementById('meta-down'))`
# Or easier: just write a safer JS replacement
safe_js = """
                const metaDownEl = document.getElementById('meta-down');
                if (metaDownEl) {
                    if (proj.source_link) {
                        metaDownEl.innerText = "Carregando...";
                        fetchGithubDownloads(proj.source_link).then(count => {
                            if (count !== null && count > 0) {
                                metaDownEl.innerHTML = count.toLocaleString('pt-BR') + ' <span style="font-size:0.8rem; color:var(--text-muted);">(GitHub)</span>';
                            } else if (proj.downloads !== undefined) {
                                metaDownEl.innerText = proj.downloads.toLocaleString('pt-BR');
                            } else {
                                metaDownEl.innerText = "N/A";
                            }
                        });
                    } else if(proj.downloads !== undefined) {
                        metaDownEl.innerText = proj.downloads.toLocaleString('pt-BR');
                    }
                }
"""

content = re.sub(r'// Fetch real downloads.*?\} else if\(proj\.downloads !== undefined\) \{\s*document\.getElementById\(\'meta-down\'\)\.innerText = proj\.downloads\.toLocaleString\(\'pt-BR\'\);\s*\}', safe_js, content, flags=re.DOTALL)


with open('project.html', 'w', encoding='utf-8') as f:
    f.write(content)
