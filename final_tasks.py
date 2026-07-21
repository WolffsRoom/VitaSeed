import json
import re

# 1. Update Deltarune GIF
catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['bannerUrl'] = "https://i.pinimg.com/originals/9c/3f/60/9c3f60365da4949c7547cd11f8d29b10.gif"
        # We also need to revert title to just "Deltarune (Chapters 1 to 5)" without HTML
        p['title'] = "Deltarune (Chapters 1 to 5)"
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)

# 2. Add formatTitle to api.js
with open('js/api.js', 'r', encoding='utf-8') as f:
    api_js = f.read()

format_title_fn = '''
window.formatTitle = function(title) {
    if (!title) return "";
    return title.replace(/(\([^)]+\)|\[[^\]]+\])/g, '<span style="font-weight: 400; font-size: 0.85em;">$1</span>');
};
'''
if 'window.formatTitle' not in api_js:
    api_js += format_title_fn
    with open('js/api.js', 'w', encoding='utf-8') as f:
        f.write(api_js)

# 3. Apply formatTitle in main.js, project.html, category.html
def replace_title(file_path, is_html=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if is_html:
        # project.html has document.getElementById('proj-title').innerText = proj.title;
        content = content.replace(
            "document.getElementById('proj-title').innerText = proj.title;",
            "document.getElementById('proj-title').innerHTML = window.formatTitle(proj.title);"
        )
        # category.html has <h3 class="card-title">${proj.title}</h3>
        content = content.replace('${proj.title}', '${window.formatTitle(proj.title)}')
    else:
        # main.js has ${proj.title} and ${heroProj.title}
        content = content.replace('${proj.title}', '${window.formatTitle(proj.title)}')
        content = content.replace('${heroProj.title}', '${window.formatTitle(heroProj.title)}')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

replace_title('js/main.js')
replace_title('project.html', is_html=True)
replace_title('category.html', is_html=True)

# 4. Add filter header to contribution.html and update JS
with open('contribution.html', 'r', encoding='utf-8') as f:
    contrib = f.read()

filter_header = '''
        <header>
            <select id="category-filter" class="filter-select">
                <option value="all">Todas as Categorias</option>
                <option value="Ports">Ports</option>
                <option value="Original games">Original games</option>
                <option value="Mods">Mods</option>
                <option value="Translations">Translations</option>
                <option value="Tools">Tools</option>
                <option value="PC Tools">PC Tools</option>
            </select>
            <select id="dev-filter" class="filter-select">
                <option value="all">Todos os responsáveis</option>
            </select>
            <input type="text" id="search-input" class="search-bar" placeholder="Buscar por título ou responsável...">
        </header>
'''

# Add header right before <main>
if '<header>' not in contrib:
    contrib = contrib.replace('<main>', filter_header + '\n        <main>')

# Update the JS logic in contribution.html to build graph as a function and apply filters
# Find the start of graph logic
js_start = 'const projectsData = await window.fetchCatalog();'

js_new_logic = '''const projectsData = await window.fetchCatalog();
            
            // Populate dev filter
            const allDevs = [...new Set(projectsData.map(p => p.responsibles))].sort();
            const devFilter = document.getElementById('dev-filter');
            allDevs.forEach(dev => {
                const opt = document.createElement('option');
                opt.value = dev;
                opt.innerText = dev;
                devFilter.appendChild(opt);
            });

            const catFilter = document.getElementById('category-filter');
            const searchInput = document.getElementById('search-input');
            const container = document.getElementById('network-container');
            let network = null;

            function renderGraph(filteredData) {
                if (network) {
                    network.destroy();
                }

                const devsMap = new Map();
                const projectNodes = [];
                const edgeList = [];

                filteredData.forEach(proj => {
                    const banner = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';
                    projectNodes.push({
                        id: proj.id,
                        label: window.formatTitle(proj.title).replace(/<[^>]+>/g, ''), // strip html for canvas
                        group: 'project',
                        shape: 'circularImage',
                        image: banner,
                        size: 25,
                        projData: proj
                    });

                    const devName = proj.responsibles;
                    if (!devsMap.has(devName)) {
                        devsMap.set(devName, {
                            id: devName,
                            label: devName,
                            group: 'dev',
                            shape: 'dot',
                            size: 15
                        });
                    }

                    edgeList.push({
                        from: devName,
                        to: proj.id
                    });
                });

                const nodesArray = Array.from(devsMap.values()).concat(projectNodes);
                const nodes = new vis.DataSet(nodesArray);
                const edges = new vis.DataSet(edgeList);

                const data = { nodes: nodes, edges: edges };
                const options = {
                    nodes: { font: { color: '#a0a0a0', size: 14, face: 'Inter, sans-serif', strokeWidth: 0, vadjust: -5 }, borderWidth: 2, shadow: { enabled: true, color: 'rgba(0,0,0,0.5)', size: 10, x: 0, y: 0 } },
                    edges: { color: { color: '#444444', highlight: '#888888', hover: '#666666' }, width: 1, smooth: { type: 'continuous' } },
                    groups: { dev: { color: { background: '#9d7cd8', border: '#7a5cb8' }, font: { color: '#c0a0ff' } }, project: { color: { background: '#4fd6be', border: '#39a895' }, font: { color: '#70e0d0' } } },
                    physics: { forceAtlas2Based: { gravitationalConstant: -120, centralGravity: 0.005, springLength: 150, springConstant: 0.04 }, maxVelocity: 50, solver: 'forceAtlas2Based', timestep: 0.35, stabilization: { iterations: 150 } },
                    interaction: { hover: true, tooltipDelay: 100, zoomView: true, dragView: true }
                };

                network = new vis.Network(container, data, options);

                // Reattach tooltip logic to the new network instance
                network.on("hoverNode", function (params) {
                    const nodeId = params.node;
                    const node = nodes.get(nodeId);
                    if (node.group === 'project') {
                        clearTimeout(hoverTimer);
                        const proj = node.projData;
                        
                        document.getElementById('tt-title').innerHTML = window.formatTitle(proj.title);
                        document.getElementById('tt-cat').innerText = proj.category;
                        const banner = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';
                        document.getElementById('tt-img').style.backgroundImage = `url('${banner}')`;
                        document.getElementById('tt-btn').href = `project.html?id=${proj.id}`;

                        const domPos = network.canvasToDOM(network.getPositions([nodeId])[nodeId]);
                        
                        tooltip.style.display = 'block';
                        requestAnimationFrame(() => {
                            tooltip.style.left = (domPos.x + 20) + 'px';
                            tooltip.style.top = (domPos.y - 80) + 'px';
                            tooltip.style.opacity = '1';
                            tooltip.style.transform = 'translateY(0) scale(1)';
                        });
                    }
                });

                network.on("blurNode", function () {
                    hideTooltip();
                });
                network.on("dragStart", function () {
                    hideTooltip(true);
                });
                network.on("zoom", function () {
                    hideTooltip(true);
                });
            }

            function applyFilters() {
                const cat = catFilter.value;
                const dev = devFilter.value;
                const search = searchInput.value.toLowerCase();

                const filtered = projectsData.filter(proj => {
                    const matchCat = cat === 'all' || proj.category === cat;
                    const matchDev = dev === 'all' || proj.responsibles === dev;
                    const matchSearch = proj.title.toLowerCase().includes(search) || proj.responsibles.toLowerCase().includes(search);
                    return matchCat && matchDev && matchSearch;
                });
                renderGraph(filtered);
            }

            catFilter.addEventListener('change', applyFilters);
            devFilter.addEventListener('change', applyFilters);
            searchInput.addEventListener('input', applyFilters);

            // Initial render
            renderGraph(projectsData);'''

# We need to replace the old graph generation block.
# The old block starts at `const projectsData = await window.fetchCatalog();` and ends before `tooltip.addEventListener('mouseenter'`
# I will use a regex to replace this entire block.
pattern = r'const projectsData = await window\.fetchCatalog\(\);.*?network\.on\("zoom", function \(\) \{\s*hideTooltip\(true\);\s*\}\);'

contrib = re.sub(pattern, js_new_logic, contrib, flags=re.DOTALL)

with open('contribution.html', 'w', encoding='utf-8') as f:
    f.write(contrib)
