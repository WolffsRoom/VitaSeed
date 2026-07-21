import glob

old_string = '<li><a href="https://www.youtube.com/@TitiClash" target="_blank"><span>Titi Clash <i class="ph ph-youtube-logo" style="font-size: 1em; margin-left: 4px; color: #ff0000; opacity: 0.8;"></i></span></a></li>'
new_string = '<li><a href="https://www.youtube.com/@TitiClash" target="_blank"><span>Titi Clash <i class="ph ph-arrow-up-right" style="font-size: 0.8em; margin-left: 4px; opacity: 0.5;"></i></span></a></li>'

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_string in content:
        content = content.replace(old_string, new_string)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
