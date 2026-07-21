// JS para gerenciar a AutenticaÃ§Ã£o com Firebase
// IMPORTANTE: O usuÃ¡rio deve substituir essa configuraÃ§Ã£o pelas credenciais do seu projeto Firebase.
const firebaseConfig = {
  apiKey: "AIzaSyD5dyoPLWh5mav-qtdW5FNgreBJVGOcGYI",
  authDomain: "vitaseed.firebaseapp.com",
  projectId: "vitaseed",
  storageBucket: "vitaseed.firebasestorage.app",
  messagingSenderId: "263996368866",
  appId: "1:263996368866:web:d8661f2d7679523a303bbb",
  measurementId: "G-WQSEM2JV93"
};
// Se as chaves nÃ£o foram preenchidas, nÃ£o inicializa para evitar erros
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
}

function updateAuthUI(user) {
    const dropdownContainers = document.querySelectorAll('#user-profile-dropdown');
    const requestBtns = document.querySelectorAll('#btn-request');
    
    if (user) {
        const avatarHtml = `<img src="${user.photoURL || 'https://via.placeholder.com/32'}" alt="Avatar" style="width:36px; height:36px; border-radius:50%; border:2px solid var(--accent-green); cursor:pointer;" onclick="toggleProfileMenu(event)" title="OpÃ§Ãµes da Conta">`;
        
        dropdownContainers.forEach(container => {
            container.classList.remove('hidden');
            // Insert avatar before the menu
            let avatarImg = container.querySelector('img');
            if (!avatarImg) {
                container.insertAdjacentHTML('afterbegin', avatarHtml);
            } else {
                avatarImg.src = user.photoURL || 'https://via.placeholder.com/32';
            }
            
            const menuName = container.querySelector('#menu-user-name');
            const menuEmail = container.querySelector('#menu-user-email');
            if(menuName) menuName.innerText = user.displayName || 'Viteiro';
            if(menuEmail) menuEmail.innerText = user.email || '';
        });
        
        // Destravar botÃµes de Request
        requestBtns.forEach(btn => {
            btn.innerHTML = `<i class="ph ph-paper-plane-tilt"></i> Request`;
            btn.classList.remove('btn-locked');
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        });

    } else {
        dropdownContainers.forEach(container => container.classList.add('hidden'));
        
        // Travar botÃµes de Request
        requestBtns.forEach(btn => {
            btn.innerHTML = `<i class="fa-solid fa-right-to-bracket"></i> Login`;
            btn.classList.add('btn-locked');
            btn.style.opacity = '0.5';
            btn.style.cursor = 'pointer';
        });
    }
}

function toggleProfileMenu(event) {
    event.stopPropagation();
    const menu = event.target.nextElementSibling;
    if(menu && menu.classList.contains('profile-menu')) {
        menu.classList.toggle('show');
    }
}

// Fechar dropdown ao clicar fora
document.addEventListener('click', (e) => {
    const menus = document.querySelectorAll('.profile-menu.show');
    menus.forEach(menu => {
        if(!menu.contains(e.target)) {
            menu.classList.remove('show');
        }
    });
});

async function loginWithGoogle() {
    if (!auth) {
        alert("Firebase nÃ£o configurado. Por favor, adicione suas credenciais no js/auth.js");
        return;
    }
    try {
        await auth.signInWithPopup(googleProvider);
        closeModal('modal-login');
    } catch (error) {
        console.error("Erro ao fazer login:", error);
        alert("Erro ao fazer login. Tente novamente.");
    }
}

async function loginWithGitHub() {
    if (!auth) {
        alert("Firebase nÃ£o configurado. Por favor, adicione suas credenciais no js/auth.js");
        return;
    }
    try {
        await auth.signInWithPopup(githubProvider);
        closeModal('modal-login');
    } catch (error) {
        console.error("Erro ao fazer login com GitHub:", error);
        alert("Erro ao fazer login. Tente novamente.");
    }
}

async function logout() {
    if (auth) {
        await auth.signOut();
    }
}

// Interceptar o botÃ£o de request
function handleRequestButtonClick(event) {
    if (event.altKey) {
        window.location.href = 'admin.html';
        return;
    }
    
    if (currentUser) {
        document.getElementById('modal-request').classList.add('show');
    } else {
        document.getElementById('modal-login').classList.add('show');
    }
}

let userProfileData = null;

async function fetchUserProfile() {
    if (!currentUser) return;
    try {
        const token = await currentUser.getIdToken();
        const res = await fetch(\\/api/user/profile\, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (res.ok) {
            userProfileData = await res.json();
            // Store global role to check admin
            currentUser.dbRole = userProfileData.role;
            if (userProfileData.role === 'admin') {
                const adminBtn = document.getElementById('menu-admin-publish');
                if (adminBtn) adminBtn.classList.remove('hidden');
            }
        }
    } catch (e) {
        console.error('Erro ao buscar perfil', e);
    }
}

function openProfileModal() {
    if (!userProfileData) {
        alert('Perfil ainda carregando, tente novamente.');
        return;
    }
    document.getElementById('profile-edit-name').value = userProfileData.display_name || '';
    document.getElementById('profile-edit-avatar').value = userProfileData.avatar_url || '';
    document.getElementById('profile-edit-avatar-preview').src = userProfileData.avatar_url || 'https://via.placeholder.com/64';
    document.getElementById('profile-edit-langs').value = userProfileData.languages || '';
    document.getElementById('profile-edit-site').value = userProfileData.website || '';
    document.getElementById('profile-edit-donations').value = userProfileData.donation_links || '';
    
    document.getElementById('modal-profile').classList.add('show');
}

async function saveProfile() {
    if (!currentUser) return;
    
    const btn = document.getElementById('btn-save-profile');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Salvando...';
    
    const data = {
        display_name: document.getElementById('profile-edit-name').value,
        avatar_url: document.getElementById('profile-edit-avatar').value,
        languages: document.getElementById('profile-edit-langs').value,
        website: document.getElementById('profile-edit-site').value,
        donation_links: document.getElementById('profile-edit-donations').value
    };
    
    try {
        const token = await currentUser.getIdToken();
        const res = await fetch(\\/api/user/profile\, {
            method: 'PUT',
            headers: { 
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            alert('Perfil salvo com sucesso!');
            closeModal('modal-profile');
            await fetchUserProfile(); // recarrega
            updateAuthUI(currentUser); // re-renderiza o avatar
        } else {
            alert('Erro ao salvar perfil.');
        }
    } catch (e) {
        alert('Erro de conexão ao salvar perfil.');
    } finally {
        btn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Salvar Alterações';
    }
}

function openSettingsModal() {
    document.getElementById('modal-settings').classList.add('show');
}
