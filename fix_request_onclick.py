import glob

for file in glob.glob('*.html'):
    if file == 'admin.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact string in the files
    target = "onclick=\"if(event.altKey) { window.location.href='admin.html'; } else { document.getElementById('modal-request').classList.add('show'); }\""
    replacement = "onclick=\"handleRequestButtonClick(event)\""
    
    new_content = content.replace(target, replacement)
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated onclick in {file}")

print("All files processed.")
