# LinkedIn Easy Apply (Bitwarden‑enabled)

A small, open‑source Python tool that automatically:

* logs into LinkedIn using credentials stored in **Bitwarden**
* searches for jobs matching a list of keywords & locations
* detects “Easy Apply” opportunities
* evaluates the job description against your résumé (via `job_analyzer`)
* records every application attempt (title, URL, status, match % …) in a **Google Sheet**

All secrets are never hard‑coded – they are pulled at runtime from a Bitwarden vault, keeping your passwords and Google service‑account keys safe.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| ✅ | Description |
|---|-------------|
| **Secure secret handling** | Bitwarden vault supplies LinkedIn login and Google Sheets service‑account JSON. |
| **Playwright‑driven UI** | Headed (or headless) Chromium automation, no Selenium headaches. |
| **Job‑fit analysis** | Uses `job_analyzer.analyze_job_fit` to compare job description with résumé skills. |
| **Google Sheets logger** | Every attempt is appended to a sheet (timestamp, company, title, URL, status, match %…). |
| **Customizable search** | Edit `KEYWORDS` and `LOCATIONS` in `linkedin_easy_apply_bw.py`. |
| **Modular** | Separate modules for credential fetching, logging, and analysis. |

---

## Prerequisites

| Tool | Why? |
|------|------|
| **Python 3.9+** | Core language. |
| **Playwright** | Browser automation (`pip install playwright && playwright install`). |
| **Bitwarden CLI (`bw`)** | Securely retrieve credentials at runtime. |
| **Google service‑account JSON** | Needed for Sheets API (stored as a Bitwarden secure note). |
| **A Google Sheet** | Destination for logs – create one and note its ID. |
| **Resume files** | `resume.txt` (plain‑text version) and `resume_pratham_meena.pdf` (optional attachment). |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/<YOUR_USERNAME>/linkedin-easy-apply-bw.git
cd linkedin-easy-apply-bw

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

> **Tip:** The `requirements.txt` contains `playwright`, `google-api-python-client`, `google-auth`, and any other helper libraries.

---

## Configuration

1. **Bitwarden**  
   - Store a login item named **`LinkedIn`** with the username & password in the *Login* fields.  
   - Store a note named **`GoogleSheets`** containing:  
     *Secure note*: the full JSON of a service‑account key (`credentials.json`).  
     *Custom field*: `SHEET_ID` → the ID of the Google Sheet you created.

2. **Unlock Bitwarden & export session**  

   ```bash
   bw unlock           # copy the session key printed
   export BW_SESSION=<session-key>
   ```

   Keep the session alive while the script runs.

3. **Edit search parameters** (optional)  
   Open `linkedin_easy_apply_bw.py` and modify the `KEYWORDS` and `LOCATIONS` lists.

4. **Resume**  
   - `resume.txt` – plain‑text version of your résumé (used for keyword matching).  
   - `resume_pratham_meena.pdf` – the file that would be uploaded if you enable the actual submit logic.

---

## Usage

```bash
python linkedin_easy_apply_bw.py
```

The script will:

1. Open a Chromium window (headful by default; change `headless=False` to `True` for headless).  
2. Log into LinkedIn with the Bitwarden‑retrieved credentials.  
3. Iterate over each keyword/location pair, collect job cards, and for each job:
   * Detect if “Easy Apply” is available (or redirects to the company site).  
   * Pull the full job description.  
   * Run `analyze_job_fit` against your résumé.  
   * If the match ≥ 70 % → log the attempt to Google Sheets via `sheets_logger.log_application`.  
4. Sleep briefly between operations to avoid triggering LinkedIn rate limits.

---

## How it works (high‑level)

```
+-------------------+      +--------------------+      +-------------------+
| Bitwarden CLI     | ---> | linkedin_easy_... | ---> | Google Sheets API |
| (bw get item)      |      |   (Playwright)     |      | (service account)|
+-------------------+      +--------------------+      +-------------------+
          ^                         ^                         ^
          |                         |                         |
   Credentials (email, pw)   Job search & apply          Logging rows:
   Google service‑account   detection, description    Timestamp, Company,
   (JSON + sheet ID)        analysis                  Title, URL, Status,
                                                     Match %, Skills…
```

* `linkedin_easy_apply_bw.py` – main driver, uses Playwright for UI actions.  
* `sheets_logger.py` – tiny wrapper that writes a row to the configured sheet.  
* `job_analyzer.py` – **not included** in this repo sample; expected to expose  
  `analyze_job_fit(job_desc, resume_text, resume_skills)` and `resume_skills`.  

All secret handling lives in the Bitwarden helper functions, so no password or API key ever appears in source control.

---

## Contributing

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature/awesome‑thing`).  
3. Keep code style consistent (PEP 8, type hints where helpful).  
4. Ensure you **do not** commit any credential data.  
5. Open a Pull Request with a clear description of the change.
---

*Happy hunting! 🎯*
