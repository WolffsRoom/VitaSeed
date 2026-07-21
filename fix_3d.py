new_css = """
/* Fix 3D Apple Effect on normal cards */
.card {
    transform-style: preserve-3d;
    perspective: 1000px;
}
.card-content {
    transform: translateZ(20px);
}
.card-banner {
    transform: translateZ(10px);
}
"""
with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(new_css)
