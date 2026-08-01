window.catalogFallbackData = [
        {
            "id": 222,
            "title": "Deltarune (Chapters 1 to 5)",
            "category": "Ports",
            "ai_used": false,
            "vibecoded": false,
            "responsibles": "Wolff",
            "description": "An unofficial port of DELTARUNE Chapters 1–5 for the PlayStation Vita.\n\nStarting with v0.36, the project directly executes GameMaker data from the Windows/Steam version using a tailored implementation of Butterscotch, with rendering powered by VitaGL. The Android version is no longer the primary asset source.\n\nThis repository and its releases do not include any commercial assets or files from DELTARUNE. Please purchase and obtain the official game at deltarune.com.",
            "install_instructions": "## Installation Guide\n\nTo install the game correctly, follow these steps:\n\n- Install kubridge and FdFix by copying `kubridge.skprx` and `fd_fix.skprx` to your taiHEN plugins folder (usually `ux0:tai`) and adding these entries to `config.txt` under `*KERNEL`:\n\n  ```text\n  *KERNEL\n  ux0:tai/kubridge.skprx\n  ux0:tai/fd_fix.skprx\n  ```\n\n  **Note:** Do not install `fd_fix.skprx` if you are using the rePatch plugin.\n\n- **Optional:** Install PSVshell to overclock your device.\n- Install `libshacccg.suprx`, if it is not already installed.\n- Purchase the official game legally at Steam.\n\n### HOW TO APPLY THE PATCH:\n\nTo run the game, make sure you have the required data files from an official game installation. The supported Steam version is **v0.0.247 Patch**.  \n*PS: The language selection in the patcher only changes the program's interface, not the in-game language.*\n\n1. Purchase and/or install DELTARUNE for PC on Steam.\n2. Ensure the installation is on version **v0.0.247 Patch** and contains no modified files.\n3. Download the .VPK (`Deltarune-vX.XX.vpk`) and the .ZIP file (`DeltaruneVita-Patcher-vX.XX.zip`) from the Releases page.\n4. Extract the ZIP file to get the patcher.\n5. Copy the `DELTARUNE` folder into the patcher directory at `SteamFiles/DELTARUNE`.\n6. Run `DeltaruneVitaPatcher.exe`, select your preferred interface language, and start the process.\n7. Copy the generated `deltarune` folder inside `VitaFiles` to `ux0:data/` on your PS Vita. USB transfer or an SD card reader is highly recommended since the file size is quite large (~1.1 GB).\n8. Finally, install `Deltarune-vX.XX.vpk` using VitaShell.\n\n#### Observations: \n\nEnsure that the data files were correctly placed and are located in the following path: `ux0:data/deltarune/deltarunevita/...`\n\n```text\nux0:data/deltarune/deltarunevita/butterscotch-probe.log\n```\n\n**IMPORTANTE:** When updating to latest Realease, verifique se é necessário generate and transfer the data again using the newest patcher. Sometimes, Updating only the VPK does not provide the complete cache and data improvements.",
            "bannerUrl": "https://i.pinimg.com/originals/9c/3f/60/9c3f60365da4949c7547cd11f8d29b10.gif",
            "screenshots": [
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003602-288879.png",
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-004312-951699.png",
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003606-442387.png",
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003701-130278.png",
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003704-049821.png",
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003816-839271.png",
                "https://raw.githubusercontent.com/WolffsRoom/DeltaruneVita/main/Assets/Screenshots/2026-07-17-003828-635093.png"
            ],
            "source_link": "https://github.com/WolffsRoom/DeltaruneVita",
            "publish_date": "21/07/2026",
            "update_date": "20/07/2026",
            "downloads": 0,
            "support_link": "https://buymeacoffee.com/5rsrt7j4z8f",
            "version": "0.52",
            "downloads_list": [
                {
                    "name": "Baixar VPK (v0.52)",
                    "url": "https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.52/Deltarune-v0.52.vpk"
                },
                {
                    "name": "Baixar Patcher (ZIP)",
                    "url": "https://github.com/WolffsRoom/DeltaruneVita/releases/download/v0.52/Deltarune.Vita.Patcher.v0.52.zip"
                }
            ],
            "status": "Em Desenvolvimento",
            "playable": "Sim",
            "bgPosition": "center bottom"
        },
        {
            "id": 1,
            "title": "Beach Buggy Racing",
            "category": "Ports",
            "responsibles": "MeninoSung",
            "description": "Um emocionante jogo de corrida estilo kart para passar o tempo.",
            "warnings": "Requer controle compatível para melhor experiência.",
            "source_link": "https://github.com/example/beach-buggy",
            "bannerUrl": "https://m.media-amazon.com/images/I/91ITdE2CVKL.png",
            "videoUrl": "https://www.w3schools.com/html/mov_bbb.mp4",
            "screenshots": [
                "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&q=80&w=400",
                "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=400"
            ],
            "install_instructions": "1. Baixe o VPK.\n2. Transfira para o console via VitaShell.\n3. Instale e divirta-se!",
            "ai_used": false,
            "vibecoded": false,
            "downloads": 6647,
            "publish_date": "30/05/2023",
            "update_date": "10/07/2023",
            "support_link": "https://ko-fi.com/wolffsroom",
            "collaborators": [
                "Wolff"
            ]
        },
        {
            "id": 2,
            "title": "Zombie Tsunami",
            "category": "Ports",
            "responsibles": "MeninoSung",
            "description": "Infecte toda a cidade com sua horda de zumbis neste divertido endless runner.",
            "warnings": "Nenhum aviso.",
            "source_link": "https://github.com/example/zombie-tsunami",
            "bannerUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIaYAw1lXstjmQJ2L12cBvYO7CmsLd3VQtrcDVA1BBkA&s=10",
            "screenshots": [
                "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&q=80&w=400"
            ],
            "install_instructions": "Basta instalar o VPK. É necessário possuir os arquivos do jogo original se quiser usar os mods de texturas.",
            "ai_used": true,
            "ai_details": {
                "name": "GitHub Copilot",
                "reason": "Acelerar criação de níveis procedurais.",
                "action": "Gerou o script base de spawn de obstáculos no mapa."
            },
            "vibecoded": false,
            "downloads": 1514,
            "publish_date": "25/01/2023",
            "update_date": "20/11/2025",
            "support_link": "https://ko-fi.com/wolffsroom",
            "collaborators": [
                "Wolff"
            ]
        },
        {
            "id": 3,
            "title": "The Case of Golden Idol",
            "category": "Ports",
            "responsibles": "Wolff",
            "description": "Investigue uma série de assassinatos misteriosos. Jogo de puzzle investigativo.",
            "warnings": "Pode conter temas pesados.",
            "source_link": "https://github.com/example/golden-idol",
            "bannerUrl": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1677770/capsule_616x353.jpg?t=1782893605",
            "ai_used": false,
            "vibecoded": false,
            "downloads": 17044,
            "publish_date": "06/04/2026",
            "update_date": "12/07/2026",
            "support_link": "https://ko-fi.com/wolffsroom"
        },
        {
            "id": 7,
            "title": "Atelier Ayesha PTBR",
            "category": "Translations",
            "responsibles": "Wolff",
            "description": "Tradução de textos e menus para Atelier Ayesha.",
            "warnings": "Faça backup do save antes de aplicar.",
            "source_link": "https://github.com/example/atelier-ayesha-ptbr",
            "bannerUrl": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1152300/capsule_616x353.jpg?t=1781064781",
            "ai_used": true,
            "ai_details": {
                "name": "GPT-4",
                "reason": "Tradução de arquivos de texto complexos de japonês para português.",
                "action": "Traduziu os arquivos JSON de diálogos principais."
            },
            "vibecoded": false,
            "downloads": 16937,
            "publish_date": "27/01/2023",
            "update_date": "08/08/2025",
            "support_link": "https://ko-fi.com/wolffsroom"
        },
        {
            "id": 10,
            "title": "NoTrpDrmGODOT",
            "category": "Plugin",
            "responsibles": "Wolff",
            "description": "uso de IA analisar estrutura do NoTrpDrm (by Rinnegatemente) para aplicar funcionamento em jogos baseados GODOT 3.5.rc5 + Vita(by SonicMastr)",
            "warnings": "Uso experimental na versão 4.x da engine.",
            "source_link": "https://github.com/example/nodrtrophiesgodot",
            "bannerUrl": "https://images.wallpaperscraft.com/image/single/code_programming_it_152538_960x544.jpg",
            "ai_used": true,
            "ai_details": {
                "name": "Claude 3.5 Sonnet",
                "reason": "Escrita do plugin do zero com GDScript.",
                "action": "Desenvolveu o addon inteiro baseado nas documentações recentes."
            },
            "vibecoded": true,
            "downloads": 6341,
            "publish_date": "05/03/2024",
            "update_date": "30/09/2024",
            "support_link": "https://ko-fi.com/wolffsroom",
            "status": "Análise",
            "playable": "Não"
        },
        {
            "id": 223,
            "title": "VitaSeed",
            "category": "Apps",
            "responsibles": "Wolff",
            "description": "O aplicativo nativo do VitaSeed para o PSVita!",
            "status": "Em desenvolvimento",
            "playable": "Em progresso",
            "source_link": "https://github.com/WolffsRoom/VitaSeed",
            "bannerUrl": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&q=80&w=400",
            "ai_used": false,
            "vibecoded": false,
            "downloads": 0,
            "publish_date": "31/07/2026",
            "update_date": "31/07/2026"
        }
];

