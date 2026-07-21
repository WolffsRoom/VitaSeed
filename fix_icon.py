import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace ph ph-question with fa-solid fa-question (FontAwesome is already loaded)
    html = html.replace(
        '<i class="ph ph-question" style="font-size: 1.2rem;"></i>',
        '<i class="fa-solid fa-question"></i>'
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
