# OrdCloud

OrdCloud is a polished local desktop file-storage application built with **Python + PySide6**. It recreates a modern cloud-storage dashboard while keeping files on the user's computer.

> Current version: **0.3.0**

## Features

### Storage
- Local storage sandbox under `data/storage`
- 5 GB configurable storage limit
- Automatic default folders
- Real storage statistics
- Safe path validation to prevent operations outside the storage root

### File management
- Browse folders
- Open files and folders
- Create folders
- Upload files
- Drag & drop upload
- Copy / paste
- Rename
- Delete to the Windows Recycle Bin
- Back / forward navigation
- Refresh
- Search
- Recent files
- Favorites
- Compact view
- Context menu

### Interface
- Dark modern dashboard
- Home dashboard with Quick Access
- Recent Files table
- Storage sidebar
- Upload panel
- Responsive layout with a reference viewport of 1366×768
- Smooth page fade transitions
- Keyboard shortcuts

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+F` | Focus search |
| `Ctrl+N` | New folder |
| `Ctrl+U` | Upload |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `F2` | Rename |
| `Delete` | Delete |
| `Alt+←` | Back |
| `Alt+→` | Forward |
| `F5` | Refresh |

## Tech stack

- Python 3.11+
- PySide6 / Qt
- Pillow
- psutil
- Send2Trash

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
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
│   ├── right_sidebar.py
│   ├── status_bar.py
│   └── top_toolbar.py
├── resources/
│   └── style.qss
└── data/
    └── storage/
```

## Development

The project is intentionally kept local-first: no account, external server, or cloud API is required. Runtime storage and local state should remain outside version control.

Before submitting changes, run:

```powershell
python -m compileall .
python main.py
```

## License

This project is currently intended as a personal portfolio project. Add a license before distributing it publicly as reusable software.
