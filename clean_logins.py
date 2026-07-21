import glob
import re

for file in glob.glob('*.html'):
    if file == 'admin.html': continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Sidebar Login
    content = re.sub(r'<li id="sidebar-login-container">[\s\S]*?</li>', '', content)
    
    # 2. Remove Mobile Login Button & Mobile User Profile
    content = re.sub(r'<div id="mobile-user-profile"[\s\S]*?</div>', '', content)
    content = re.sub(r'<button id="mobile-login-btn"[\s\S]*?</button>', '', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Redundant login buttons removed.")
