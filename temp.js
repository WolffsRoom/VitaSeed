
        document.addEventListener("DOMContentLoaded", async () => {
            
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

            
            // Tooltip Logic Improved
            const tooltip = document.getElementById('custom-tooltip');
            let hoverTimer;

            function showTooltip(nodeId) {
                const node = nodes.get(nodeId);
                if (node.group === 'project') {
                    clearTimeout(hoverTimer);
                    const proj = node.projData;
                    
                    document.getElementById('tt-title').innerText = proj.title;
                    document.getElementById('tt-cat').innerText = proj.category;
                    const banner = proj.bannerUrl || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400';
                    document.getElementById('tt-img').style.backgroundImage = `url('${banner}')`;
                    document.getElementById('tt-btn').href = `project.html?id=${proj.id}`;

                    const domPos = network.canvasToDOM(network.getPositions([nodeId])[nodeId]);
                    
                    tooltip.style.display = 'block';
                    // Allow display block to apply before animating opacity
                    requestAnimationFrame(() => {
                        tooltip.style.left = (domPos.x + 20) + 'px';
                        tooltip.style.top = (domPos.y - 80) + 'px';
                        tooltip.style.opacity = '1';
                        tooltip.style.transform = 'translateY(0) scale(1)';
                    });
                }
            }

            function hideTooltip(immediate = false) {
                if (immediate) {
                    tooltip.style.display = 'none';
                    tooltip.style.opacity = '0';
                    tooltip.style.transform = 'translateY(10px) scale(0.95)';
                } else {
                    hoverTimer = setTimeout(() => {
                        tooltip.style.opacity = '0';
                        tooltip.style.transform = 'translateY(10px) scale(0.95)';
                        setTimeout(() => tooltip.style.display = 'none', 300);
                    }, 400);
                }
            }

            // Desktop Hover
            network.on("hoverNode", function (params) {
                showTooltip(params.node);
            });

            network.on("blurNode", function (params) {
                hideTooltip();
            });

            // Mobile Click/Touch
            network.on("click", function (params) {
                if (params.nodes.length > 0) {
                    showTooltip(params.nodes[0]);
                } else {
                    hideTooltip(true);
                }
            });
            
            // Dragging should hide tooltip so it doesn't get stuck
            network.on("dragStart", function (params) {
                hideTooltip(true);
            });

            // Keep alive when hovering tooltip
            tooltip.addEventListener('mouseenter', () => clearTimeout(hoverTimer));
            tooltip.addEventListener('mouseleave', () => hideTooltip());

    