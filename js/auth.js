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
    });
}

function updateAuthUI(user) {
    const loginBtn = document.getElementById('login-btn');
    const userProfile = document.getElementById('user-profile');
    const trLoginBtn = document.getElementById('tr-login-btn');
    const trUserAvatar = document.getElementById('tr-user-avatar');
    
    // Atualizar botões de Request
    const requestBtns = document.querySelectorAll('#btn-request');
    
    if (user) {
        if (loginBtn) loginBtn.classList.add('hidden');
        if (trLoginBtn) trLoginBtn.classList.add('hidden');
        
        const avatarHtml = `<img src="${user.photoURL || 'https://via.placeholder.com/32'}" alt="Avatar" style="width:28px; height:28px; border-radius:50%; border:2px solid var(--accent-green); cursor:pointer;" onclick="logout()" title="Clique para sair">`;
        
        if (userProfile) {
            userProfile.classList.remove('hidden');
            userProfile.innerHTML = avatarHtml;
        }
        
        if (trUserAvatar) {
            trUserAvatar.classList.remove('hidden');
            trUserAvatar.innerHTML = avatarHtml + `<span>${user.displayName ? user.displayName.split(' ')[0] : 'Viteiro'}</span>`;
        }
        
        // Destravar botões de Request
        requestBtns.forEach(btn => {
            btn.innerHTML = `<i class="ph ph-paper-plane-tilt"></i> Request`;
            btn.classList.remove('btn-locked');
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        });

    } else {
        if (loginBtn) loginBtn.classList.remove('hidden');
        if (userProfile) userProfile.classList.add('hidden');
        if (trLoginBtn) trLoginBtn.classList.remove('hidden');
        if (trUserAvatar) trUserAvatar.classList.add('hidden');
        
        // Travar botões de Request
        requestBtns.forEach(btn => {
            btn.innerHTML = `<i class="fa-solid fa-lock"></i> Entrar para Request`;
            btn.classList.add('btn-locked');
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        });
    }
}

async function loginWithGoogle() {
    if (!auth) {
        alert("Firebase não configurado. Por favor, adicione suas credenciais no js/auth.js");
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
        alert("Firebase não configurado. Por favor, adicione suas credenciais no js/auth.js");
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

// Interceptar o botão de request
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
