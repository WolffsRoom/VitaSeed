import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace the `function sendRequest() { ... }` logic completely.
    # It starts with `function sendRequest()` and ends right before `document.addEventListener('keydown'`
    
    pattern = r"function sendRequest\(\)\s*\{.*?setTimeout[^\}]+\}\s*\;\s*\}"
    new_content = re.sub(pattern, "", content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Removed inline sendRequest from HTML files.")
