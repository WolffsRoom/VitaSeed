import re

with open('project.html', 'r', encoding='utf-8') as f:
    content = f.read()

lightbox_css_html = """
    <style>
        /* Lightbox Styles */
        #lightbox {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            opacity: 0;
            transition: opacity 0.3s;
        }
        #lightbox.show {
            display: flex;
            opacity: 1;
        }
        #lightbox-img {
            max-width: 90%;
            max-height: 90vh;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        .lightbox-close, .lightbox-prev, .lightbox-next {
            position: absolute;
            color: #fff;
            font-size: 2.5rem;
            cursor: pointer;
            user-select: none;
            background: rgba(0,0,0,0.5);
            border-radius: 50%;
            width: 50px; height: 50px;
            display: flex; justify-content: center; align-items: center;
            transition: 0.2s;
        }
        .lightbox-close:hover, .lightbox-prev:hover, .lightbox-next:hover {
            background: var(--accent-green);
            color: #000;
        }
        .lightbox-close { top: 20px; right: 30px; }
        .lightbox-prev { left: 30px; }
        .lightbox-next { right: 30px; }
    </style>

    <div id="lightbox">
        <div class="lightbox-close"><i class="ph ph-x"></i></div>
        <div class="lightbox-prev"><i class="ph ph-caret-left"></i></div>
        <img id="lightbox-img" src="" alt="Maximizado">
        <div class="lightbox-next"><i class="ph ph-caret-right"></i></div>
    </div>
"""

# Insert lightbox CSS and HTML before the scripts at the bottom
content = content.replace('    <script src="js/api.js"></script>', lightbox_css_html + '\n    <script src="js/api.js"></script>')

# Add JS logic
lightbox_js = """
                // Setup Lightbox
                const lightbox = document.getElementById('lightbox');
                const lightboxImg = document.getElementById('lightbox-img');
                const btnClose = document.querySelector('.lightbox-close');
                const btnPrev = document.querySelector('.lightbox-prev');
                const btnNext = document.querySelector('.lightbox-next');
                
                let currentImgIndex = 0;
                let imagesArray = [];

                if (hasMedia) {
                    document.getElementById('media-section').classList.remove('hidden');
                    // Setup images array and click events
                    const imgs = mediaContainer.querySelectorAll('img');
                    imgs.forEach((img, idx) => {
                        imagesArray.push(img.src);
                        img.addEventListener('click', () => {
                            currentImgIndex = idx;
                            showLightbox(currentImgIndex);
                        });
                    });
                }

                function showLightbox(index) {
                    if (imagesArray.length === 0) return;
                    lightboxImg.src = imagesArray[index];
                    lightbox.classList.add('show');
                    document.body.style.overflow = 'hidden'; // Prevent scrolling background
                }

                function closeLightbox() {
                    lightbox.classList.remove('show');
                    document.body.style.overflow = 'auto';
                }

                function nextImage() {
                    currentImgIndex = (currentImgIndex + 1) % imagesArray.length;
                    lightboxImg.src = imagesArray[currentImgIndex];
                }

                function prevImage() {
                    currentImgIndex = (currentImgIndex - 1 + imagesArray.length) % imagesArray.length;
                    lightboxImg.src = imagesArray[currentImgIndex];
                }

                btnClose.addEventListener('click', closeLightbox);
                btnNext.addEventListener('click', nextImage);
                btnPrev.addEventListener('click', prevImage);
                
                lightbox.addEventListener('click', (e) => {
                    if (e.target === lightbox) closeLightbox();
                });

                document.addEventListener('keydown', (e) => {
                    if (!lightbox.classList.contains('show')) return;
                    if (e.key === 'Escape') closeLightbox();
                    if (e.key === 'ArrowRight') nextImage();
                    if (e.key === 'ArrowLeft') prevImage();
                });

                // Install Instructions
"""

# Replace the part before "Install Instructions" to inject the lightbox logic
content = content.replace("""
                if (hasMedia) {
                    document.getElementById('media-section').classList.remove('hidden');
                }

                // Install Instructions""", lightbox_js)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(content)
