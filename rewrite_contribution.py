import re

with open('contribution.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a tooltip div to the HTML
tooltip_html = """
            <div id="network-container"></div>
            
            <div id="custom-tooltip" style="display:none; position:absolute; z-index:100; background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:1rem; box-shadow:0 10px 20px rgba(0,0,0,0.5); width:220px; pointer-events:auto; transition: opacity 0.2s;">
                <div id="tt-img" style="width:100%; height:100px; background-size:cover; background-position:center; border-radius:8px; margin-bottom:0.8rem;"></div>
                <h4 id="tt-title" style="margin-bottom:0.3rem; color:var(--text-main);">Title</h4>
                <div id="tt-cat" style="font-size:0.75rem; color:var(--text-muted); margin-bottom:1rem;">Category</div>
                <a id="tt-btn" href="#" class="btn-primary" style="display:block; text-align:center; padding:0.5rem; text-decoration:none; font-size:0.8rem;"><i class="ph ph-arrow-square-out"></i> Ver Projeto</a>
            </div>
"""

content = content.replace('<div id="network-container"></div>', tooltip_html)

# Rewrite the JS logic for nodes and events
js_logic = """
            const projectsData = await window.fetchCatalog();
            
            // Generate nodes from projectsData
            const devsMap = new Map();
            const projectNodes = [];
            const edgeList = [];

            projectsData.forEach(proj => {
                const banner = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';
                
                // Add project node with image
                projectNodes.push({
                    id: proj.id,
                    label: proj.title,
                    group: 'project',
                    shape: 'circularImage',
                    image: banner,
                    size: 25,
                    projData: proj // Save data for tooltip
                });

                // Add dev node if not exists
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

                // Add edge between dev and project
                edgeList.push({
                    from: devName,
                    to: proj.id
                });
            });

            const nodesArray = Array.from(devsMap.values()).concat(projectNodes);
            const nodes = new vis.DataSet(nodesArray);
            const edges = new vis.DataSet(edgeList);

            const container = document.getElementById('network-container');
            const data = { nodes: nodes, edges: edges };
            
            const options = {
                nodes: {
                    font: { 
                        color: '#a0a0a0', 
                        size: 14,
                        face: 'Inter, sans-serif',
                        strokeWidth: 0,
                        vadjust: -5
                    },
                    borderWidth: 2,
                    shadow: { enabled: true, color: 'rgba(0,0,0,0.5)', size: 10, x: 0, y: 0 }
                },
                edges: {
                    color: { color: '#444444', highlight: '#888888', hover: '#666666' },
                    width: 1,
                    smooth: { type: 'continuous' }
                },
                groups: {
                    dev: { color: { background: '#9d7cd8', border: '#7a5cb8' }, font: { color: '#c0a0ff' } },
                    project: { color: { background: '#4fd6be', border: '#39a895' }, font: { color: '#70e0d0' } }
                },
                physics: {
                    forceAtlas2Based: { gravitationalConstant: -120, centralGravity: 0.005, springLength: 150, springConstant: 0.04 },
                    maxVelocity: 50,
                    solver: 'forceAtlas2Based',
                    timestep: 0.35,
                    stabilization: { iterations: 150 }
                },
                interaction: { hover: true, tooltipDelay: 100, zoomView: true, dragView: true }
            };

            const network = new vis.Network(container, data, options);

            // Tooltip Logic
            const tooltip = document.getElementById('custom-tooltip');
            let hoverTimer;

            network.on("hoverNode", function (params) {
                const nodeId = params.node;
                const node = nodes.get(nodeId);
                
                if (node.group === 'project') {
                    clearTimeout(hoverTimer);
                    const proj = node.projData;
                    
                    document.getElementById('tt-title').innerText = proj.title;
                    document.getElementById('tt-cat').innerText = proj.category;
                    const banner = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';
                    document.getElementById('tt-img').style.backgroundImage = `url('${banner}')`;
                    document.getElementById('tt-btn').href = `project.html?id=${proj.id}`;

                    // Position tooltip near mouse
                    const domPos = network.canvasToDOM(network.getPositions([nodeId])[nodeId]);
                    const containerRect = container.getBoundingClientRect();
                    
                    tooltip.style.left = (domPos.x + 20) + 'px';
                    tooltip.style.top = (domPos.y - 50) + 'px';
                    tooltip.style.display = 'block';
                    tooltip.style.opacity = '1';
                }
            });

            network.on("blurNode", function (params) {
                // Give a small delay before hiding so user can move mouse into tooltip
                hoverTimer = setTimeout(() => {
                    tooltip.style.opacity = '0';
                    setTimeout(() => tooltip.style.display = 'none', 200);
                }, 400);
            });

            // Prevent tooltip from disappearing when hovering over it
            tooltip.addEventListener('mouseenter', () => clearTimeout(hoverTimer));
            tooltip.addEventListener('mouseleave', () => {
                tooltip.style.opacity = '0';
                setTimeout(() => tooltip.style.display = 'none', 200);
            });
"""

# We need to replace the old script logic
content = re.sub(r'const projectsData = await window\.fetchCatalog\(\);.*?const network = new vis\.Network\(container, data, options\);', js_logic, content, flags=re.DOTALL)

with open('contribution.html', 'w', encoding='utf-8') as f:
    f.write(content)
