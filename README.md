# OrdCloud

**OrdCloud** is a local-first desktop file-storage application built with **Python + PySide6**. It combines a polished dark cloud-drive interface with real local file management.

> Current version: **0.6.0**

## What it does

- Reference-matched dark dashboard UI
- Russian interface and cloud-drive style navigation
- Local sandboxed storage under `data/storage`
- Configurable 5 GB storage quota
- Quick Access dashboard with Documents, Photos, Video, Presentations and Archives
- Recent files and favorites
- Folder navigation and breadcrumbs
- Upload and drag & drop
- Create folders
- Copy / paste
- Rename
- Delete to the Windows Recycle Bin
- Recursive search with debounce and background worker execution
- Search result race protection so stale results cannot overwrite newer navigation
- Compact view
- Context menu with favorites
- Back / forward navigation
- Keyboard shortcuts
- Shared cached storage statistics to avoid repeated filesystem scans
- Painted file-type icons for consistent rendering
- Safe path validation so file operations stay inside the storage sandbox
- Smooth lightweight page transitions
- Automated compile, storage tests and offscreen UI smoke checks in GitHub Actions

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+F` | Focus search |
| `Ctrl+N` | New folder |
| `Ctrl+U` | Upload files |
| `Ctrl+C` | Copy selected item |
| `Ctrl+V` | Paste |
| `F2` | Rename selected item |
| `Delete` | Move selected item to Recycle Bin |
| `Alt+←` | Back |
| `Alt+→` | Forward |
| `F5` | Refresh |
| `Escape` | Clear selection |

## Tech stack

- Python 3.11+
- PySide6 / Qt
- Send2Trash
- `unittest` for storage tests
- GitHub Actions for automated quality checks

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

If PowerShell blocks script activation, run the project without activation:

```powershell
.venv\Scripts\python.exe main.py
```

## Quality checks

```powershell
python -m compileall .
python -m unittest discover -s tests -v
```

## Project structure

```text
OrdCloud/
├── config.py
├── main.py
├── requirements.txt
├── modules/
│   ├── clipboard.py
│   ├── favorites.py
│   ├── file_model.py
│   ├── recent.py
│   ├── search_worker.py
│   ├── storage.py
│   ├── storage_service.py
│   └── ui_actions.py
├── ui/
│   ├── action_bar.py
│   ├── dashboard.py
│   ├── explorer.py
│   ├── file_row.py
│   ├── file_type_icon.py
│   ├── left_menu.py
│   ├── main_window.py
│   ├── navigation.py
│   ├── right_sidebar.py
│   ├── search_box.py
│   ├── status_bar.py
│   ├── storage_panel.py
│   ├── storage_segment.py
│   ├── storage_stats.py
│   └── top_toolbar.py
├── resources/
│   ├── icons/
│   └── style.qss
├── tests/
│   └── test_storage.py
├── screenshots/
└── data/
    └── storage/
```

## Architecture

The project separates responsibilities into small modules:

- `modules/storage.py` — safe filesystem primitives and shared storage statistics
- `modules/storage_service.py` — application storage configuration
- `modules/search_worker.py` — non-blocking recursive search worker
- `modules/ui_actions.py` — commands initiated by the interface
- `modules/file_model.py` — converts filesystem entries into UI data
- `ui/main_window.py` — application shell, navigation, search and shortcuts
- `ui/dashboard.py` — Home dashboard
- `ui/explorer.py` — file browser
- `ui/file_type_icon.py` — consistent file/folder icon rendering
- `resources/style.qss` — visual system

OrdCloud is intentionally **local-first**: it does not require an account, external server, or cloud API.

## Development

Before committing changes, run:

```powershell
python -m compileall .
python -m unittest discover -s tests -v
python main.py
```

The reference image is stored in `screenshots/1.png`; `screenshots/current.png` is the latest local application capture.

## License

This repository is currently a personal portfolio project. Add a license before distributing OrdCloud as reusable software.
