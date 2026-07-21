// JS para gerenciar a Autenticação com Firebase
// IMPORTANTE: O usuário deve substituir essa configuração pelas credenciais do seu projeto Firebase.
const firebaseConfig = {
    apiKey: "Sua_API_Key_Aqui",
    authDomain: "seu-projeto.firebaseapp.com",
    projectId: "seu-projeto",
    storageBucket: "seu-projeto.firebasestorage.app",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef"
};

// Se as chaves não foram preenchidas, não inicializa para evitar erros
let auth = null;
let provider = null;
let currentUser = null;

if (firebaseConfig.apiKey !== "Sua_API_Key_Aqui") {
    // Inicializar Firebase
    const app = firebase.initializeApp(firebaseConfig);
    auth = firebase.auth();
    provider = new firebase.auth.GoogleAuthProvider();

    auth.onAuthStateChanged((user) => {
        currentUser = user;
        updateAuthUI(user);
    });
}

function updateAuthUI(user) {
    const loginBtn = document.getElementById('login-btn');
    const userProfile = document.getElementById('user-profile');
    
    if (user) {
        if (loginBtn) loginBtn.classList.add('hidden');
        if (userProfile) {
            userProfile.classList.remove('hidden');
            userProfile.innerHTML = `<img src="${user.photoURL}" alt="Avatar" style="width:32px; height:32px; border-radius:50%; border:2px solid var(--accent-green); cursor:pointer;" onclick="logout()" title="Clique para sair">`;
        }
    } else {
        if (loginBtn) loginBtn.classList.remove('hidden');
        if (userProfile) userProfile.classList.add('hidden');
    }
}

async function loginWithGoogle() {
    if (!auth) {
        alert("Firebase não configurado. Por favor, adicione suas credenciais no js/auth.js");
        return;
    }
    try {
        await auth.signInWithPopup(provider);
        closeModal('modal-login');
    } catch (error) {
        console.error("Erro ao fazer login:", error);
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
