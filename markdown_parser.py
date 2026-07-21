import re

# 1. Update project.html
with open('project.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Inject marked.js CDN
if 'marked.min.js' not in html_content:
    marked_script = '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n'
    html_content = html_content.replace('</head>', marked_script + '</head>')

# Change innerText to innerHTML = marked.parse()
old_js = "document.getElementById('install-text').innerText = proj.install_instructions;"
new_js = "document.getElementById('install-text').innerHTML = marked.parse(proj.install_instructions);"
html_content = html_content.replace(old_js, new_js)

# We should also remove 'white-space: pre-line;' from install-text inline styles because marked creates paragraphs
html_content = html_content.replace('white-space: pre-line;', '')

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# 2. Update style.css
css_rules = """
/* Markdown Styles for Install Text */
#install-text ul, #install-text ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}
#install-text li {
    margin-bottom: 0.5rem;
}
#install-text p {
    margin-bottom: 1rem;
}
#install-text code {
    background: rgba(128, 128, 128, 0.2);
    padding: 0.1rem 0.3rem;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9em;
}
#install-text pre {
    background: rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    overflow-x: auto;
}
#install-text pre code {
    background: transparent;
    padding: 0;
}
#install-text a {
    color: var(--accent-green);
    text-decoration: none;
    font-weight: 500;
}
#install-text a:hover {
    text-decoration: underline;
}
#install-text h1, #install-text h2, #install-text h3, #install-text h4 {
    color: var(--text-main);
    margin-top: 1.5rem;
    margin-bottom: 1rem;
}
"""

with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(css_rules)
