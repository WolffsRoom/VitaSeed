import glob

for file in glob.glob('*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove the inline redirect logic that was added via sync_header.py
    html = html.replace(
        ' oninput="if(window.location.pathname.indexOf(\'index\')===-1&&this.value.length>0){window.location.href=\'index.html?q=\'+encodeURIComponent(this.value);}"',
        ''
    )
    html = html.replace(
        ' onchange="if(this.value!==\'all\'){window.location.href=\'category.html?cat=\'+this.value;}"',
        ''
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Cleaned up redirect attributes from all pages.")
