import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('src="js/api.js"', 'src="js/api.js?v=2"')
    content = content.replace('src="js/main.js"', 'src="js/main.js?v=2"')
    content = content.replace('src="js/theme.js"', 'src="js/theme.js?v=2"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
