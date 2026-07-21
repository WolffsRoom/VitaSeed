import glob

old_string = '<span>Colaborações</span>'
new_string = '<span>COLABORAÇÕES</span>'

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_string in content:
        content = content.replace(old_string, new_string)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
