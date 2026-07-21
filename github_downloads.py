import re

with open('project.html', 'r', encoding='utf-8') as f:
    content = f.read()

github_fetch_js = """
                async function fetchGithubDownloads(repoUrl) {
                    if (!repoUrl || !repoUrl.includes('github.com')) return null;
                    try {
                        let path = repoUrl.split('github.com/')[1];
                        if (path.endsWith('/')) path = path.slice(0, -1);
                        const parts = path.split('/');
                        const user = parts[0];
                        const repo = parts[1];
                        if (!user || !repo) return null;
                        
                        const apiUrl = `https://api.github.com/repos/${user}/${repo}/releases`;
                        const res = await fetch(apiUrl);
                        if (!res.ok) return null;
                        const releases = await res.json();
                        
                        let total = 0;
                        releases.forEach(release => {
                            if (release.assets) {
                                release.assets.forEach(asset => {
                                    total += asset.download_count;
                                });
                            }
                        });
                        return total;
                    } catch (e) {
                        return null;
                    }
                }

                // Fetch real downloads
                if (proj.source_link) {
                    document.getElementById('meta-down').innerText = "Carregando...";
                    fetchGithubDownloads(proj.source_link).then(count => {
                        if (count !== null && count > 0) {
                            document.getElementById('meta-down').innerHTML = count.toLocaleString('pt-BR') + ' <span style="font-size:0.8rem; color:var(--text-muted);">(GitHub)</span>';
                        } else if (proj.downloads !== undefined) {
                            document.getElementById('meta-down').innerText = proj.downloads.toLocaleString('pt-BR');
                        } else {
                            document.getElementById('meta-down').innerText = "N/A";
                        }
                    });
                } else if(proj.downloads !== undefined) {
                    document.getElementById('meta-down').innerText = proj.downloads.toLocaleString('pt-BR');
                }
"""

# Find where we used to set downloads
old_downloads_code = "if(proj.downloads) document.getElementById('meta-down').innerText = proj.downloads.toLocaleString('pt-BR');"
content = content.replace(old_downloads_code, github_fetch_js)

with open('project.html', 'w', encoding='utf-8') as f:
    f.write(content)
