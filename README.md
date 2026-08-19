# ☁️ OrdCloud

> **A polished local-first cloud-drive style file manager for Windows, built with Python and PySide6.**

[![CI](https://github.com/Ordboybro/OrdCloud/actions/workflows/ci.yml/badge.svg)](https://github.com/Ordboybro/OrdCloud/actions/workflows/ci.yml)

OrdCloud is a desktop file manager designed to feel like a modern cloud drive while keeping files **local and private**. It combines a dark, cloud-style interface with real filesystem operations, a sandboxed storage area, search, favorites, recent files, drag & drop, keyboard shortcuts and cached storage analytics.

**Current release:** `0.7.0`  
**Platform:** Windows  
**Language:** Russian  
**Architecture:** local-first desktop application

---

## ✨ Features

### File management

- 📁 Create folders
- ⬆️ Upload files
- 🖱️ Drag & drop
- 📋 Copy / paste
- ✂️ Cut / move
- ✏️ Rename
- 🗑️ Delete to the Windows Recycle Bin
- ⭐ Favorites
- 🕘 Recent files
- 🔎 Recursive background search
- ↩️ Back / forward navigation
- 🔃 Refresh
- 📊 Storage usage and category statistics

### Interface

- Dark cloud-drive inspired dashboard
- Sidebar navigation
- Breadcrumb navigation
- Quick Access cards
- Recent files table
- Storage analytics panel
- Upload area
- Context menus
- List and compact views
- Lightweight transitions
- Tooltips and hover states
- Russian UI

### Safety

- Files are restricted to the local `data/storage` sandbox
- Root storage cannot be deleted or renamed
- Invalid/path-traversal names are rejected
- Symlinks are ignored by storage accounting/search
- Existing copy destinations are rejected instead of silently overwritten
- Storage quota is checked before adding data
- Search results are protected against stale asynchronous responses

### Performance

- Search runs outside the UI thread
- Search input is debounced
- Filesystem statistics use a shared short-lived snapshot
- Mutating operations invalidate the statistics cache
- UI refreshes are kept local where possible

---

## 🖼️ Screenshots

The repository contains the design reference and the latest application capture:

- `screenshots/1.png` — target/reference design
- `screenshots/current.png` — latest local build

---

## 🛠️ Tech stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Application language |
| PySide6 / Qt | Desktop UI |
| Send2Trash | Safe deletion to Recycle Bin |
| unittest | Automated tests |
| GitHub Actions | CI quality checks |

---

## 🚀 Installation

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/Ordboybro/OrdCloud.git
cd OrdCloud

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

If PowerShell does not allow script activation, activation is not required:

```powershell
.venv\Scripts\python.exe main.py
```

---

## ⌨️ Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+F` | Focus search |
| `Ctrl+N` | New folder |
| `Ctrl+U` | Upload files |
| `Ctrl+C` | Copy |
| `Ctrl+X` | Cut / move |
| `Ctrl+V` | Paste |
| `F2` | Rename |
| `Delete` | Move to Recycle Bin |
| `Alt+←` | Back |
| `Alt+→` | Forward |
| `F5` | Refresh |
| `Escape` | Clear selection |

---

## 🧱 Project structure

```text
OrdCloud/
├── main.py
├── config.py
├── requirements.txt
├── modules/
│   ├── clipboard.py
│   ├── favorites.py
│   ├── file_model.py
│   ├── recent.py
│   ├── search_worker.py
│   ├── settings.py
│   ├── storage.py
│   ├── storage_service.py
│   └── ui_actions.py
├── ui/
│   ├── dashboard.py
│   ├── explorer.py
│   ├── file_row.py
│   ├── file_type_icon.py
│   ├── left_menu.py
│   ├── main_window.py
│   ├── navigation.py
│   ├── right_sidebar.py
│   ├── search_box.py
│   ├── storage_panel.py
│   └── top_toolbar.py
├── resources/
│   ├── icons/
│   └── style.qss
├── tests/
│   └── test_storage.py
└── screenshots/
```

---

## 🧠 Architecture

OrdCloud follows a small modular architecture rather than putting all application logic into the window class.

```text
                  ┌─────────────────┐
                  │   PySide6 UI    │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │  UI actions /   │
                  │ application flow│
                  └────────┬────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
      ┌──────▼──────┐             ┌──────▼──────┐
      │   Storage   │             │    Search   │
      │    layer    │             │    worker   │
      └──────┬──────┘             └─────────────┘
             │
      ┌──────▼──────┐
      │ data/storage│
      └─────────────┘
```

The application is deliberately **local-first**. There is no account, cloud API or external server required to use it.

---

## 🧪 Quality checks

Run the compiler check:

```powershell
python -m compileall -q main.py config.py modules ui
```

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

Run the application:

```powershell
python main.py
```

GitHub Actions automatically performs the project's quality checks on relevant code changes.

---

## 🔒 Privacy

OrdCloud is local-first. Files remain inside the local application storage directory unless the user explicitly moves or copies them elsewhere.

No account or cloud service is required.

---

## 📌 Roadmap

### v1.0 — Desktop foundation

- [x] Modern cloud-drive UI
- [x] Local sandboxed storage
- [x] File management
- [x] Search
- [x] Favorites and recent files
- [x] Storage analytics
- [x] Settings
- [x] Keyboard shortcuts
- [x] Automated tests and CI

### v2.0 — Cloud edition

A future version can add a real backend without compromising the desktop architecture:

```text
OrdCloud Desktop
       │ HTTPS
       ▼
   FastAPI API
       │
       ├── PostgreSQL
       │
       └── Object Storage
```

Possible future capabilities include accounts, authentication, synchronization, remote storage, sharing links and a web/mobile client.

---

## 📄 License

This repository is currently a personal portfolio project. A formal open-source license should be added before redistributing the software.

---

## 👤 Author

**Ordboybro**

Built as a portfolio project to practice Python, PySide6, filesystem architecture, testing, Git/GitHub and software engineering.
