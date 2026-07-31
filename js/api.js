window.fetchCatalog = async function() {
    if (window.projectsData) return window.projectsData;
    try {
        const res = await fetch('api/catalog.json');
        if (!res.ok) throw new Error('Falha ao baixar o catálogo');
        const data = await res.json();
        window.projectsData = data.projects;
        return window.projectsData;
    } catch (e) {
        console.warn("API/CORS fetch fallbacked (File Protocol):", e);
        if (window.catalogFallbackData) {
            window.projectsData = window.catalogFallbackData;
            return window.projectsData;
        }
        return [];
    }
}

window.formatTitle = function(title) {
    if (!title) return "";
    return title.replace(/(\([^)]+\)|\[[^\]]+\])/g, '<span style="font-weight: 400; font-size: 0.85em;">$1</span>');
};
