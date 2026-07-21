with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Infinite Carousel Logic
# Find where the top10.forEach generates the HTML
# Instead of doing it once, we'll store the HTML in a variable, then set innerHTML to it 3 times!
# Wait, it's better to just clone the elements after they are added.

# 2. Update the scroll listener in main.js
old_scroll_logic = '''                    top10Container.addEventListener('scroll', () => {
                        if (top10Container.scrollLeft > 10) {
                            top10Container.classList.add('scrolled');
                        } else {
                            top10Container.classList.remove('scrolled');
                        }
                    });'''

new_scroll_logic = '''                    let scrollTimeout;
                    top10Container.addEventListener('scroll', () => {
                        // Sempre que estiver rolando (e não estiver no início absoluto), mostra o fade
                        if (top10Container.scrollLeft > 10) {
                            top10Container.classList.add('scrolled');
                        } else {
                            top10Container.classList.remove('scrolled');
                        }
                        
                        // Quando parar de rolar, remove o fade da esquerda
                        clearTimeout(scrollTimeout);
                        scrollTimeout = setTimeout(() => {
                            top10Container.classList.remove('scrolled');
                        }, 250);
                    });'''

js = js.replace(old_scroll_logic, new_scroll_logic)

# To make infinite loop, let's change the scrollBtn click logic
old_btn_logic = '''                    scrollRightBtn.addEventListener('click', () => {
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
                    });'''

# If they want an infinite visual loop (after 10 comes 1 visually), doing that with `scroll-snap` and `flex` requires duplicating DOM elements.
# Let's clone the first 5 elements and append them, and clone the last 5 elements and prepend them.
# We will do this right after rendering the first 10.

injection_code = '''
                // Clona para criar um loop infinito visual
                const cards = Array.from(top10Container.children);
                cards.forEach(card => {
                    let clone = card.cloneNode(true);
                    top10Container.appendChild(clone);
                });
                
                // Agora top10Container tem 20 itens (1-10, 1-10)
                
                // Scroll Logic
'''
js = js.replace('// Scroll Logic', injection_code)

new_btn_logic = '''                    scrollRightBtn.addEventListener('click', () => {
                        const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                        if (top10Container.scrollLeft >= maxScrollLeft - 50) {
                            // Volta silenciosamente para o começo do segundo bloco (item 11) ou do primeiro bloco (item 1)
                            top10Container.scrollTo({ left: 0, behavior: 'auto' }); // Pula invisivelmente
                            setTimeout(() => { top10Container.scrollBy({ left: 300, behavior: 'smooth' }); }, 50);
                        } else {
                            top10Container.scrollBy({ left: 300, behavior: 'smooth' });
                        }
                    });

                    scrollLeftBtn.addEventListener('click', () => {
                        if (top10Container.scrollLeft <= 10) {
                            const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                            top10Container.scrollTo({ left: maxScrollLeft / 2, behavior: 'auto' }); // Pula invisivelmente para o meio
                            setTimeout(() => { top10Container.scrollBy({ left: -300, behavior: 'smooth' }); }, 50);
                        } else {
                            top10Container.scrollBy({ left: -300, behavior: 'smooth' });
                        }
                    });'''

js = js.replace(old_btn_logic, new_btn_logic)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=11', 'js/main.js?v=12')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
