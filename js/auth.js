const API_URL = "https://vitaseed-api.9h9rnjjcrf.workers.dev";
// JS para gerenciar a Autenticação com Firebase
// IMPORTANTE: O usuário deve substituir essa configuração pelas credenciais do seu projeto Firebase.
const firebaseConfig = {
  apiKey: "AIzaSyD5dyoPLWh5mav-qtdW5FNgreBJVGOcGYI",
  authDomain: "vitaseed.firebaseapp.com",
  projectId: "vitaseed",
  storageBucket: "vitaseed.firebasestorage.app",
  messagingSenderId: "263996368866",
  appId: "1:263996368866:web:d8661f2d7679523a303bbb",
  measurementId: "G-WQSEM2JV93"
};
// Se as chaves não foram preenchidas, não inicializa para evitar erros
let auth = null;
let googleProvider = null;
let githubProvider = null;
let currentUser = null;

if (firebaseConfig.apiKey !== "Sua_API_Key_Aqui") {
    // Inicializar Firebase
    const app = firebase.initializeApp(firebaseConfig);
    auth = firebase.auth();
    googleProvider = new firebase.auth.GoogleAuthProvider();
    githubProvider = new firebase.auth.GithubAuthProvider();

    auth.onAuthStateChanged((user) => {
        currentUser = user;
        updateAuthUI(user);
        if(user) fetchUserProfile();
        else userProfileData = null;
    });

    auth.getRedirectResult().then((result) => {
        if (result && result.user) {
            const loginModal = document.querySelector('.overlay.open') || document.querySelector('.modal.show');
            if (loginModal) {
                loginModal.classList.remove('open', 'show');
            }
            if (typeof closeModal === 'function') {
                closeModal('loginOverlay');
                closeModal('modal-login');
            }
        }
    }).catch((error) => {
        console.error("Erro no processamento de redirecionamento de login:", error);
        alert("Authentication Error: " + error.message + " (Code: " + error.code + ")");
    });
}

function updateAuthUI(user) {
    const dropdownContainers = document.querySelectorAll('#user-profile-dropdown');
    const requestBtns = document.querySelectorAll('#btn-request');
    const loginBtns = document.querySelectorAll('#openLoginBtn');
    
    if (user) {
        // Hide sign-in buttons on all pages
        loginBtns.forEach(btn => btn.style.display = 'none');
        
        const photoUrl = (userProfileData && userProfileData.avatar_url) ? userProfileData.avatar_url : (user.photoURL || 'https://via.placeholder.com/32');
        const displayName = (userProfileData && userProfileData.display_name) ? userProfileData.display_name : (user.displayName || 'Viteiro');
        const avatarHtml = `<img src="${photoUrl}" alt="Avatar" style="width:36px; height:36px; border-radius:50%; border:2px solid var(--accent-green); cursor:pointer; object-fit:cover;" onclick="toggleProfileMenu(event)" title="Account Options">`;
        
        dropdownContainers.forEach(container => {
            container.classList.remove('hidden');
            container.style.display = 'inline-block';
            let avatarImg = container.querySelector('img');
            if (!avatarImg) {
                container.insertAdjacentHTML('afterbegin', avatarHtml);
            } else {
                avatarImg.src = photoUrl;
            }
            
            const menuName = container.querySelector('#menu-user-name');
            const menuEmail = container.querySelector('#menu-user-email');
            if(menuName) menuName.innerText = displayName;
            if(menuEmail) menuEmail.innerText = user.email || '';
            
            const adminPanelBtn = container.querySelector('#menu-admin-panel');
            if (adminPanelBtn && (user.email === 'gabrielfwchaves@gmail.com' || window.isAdmin)) {
                adminPanelBtn.classList.remove('hidden');
            }
        });
        
        // Destravar botões de Request
        requestBtns.forEach(btn => {
            btn.innerHTML = `<i class="ph ph-paper-plane-tilt"></i> Request`;
            btn.classList.remove('btn-locked');
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        });

    } else {
        // Show sign-in buttons
        loginBtns.forEach(btn => btn.style.display = 'inline-block');
        
        dropdownContainers.forEach(container => {
            container.classList.add('hidden');
            container.style.display = 'none';
            let avatarImg = container.querySelector('img');
            if (avatarImg) avatarImg.remove();
        });
        
        // Travar botões de Request
        requestBtns.forEach(btn => {
            btn.innerHTML = `<i class="ph ph-lock"></i> Login`;
            btn.classList.add('btn-locked');
            btn.style.opacity = '0.5';
            btn.style.cursor = 'pointer';
        });
    }
}

function toggleProfileMenu(event) {
    event.stopPropagation();
    const menu = document.getElementById('profile-menu');
    if (menu) {
        if (menu.style.display === 'none' || menu.style.display === '') {
            menu.style.display = 'flex';
        } else {
            menu.style.display = 'none';
        }
    }
}

// Fechar dropdown ao clicar fora
document.addEventListener('click', (e) => {
    const menu = document.getElementById('profile-menu');
    if (menu && !menu.contains(e.target) && e.target.id !== 'user-profile-dropdown' && !e.target.closest('#user-profile-dropdown')) {
        menu.style.display = 'none';
    }
});

async function loginWithGoogle() {
    if (!auth) {
        alert("Firebase não configurado. Por favor, adicione suas credenciais no js/auth.js");
        return;
    }
    try {
        await auth.signInWithPopup(googleProvider);
        if (typeof closeModal === 'function') {
            closeModal('loginOverlay');
            closeModal('modal-login');
        }
    } catch (error) {
        console.warn("Popup blocked or failed, trying redirect flow...", error);
        try {
            await auth.signInWithRedirect(googleProvider);
        } catch (err) {
            console.error("Erro ao fazer login com Google:", err);
            alert("Erro ao iniciar login: " + err.message);
        }
    }
}

async function loginWithGitHub() {
    if (!auth) {
        alert("Firebase não configurado. Por favor, adicione suas credenciais no js/auth.js");
        return;
    }
    try {
        await auth.signInWithPopup(githubProvider);
        if (typeof closeModal === 'function') {
            closeModal('loginOverlay');
            closeModal('modal-login');
        }
    } catch (error) {
        console.warn("Popup blocked or failed, trying redirect flow...", error);
        try {
            await auth.signInWithRedirect(githubProvider);
        } catch (err) {
            console.error("Erro ao fazer login com GitHub:", err);
            alert("Erro ao iniciar login: " + err.message);
        }
    }
}

async function logout() {
    if (auth) {
        await auth.signOut();
        window.location.reload();
    }
}

// Interceptar o botão de request
function handleRequestButtonClick(event) {
    if (event && event.altKey) {
        window.location.href = 'admin.html';
        return;
    }
    
    if (currentUser) {
        if (typeof openModal === 'function') openModal('requestOverlay');
    } else {
        if (typeof openModal === 'function') openModal('loginOverlay');
    }
}

let userProfileData = null;

async function fetchUserProfile() {
    if (!currentUser) return;
    try {
        const token = await currentUser.getIdToken();
        const res = await fetch(`${API_URL}/api/user/profile`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (res.ok) {
            userProfileData = await res.json();
            if (userProfileData && userProfileData.role === 'admin') {
                window.isAdmin = true;
                const adminBtn = document.getElementById('menu-admin-publish');
                if (adminBtn) adminBtn.classList.remove('hidden');
            }
            // Update UI with newly loaded profile
            updateAuthUI(currentUser);
            if (typeof syncFavoritesUI === 'function') {
                syncFavoritesUI();
            }
        } else {
            userProfileData = {};
        }
    } catch (e) {
        userProfileData = {};
    }
}

function openProfileModal() {
    if (!userProfileData) {
        alert('Profile still loading, please try again.');
        return;
    }
    // Close settings if open
    closeModal('modal-settings');

    const modal = document.getElementById('modal-profile');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('show');
    }
    
    document.getElementById('profile-edit-name').value = userProfileData.display_name || '';
    document.getElementById('profile-edit-avatar-preview').src = userProfileData.avatar_url || 'https://via.placeholder.com/64';
    document.getElementById('profile-edit-langs').value = userProfileData.languages || '';
    document.getElementById('profile-edit-site').value = userProfileData.website || '';
    document.getElementById('profile-edit-donations').value = userProfileData.donation_links || '';
    
    // Switch to first tab by default
    const firstTabBtn = document.querySelector('.profile-tab');
    if (firstTabBtn) {
        switchProfileTab('edit-profile-fields', firstTabBtn);
    }
}

async function saveProfile() {
    if (!currentUser) return;
    
    const btn = document.getElementById('btn-save-profile');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
    
    const data = {
        display_name: document.getElementById('profile-edit-name').value,
        avatar_url: document.getElementById('profile-edit-avatar-preview').src,
        languages: document.getElementById('profile-edit-langs').value,
        website: document.getElementById('profile-edit-site').value,
        donation_links: document.getElementById('profile-edit-donations').value
    };
    
    try {
        const token = await currentUser.getIdToken();
        const res = await fetch(`${API_URL}/api/user/profile`, {
            method: 'PUT',
            headers: { 
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            alert('Profile saved successfully!');
            closeModal('modal-profile');
            await fetchUserProfile(); // recarrega
            updateAuthUI(currentUser); // re-renderiza o avatar
        } else {
            alert('Error saving profile.');
        }
    } catch (e) {
        alert('Connection error while saving profile.');
    } finally {
        btn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Save Changes';
    }
}

function openSettingsModal() {
    // Close profile if open
    closeModal('modal-profile');

    const modal = document.getElementById('modal-settings');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('show');
    }
}

window.handleAvatarUpload = function(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            const canvas = document.createElement('canvas');
            const MAX_SIZE = 150; // Limitar tamanho para não estourar base64
            let width = img.width;
            let height = img.height;
            
            if (width > height) {
                if (width > MAX_SIZE) {
                    height *= MAX_SIZE / width;
                    width = MAX_SIZE;
                }
            } else {
                if (height > MAX_SIZE) {
                    width *= MAX_SIZE / height;
                    height = MAX_SIZE;
                }
            }
            
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            
            // Converter para base64 JPEG com qualidade 80%
            const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
            document.getElementById('profile-edit-avatar-preview').src = dataUrl;
        }
        img.src = e.target.result;
    }
    reader.readAsDataURL(file);
}

// DYNAMIC MODALS AND DROPDOWN INJECTION

function injectProfileDropdown() {
    const topbarRight = document.querySelector('.topbar-right');
    if (topbarRight && !document.getElementById('user-profile-dropdown')) {
        const dropdownHtml = `
            <div id="user-profile-dropdown" class="hidden" style="position: relative; display: inline-block; margin-left: 8px; vertical-align: middle;">
                <div id="profile-menu" class="profile-menu" style="position: absolute; right: 0; top: 45px; background: var(--bg-card, #121214); border: 1px solid var(--border-color, #29292c); border-radius: 8px; padding: 8px 0; width: 200px; display: none; flex-direction: column; box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 1000;">
                    <div style="padding: 12px; text-align: center; border-bottom: 1px solid var(--border-color, #29292c); margin-bottom: 8px;">
                        <strong id="menu-user-name" style="color: var(--text, #ededed);">User</strong><br>
                        <span id="menu-user-email" style="font-size: 0.75rem; color: var(--text-muted, #a1a1a5); word-break: break-all;">email</span>
                    </div>
                    <a href="#" onclick="openProfileModal(); return false;" style="padding: 8px 16px; color: var(--text, #ededed); text-decoration: none; display: flex; align-items: center; gap: 8px; font-size: 13px;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'"><i class="ph ph-user-circle" style="font-size: 16px;"></i> Edit Profile</a>
                    <a href="#" onclick="openSettingsModal(); return false;" style="padding: 8px 16px; color: var(--text, #ededed); text-decoration: none; display: flex; align-items: center; gap: 8px; font-size: 13px;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'"><i class="ph ph-gear" style="font-size: 16px;"></i> Settings</a>
                    <hr style="border: none; border-top: 1px solid var(--border-color, #29292c); margin: 6px 0;">
                    <button onclick="logout()" style="padding: 8px 16px; background: transparent; border: none; color: #ff4d4d; width: 100%; text-align: left; display: flex; align-items: center; gap: 8px; font-size: 13px; cursor: pointer; font-family: inherit;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'"><i class="ph ph-sign-out" style="font-size: 16px;"></i> Logout</button>
                </div>
            </div>
        `;
        topbarRight.insertAdjacentHTML('beforeend', dropdownHtml);
    }
}

function injectProfileModals() {
    if (!document.getElementById('modal-profile')) {
        const modalsHtml = `
            <!-- Profile Modal Drawer -->
            <div id="modal-profile" class="modal" onclick="if(event.target===this)closeModal('modal-profile')" style="position: fixed; top: 0; right: 0; left: auto; width: 100%; max-width: 440px; height: 100vh; background: rgba(10,10,11,0.75); z-index: 10000; display: none; align-items: stretch; justify-content: flex-end; backdrop-filter: blur(8px); font-family: system-ui, -apple-system, sans-serif;">
                <div class="modal-content" style="width: 100%; height: 100vh; background: var(--bg-card, #121214); border-left: 1px solid var(--border-color, #29292c); border-radius: 0; padding: 2rem; overflow-y: auto; position: relative; box-shadow: -10px 0 30px rgba(0,0,0,0.5);">
                    <span class="close-btn" onclick="closeModal('modal-profile')" style="position: absolute; right: 20px; top: 20px; font-size: 24px; color: var(--text-muted); cursor: pointer;">&times;</span>
                    
                    <h2 style="font-family: var(--mono); color: var(--text); margin-bottom: 1.5rem; font-size: 1.4rem; text-align: left;">User Profile</h2>
                    
                    <div class="profile-tabs" style="display: flex; gap: 8px; border-bottom: 1px solid var(--border-color, #29292c); padding-bottom: 8px; margin-bottom: 1.5rem;">
                        <button class="profile-tab active" onclick="switchProfileTab('edit-profile-fields', this)" style="background: transparent; border: none; color: var(--green); border-bottom: 2px solid var(--green); font-family: var(--mono); font-weight: bold; cursor: pointer; padding: 6px 12px; font-size: 13px;">Edit Profile</button>
                        <button class="profile-tab" onclick="switchProfileTab('favorites-list-tab', this)" style="background: transparent; border: none; color: var(--text-muted); font-family: var(--mono); cursor: pointer; padding: 6px 12px; font-size: 13px;">My Favorites</button>
                    </div>

                    <div id="edit-profile-fields" class="profile-tab-content">
                        <div style="display: flex; flex-direction: column; gap: 1rem; text-align: left;">
                            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                                <img id="profile-edit-avatar-preview" src="https://via.placeholder.com/64" style="width:64px; height:64px; border-radius:50%; border:2px solid var(--accent-green); object-fit: cover;">
                                <div style="flex: 1;">
                                    <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">Profile Picture</label>
                                    <input type="file" id="profile-edit-avatar" accept="image/*" class="search-bar" style="width: 100%; box-sizing: border-box; padding: 0.5rem; background: var(--surface); border: 1px solid var(--border-2); border-radius: var(--r); color: var(--text);" onchange="handleAvatarUpload(event)">
                                </div>
                            </div>

                            <div>
                                <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">Display Name</label>
                                <input type="text" id="profile-edit-name" class="search-bar" placeholder="Your display name" style="width: 100%; box-sizing: border-box; background: var(--surface); border: 1px solid var(--border-2); border-radius: var(--r); padding: 8px 12px; color: var(--text); font-family: inherit;">
                            </div>
                            
                            <div>
                                <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">Languages (e.g. C++, Lua, C#)</label>
                                <input type="text" id="profile-edit-langs" class="search-bar" placeholder="Languages you write" style="width: 100%; box-sizing: border-box; background: var(--surface); border: 1px solid var(--border-2); border-radius: var(--r); padding: 8px 12px; color: var(--text); font-family: inherit;">
                            </div>
                            
                            <div>
                                <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">Website / Portfolio</label>
                                <input type="text" id="profile-edit-site" class="search-bar" placeholder="https://yourpage.com" style="width: 100%; box-sizing: border-box; background: var(--surface); border: 1px solid var(--border-2); border-radius: var(--r); padding: 8px 12px; color: var(--text); font-family: inherit;">
                            </div>
                            
                            <div>
                                <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.3rem;">Donation Links (Patreon, Ko-fi, PayPal)</label>
                                <input type="text" id="profile-edit-donations" class="search-bar" placeholder="Comma separated, e.g. https://ko-fi.com/user" style="width: 100%; box-sizing: border-box; background: var(--surface); border: 1px solid var(--border-2); border-radius: var(--r); padding: 8px 12px; color: var(--text); font-family: inherit;">
                            </div>

                            <button id="btn-save-profile" class="btn-primary" onclick="saveProfile()" style="justify-content: center; margin-top: 1rem; width: 100%;">
                                <i class="ph ph-floppy-disk" style="font-size: 16px;"></i> Save Changes
                            </button>
                        </div>
                    </div>

                    <div id="favorites-list-tab" class="profile-tab-content" style="display: none;">
                        <div id="favorites-container" style="max-height: calc(100vh - 200px); overflow-y: auto; display: flex; flex-direction: column; gap: 8px; margin-top: 0.5rem; text-align: left;">
                            <!-- Dynamically populated favorites -->
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Settings Modal Drawer -->
            <div id="modal-settings" class="modal" onclick="if(event.target===this)closeModal('modal-settings')" style="position: fixed; top: 0; right: 0; left: auto; width: 100%; max-width: 380px; height: 100vh; background: rgba(10,10,11,0.75); z-index: 10000; display: none; align-items: stretch; justify-content: flex-end; backdrop-filter: blur(8px); font-family: system-ui, -apple-system, sans-serif;">
                <div class="modal-content" style="width: 100%; height: 100vh; background: var(--bg-card, #121214); border-left: 1px solid var(--border-color, #29292c); border-radius: 0; padding: 2rem; overflow-y: auto; position: relative; box-shadow: -10px 0 30px rgba(0,0,0,0.5);">
                    <span class="close-btn" onclick="closeModal('modal-settings')" style="position: absolute; right: 20px; top: 20px; font-size: 24px; color: var(--text-muted); cursor: pointer;">&times;</span>
                    <h2 style="font-family: var(--mono); color: var(--text); margin-bottom: 1.5rem; font-size: 1.4rem; text-align: left;">Settings</h2>
                    <div style="display: flex; flex-direction: column; gap: 1rem; text-align: left;">
                        <div>
                            <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.5rem;">Language / Idioma</label>
                            <select id="settings-lang-select" class="filter-select" style="width: 100%; background: var(--surface); border: 1px solid var(--border-2); border-radius: var(--r); padding: 8px 12px; color: var(--text);" onchange="changeLanguage(this.value)">
                                <option value="pt-BR">Português (Brasil)</option>
                                <option value="en" selected>English</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalsHtml);
    }
}

window.switchProfileTab = function(tabId, tabButton) {
    document.querySelectorAll('.profile-tab-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.profile-tab').forEach(el => {
        el.style.color = 'var(--text-muted)';
        el.style.borderBottom = 'none';
    });
    
    const activeContent = document.getElementById(tabId);
    if (activeContent) activeContent.style.display = 'block';
    
    tabButton.style.color = 'var(--green)';
    tabButton.style.borderBottom = '2px solid var(--green)';
    
    if (tabId === 'favorites-list-tab') {
        renderProfileFavorites();
    }
}

function renderProfileFavorites() {
    const container = document.getElementById('favorites-container');
    if (!container) return;

    container.innerHTML = '';
    
    if (!userProfileData || !userProfileData.favorites || userProfileData.favorites.length === 0) {
        container.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 1.5rem; font-family: var(--mono); font-size: 12px;">No favorites saved yet.</div>`;
        return;
    }

    const catalog = window.projectsData || [];
    
    userProfileData.favorites.forEach(id => {
        const proj = catalog.find(p => p.id == id);
        if (!proj) return;

        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.alignItems = 'center';
        row.style.justifyContent = 'space-between';
        row.style.padding = '8px 12px';
        row.style.background = 'rgba(255,255,255,0.03)';
        row.style.border = '1px solid var(--border-color, #29292c)';
        row.style.borderRadius = '8px';

        row.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 10px; color: var(--green); font-family: var(--mono); background: rgba(0, 230, 118, 0.08); padding: 2px 6px; border-radius: 4px;">${proj.category}</span>
                <a href="project.html?id=${proj.id}" style="color: var(--text); font-weight: 600; text-decoration: none; font-size: 13px;" onclick="closeModal('modal-profile')">${proj.title}</a>
            </div>
            <button onclick="removeFavoriteFromProfile(event, ${proj.id})" style="background: transparent; border: none; color: #ff4d4d; cursor: pointer; padding: 4px;" title="Remove from favorites"><i class="ph ph-trash" style="font-size: 16px;"></i></button>
        `;
        container.appendChild(row);
    });
}

window.toggleFavorite = async function(event, projectId, buttonElement) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    if (!currentUser) {
        if (typeof openModal === 'function') {
            openModal('loginOverlay');
        } else {
            const overlay = document.getElementById('loginOverlay');
            if (overlay) overlay.style.display = 'flex';
        }
        return;
    }

    if (!userProfileData) userProfileData = { favorites: [] };
    if (!userProfileData.favorites) userProfileData.favorites = [];
    
    try {
        const token = await currentUser.getIdToken();
        const res = await fetch(`${API_URL}/api/user/favorites`, {
            method: 'POST',
            headers: { 
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_id: projectId })
        });
        
        if (res.ok) {
            const data = await res.json();
            const isAdded = data.status === 'added';
            
            if (isAdded) {
                if (!userProfileData.favorites.some(id => id == projectId)) {
                    userProfileData.favorites.push(projectId);
                }
            } else {
                userProfileData.favorites = userProfileData.favorites.filter(id => id != projectId);
            }
            
            // Update button element UI if provided
            if (buttonElement) {
                buttonElement.style.transition = 'transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                buttonElement.style.transform = 'scale(1.35)';
                setTimeout(() => { buttonElement.style.transform = 'scale(1)'; }, 200);

                if (buttonElement.id === 'btn-project-star') {
                    const icon = buttonElement.querySelector('i');
                    if (isAdded) {
                        buttonElement.style.color = '#fbbf24';
                        buttonElement.title = 'Remove from Favorites';
                        if (icon) icon.className = 'ph-fill ph-star';
                    } else {
                        buttonElement.style.color = 'var(--text-muted)';
                        buttonElement.title = 'Add to Favorites';
                        if (icon) icon.className = 'ph ph-star';
                    }
                } else {
                    if (isAdded) {
                        buttonElement.classList.add('saved');
                        buttonElement.textContent = '✓';
                    } else {
                        buttonElement.classList.remove('saved');
                        buttonElement.textContent = '+';
                    }
                }
            }
            
            if (typeof showToast === 'function') {
                showToast(isAdded ? 'Added to your favorites!' : 'Removed from your favorites', 'info');
            }
            
            // Trigger global syncs
            if (typeof syncFavoritesUI === 'function') {
                syncFavoritesUI();
            }
        }
    } catch (e) {
        console.error('Error toggling favorite:', e);
    }
}

window.removeFavoriteFromProfile = async function(event, projectId) {
    event.preventDefault();
    event.stopPropagation();
    
    if (!currentUser) return;
    
    try {
        const token = await currentUser.getIdToken();
        const res = await fetch(`${API_URL}/api/user/favorites`, {
            method: 'POST',
            headers: { 
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_id: projectId })
        });
        
        if (res.ok) {
            if (userProfileData && userProfileData.favorites) {
                userProfileData.favorites = userProfileData.favorites.filter(id => id != projectId);
            }
            renderProfileFavorites();
            
            // Also notify any index pages to update heart icons
            if (typeof syncFavoritesUI === 'function') syncFavoritesUI();
            if (typeof renderCatalog === 'function') renderCatalog();
            if (typeof renderGrid === 'function') renderGrid();
        }
    } catch (e) {
        console.error('Error removing favorite:', e);
    }
}

// UNIFIED SEND REQUEST FUNCTION (Shared globally)
async function sendRequest() {
    const titleEl = document.getElementById('req-title');
    const linkEl = document.getElementById('req-link');
    const descEl = document.getElementById('req-desc');
    const msgBox = document.getElementById('req-msg');
    
    if (!titleEl) return;
    const title = titleEl.value.trim();
    const link = linkEl ? linkEl.value.trim() : '';
    const desc = descEl ? descEl.value.trim() : '';

    if (!title) {
        if (msgBox) {
            msgBox.style.color = '#ff4d4d';
            msgBox.innerText = 'Please enter the project name.';
        }
        return;
    }
    
    const btn = document.querySelector('#requestOverlay .btn-green-sm') || document.querySelector('#modal-request .btn-primary') || document.querySelector('#requestOverlay button[onclick*="sendRequest"]');
    const oldHtml = btn ? btn.innerHTML : 'submit request';
    if (btn) {
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
        btn.style.pointerEvents = 'none';
    }
    
    try {
        let token = "";
        if (auth && auth.currentUser) {
            token = await auth.currentUser.getIdToken();
        }

        const res = await fetch(`${API_URL}/api/request`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` 
            },
            body: JSON.stringify({ title, link, desc })
        });
        
        const data = await res.json();
        
        if (!res.ok) {
            throw new Error(data.error || "Error sending request.");
        }
        
        if (msgBox) {
            msgBox.style.color = 'var(--accent-green)';
            msgBox.innerText = 'Request submitted successfully!';
        }
        
        // Clear fields
        titleEl.value = '';
        if (linkEl) linkEl.value = '';
        if (descEl) descEl.value = '';
        
        setTimeout(() => {
            closeModal('requestOverlay');
            closeModal('modal-request');
            if (msgBox) msgBox.innerText = '';
        }, 2000);
        
    } catch (e) {
        if (msgBox) {
            msgBox.style.color = '#ff4d4d';
            msgBox.innerText = e.message;
        }
    } finally {
        if (btn) {
            btn.innerHTML = oldHtml;
            btn.style.pointerEvents = 'auto';
        }
    }
}

// Global modal open/close override/wrapper to handle the flex display
const originalCloseModal = window.closeModal;
window.closeModal = function(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = 'none';
        el.classList.remove('show', 'open');
    }
    if (typeof originalCloseModal === 'function') {
        try {
            originalCloseModal(id);
        } catch(e) {}
    }
};

window.openModal = function(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = 'flex';
        el.classList.add('open', 'show');
    }
};

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal, .overlay').forEach(m => {
            m.style.display = 'none';
            m.classList.remove('show', 'open');
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    injectProfileDropdown();
    injectProfileModals();
});
