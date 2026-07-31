import re

with open('js/main.js', 'r', encoding='utf-8') as f:
    main_code = f.read()

# Add favorite check and heart button to the grid card
card_html_old = """              card.innerHTML = `
                  <div class="card-banner" style="background-image: url('${bannerUrl}'); background-position: ${proj.bgPosition || 'center'};"></div>"""

card_html_new = """              const isFav = window.userProfileData && window.userProfileData.favorites && window.userProfileData.favorites.includes(proj.id);
              const favIcon = isFav ? 'ph-heart-fill' : 'ph-heart';
              const favColor = isFav ? 'var(--accent-green)' : '#fff';

              card.innerHTML = `
                  <div class="card-banner" style="background-image: url('${bannerUrl}'); background-position: ${proj.bgPosition || 'center'};">
                      <button class="fav-btn" onclick="toggleFavorite(event, '${proj.id}')" style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 50%; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; cursor: pointer; backdrop-filter: blur(5px); z-index: 10; transition: all 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                          <i class="ph ${favIcon}" style="color: ${favColor}; font-size: 1.2rem;"></i>
                      </button>
                  </div>"""

main_code = main_code.replace(card_html_old, card_html_new)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_code)

print("Added favorite button to cards.")
