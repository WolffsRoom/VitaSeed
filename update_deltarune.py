import json

catalog_path = 'api/catalog.json'
with open(catalog_path, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for p in catalog.get('projects', []):
    if p.get('id') == 222:
        p['bannerUrl'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5BTHe2Ec8IvT5uEljcMl2yhwQb7c97Wi-K3j7tLT08AuLSuTlROfvmQs&s=10"
        
        p['description'] = "An unofficial port of DELTARUNE Chapters 1–5 for the PlayStation Vita.\n\nStarting with v0.36, the project directly executes GameMaker data from the Windows/Steam version using a tailored implementation of Butterscotch, with rendering powered by VitaGL. The Android version is no longer the primary asset source.\n\nThis repository and its releases do not include any commercial assets or files from DELTARUNE. Please purchase and obtain the official game at deltarune.com."
        
        p['screenshots'] = [
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003602-288879.png",
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-004312-951699.png",
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003606-442387.png",
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003701-130278.png",
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003704-049821.png",
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003816-839271.png",
            "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003828-635093.png"
        ]
        
        p['install_instructions'] = """## Installation Guide\n\nTo install the game correctly, follow these steps:\n\n- Install kubridge and FdFix by copying `kubridge.skprx` and `fd_fix.skprx` to your taiHEN plugins folder (usually `ux0:tai`) and adding these entries to `config.txt` under `*KERNEL`:\n\n  ```text\n  *KERNEL\n  ux0:tai/kubridge.skprx\n  ux0:tai/fd_fix.skprx\n  ```\n\n  **Note:** Do not install `fd_fix.skprx` if you are using the rePatch plugin.\n\n- **Optional:** Install PSVshell to overclock your device.\n- Install `libshacccg.suprx`, if it is not already installed.\n- Purchase the official game legally at Steam.\n\n### HOW TO APPLY THE PATCH:\n\nTo run the game, make sure you have the required data files from an official game installation. The supported Steam version is **v0.0.247 Patch**.  \n*PS: The language selection in the patcher only changes the program's interface, not the in-game language.*\n\n1. Purchase and/or install DELTARUNE for PC on Steam.\n2. Ensure the installation is on version **v0.0.247 Patch** and contains no modified files.\n3. Download the .VPK (`Deltarune-vX.XX.vpk`) and the .ZIP file (`DeltaruneVita-Patcher-vX.XX.zip`) from the Releases page.\n4. Extract the ZIP file to get the patcher.\n5. Copy the `DELTARUNE` folder into the patcher directory at `SteamFiles/DELTARUNE`.\n6. Run `DeltaruneVitaPatcher.exe`, select your preferred interface language, and start the process.\n7. Copy the generated `deltarune` folder inside `VitaFiles` to `ux0:data/` on your PS Vita. USB transfer or an SD card reader is highly recommended since the file size is quite large (~1.1 GB).\n8. Finally, install `Deltarune-vX.XX.vpk` using VitaShell.\n\n#### Observations: \n\nEnsure that the data files were correctly placed and are located in the following path: `ux0:data/deltarune/deltarunevita/...`\n\n```text\nux0:data/deltarune/deltarunevita/butterscotch-probe.log\n```\n\n**IMPORTANTE:** When updating to latest Realease, verifique se é necessário generate and transfer the data again using the newest patcher. Sometimes, Updating only the VPK does not provide the complete cache and data improvements."""
        
        p['support_link'] = "https://buymeacoffee.com/5rsrt7j4z8f"
        break

with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=4, ensure_ascii=False)
