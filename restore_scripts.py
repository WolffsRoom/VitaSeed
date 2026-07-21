import glob
for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'js/api.js' not in content:
        content = content.replace('<script src="js/i18n.js"></script>', '<script src="js/api.js"></script>\n    <script src="js/theme.js"></script>\n    <script src="js/i18n.js"></script>')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
