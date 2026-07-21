with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Phosphor icons with FontAwesome icons
html = html.replace('<i class="ph ph-caret-left"></i>', '<i class="fa-solid fa-chevron-left"></i>')
html = html.replace('<i class="ph ph-caret-right"></i>', '<i class="fa-solid fa-chevron-right"></i>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I need to inject the event listeners.
# Let's find a good place. After "top10Container.innerHTML = top10Html;"
target = "top10Container.innerHTML = top10Html;"

js_to_inject = """top10Container.innerHTML = top10Html;

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
                    const maxScrollLeft = top10Container.scrollWidth - top10Container.clientWidth;
                    if (top10Container.scrollLeft <= 10) {
                        top10Container.scrollTo({ left: maxScrollLeft, behavior: 'smooth' });
                    } else {
                        top10Container.scrollBy({ left: -300, behavior: 'smooth' });
                    }
                });
                
                // Ensure dynamic fade also works
                top10Container.addEventListener('scroll', () => {
                    if (top10Container.scrollLeft > 10) {
                        top10Container.classList.add('scrolled');
                    } else {
                        top10Container.classList.remove('scrolled');
                    }
                });
            }"""

if "scrollRightBtn.addEventListener" not in js:
    js = js.replace(target, js_to_inject)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('js/main.js?v=7', 'js/main.js?v=8')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
