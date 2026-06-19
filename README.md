# SahiChuno 🚗

**SahiChuno** is a full-stack Indian Automotive Market Intelligence Web Application built using Python, Flask, and SQLite. It provides an intuitive platform for users to dynamically search, filter, and compare vehicle variants across brands based on real-time budgets, segments, and dual-engine efficiency metrics.

The application is engineered to operate seamlessly as a localized web server or compile into a standalone Windows executable (`.exe`) via PyInstaller—requiring zero technical dependencies or prior Python setups for end-users.

---

## 🚀 Key Engineering Features

* **Dual-Engine Filtering Architecture:** Handles queries for both Internal Combustion Engine (ICE) and Electric Vehicles (EV) simultaneously by dynamically evaluating dual-column criteria (`mileage_kmpl` and `ev_range_km`).
* **Input Normalization Layer:** Built-in defensive backend scaling converts frontend shorthand UI metrics (e.g., Budget sliders in Lakhs/Crores) into absolute database values (Rupees) seamlessly.
* **Resilient Parameter Mapping:** Dynamically sanitizes complex frontend human-readable string requests (like `"Diesel Only"`) to guarantee flawless database string matches.
* **Local Database Persistence:** Powered by a self-contained SQLite configuration that automatically provisions and seeds an unabridged catalog matrix on initialization.
* **Native Desktop Auto-Launch:** Leverages non-blocking asynchronous `threading.Timer` routing to automatically launch the user's native default web browser instantly upon execution.

---

## 🛠️ Project Structure

```text
SahiChuno/
├── app.py                 # Core Flask application, database lifecycle, & routing
├── cars.db                # Auto-generated SQLite database catalog matrix
├── static/                # UI presentation assets (CSS layouts, JavaScript)
│   └── style.css
├── templates/             # HTML Jinja2 frontend view templates
│   └── index.html
├── requirements.txt       # Core python ecosystem dependencies
└── README.md              # Project documentation
