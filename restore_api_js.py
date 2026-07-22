import re
import glob

# 1. Recreate api.js
api_code = """window.fetchCatalog = async function() {
    if (window.projectsData) return window.projectsData;
    try {
        const res = await fetch('api/catalog.json');
        if (!res.ok) throw new Error('Falha ao baixar o catálogo');
        const data = await res.json();
        window.projectsData = data.projects;
        return window.projectsData;
    } catch (e) {
        console.error("Erro na API:", e);
        return [];
    }
}

window.formatTitle = function(title) {
    if (!title) return "";
    return title.replace(/(\([^)]+\)|\[[^\]]+\])/g, '<span style="font-weight: 400; font-size: 0.85em;">$1</span>');
};
"""
with open('js/api.js', 'w', encoding='utf-8') as f:
    f.write(api_code)

# 2. Remove from main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_code = f.read()
main_code = main_code.replace(api_code + '\n\n', '')
with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_code)

# 3. Add to all HTML files
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if '<script src="js/api.js"></script>' not in html and '<script src="js/api.js?v=2"></script>' not in html:
        # Inject it right before theme.js
        html = re.sub(r'<script src="js/theme\.js(\?v=\d+)?"></script>', r'<script src="js/api.js?v=3"></script>\n    <script src="js/theme.js\1"></script>', html)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Restored api.js across all files!")
