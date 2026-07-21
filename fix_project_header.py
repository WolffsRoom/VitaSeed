css_fix = """
/* Project Header Banner */
.project-header {
    height: 350px;
    background-size: cover;
    background-position: center;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    border: 1px solid var(--card-border);
}

.project-header::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 80%;
    background: linear-gradient(to top, rgba(14, 14, 14, 1) 0%, rgba(14, 14, 14, 0) 100%);
    pointer-events: none;
}

.project-header-content {
    position: relative;
    padding: 2rem;
    width: 100%;
    z-index: 2;
}
"""

with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(css_fix)
