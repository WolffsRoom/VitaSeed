with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_block = '''                });
            }
            
            // O catálogo completo exibe do 2º em diante (ou todos) para não parecer vazio'''

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
            }
            
            // O catálogo completo exibe do 2º em diante (ou todos) para não parecer vazio'''

js = js.replace(old_block, new_block)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=9', 'js/main.js?v=10')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
