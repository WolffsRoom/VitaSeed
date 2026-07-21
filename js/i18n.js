const translations = {
    "pt-BR": {
        "menu_home": "Home",
        "menu_library": "Biblioteca (Em breve)",
        "menu_top10": "Top 10 do Mês",
        "menu_colab": "Colaboradores",
        "menu_login": "Login",
        "search_placeholder": "Buscar por título ou responsável...",
        "filter_all": "Todas as Categorias",
        "btn_request": "Request",
        "btn_login": "Login",
        "about_title": "Sobre o VitaSeed",
        "about_desc": "O VitaSeed é um centralizador para a cena brasileira homebrew do PSVita. Aqui centralizamos Ports, Mods, Traduções, Plugins, Apps e Ferramentas, garantindo um acesso centralizado.",
        "request_title": "Solicitar Projeto",
        "request_desc": "Não encontrou o que procurava?<br>Envie um request para adicionarmos o projeto ao catálogo!",
        "request_name": "Nome do Projeto / Jogo",
        "request_link": "Link (Opcional)",
        "request_reason": "Por que devemos adicionar?",
        "btn_send": "Enviar Request",
        "profile_edit": "Editar Perfil",
        "profile_projects": "Meus Projetos",
        "profile_settings": "Configurações",
        "profile_logout": "Sair",
        "settings_title": "Configurações",
        "settings_lang": "Idioma do Site",
        "btn_save": "Salvar Alterações"
    },
    "en": {
        "menu_home": "Home",
        "menu_library": "Library (Soon)",
        "menu_top10": "Top 10 of the Month",
        "menu_colab": "Collaborators",
        "menu_login": "Login",
        "search_placeholder": "Search by title or author...",
        "filter_all": "All Categories",
        "btn_request": "Request",
        "btn_login": "Login",
        "about_title": "About VitaSeed",
        "about_desc": "VitaSeed is a centralized hub for the PSVita homebrew scene. We index Ports, Mods, Translations, Plugins, Apps, and Tools to guarantee easy access for everyone.",
        "request_title": "Request Project",
        "request_desc": "Didn't find what you were looking for?<br>Send a request to add it to the catalog!",
        "request_name": "Project / Game Name",
        "request_link": "Link (Optional)",
        "request_reason": "Why should we add this?",
        "btn_send": "Send Request",
        "profile_edit": "Edit Profile",
        "profile_projects": "My Projects",
        "profile_settings": "Settings",
        "profile_logout": "Logout",
        "settings_title": "Settings",
        "settings_lang": "Site Language",
        "btn_save": "Save Changes"
    }
};

let currentLang = localStorage.getItem('vitaseed_lang') || 'pt-BR';

function changeLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    localStorage.setItem('vitaseed_lang', lang);
    applyTranslations();
}

function applyTranslations() {
    const dict = translations[currentLang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            if (el.tagName === 'INPUT' && el.type === 'text') {
                el.placeholder = dict[key];
            } else {
                el.innerHTML = dict[key];
            }
        }
    });
    
    // Also trigger catalog re-render if data.js is loaded
    if (typeof renderCatalog === 'function') {
        renderCatalog();
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    applyTranslations();
    const select = document.getElementById('settings-lang-select');
    if (select) select.value = currentLang;
    const selectMain = document.getElementById('settings-lang-select-main');
    if (selectMain) selectMain.value = currentLang;
});
