# OrdCloud

**OrdCloud** is a local-first desktop file-storage application built with **Python + PySide6**. It combines a modern cloud-drive style interface with real local file management.

> Current version: **0.3.1**

## What it does

- Modern dark storage dashboard
- Local sandboxed storage under `data/storage`
- Configurable 5 GB storage quota
- Home dashboard with Quick Access and Recent Files
- Folder navigation and breadcrumbs
- Upload and drag & drop
- Create folders
- Copy / paste
- Rename
- Delete to the Windows Recycle Bin
- Search
- Recent files
- Favorites
- Compact view
- Context menu
- Back / forward navigation
- Keyboard shortcuts
- Real-time storage statistics
- Safe path validation so file operations stay inside the storage sandbox
- Smooth lightweight page transitions

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

## Tech stack

- Python 3.11+
- PySide6 / Qt
- Send2Trash
- `unittest` for storage tests
- GitHub Actions for automated compile/test checks

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
│   ├── storage_service.py
│   └── ui_actions.py
├── ui/
│   ├── action_bar.py
│   ├── dashboard.py
│   ├── explorer.py
│   ├── file_row.py
│   ├── left_menu.py
│   ├── main_window.py
│   ├── navigation.py
│   ├── navigation.py
│   ├── right_sidebar.py
│   ├── status_bar.py
│   └── top_toolbar.py
├── resources/
│   └── style.qss
├── tests/
│   └── test_storage.py
├── screenshots/
└── data/
    └── storage/
```

## Architecture

The project separates responsibilities into small modules:

- `modules/storage_service.py` — storage rules and filesystem operations
- `modules/ui_actions.py` — commands initiated by the interface
- `modules/file_model.py` — converts filesystem entries into UI data
- `modules/recent.py` / `favorites.py` — local UI state
- `ui/main_window.py` — application orchestration and navigation
- `ui/dashboard.py` — Home dashboard
- `ui/explorer.py` — file browser
- `resources/style.qss` — visual system

OrdCloud is intentionally **local-first**: it does not require an account, external server, or cloud API.

## Development

Before committing changes, run both checks:

```powershell
python -m compileall .
python -m unittest discover -s tests -v
```

Then launch the application and manually verify the file-management flows.

## License

This repository is currently a personal portfolio project. Add a license before distributing OrdCloud as reusable software.
