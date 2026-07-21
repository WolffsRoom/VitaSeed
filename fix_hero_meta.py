import re

with open('js/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

# Fix hero-meta in main.js
old_hero_meta = '<div class="hero-meta">${heroProj.category}   Por ${heroProj.responsibles}</div>'
new_hero_meta = '''<div class="hero-meta" style="display: flex; gap: 0.8rem; align-items: center; margin-top: 0.5rem; flex-wrap: wrap;">
                            <span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-folder"></i> ${heroProj.category}</span>
                            <span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-user"></i> Por ${heroProj.responsibles}</span>
                            ${heroProj.version ? `<span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-tag"></i> v${heroProj.version}</span>` : ''}
                            ${heroProj.update_date ? `<span style="display: flex; align-items: center; gap: 0.3rem;"><i class="ph ph-calendar-blank"></i> ${heroProj.update_date}</span>` : ''}
                        </div>'''

main_js = main_js.replace(old_hero_meta, new_hero_meta)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)
