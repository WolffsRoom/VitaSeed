import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact string in the files
    target = "onclick=\"document.getElementById('modal-request').classList.add('show')\""
    replacement = "onclick=\"if(event.altKey) { window.location.href='admin.html'; } else { document.getElementById('modal-request').classList.add('show'); }\""
    
    new_content = content.replace(target, replacement)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file}")

print("All files processed.")
