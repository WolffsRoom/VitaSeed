import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'modal-about' not in html:
        continue

    # 1. Update "Sobre" description
    html = html.replace(
        '''O VitaSeed é o seu diretório definitivo para a cena homebrew do PSVita. 
                Aqui centralizamos Ports, Mods, Traduções, Plugins, Apps e Ferramentas, 
                garantindo que você sempre tenha acesso às versões mais atualizadas.''',
        '''O VitaSeed é um centralizador para a cena brasileira homebrew do PSVita. Aqui centralizamos Ports, Mods, Traduções, Plugins, Apps e Ferramentas, garantindo um acesso centralizado.'''
    )

    # 2. Remove the IP limit text from Request modal
    html = html.replace(
        'Não encontrou o que procurava? Envie um request para adicionarmos o projeto ao catálogo! (Limite: 2 envios por dia por IP)',
        'Não encontrou o que procurava? Envie um request para adicionarmos o projeto ao catálogo!'
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# 2. Update modal CSS for better centering and look
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the modal CSS block entirely for better centered styling
old_modal_css = '''.modal {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    display: flex; align-items: center; justify-content: center;
    z-index: 9999;
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease;
}
.modal.show {
    opacity: 1; pointer-events: auto;
}
.modal-content {
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    padding: 2rem;
    border-radius: 12px;
    width: 90%; max-width: 500px;
    position: relative;
    transform: translateY(20px);
    transition: transform 0.3s ease;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}
.modal.show .modal-content {
    transform: translateY(0);
}
.close-btn {
    position: absolute;
    top: 1rem; right: 1.5rem;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-muted);
}
.close-btn:hover { color: white; }'''

new_modal_css = '''.modal {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex; align-items: center; justify-content: center;
    z-index: 9999;
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease;
    padding: 1rem;
    box-sizing: border-box;
}
.modal.show {
    opacity: 1; pointer-events: auto;
}
.modal-content {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    width: 100%; max-width: 480px;
    position: relative;
    transform: translateY(24px) scale(0.97);
    transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    text-align: center;
}
.modal.show .modal-content {
    transform: translateY(0) scale(1);
}
.modal-content h2 {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
}
.close-btn {
    position: absolute;
    top: 1rem; right: 1.25rem;
    font-size: 1.4rem;
    cursor: pointer;
    color: var(--text-muted);
    line-height: 1;
    transition: color 0.2s;
}
.close-btn:hover { color: white; }'''

css = css.replace(old_modal_css, new_modal_css)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

import glob as g
for file in g.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('css/style.css?v=28', 'css/style.css?v=29')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
