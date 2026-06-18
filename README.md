# SahiChuno 🚗

**SahiChuno** is a lightweight, local web application built using Python, Flask, and SQLite designed to help users search, filter, and choose the right cars. The application is designed to run seamlessly as a web server locally or be compiled into a standalone Windows executable (`.exe`) using PyInstaller without needing any prior Python installation.

---

## 🚀 Features

* **Dynamic Car Selection:** View, filter, and select cars effortlessly via a clean web interface.
* **Local Database Integration:** Uses a self-contained SQLite (`cars.db`) database that auto-initializes on the first run.
* **Auto-Launch Browser:** Automatically opens your default web browser to the app's local address upon startup.
* **Portable Executable Ready:** Configured to bundle cleanly into a single `.exe` file using PyInstaller while safely managing paths for templates, static files, and database persistence.

---

## 🛠️ Project Structure

```text
SahiChuno/
├── app.py                 # Core Flask application & database logic
├── cars.db                # SQLite database (auto-generated)
├── static/                # CSS, JavaScript, and Images
│   └── style.css
├── templates/             # HTML Frontend templates
│   └── index.html
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
