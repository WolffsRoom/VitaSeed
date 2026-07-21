import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make sidebar-footer ul behave like nav-links
css = css.replace(
    '.nav-links {',
    '.nav-links, .sidebar-footer ul {'
)
css = css.replace(
    '.nav-links li a {',
    '.nav-links li a, .sidebar-footer ul li a {'
)
css = css.replace(
    '.nav-links li a:hover {',
    '.nav-links li a:hover, .sidebar-footer ul li a:hover {'
)
css = css.replace(
    '.nav-links li a.active {',
    '.nav-links li a.active, .sidebar-footer ul li a.active {'
)
css = css.replace(
    '.nav-links li a i {',
    '.nav-links li a i, .sidebar-footer ul li a i {'
)

# Also fix the padding in sidebar-footer if it has left padding
css = css.replace(
    '''.sidebar-footer {
    font-size: 0.75rem;
    color: var(--text-muted);
    padding-left: 0.5rem;
}''',
    '''.sidebar-footer {
    font-size: 0.75rem;
    color: var(--text-muted);
}
.sidebar-footer .version {
    padding-left: 1.2rem;
    padding-top: 0.5rem;
}'''
)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
