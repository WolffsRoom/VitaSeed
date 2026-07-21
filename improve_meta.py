import re

# Update main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

old_meta_regex = r'<div class="card-meta">.*?</div>'
new_meta = '''<div class="card-meta" style="display: flex; flex-wrap: wrap; gap: 0.8rem; align-items: center; color: var(--text-muted); font-size: 0.75rem; margin-top: auto; padding-top: 0.5rem;">
                            <span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-user"></i> ${proj.responsibles}</span>
                            ${proj.version ? `<span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-tag"></i> v${proj.version}</span>` : ''}
                            ${proj.update_date ? `<span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-calendar-blank"></i> ${proj.update_date}</span>` : ''}
                        </div>'''

main_js = re.sub(old_meta_regex, new_meta, main_js, flags=re.DOTALL)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

# Update category.html
with open('category.html', 'r', encoding='utf-8') as f:
    cat_html = f.read()

cat_html = re.sub(old_meta_regex, new_meta, cat_html, flags=re.DOTALL)

with open('category.html', 'w', encoding='utf-8') as f:
    f.write(cat_html)
