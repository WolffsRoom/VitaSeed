import glob

# 1. Remove data.js from all HTML files
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<script src="js/data.js' in content:
        import re
        content = re.sub(r'<script src="js/data\.js[^>]+></script>\n?', '', content)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

# 2. Make projectsData global in main.js
with open('js/main.js', 'r', encoding='utf-8') as f:
    main_content = f.read()

main_content = main_content.replace('const projectsData = await window.fetchCatalog();', 'window.projectsData = await window.fetchCatalog();\n    const projectsData = window.projectsData;')
with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(main_content)

# 3. Update style.css for sony theme background
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'https://t2.tudocdn.net/388054?w=1920&h=1080' in css:
    css = css.replace("url('https://t2.tudocdn.net/388054?w=1920&h=1080')", "url('../assets/sony_bg.jpg')")
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

print("Fixes applied.")
