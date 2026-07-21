import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

buttons_html = '''                <button class="scroll-btn scroll-left"><i class="ph ph-caret-left"></i></button>
                <button class="scroll-btn scroll-right"><i class="ph ph-caret-right"></i></button>
                <div id="top10-container" class="top10-scroll">'''

html = html.replace('<div id="top10-container" class="top10-scroll">', buttons_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update css/style.css
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

scroll_css = '''
/* Top 10 Scroll Buttons */
.scroll-btn {
    position: absolute;
    top: 60%;
    transform: translateY(-50%);
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: white;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10;
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
#top10-section:hover .scroll-btn {
    opacity: 0.4;
}
.scroll-btn:hover {
    background: rgba(0, 230, 118, 0.8);
    opacity: 1 !important;
    transform: translateY(-50%) scale(1.1);
}
.scroll-left { left: 10px; }
.scroll-right { right: 10px; }
'''
css += scroll_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update js/main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js_scroll = '''
            // Top 10 Scroll Buttons
            const top10Container = document.getElementById('top10-container');
            const btnLeft = document.querySelector('.scroll-left');
            const btnRight = document.querySelector('.scroll-right');

            if (btnLeft && btnRight && top10Container) {
                btnLeft.addEventListener('click', () => {
                    top10Container.scrollBy({ left: -400, behavior: 'smooth' });
                });
                btnRight.addEventListener('click', () => {
                    top10Container.scrollBy({ left: 400, behavior: 'smooth' });
                });
            }
'''

# Find the place to inject (e.g. after rendering top10)
# Top 10 is rendered in: document.getElementById('top10-container').innerHTML = top10Html;
js = js.replace("document.getElementById('top10-container').innerHTML = top10Html;", "document.getElementById('top10-container').innerHTML = top10Html;\n" + js_scroll)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
