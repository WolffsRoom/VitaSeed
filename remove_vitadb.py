import glob

for file in glob.glob('*.html'):
    if file == 'admin.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the line containing VitaDB link and remove it
    lines = content.split('\n')
    new_lines = [line for line in lines if 'https://www.rinnegatamante.eu/vitadb/#/' not in line]
    
    new_content = '\n'.join(new_lines)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed VitaDB from {file}")
