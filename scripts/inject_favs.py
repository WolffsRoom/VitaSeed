import re
with open('js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

fav_btn = """
                        <button class="btn-fav" onclick="toggleFavorite(event, '${proj.id}')" style="background:none; border:none; color:var(--text-muted); cursor:pointer; padding:0.2rem; transition:0.2s;">
                            <i class="${(typeof userProfileData !== 'undefined' && userProfileData && userProfileData.favorites && userProfileData.favorites.includes(proj.id)) ? 'fa-solid fa-heart' : 'fa-regular fa-heart'}" style="font-size:1.2rem; ${(typeof userProfileData !== 'undefined' && userProfileData && userProfileData.favorites && userProfileData.favorites.includes(proj.id)) ? 'color:var(--accent-green);' : ''}"></i>
                        </button>
"""
if 'btn-fav' not in content:
    content = content.replace('<div class="card-tags">\n                          ${badgesHtml}\n                      </div>', 
    '<div class="card-tags" style="display:flex; justify-content:space-between; align-items:center; width:100%;">\n                          <div>${badgesHtml}</div>\n                          ' + fav_btn + '\n                      </div>')
    
    with open('js/main.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Favorites UI injected')
