import re

with open('contribution.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update tooltip CSS for better animation
old_tooltip_style = 'id="custom-tooltip" style="display:none; position:absolute; z-index:100; background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:1rem; box-shadow:0 10px 20px rgba(0,0,0,0.5); width:220px; pointer-events:auto; transition: opacity 0.2s;"'
new_tooltip_style = 'id="custom-tooltip" style="display:none; position:absolute; z-index:100; background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:1rem; box-shadow:0 15px 35px rgba(0,0,0,0.6); width:240px; pointer-events:auto; opacity:0; transform: translateY(10px) scale(0.95); transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);"'
content = content.replace(old_tooltip_style, new_tooltip_style)

# Rewrite the Event Listeners
old_events_block = r'// Tooltip Logic.*?// Prevent tooltip from disappearing when hovering over it.*?tooltip\.addEventListener\(\'mouseleave\', \(\) => \{\n.*?tooltip\.style\.opacity = \'0\';\n.*?setTimeout\(\(\) => tooltip\.style\.display = \'none\', 200\);\n.*\}\);'

new_events_block = """
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
"""

content = re.sub(old_events_block, new_events_block, content, flags=re.DOTALL)

with open('contribution.html', 'w', encoding='utf-8') as f:
    f.write(content)
