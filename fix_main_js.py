with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix Top 10 info
old_info = '''                            <div class="top10-overlay">
                                <div class="top10-title">${window.formatTitle(proj.title)}</div>
                                <div class="top10-cat">${proj.category}</div>
                            </div>'''

new_info = '''                            <div class="top10-overlay">
                                <div class="top10-title">${window.formatTitle(proj.title)}</div>
                                <div class="top10-cat" style="font-weight: bold;">${proj.category}</div>
                                <div class="top10-resp" style="font-size: 0.8rem; margin-top: 4px; opacity: 0.8;"><i class="ph ph-user"></i> ${proj.responsibles}</div>
                            </div>'''

js = js.replace(old_info, new_info)

# Add scroll logic
old_block = '''                });
            } else {'''

new_block = '''                });
                
                // Scroll Logic
                const scrollLeftBtn = document.querySelector('.scroll-left');
                const scrollRightBtn = document.querySelector('.scroll-right');
                if(scrollLeftBtn && scrollRightBtn) {
                    scrollRightBtn.addEventListener('click', () => {
                        const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                        if (top10Container.scrollLeft >= maxScrollLeft - 10) {
                            top10Container.scrollTo({ left: 0, behavior: 'smooth' });
                        } else {
                            top10Container.scrollBy({ left: 300, behavior: 'smooth' });
                        }
                    });

                    scrollLeftBtn.addEventListener('click', () => {
                        if (top10Container.scrollLeft <= 10) {
                            const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                            top10Container.scrollTo({ left: maxScrollLeft, behavior: 'smooth' });
                        } else {
                            top10Container.scrollBy({ left: -300, behavior: 'smooth' });
                        }
                    });
                    
                    top10Container.addEventListener('scroll', () => {
                        if (top10Container.scrollLeft > 10) {
                            top10Container.classList.add('scrolled');
                        } else {
                            top10Container.classList.remove('scrolled');
                        }
                    });
                }
            } else {'''

if "scrollRightBtn.addEventListener" not in js:
    js = js.replace(old_block, new_block)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=8', 'js/main.js?v=9')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
