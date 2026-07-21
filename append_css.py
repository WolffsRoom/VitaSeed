new_css = """
/* Fix Settings Active State */
.sidebar-footer ul li a.active {
    color: var(--accent-green);
    background: rgba(0, 230, 118, 0.1);
}

/* Fix Filter Options Styling */
.filter-select option {
    background-color: #1a1a1a;
    color: #ffffff;
}
[data-theme="light"] .filter-select option {
    background-color: #ffffff;
    color: #000000;
}
[data-theme="sony"] .filter-select option {
    background-color: #003399;
    color: #ffffff;
}
"""
with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
